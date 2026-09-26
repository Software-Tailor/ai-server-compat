"""Source of truth for catalog/projects.json. Edit here, run `python build_catalog.py`.

Fields: name, repo, category, license (SPDX as reported by GitHub), license_note, config (how to point the tool
at AI Server), needs (probe scenarios the tool depends on), optional (scenarios it can use), verification:
  verified   — run end to end against AI Server by us (see `evidence`)
  documented — configuration published in ai-server-dropin-recipes, tool not yet exercised by us
  protocol   — listed on protocol grounds: compatible if the probe passes every scenario in `needs`
Licence policy: permissive licences only (MIT, Apache-2.0, BSD). Source-available / modified licences are in
the `caution` list with a note and are never redistributed; copyleft and fair-code projects are excluded.
"""
import json

CHAT = ["models_list", "chat_stream"]
AGENT = ["tools_auto", "tool_roundtrip"]
RAG = ["chat_basic", "embeddings_list"]
EVAL = ["chat_basic"]

DROPIN = "https://github.com/Software-Tailor/ai-server-dropin-recipes"
FRAMEWORKS = "https://github.com/Software-Tailor/ai-server-agent-frameworks"
SECURITY = "https://github.com/Software-Tailor/ai-server-security-agents"


def p(name, repo, category, lic, config, needs, optional=(), verification="protocol", evidence=None, note=None):
    d = {"name": name, "repo": f"https://github.com/{repo}", "category": category, "license": lic, "config": config,
         "needs": list(needs), "optional": list(optional), "verification": verification}
    if evidence:
        d["evidence"] = evidence
    if note:
        d["note"] = note
    return d


