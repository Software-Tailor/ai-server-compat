# Works with AI Server — status

Generated from probe run `dev-2.2.5-qwen3-8b.json`: AI Server 2.2.5, model `enginea/qwen3/8b`, 2026-09-26T20:53:14Z.

**77 permissively licensed projects:** ✅ Verified 8 · ⚙️ Config documented 3 · 🟢 Expected to work 66 · 🔴 Blocked 0

Status meanings: **Verified** = run end to end against AI Server by us (evidence linked). **Config documented** = configuration published, tool not yet exercised by us. **Expected to work** = every protocol check the tool depends on passes. **Blocked** = a check the tool depends on currently fails (named).

## Protocol checks in this run

| Check | Result | Detail |
| --- | --- | --- |
| `models_list` | ✅ | 61 models |
| `chat_basic` | ✅ | ok |
| `chat_stream` | ✅ | 382 content chunks |
| `stream_usage` | ❌ | no usage chunk with stream_options.include_usage |
| `tools_auto` | ✅ | structured call, finish_reason=tool_calls |
| `tools_required` | ❌ | tool_choice=required did not force a call |
| `tool_roundtrip` | ✅ | answer uses the tool result |
| `json_mode` | ✅ | valid JSON object |
| `embeddings_string` | ✅ | ok |
| `embeddings_list` | ✅ | 2 vectors |
| `embed_model_listed` | ❌ | embedding model not listed in /v1/models |
| `responses_api` | ❌ | HTTP 404 (Responses API not available) |
| `error_shape` | ✅ | HTTP 503 with OpenAI error envelope |
| `cors` | ❌ | no CORS (HTTP 405); browser-only apps need a proxy |

