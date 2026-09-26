# Works with AI Server

**[Software Tailor AI Server](https://softwaretailor.com/docs/ai-server/index.htm)** speaks the OpenAI API, so
tools with an "OpenAI-compatible base URL" setting can use models running on your own hardware. This repo
answers the practical question, **"will *my* tool work?"**, with evidence instead of adjectives:

1. **[`probe/probe.py`](probe/probe.py)** checks the behaviours real tools depend on: model discovery,
   streaming, structured tool calls, tool-result round trips, `tool_choice: "required"`, JSON mode, embeddings,
   usage in streams, the Responses API, error envelopes and CORS. It uses only the Python standard library.
2. **[`catalog/projects.json`](catalog/projects.json)** lists **77 permissively licensed open-source
   projects** (MIT, Apache-2.0, BSD). For each one it records how to point the tool at AI Server and which
   checks it needs. Licences are checked against GitHub, and archived projects are dropped.
3. **[`catalog/STATUS.md`](catalog/STATUS.md)** combines the two for a given AI Server build.

➡️ **[See the current status](catalog/STATUS.md)**

## Status levels, honestly

| Level | Meaning |
| --- | --- |
| ✅ **Verified** | We ran it end to end against AI Server; the evidence repo is linked |
| ⚙️ **Config documented** | The configuration is published in [ai-server-dropin-recipes](https://github.com/Software-Tailor/ai-server-dropin-recipes); we haven't exercised the tool itself yet |
| 🟢 **Expected to work** | Every protocol check the tool depends on passes on this build. This is inferred from the protocol, not tested with the tool |
| 🔴 **Blocked** | A check the tool depends on currently fails; the check is named |

Tried a tool? Open an issue with the tool, its version, your AI Server version and what happened. That's
how an entry moves from 🟢 to ✅.

## Latest protocol run (AI Server 2.2.5 development build — the Store release is 2.2.4 — with `enginea/qwen3/8b`)

| Check | Result |
| --- | --- |
| Model discovery, chat, streaming (382 chunks) | ✅ |
| Structured tool calls (`finish_reason: tool_calls`), tool-result round trip | ✅ |
| JSON mode, embeddings (string and list input), OpenAI error envelope | ✅ |
| `tool_choice: "required"` | ❌ not yet enforced on the default local engine |
| `stream_options.include_usage` | ❌ no usage chunk yet |
| Embedding models listed in `/v1/models` | ❌ usable but not listed |
| Responses API (`/v1/responses`) | ❌ not implemented, so use Chat Completions mode |
| CORS for browser-only apps | ❌ by design, so use a same-origin proxy |

These results are the AI Server team's own to-do list, and they're published so you can plan around them.

## Run the probe yourself

```bash
export AISERVER_BASE_URL="http://192.168.1.42:11436/v1"      # ends in /v1
export AISERVER_API_KEY="ai-suite_..."
export AISERVER_MODEL="enginea/qwen3/8b"                     # a tool-capable chat model
export AISERVER_EMBED_MODEL="enginea/nomic-embed-text/latest" # optional
python probe/probe.py --out results/mine.json
cd catalog && python evaluate.py ../results/mine.json         # rewrites STATUS.md for your server
```

On the Free tier, generic clients are rate-limited (1 request a minute, 10 a day), so run the probe against a
licensed server or with a key. The probe honours `Retry-After`.

## Licence policy for the catalogue

Only permissive licences are listed as recommendations. Projects whose licence adds conditions (branding,
SaaS or enterprise clauses) are in a separate **"check the licence first"** table. Copyleft and fair-code
projects are not recommended, even where they work. We publish configuration and recipes only, never
anyone else's code.

## Related

- [ai-server-agent-frameworks](https://github.com/Software-Tailor/ai-server-agent-frameworks): tested agents in LangGraph, LlamaIndex, Pydantic AI, OpenAI Agents SDK, smolagents
- [ai-server-security-agents](https://github.com/Software-Tailor/ai-server-security-agents): SOC triage agent (Python + C#)
- [ai-server-dropin-recipes](https://github.com/Software-Tailor/ai-server-dropin-recipes) · [ai-server-quickstarts](https://github.com/Software-Tailor/ai-server-quickstarts)
- [Developer hub](https://softwaretailor.com/developers.htm) · [Partner Programme](https://softwaretailor.com/partners/)

MIT licensed. See [LICENSE](LICENSE).