PROJECTS = [
    # SDKs & frameworks
    p("OpenAI Python SDK", "openai/openai-python", "SDK & frameworks", "Apache-2.0", "OpenAI(base_url=..., api_key=...)", ["models_list", "chat_stream"], ["tools_auto", "embeddings_list"], "verified", DROPIN),
    p("OpenAI .NET SDK", "openai/openai-dotnet", "SDK & frameworks", "MIT", "new ChatClient(model, key, new OpenAIClientOptions { Endpoint = baseUrl })", AGENT, [], "verified", SECURITY),
    p("LangChain / LangGraph", "langchain-ai/langgraph", "SDK & frameworks", "MIT", "ChatOpenAI(model=..., base_url=..., api_key=...)", AGENT, ["chat_stream", "embeddings_list"], "verified", FRAMEWORKS),
    p("LlamaIndex", "run-llama/llama_index", "SDK & frameworks", "MIT", "OpenAILike(api_base=..., is_chat_model=True, is_function_calling_model=True)", AGENT, ["embeddings_list"], "verified", FRAMEWORKS),
    p("Pydantic AI", "pydantic/pydantic-ai", "SDK & frameworks", "MIT", "OpenAIChatModel(model, provider=OpenAIProvider(base_url=..., api_key=...))", AGENT, ["json_mode"], "verified", FRAMEWORKS),
    p("OpenAI Agents SDK", "openai/openai-agents-python", "SDK & frameworks", "MIT", "OpenAIChatCompletionsModel + set_tracing_disabled(True)", AGENT, [], "verified", FRAMEWORKS, "Use the Chat Completions model class; the default speaks the Responses API."),
    p("smolagents", "huggingface/smolagents", "SDK & frameworks", "Apache-2.0", "OpenAIServerModel(model_id=..., api_base=..., api_key=...)", AGENT + ["tools_required"], [], "verified", FRAMEWORKS, "Sends tool_choice=required; 4 of 5 runs passed until AI Server enforces it."),
    p("Semantic Kernel", "microsoft/semantic-kernel", "SDK & frameworks", "MIT", "AddOpenAIChatCompletion(modelId, endpoint WITHOUT /v1, apiKey)", AGENT, [], "documented", DROPIN),
    p("Microsoft Agent Framework", "microsoft/agent-framework", "SDK & frameworks", "MIT", "OpenAI chat client with base URL", AGENT),
    p("CrewAI", "crewAIInc/crewAI", "SDK & frameworks", "MIT", "LLM(model='openai/<id>', base_url=..., api_key=...)", AGENT),
    p("Agno", "agno-agi/agno", "SDK & frameworks", "Apache-2.0", "OpenAILike(id=..., base_url=..., api_key=...)", AGENT),
    p("CAMEL", "camel-ai/camel", "SDK & frameworks", "Apache-2.0", "ModelFactory OPENAI_COMPATIBLE_MODEL with url=...", AGENT),
    p("DSPy", "stanfordnlp/dspy", "SDK & frameworks", "MIT", "dspy.LM('openai/<id>', api_base=..., api_key=...)", ["chat_basic"]),
    p("Haystack", "deepset-ai/haystack", "SDK & frameworks", "Apache-2.0", "OpenAIChatGenerator(api_base_url=...)", ["chat_basic"], ["embeddings_list"]),
    p("Instructor", "567-labs/instructor", "SDK & frameworks", "MIT", "instructor.from_openai(OpenAI(base_url=...), mode=Mode.TOOLS)", ["tools_auto"], ["json_mode"]),
    p("Guidance", "guidance-ai/guidance", "SDK & frameworks", "MIT", "OpenAI-compatible endpoint", ["chat_basic"]),
    p("Mem0", "mem0ai/mem0", "SDK & frameworks", "Apache-2.0", "openai_base_url in llm + embedder config", RAG),
    p("Letta", "letta-ai/letta", "SDK & frameworks", "Apache-2.0", "OpenAI-compatible provider base URL", AGENT + ["embeddings_list"]),
    # Coding assistants
    p("Continue", "continuedev/continue", "Coding assistants", "Apache-2.0", "config: provider openai, apiBase, apiKey", ["chat_stream"], ["tools_auto", "embeddings_list"], "documented", DROPIN),
    p("aider", "Aider-AI/aider", "Coding assistants", "Apache-2.0", "--openai-api-base ... --model openai/<id>", ["chat_stream"], [], "documented", DROPIN),
    p("Cline", "cline/cline", "Coding assistants", "Apache-2.0", "API Provider: OpenAI Compatible — Base URL, API Key, Model ID", ["chat_stream", "tools_auto"]),
    p("Kilo Code", "Kilo-Org/kilocode", "Coding assistants", "MIT", "OpenAI Compatible provider", ["chat_stream", "tools_auto"]),
    p("OpenHands", "OpenHands/OpenHands", "Coding assistants", "MIT", "LLM_BASE_URL + model openai/<id>", AGENT + ["chat_stream"]),
    p("opencode", "anomalyco/opencode", "Coding assistants", "MIT", "custom provider baseURL", AGENT + ["chat_stream"]),
    p("Qwen Code", "QwenLM/qwen-code", "Coding assistants", "Apache-2.0", "OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL", AGENT + ["chat_stream"]),
    p("Codex CLI", "openai/codex", "Coding assistants", "Apache-2.0", "config.toml model_providers.<x>.base_url + wire_api = \"chat\"", AGENT + ["chat_stream"], [], note="Set wire_api = \"chat\"; the default is the Responses API."),
    p("Goose", "block/goose", "Coding assistants", "Apache-2.0", "OpenAI provider OPENAI_HOST / OPENAI_BASE_PATH", AGENT + ["chat_stream"]),
    p("Plandex", "plandex-ai/plandex", "Coding assistants", "MIT", "custom OpenAI-compatible model base URL", AGENT),
    p("gptme", "gptme/gptme", "Coding assistants", "MIT", "OPENAI_BASE_URL", ["chat_stream"], ["tools_auto"]),
    p("bolt.diy", "stackblitz-labs/bolt.diy", "Coding assistants", "MIT", "OpenAILike provider base URL", ["chat_stream"]),
    # Chat UIs
    p("LibreChat", "danny-avila/LibreChat", "Chat UIs", "MIT", "librechat.yaml endpoints.custom baseURL + apiKey", CHAT, ["embeddings_list"]),
    p("NextChat", "ChatGPTNextWeb/NextChat", "Chat UIs", "MIT", "BASE_URL + OPENAI_API_KEY (server-side proxy)", CHAT),
    p("Hugging Face Chat UI", "huggingface/chat-ui", "Chat UIs", "Apache-2.0", "MODELS[].endpoints type openai, baseURL", CHAT),
    p("big-AGI", "enricoros/big-AGI", "Chat UIs", "MIT", "OpenAI-compatible service with custom host", CHAT),
    p("Chatbot UI", "mckaywrigley/chatbot-ui", "Chat UIs", "MIT", "custom base URL", CHAT),
    p("GPT4All", "nomic-ai/gpt4all", "Chat UIs", "MIT", "remote OpenAI-compatible model: base URL, key, model", ["chat_basic"]),
    # RAG & knowledge
    p("RAGFlow", "infiniflow/ragflow", "RAG & knowledge", "Apache-2.0", "model provider: OpenAI-API-Compatible, base URL", RAG),
    p("kotaemon", "Cinnamon/kotaemon", "RAG & knowledge", "Apache-2.0", "OpenAI-compatible LLM + embedding base URL", RAG),
    p("GraphRAG", "microsoft/graphrag", "RAG & knowledge", "MIT", "settings.yaml api_base for chat + embeddings", RAG + ["json_mode"]),
    p("LightRAG", "HKUDS/LightRAG", "RAG & knowledge", "MIT", "openai_complete_if_cache(base_url=...) + openai_embed(base_url=...)", RAG),
    p("GPT Researcher", "assafelovic/gpt-researcher", "RAG & knowledge", "Apache-2.0", "OPENAI_BASE_URL + FAST_LLM/SMART_LLM openai:<id>", RAG),
    p("DocsGPT", "arc53/DocsGPT", "RAG & knowledge", "MIT", "OPENAI_BASE_URL", RAG),
    # Workflow
    p("Langflow", "langflow-ai/langflow", "Workflow builders", "MIT", "OpenAI component: OpenAI API Base", ["chat_basic"], ["tools_auto"]),
    p("DB-GPT", "eosphoros-ai/DB-GPT", "Workflow builders", "MIT", "proxy LLM base URL", ["chat_basic"], ["embeddings_list"]),
    # Evaluation & red-teaming
    p("promptfoo", "promptfoo/promptfoo", "Evaluation & red-teaming", "MIT", "provider openai:chat:<id> with config.apiBaseUrl", EVAL, ["json_mode", "tools_auto"]),
    p("garak", "NVIDIA/garak", "Evaluation & red-teaming", "Apache-2.0", "OpenAI-compatible generator with custom uri", EVAL),
    p("PyRIT", "microsoft/PyRIT", "Evaluation & red-teaming", "MIT", "OpenAIChatTarget(endpoint=..., api_key=...)", EVAL),
    p("DeepEval", "confident-ai/deepeval", "Evaluation & red-teaming", "Apache-2.0", "custom OpenAI base URL model", EVAL, ["json_mode"]),
    p("Ragas", "vibrantlabsai/ragas", "Evaluation & red-teaming", "Apache-2.0", "wrap a LangChain ChatOpenAI(base_url=...)", EVAL + ["embeddings_list"]),
    p("Inspect", "UKGovernmentBEIS/inspect_ai", "Evaluation & red-teaming", "MIT", "--model openai-api/<id> with OPENAI_BASE_URL", EVAL, ["tools_auto"]),
    p("lm-evaluation-harness", "EleutherAI/lm-evaluation-harness", "Evaluation & red-teaming", "MIT", "--model local-chat-completions --model_args base_url=...", EVAL),
    p("Giskard", "Giskard-AI/giskard-oss", "Evaluation & red-teaming", "Apache-2.0", "OpenAI-compatible client base URL", EVAL),
    p("Guardrails", "guardrails-ai/guardrails", "Evaluation & red-teaming", "Apache-2.0", "model='openai/<id>', api_base=...", EVAL),
    p("agentic-radar", "splx-ai/agentic-radar", "Evaluation & red-teaming", "Apache-2.0", "OpenAI base URL", EVAL),
    p("Agentic Security", "msoedov/agentic_security", "Evaluation & red-teaming", "Apache-2.0", "target URL of an OpenAI-compatible endpoint", EVAL),
    p("Prompt Fuzzer", "prompt-security/ps-fuzz", "Evaluation & red-teaming", "MIT", "OpenAI base URL", EVAL),
    # Cybersecurity
    p("SOC triage agent", "Software-Tailor/ai-server-security-agents", "Cybersecurity", "MIT", "AISERVER_BASE_URL / AISERVER_API_KEY / AISERVER_MODEL", AGENT, [], "verified", SECURITY),
    p("PentestGPT", "GreyDGL/PentestGPT", "Cybersecurity", "MIT", "OpenAI-compatible base URL", ["chat_stream"], [], note="Authorised targets only."),
    p("PentAGI", "vxcontrol/pentagi", "Cybersecurity", "MIT", "custom OpenAI-compatible LLM provider URL", AGENT, [], note="Authorised targets only."),
    p("Strix", "usestrix/strix", "Cybersecurity", "Apache-2.0", "LLM_API_BASE + model openai/<id>", AGENT, [], note="Authorised targets only."),
    p("hackingBuddyGPT", "ipa-lab/hackingBuddyGPT", "Cybersecurity", "MIT", "llm.api_url", ["chat_basic"], [], note="Authorised targets only."),
    p("MCP Scanner", "cisco-ai-defense/mcp-scanner", "Cybersecurity", "Apache-2.0", "LLM analyzer base URL", ["chat_basic"]),
    # CLI
    p("llm (Simon Willison)", "simonw/llm", "Command line", "Apache-2.0", "extra-openai-models.yaml api_base", ["chat_stream"], ["embeddings_list"]),
    p("aichat", "sigoden/aichat", "Command line", "Apache-2.0", "config.yaml type openai-compatible, api_base", ["chat_stream"], ["tools_auto"]),
    p("Shell GPT", "TheR1D/shell_gpt", "Command line", "MIT", "API_BASE_URL", ["chat_stream"]),
    p("Open Interpreter", "openinterpreter/openinterpreter", "Command line", "Apache-2.0", "--api_base", ["chat_stream"]),
    # Observability & gateways
    p("Portkey Gateway", "Portkey-AI/gateway", "Observability & gateways", "MIT", "custom provider customHost", ["chat_basic", "chat_stream"], ["stream_usage"]),
    p("Helicone", "Helicone/helicone", "Observability & gateways", "Apache-2.0", "proxy base_url", ["chat_basic"], ["stream_usage"]),
    p("Opik", "comet-ml/opik", "Observability & gateways", "Apache-2.0", "track an OpenAI client with base_url", ["chat_basic"]),
    p("OpenLLMetry", "traceloop/openllmetry", "Observability & gateways", "Apache-2.0", "instruments the OpenAI SDK", ["chat_basic"], ["stream_usage"]),
    # Data & documents
    p("MarkItDown", "microsoft/markitdown", "Data & documents", "MIT", "llm_client=OpenAI(base_url=...) for image captions", ["chat_basic"]),
    p("Docling", "docling-project/docling", "Data & documents", "MIT", "VLM options with OpenAI-compatible URL", ["chat_basic"]),
    p("Marker", "datalab-to/marker", "Data & documents", "Apache-2.0", "LLM service base URL", ["chat_basic"]),
    p("paperless-gpt", "icereed/paperless-gpt", "Data & documents", "MIT", "OPENAI_BASE_URL", ["chat_basic"]),
    p("Presenton", "presenton/presenton", "Data & documents", "Apache-2.0", "custom OpenAI-compatible URL", ["chat_stream"]),
    # Browser automation
    p("browser-use", "browser-use/browser-use", "Browser automation", "MIT", "ChatOpenAI(base_url=...)", AGENT),
    p("Stagehand", "browserbase/stagehand", "Browser automation", "MIT", "modelClientOptions.baseURL", AGENT),
]