## SDK & frameworks

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [OpenAI Python SDK](https://github.com/openai/openai-python) | Apache-2.0 | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-dropin-recipes)) | `OpenAI(base_url=..., api_key=...)` |
| [OpenAI .NET SDK](https://github.com/openai/openai-dotnet) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-security-agents)) | `new ChatClient(model, key, new OpenAIClientOptions { Endpoint = baseUrl })` |
| [LangChain / LangGraph](https://github.com/langchain-ai/langgraph) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-agent-frameworks)) | `ChatOpenAI(model=..., base_url=..., api_key=...)` |
| [LlamaIndex](https://github.com/run-llama/llama_index) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-agent-frameworks)) | `OpenAILike(api_base=..., is_chat_model=True, is_function_calling_model=True)` |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-agent-frameworks)) | `OpenAIChatModel(model, provider=OpenAIProvider(base_url=..., api_key=...))` |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-agent-frameworks)) — Use the Chat Completions model class; the default speaks the Responses API. | `OpenAIChatCompletionsModel + set_tracing_disabled(True)` |
| [smolagents](https://github.com/huggingface/smolagents) | Apache-2.0 | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-agent-frameworks)) — Sends tool_choice=required; 4 of 5 runs passed until AI Server enforces it. | `OpenAIServerModel(model_id=..., api_base=..., api_key=...)` |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | MIT | ⚙️ Config documented ([evidence](https://github.com/Software-Tailor/ai-server-dropin-recipes)) | `AddOpenAIChatCompletion(modelId, endpoint WITHOUT /v1, apiKey)` |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | MIT | 🟢 Expected to work | `OpenAI chat client with base URL` |
| [CrewAI](https://github.com/crewAIInc/crewAI) | MIT | 🟢 Expected to work | `LLM(model='openai/<id>', base_url=..., api_key=...)` |
| [Agno](https://github.com/agno-agi/agno) | Apache-2.0 | 🟢 Expected to work | `OpenAILike(id=..., base_url=..., api_key=...)` |
| [CAMEL](https://github.com/camel-ai/camel) | Apache-2.0 | 🟢 Expected to work | `ModelFactory OPENAI_COMPATIBLE_MODEL with url=...` |
| [DSPy](https://github.com/stanfordnlp/dspy) | MIT | 🟢 Expected to work | `dspy.LM('openai/<id>', api_base=..., api_key=...)` |
| [Haystack](https://github.com/deepset-ai/haystack) | Apache-2.0 | 🟢 Expected to work | `OpenAIChatGenerator(api_base_url=...)` |
| [Instructor](https://github.com/567-labs/instructor) | MIT | 🟢 Expected to work | `instructor.from_openai(OpenAI(base_url=...), mode=Mode.TOOLS)` |
| [Guidance](https://github.com/guidance-ai/guidance) | MIT | 🟢 Expected to work | `OpenAI-compatible endpoint` |
| [Mem0](https://github.com/mem0ai/mem0) | Apache-2.0 | 🟢 Expected to work | `openai_base_url in llm + embedder config` |
| [Letta](https://github.com/letta-ai/letta) | Apache-2.0 | 🟢 Expected to work | `OpenAI-compatible provider base URL` |

## Coding assistants

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [Continue](https://github.com/continuedev/continue) | Apache-2.0 | ⚙️ Config documented ([evidence](https://github.com/Software-Tailor/ai-server-dropin-recipes)) | `config: provider openai, apiBase, apiKey` |
| [aider](https://github.com/Aider-AI/aider) | Apache-2.0 | ⚙️ Config documented ([evidence](https://github.com/Software-Tailor/ai-server-dropin-recipes)) | `--openai-api-base ... --model openai/<id>` |
| [Cline](https://github.com/cline/cline) | Apache-2.0 | 🟢 Expected to work | `API Provider: OpenAI Compatible — Base URL, API Key, Model ID` |
| [Kilo Code](https://github.com/Kilo-Org/kilocode) | MIT | 🟢 Expected to work | `OpenAI Compatible provider` |
| [OpenHands](https://github.com/OpenHands/OpenHands) | MIT | 🟢 Expected to work | `LLM_BASE_URL + model openai/<id>` |
| [opencode](https://github.com/anomalyco/opencode) | MIT | 🟢 Expected to work | `custom provider baseURL` |
| [Qwen Code](https://github.com/QwenLM/qwen-code) | Apache-2.0 | 🟢 Expected to work | `OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL` |
| [Codex CLI](https://github.com/openai/codex) | Apache-2.0 | 🟢 Expected to work — Set wire_api = "chat"; the default is the Responses API. | `config.toml model_providers.<x>.base_url + wire_api = "chat"` |
| [Goose](https://github.com/block/goose) | Apache-2.0 | 🟢 Expected to work | `OpenAI provider OPENAI_HOST / OPENAI_BASE_PATH` |
| [Plandex](https://github.com/plandex-ai/plandex) | MIT | 🟢 Expected to work | `custom OpenAI-compatible model base URL` |
| [gptme](https://github.com/gptme/gptme) | MIT | 🟢 Expected to work | `OPENAI_BASE_URL` |
| [bolt.diy](https://github.com/stackblitz-labs/bolt.diy) | MIT | 🟢 Expected to work | `OpenAILike provider base URL` |

## Chat UIs

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [LibreChat](https://github.com/danny-avila/LibreChat) | MIT | 🟢 Expected to work | `librechat.yaml endpoints.custom baseURL + apiKey` |
| [NextChat](https://github.com/ChatGPTNextWeb/NextChat) | MIT | 🟢 Expected to work | `BASE_URL + OPENAI_API_KEY (server-side proxy)` |
| [Hugging Face Chat UI](https://github.com/huggingface/chat-ui) | Apache-2.0 | 🟢 Expected to work | `MODELS[].endpoints type openai, baseURL` |
| [big-AGI](https://github.com/enricoros/big-AGI) | MIT | 🟢 Expected to work | `OpenAI-compatible service with custom host` |
| [Chatbot UI](https://github.com/mckaywrigley/chatbot-ui) | MIT | 🟢 Expected to work | `custom base URL` |
| [GPT4All](https://github.com/nomic-ai/gpt4all) | MIT | 🟢 Expected to work | `remote OpenAI-compatible model: base URL, key, model` |

## RAG & knowledge

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [RAGFlow](https://github.com/infiniflow/ragflow) | Apache-2.0 | 🟢 Expected to work | `model provider: OpenAI-API-Compatible, base URL` |
| [kotaemon](https://github.com/Cinnamon/kotaemon) | Apache-2.0 | 🟢 Expected to work | `OpenAI-compatible LLM + embedding base URL` |
| [GraphRAG](https://github.com/microsoft/graphrag) | MIT | 🟢 Expected to work | `settings.yaml api_base for chat + embeddings` |
| [LightRAG](https://github.com/HKUDS/LightRAG) | MIT | 🟢 Expected to work | `openai_complete_if_cache(base_url=...) + openai_embed(base_url=...)` |
| [GPT Researcher](https://github.com/assafelovic/gpt-researcher) | Apache-2.0 | 🟢 Expected to work | `OPENAI_BASE_URL + FAST_LLM/SMART_LLM openai:<id>` |
| [DocsGPT](https://github.com/arc53/DocsGPT) | MIT | 🟢 Expected to work | `OPENAI_BASE_URL` |

## Workflow builders

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [Langflow](https://github.com/langflow-ai/langflow) | MIT | 🟢 Expected to work | `OpenAI component: OpenAI API Base` |
| [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) | MIT | 🟢 Expected to work | `proxy LLM base URL` |

## Evaluation & red-teaming

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [promptfoo](https://github.com/promptfoo/promptfoo) | MIT | 🟢 Expected to work | `provider openai:chat:<id> with config.apiBaseUrl` |
| [garak](https://github.com/NVIDIA/garak) | Apache-2.0 | 🟢 Expected to work | `OpenAI-compatible generator with custom uri` |
| [PyRIT](https://github.com/microsoft/PyRIT) | MIT | 🟢 Expected to work | `OpenAIChatTarget(endpoint=..., api_key=...)` |
| [DeepEval](https://github.com/confident-ai/deepeval) | Apache-2.0 | 🟢 Expected to work | `custom OpenAI base URL model` |
| [Ragas](https://github.com/vibrantlabsai/ragas) | Apache-2.0 | 🟢 Expected to work | `wrap a LangChain ChatOpenAI(base_url=...)` |
| [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | MIT | 🟢 Expected to work | `--model openai-api/<id> with OPENAI_BASE_URL` |
| [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | MIT | 🟢 Expected to work | `--model local-chat-completions --model_args base_url=...` |
| [Giskard](https://github.com/Giskard-AI/giskard-oss) | Apache-2.0 | 🟢 Expected to work | `OpenAI-compatible client base URL` |
| [Guardrails](https://github.com/guardrails-ai/guardrails) | Apache-2.0 | 🟢 Expected to work | `model='openai/<id>', api_base=...` |
| [agentic-radar](https://github.com/splx-ai/agentic-radar) | Apache-2.0 | 🟢 Expected to work | `OpenAI base URL` |
| [Agentic Security](https://github.com/msoedov/agentic_security) | Apache-2.0 | 🟢 Expected to work | `target URL of an OpenAI-compatible endpoint` |
| [Prompt Fuzzer](https://github.com/prompt-security/ps-fuzz) | MIT | 🟢 Expected to work | `OpenAI base URL` |

## Cybersecurity

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [SOC triage agent](https://github.com/Software-Tailor/ai-server-security-agents) | MIT | ✅ Verified ([evidence](https://github.com/Software-Tailor/ai-server-security-agents)) | `AISERVER_BASE_URL / AISERVER_API_KEY / AISERVER_MODEL` |
| [PentestGPT](https://github.com/GreyDGL/PentestGPT) | MIT | 🟢 Expected to work — Authorised targets only. | `OpenAI-compatible base URL` |
| [PentAGI](https://github.com/vxcontrol/pentagi) | MIT | 🟢 Expected to work — Authorised targets only. | `custom OpenAI-compatible LLM provider URL` |
| [Strix](https://github.com/usestrix/strix) | Apache-2.0 | 🟢 Expected to work — Authorised targets only. | `LLM_API_BASE + model openai/<id>` |
| [hackingBuddyGPT](https://github.com/ipa-lab/hackingBuddyGPT) | MIT | 🟢 Expected to work — Authorised targets only. | `llm.api_url` |
| [MCP Scanner](https://github.com/cisco-ai-defense/mcp-scanner) | Apache-2.0 | 🟢 Expected to work | `LLM analyzer base URL` |

## Command line

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [llm (Simon Willison)](https://github.com/simonw/llm) | Apache-2.0 | 🟢 Expected to work | `extra-openai-models.yaml api_base` |
| [aichat](https://github.com/sigoden/aichat) | Apache-2.0 | 🟢 Expected to work | `config.yaml type openai-compatible, api_base` |
| [Shell GPT](https://github.com/TheR1D/shell_gpt) | MIT | 🟢 Expected to work | `API_BASE_URL` |
| [Open Interpreter](https://github.com/openinterpreter/openinterpreter) | Apache-2.0 | 🟢 Expected to work | `--api_base` |

## Observability & gateways

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | MIT | 🟢 Expected to work | `custom provider customHost` |
| [Helicone](https://github.com/Helicone/helicone) | Apache-2.0 | 🟢 Expected to work | `proxy base_url` |
| [Opik](https://github.com/comet-ml/opik) | Apache-2.0 | 🟢 Expected to work | `track an OpenAI client with base_url` |
| [OpenLLMetry](https://github.com/traceloop/openllmetry) | Apache-2.0 | 🟢 Expected to work | `instruments the OpenAI SDK` |

## Data & documents

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [MarkItDown](https://github.com/microsoft/markitdown) | MIT | 🟢 Expected to work | `llm_client=OpenAI(base_url=...) for image captions` |
| [Docling](https://github.com/docling-project/docling) | MIT | 🟢 Expected to work | `VLM options with OpenAI-compatible URL` |
| [Marker](https://github.com/datalab-to/marker) | Apache-2.0 | 🟢 Expected to work | `LLM service base URL` |
| [paperless-gpt](https://github.com/icereed/paperless-gpt) | MIT | 🟢 Expected to work | `OPENAI_BASE_URL` |
| [Presenton](https://github.com/presenton/presenton) | Apache-2.0 | 🟢 Expected to work | `custom OpenAI-compatible URL` |

## Browser automation

| Project | Licence | Status | How to point it at AI Server |
| --- | --- | --- | --- |
| [browser-use](https://github.com/browser-use/browser-use) | MIT | 🟢 Expected to work | `ChatOpenAI(base_url=...)` |
| [Stagehand](https://github.com/browserbase/stagehand) | MIT | 🟢 Expected to work | `modelClientOptions.baseURL` |

## Check the licence first

| Project | Licence | Note |
| --- | --- | --- |
| [Open WebUI](https://github.com/open-webui/open-webui) | Open WebUI License (BSD-3 + branding clause) | Works (config in ai-server-dropin-recipes); the licence restricts rebranding, so check it before redistributing a customised build. |
| [Dify](https://github.com/langgenius/dify) | Modified Apache-2.0 | Restricts multi-tenant SaaS use; read before commercial deployment. |
| [LiteLLM](https://github.com/BerriAI/litellm) | MIT core + enterprise directory | Core is MIT; enterprise features are separately licensed. |
| [Flowise](https://github.com/FlowiseAI/Flowise) | Apache-2.0 + commercial terms for some parts | Check the current licence file. |
| [Langfuse](https://github.com/langfuse/langfuse) | MIT core + EE directory | Enterprise directory is not MIT. |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | Elastic License 2.0 | Source-available; not for managed-service resale. |
| [Lobe Chat](https://github.com/lobehub/lobe-chat) | Custom (Apache-2.0 based) | Commercial-use conditions apply. |
| [Jan](https://github.com/janhq/jan) | Check current licence | Licence has changed over time. |

Copyleft or fair-code projects (GPL, AGPL, SSPL, Sustainable Use) are not listed as recommendations, even though several work with AI Server: e.g. n8n, SillyTavern, Chatbox, Cherry Studio, Khoj.
