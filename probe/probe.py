"""
AI Server compatibility probe — checks the OpenAI-API behaviours that real tools depend on.

Standard library only (Python 3.9+). Point it at a server and it writes a JSON result:

  export AISERVER_BASE_URL=http://localhost:11436/v1
  export AISERVER_API_KEY=ai-suite_...
  export AISERVER_MODEL=enginea/qwen3/8b            # a tool-capable chat model
  export AISERVER_EMBED_MODEL=enginea/nomic-embed-text/latest   # optional
  python probe.py --out ../results/latest.json

Each scenario is independent and reports pass / fail / skip with a one-line reason. The catalogue
(`catalog/projects.json`) maps every listed project to the scenarios it needs, so one probe run tells you
which tools should work against a given server build (see catalog/evaluate.py).
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = os.environ.get("AISERVER_BASE_URL", "http://localhost:11436/v1").rstrip("/")
KEY = os.environ.get("AISERVER_API_KEY", "")
MODEL = os.environ.get("AISERVER_MODEL", "")
EMBED_MODEL = os.environ.get("AISERVER_EMBED_MODEL", "")
TIMEOUT = 300


def http(method, path, body=None, headers=None, stream=False, base=None):
    url = (base or BASE) + path
    data = json.dumps(body).encode() if body is not None else None
    h = {"Content-Type": "application/json"}
    if KEY:
        h["Authorization"] = f"Bearer {KEY}"
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    for attempt in range(6):  # honour 429/503 Retry-After like a well-behaved client
        try:
            resp = urllib.request.urlopen(req, timeout=TIMEOUT)
            if stream:
                return resp.status, dict(resp.headers), resp
            raw = resp.read().decode("utf-8", "replace")
            return resp.status, dict(resp.headers), raw
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < 5 and e.headers.get("X-AISuite-Upgrade") is None:
                time.sleep(min(int(e.headers.get("Retry-After", "5") or 5), 60))
                continue
            return e.code, dict(e.headers or {}), e.read().decode("utf-8", "replace")


def chat(messages, **extra):
    return http("POST", "/chat/completions", {"model": MODEL, "messages": messages, **extra})


def sse_events(resp):
    for raw in resp:
        line = raw.decode("utf-8", "replace").strip()
        if line.startswith("data:"):
            yield line[5:].strip()


TOOL = {"type": "function", "function": {
    "name": "get_weather", "description": "Current weather for a city.",
    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}


# ── Scenarios ────────────────────────────────────────────────────────────────────────────────────────
# Each returns (status, reason) with status in {"pass", "fail", "skip"}.

def s_models():
    code, _, body = http("GET", "/models")
    if code != 200:
        return "fail", f"HTTP {code}"
    ids = [m.get("id") for m in json.loads(body).get("data", [])]
    return ("pass", f"{len(ids)} models") if ids else ("fail", "empty model list")


def s_chat_basic():
    code, _, body = chat([{"role": "user", "content": "Reply with the single word: pong"}])
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    msg = json.loads(body)["choices"][0]["message"]
    return ("pass", "ok") if (msg.get("content") or "").strip() else ("fail", "empty content")


def s_chat_stream():
    code, headers, resp = http("POST", "/chat/completions", {
        "model": MODEL, "stream": True, "messages": [{"role": "user", "content": "Count from 1 to 5."}]}, stream=True)
    if code != 200:
        return "fail", f"HTTP {code}"
    if "text/event-stream" not in headers.get("Content-Type", headers.get("content-type", "")):
        return "fail", "not text/event-stream"
    chunks, done = 0, False
    for data in sse_events(resp):
        if data == "[DONE]":
            done = True
            break
        if json.loads(data)["choices"][0].get("delta", {}).get("content"):
            chunks += 1
    return ("pass", f"{chunks} content chunks") if chunks > 1 and done else ("fail", f"chunks={chunks} done={done}")


def s_stream_usage():
    code, _, resp = http("POST", "/chat/completions", {
        "model": MODEL, "stream": True, "stream_options": {"include_usage": True},
        "messages": [{"role": "user", "content": "Say hi."}]}, stream=True)
    if code != 200:
        return "fail", f"HTTP {code}"
    usage = None
    for data in sse_events(resp):
        if data == "[DONE]":
            break
        obj = json.loads(data)
        if obj.get("usage"):
            usage = obj["usage"]
    return ("pass", "usage chunk present") if usage else ("fail", "no usage chunk with stream_options.include_usage")


def s_tools_auto():
    code, _, body = chat([{"role": "user", "content": "What's the weather in Dublin? Use the tool."}], tools=[TOOL], tool_choice="auto")
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    ch = json.loads(body)["choices"][0]
    calls = ch["message"].get("tool_calls") or []
    if not calls:
        return "fail", "no structured tool_calls (model answered in text?)"
    args = json.loads(calls[0]["function"]["arguments"] or "{}")
    ok = calls[0]["function"]["name"] == "get_weather" and "city" in args and ch.get("finish_reason") == "tool_calls"
    return ("pass", "structured call, finish_reason=tool_calls") if ok else ("fail", f"call={calls[0]} finish={ch.get('finish_reason')}")


def s_tools_required():
    code, _, body = chat([{"role": "user", "content": "Hello!"}], tools=[TOOL], tool_choice="required")
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    calls = json.loads(body)["choices"][0]["message"].get("tool_calls") or []
    return ("pass", "forced call") if calls else ("fail", "tool_choice=required did not force a call")


def s_tool_roundtrip():
    msgs = [{"role": "user", "content": "What's the weather in Dublin? Use the tool."}]
    code, _, body = chat(msgs, tools=[TOOL])
    if code != 200:
        return "fail", f"HTTP {code}"
    msg = json.loads(body)["choices"][0]["message"]
    calls = msg.get("tool_calls") or []
    if not calls:
        return "skip", "model made no tool call"
    msgs.append({"role": "assistant", "content": msg.get("content") or "", "tool_calls": calls})
    msgs.append({"role": "tool", "tool_call_id": calls[0]["id"], "content": json.dumps({"city": "Dublin", "forecast": "ZEPHYR-42 sunshine"})})
    code, _, body = chat(msgs, tools=[TOOL])
    if code != 200:
        return "fail", f"HTTP {code} on tool result: {body[:120]}"
    text = json.loads(body)["choices"][0]["message"].get("content") or ""
    return ("pass", "answer uses the tool result") if "ZEPHYR" in text.upper() else ("fail", "tool result not reflected in answer")


def s_json_mode():
    code, _, body = chat([{"role": "user", "content": "Return a JSON object with keys name and age for Alice aged 30."}],
                         response_format={"type": "json_object"})
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    content = json.loads(body)["choices"][0]["message"].get("content") or ""
    try:
        obj = json.loads(content)
        return ("pass", "valid JSON object") if isinstance(obj, dict) else ("fail", "not an object")
    except ValueError:
        return "fail", "content is not valid JSON"


def _embed(inp):
    return http("POST", "/embeddings", {"model": EMBED_MODEL, "input": inp})


def s_embeddings_string():
    if not EMBED_MODEL:
        return "skip", "set AISERVER_EMBED_MODEL"
    code, _, body = _embed("hello world")
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    return ("pass", "ok") if json.loads(body)["data"][0]["embedding"] else ("fail", "empty vector")


def s_embeddings_list():
    if not EMBED_MODEL:
        return "skip", "set AISERVER_EMBED_MODEL"
    code, _, body = _embed(["hello", "world"])
    if code != 200:
        return "fail", f"HTTP {code}: {body[:120]}"
    return ("pass", "2 vectors") if len(json.loads(body)["data"]) == 2 else ("fail", "wrong vector count")


def s_embed_model_listed():
    if not EMBED_MODEL:
        return "skip", "set AISERVER_EMBED_MODEL"
    code, _, body = http("GET", "/models")
    ids = [m.get("id") for m in json.loads(body).get("data", [])] if code == 200 else []
    return ("pass", "listed") if EMBED_MODEL in ids else ("fail", "embedding model not listed in /v1/models")


def s_responses_api():
    code, _, body = http("POST", "/responses", {"model": MODEL, "input": "Say hi."})
    if code == 200:
        return "pass", "ok"
    return "fail", f"HTTP {code} (Responses API not available)"


def s_error_shape():
    code, _, body = http("POST", "/chat/completions", {"model": "no-such-model/x/y", "messages": [{"role": "user", "content": "hi"}]})
    if code < 400:
        return "fail", f"HTTP {code} for unknown model"
    try:
        err = json.loads(body).get("error")
        return ("pass", f"HTTP {code} with OpenAI error envelope") if isinstance(err, dict) and err.get("message") else ("fail", "no error.message")
    except ValueError:
        return "fail", "error body is not JSON"


def s_cors():
    code, headers, _ = http("OPTIONS", "/models", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"})
    allow = {k.lower(): v for k, v in headers.items()}.get("access-control-allow-origin")
    return ("pass", f"allow-origin={allow}") if allow else ("fail", f"no CORS (HTTP {code}); browser-only apps need a proxy")


SCENARIOS = {
    "models_list": s_models, "chat_basic": s_chat_basic, "chat_stream": s_chat_stream, "stream_usage": s_stream_usage,
    "tools_auto": s_tools_auto, "tools_required": s_tools_required, "tool_roundtrip": s_tool_roundtrip,
    "json_mode": s_json_mode, "embeddings_string": s_embeddings_string, "embeddings_list": s_embeddings_list,
    "embed_model_listed": s_embed_model_listed, "responses_api": s_responses_api, "error_shape": s_error_shape,
    "cors": s_cors,
}


def server_version():
    root = BASE[:-3] if BASE.endswith("/v1") else BASE
    code, _, body = http("GET", "/api/version", base=root)
    try:
        return json.loads(body).get("version") if code == 200 else None
    except ValueError:
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="")
    ap.add_argument("--only", default="", help="comma-separated scenario ids")
    a = ap.parse_args()
    if not MODEL:
        sys.exit("Set AISERVER_MODEL to a tool-capable chat model id (see GET /v1/models).")
    only = [s for s in a.only.split(",") if s]
    results = {}
    for sid, fn in SCENARIOS.items():
        if only and sid not in only:
            continue
        try:
            status, reason = fn()
        except Exception as e:  # a probe must report, not crash
            status, reason = "fail", f"{type(e).__name__}: {str(e)[:120]}"
        results[sid] = {"status": status, "reason": reason}
        print(f"{status:5} {sid:20} {reason}")
    out = {"server_version": server_version(), "model": MODEL, "embed_model": EMBED_MODEL or None,
           "run_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "results": results}
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2)
        print(f"wrote {a.out}")


if __name__ == "__main__":
    main()