CAUTION = [
    {"name": "Open WebUI", "repo": "https://github.com/open-webui/open-webui", "license": "Open WebUI License (BSD-3 + branding clause)",
     "note": "Works (config in ai-server-dropin-recipes); the licence restricts rebranding, so check it before redistributing a customised build."},
    {"name": "Dify", "repo": "https://github.com/langgenius/dify", "license": "Modified Apache-2.0", "note": "Restricts multi-tenant SaaS use; read before commercial deployment."},
    {"name": "LiteLLM", "repo": "https://github.com/BerriAI/litellm", "license": "MIT core + enterprise directory", "note": "Core is MIT; enterprise features are separately licensed."},
    {"name": "Flowise", "repo": "https://github.com/FlowiseAI/Flowise", "license": "Apache-2.0 + commercial terms for some parts", "note": "Check the current licence file."},
    {"name": "Langfuse", "repo": "https://github.com/langfuse/langfuse", "license": "MIT core + EE directory", "note": "Enterprise directory is not MIT."},
    {"name": "Arize Phoenix", "repo": "https://github.com/Arize-ai/phoenix", "license": "Elastic License 2.0", "note": "Source-available; not for managed-service resale."},
    {"name": "Lobe Chat", "repo": "https://github.com/lobehub/lobe-chat", "license": "Custom (Apache-2.0 based)", "note": "Commercial-use conditions apply."},
    {"name": "Jan", "repo": "https://github.com/janhq/jan", "license": "Check current licence", "note": "Licence has changed over time."},
]

EXCLUDED_NOTE = "Copyleft or fair-code projects (GPL, AGPL, SSPL, Sustainable Use) are not listed as recommendations, even though several work with AI Server: e.g. n8n, SillyTavern, Chatbox, Cherry Studio, Khoj."

# Keep the catalogue strictly permissive: drop anything copyleft that slipped in above.
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-3-Clause", "BSD-2-Clause"}
excluded = [x["name"] for x in PROJECTS if x["license"] not in PERMISSIVE]
PROJECTS = [x for x in PROJECTS if x["license"] in PERMISSIVE]

if __name__ == "__main__":
    out = {"projects": PROJECTS, "caution": CAUTION, "excluded_note": EXCLUDED_NOTE}
    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"{len(PROJECTS)} projects, {len(CAUTION)} caution; dropped as non-permissive: {', '.join(excluded) or 'none'}")
