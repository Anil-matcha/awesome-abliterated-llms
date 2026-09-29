#!/usr/bin/env node
// Stream text from a Muapi model endpoint using Node.js built-in fetch.

const [model, ...promptParts] = process.argv.slice(2);
const prompt = promptParts.join(" ");
const apiKey = process.env.MUAPI_API_KEY;

if (!model || !prompt || !apiKey) {
  console.error("Usage: MUAPI_API_KEY=... node stream.mjs <model-slug> <prompt>");
  process.exit(2);
}
if (!/^[a-z0-9-]+$/.test(model)) {
  console.error("Model must be a lowercase endpoint slug from the README table.");
  process.exit(2);
}

const response = await fetch(`https://api.muapi.ai/api/v1/${model}/stream`, {
  method: "POST",
  headers: {
    "x-api-key": apiKey,
    "Content-Type": "application/json",
    Accept: "text/event-stream",
  },
  body: JSON.stringify({ prompt, max_tokens: 512 }),
});

if (!response.ok || !response.body) {
  console.error(`Muapi returned HTTP ${response.status}: ${await response.text()}`);
  process.exit(1);
}

const reader = response.body.getReader();
const decoder = new TextDecoder();
let buffer = "";
let finished = false;

while (!finished) {
  const { value, done } = await reader.read();
  buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
  const events = buffer.split("\n\n");
  buffer = events.pop() || "";

  for (const event of events) {
    const line = event.split("\n").find((entry) => entry.startsWith("data: "));
    if (!line) continue;
    const data = line.slice(6);
    if (data === "[DONE]") {
      finished = true;
      break;
    }
    const parsed = JSON.parse(data);
    if (parsed.error) throw new Error(parsed.error);
    const text = parsed.choices?.[0]?.delta?.content;
    if (text) process.stdout.write(text);
  }

  if (done) finished = true;
}
process.stdout.write("\n");
