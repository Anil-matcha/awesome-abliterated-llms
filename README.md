# Awesome Abliterated LLMs

> A practical guide to deployed abliterated and derestricted LLM endpoints on Muapi, with model comparisons and copy-paste API examples.

This repository focuses on using the hosted endpoints through one API. It is a developer guide, while [awesome-uncensored-llms](https://github.com/Anil-matcha/awesome-uncensored-llms) is the broader catalog of open-weight and community-reported language models.

“Abliterated” and “derestricted” describe modifications intended to reduce refusal behavior. They do not guarantee unrestricted responses, consistent behavior, or better answer quality. A hosted route name is not proof of the exact upstream checkpoint or license. Verify current terms and evaluate each model for your use case.

**README and live capability snapshot reviewed:** 2026-10-06. Routes, prices, and model capabilities can change; check the linked live pages before use.

## Contents

- [Use cases](#use-cases)
- [Quick start](#quick-start)
- [Deployed endpoint catalog](#deployed-endpoint-catalog)
- [Choose an endpoint for your workflow](#choose-an-endpoint-for-your-workflow)
- [Streaming](#streaming)
- [Request fields and limits](#request-fields-and-limits)
- [Coding agents and tool calling](#coding-agents-and-tool-calling)
- [Provenance and evaluation](#provenance-and-evaluation)

## Related Projects

- [Muapi Abliterated LLM API](https://muapi.ai/abliterated-llm-api) — Live model lineup, per-token prices, endpoint details, and playground links.
- [Muapi API quick start](https://muapi.ai/docs/quick-start) — Authentication and request lifecycle.
- [Muapi access keys](https://muapi.ai/access-keys) — Create an API key for the examples below.
- [Broader language-model catalog](https://github.com/Anil-matcha/awesome-uncensored-llms) — Open-weight and community-reported models with source and provenance notes.
- [Awesome Uncensored Coding Models](https://github.com/Anil-matcha/awesome-uncensored-coding-models) — coding use cases, hosted candidates, benchmark runner, and agent setup.
- [Awesome Uncensored AI Agents](https://github.com/Anil-matcha/awesome-uncensored-ai-agents) — general-purpose agent setup and safety guidance.
- [Awesome Uncensored AI Models](https://github.com/Anil-matcha/awesome-uncensored-ai-models) — index for the language, image, and video catalogs.

## Quick start

Create a Muapi key, then set it in your shell:

```bash
export MUAPI_API_KEY="your-api-key"
```

Submit one prompt to an endpoint. Replace the slug with any entry from the catalog below:

```bash
curl -X POST "https://api.muapi.ai/api/v1/qwen-3-8-27b-abliterated" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Compare the trade-offs in this design proposal.","system_prompt":"Be concise and explain uncertainty.","max_tokens":512}'
```

The response contains a `request_id`. Poll for the result:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  -H "x-api-key: $MUAPI_API_KEY"
```

The Python example in [`examples/python/submit_and_poll.py`](examples/python/submit_and_poll.py) submits a prompt and polls until it completes. It uses only the Python standard library.

## Use cases

The hosted routes are useful for trying model variants through one API and adding text generation to an application. The exact route determines its supported inputs and behavior.

| Use case | API path to consider | What to check |
|---|---|---|
| **One-shot question or chat turn** | A model-specific endpoint such as `/api/v1/qwen-3-8-27b-abliterated`. | Send one prompt; keep conversation state in your application if needed. Check per-model output limits and price. |
| **Summaries, drafts, and transformations** | Model-specific endpoint; use `system_prompt` for task instructions. | Test against representative examples and preserve source facts. Do not treat a lower refusal rate as better writing or accuracy. |
| **Image-grounded question** | A model-specific endpoint that lists image input support; supply `image_url`. | Confirm that the exact route accepts the image format and that the asset is accessible to the API. |
| **Incremental UI output** | Append `/stream` to a model-specific endpoint. | Handle SSE chunks, errors, and the terminal `[DONE]` event in the client. |
| **Coding answer from one prompt** | A text or vision-capable route suited to the input. | Compare the result with tests or a known answer. A code answer is not evidence of repository tool use. |
| **Coding agent or multi-turn tool workflow** | Muapi’s OpenAI-compatible chat/agent endpoint rather than the single-turn route below. | Check the live model’s tool capability, exact agent protocol, tool-call round trip, and permissions. Start with [Awesome Uncensored Coding Models](https://github.com/Anil-matcha/awesome-uncensored-coding-models). |

These model-specific generation endpoints accept one prompt per request; they do not expose an agent tool loop. Use the separate compatible chat endpoint for agent integrations and verify the capabilities at that route.

## Deployed endpoint catalog

The links below go to Muapi's live family landing pages. They contain current prices, model-specific input support, and playground links. Prices and route capabilities can change, so check the landing page before shipping an integration.

| Model | Endpoint slug | Muapi model guide |
| --- | --- | --- |
| Abliterated Model | `abliterated-model` | [Abliterated Model API](https://muapi.ai/abliterated-model-api) |
| Abliterated Model Large | `abliterated-model-large` | [Abliterated Model API](https://muapi.ai/abliterated-model-api) |
| Abliterated Model Large V2 | `abliterated-model-large-v2` | [Abliterated Model API](https://muapi.ai/abliterated-model-api) |
| MiMo V2.6 Flash Abliterated | `mimo-v2-6-flash-abliterated` | [MiMo Abliterated API](https://muapi.ai/mimo-abliterated-api) |
| Qwen 3.8 27B Abliterated | `qwen-3-8-27b-abliterated` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Qwen 3.8 27B Obliterated | `qwen-3-8-27b-obliterated` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Qwen 2.5 32B Abliterated | `qwen-2-5-32b-abliterated` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Qwen3.5 27B Queen Derestricted | `qwen-3-5-27b-queen-derestricted` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Qwen3.5 27B Blossom Derestricted | `qwen-3-5-27b-blossom-derestricted` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Qwen3.5 27B Opus-Distilled Derestricted | `qwen-3-5-27b-opus-distilled-derestricted` | [Qwen Abliterated API](https://muapi.ai/qwen-abliterated-api) |
| Llama 3.3 70B Abliterated | `llama-3-3-70b-abliterated` | [Llama Abliterated API](https://muapi.ai/llama-abliterated-api) |
| NeuralDaredevil 8B Abliterated | `neuraldaredevil-8b-abliterated` | [Llama Abliterated API](https://muapi.ai/llama-abliterated-api) |
| DeepSeek R1 Distill Llama 70B Abliterated | `deepseek-r1-llama-70b-abliterated` | [DeepSeek R1 Abliterated API](https://muapi.ai/deepseek-r1-abliterated-api) |
| DeepSeek R1 Distill Qwen 32B Abliterated | `deepseek-r1-qwen-32b-abliterated` | [DeepSeek R1 Abliterated API](https://muapi.ai/deepseek-r1-abliterated-api) |
| GLM 5.3 Flash Abliterated | `glm-5-3-flash-abliterated` | [GLM Abliterated API](https://muapi.ai/glm-abliterated-api) |
| GLM 5.3 Abliterated | `glm-5-3-abliterated` | [GLM Abliterated API](https://muapi.ai/glm-abliterated-api) |
| GLM 4.6 Derestricted v5 | `glm-4-6-derestricted-v5` | [GLM Abliterated API](https://muapi.ai/glm-abliterated-api) |
| Gemma 4 26B A4B Abliterated | `gemma-4-26b-a4b-abliterated` | [Gemma Abliterated API](https://muapi.ai/gemma-abliterated-api) |
| Gemma 4 31B Gembrain Abliterated | `gemma-4-31b-gembrain-abliterated` | [Gemma Abliterated API](https://muapi.ai/gemma-abliterated-api) |
| Gemma 4 31B SDFT Abliterated | `gemma-4-31b-sdft-abliterated` | [Gemma Abliterated API](https://muapi.ai/gemma-abliterated-api) |

### Choosing a model

Compare these points on the linked family pages before choosing an endpoint:

| Criterion | What to check |
| --- | --- |
| Cost | Current input and output price per million tokens, plus minimum request charge. |
| Context | Maximum input context and output-token cap for the exact model. |
| Inputs | Text-only or image input; image support varies by endpoint. |
| Reasoning | `thinking` is available on the two Qwen 3.8 variants only. |
| Tool use | Supported models vary; verify the exact model and request route before relying on tool calls. |
| Quality | Test ordinary tasks, edge cases, factuality, and refusal behavior against a baseline. |

Do not use a single “low-refusal score” as a quality ranking. Record the endpoint slug, date, prompt setup, and separate refusal behavior from accuracy, instruction following, latency, and cost.

## Choose an endpoint for your workflow

Start with the input and interaction shape you need, then compare exact models using the current model-specific landing pages.

1. **Text only:** choose a text endpoint and keep the request small enough for its current input/output limits.
2. **Image input:** use a route whose page and live model metadata both show vision support; test image delivery end to end.
3. **Reasoning mode:** the live Muapi text list currently marks the two Qwen 3.8 abliterated/obliterated IDs as `thinking: true`. Confirm the dedicated route’s supported `thinking` option and current guidance before sending it.
4. **Streaming:** use `/stream` when your application needs incremental events; preserve the same model-specific fields and parse SSE correctly.
5. **Agent tools:** use the OpenAI-compatible endpoint and require `capabilities.tools: true`. A dedicated model route accepting a prompt does not itself make an agent integration.
6. **Cost-sensitive batches:** check the current model price and output cap, estimate the number of requests, and monitor dashboard usage during a small trial.

### Inspect live text-model capabilities

Do not copy a model list into a long-lived integration. Query the model catalog and check the exact model ID and flags:

```bash
curl -s "https://api.muapi.ai/v1/models?type=text" \
  -H "Authorization: Bearer $MUAPI_API_KEY"
```

For an agent, use the exact ID from the compatible endpoint’s own `/models` route when available. `capabilities.tools: true` indicates tool-call support in the listed API; test an actual call through your chosen agent before relying on it.

## Streaming

Append `/stream` to the model endpoint and send the same prompt fields. The response uses Server-Sent Events:

```bash
curl -N -X POST "https://api.muapi.ai/api/v1/qwen-3-8-27b-abliterated/stream" \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain the key trade-offs in three short points.","max_tokens":256}'
```

The stream sends `data:` events and ends with `data: [DONE]`. See [`examples/javascript/stream.mjs`](examples/javascript/stream.mjs) for a minimal Node.js reader.

## Request fields and limits

The single-turn endpoint accepts:

- `prompt` (required)
- `system_prompt` (optional)
- `max_tokens` (optional; clamped to the per-model limit)
- `image_url` (optional, only for image-capable endpoints)
- `thinking` (optional, only for Qwen 3.8 Abliterated and Obliterated)

These routes take one prompt per request. For multi-turn conversation state or additional sampling controls, use the [Muapi API reference](https://muapi.ai/docs/api-reference) and verify the model's supported chat-completions features. Tool calling is model-specific. No endpoint guarantees a particular answer or refusal policy.

## Coding agents and tool calling

The model-specific `/api/v1/{model}` examples above are single-turn generation calls. For coding agents, use the [OpenAI-compatible Chat Completions API](https://muapi.ai/docs/openai-compatible) or the relevant native agent integration, then select an exact model that advertises tool support on that endpoint. Muapi also documents [Codex CLI, Claude Code, and other coding-agent setup](https://muapi.ai/docs/ai-agent-install-chat-agents).

Do not infer agent compatibility from a model family, model card, or the model-specific endpoint. Test a harmless read-only task first, then a bounded edit in a disposable workspace. Check the agent’s permissions, usage, and provider terms before connecting a real repository or channel.

## Provenance and evaluation

The endpoint slug identifies a deployed Muapi route; it does not verify the exact checkpoint, derivative method, license, or consistent refusal behavior. Follow the linked family page to its primary source where available, and keep upstream-family claims separate from claims about a hosted variant.

There is no benchmark ranking in this repository. If you compare models, hold prompts and settings constant, use a task set relevant to your use case, repeat variable tasks, preserve raw results, and report failure cases. Score quality, instruction following, refusal behavior, latency, and cost separately. For coding-specific candidate workflows and an evaluation runner, see [Awesome Uncensored Coding Models](https://github.com/Anil-matcha/awesome-uncensored-coding-models).

## How to contribute

Open an issue or pull request with the exact endpoint slug, a current Muapi page, access and input details, the date checked, and evidence for any behavior claim. Do not infer upstream weights, licenses, or behavior from an endpoint name. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Responsible use

Use the models lawfully and responsibly. Do not create or facilitate sexual content involving minors, non-consensual intimate imagery, targeted harassment, fraud, impersonation, or other illegal or abusive material. Follow Muapi terms, model licenses, and applicable law.

## License

Original documentation and example code in this repository are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The models, services, APIs, and linked resources have their own licenses and terms.
