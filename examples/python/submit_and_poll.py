#!/usr/bin/env python3
"""Submit one prompt to a Muapi model endpoint and poll its result."""

import argparse
import json
import os
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_ROOT = "https://api.muapi.ai"


def request_json(url: str, api_key: str, method: str = "GET", payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = Request(
        url,
        data=body,
        method=method,
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urlopen(req, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", help="Endpoint slug from the README model table")
    parser.add_argument("prompt", help="Prompt text to submit")
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--timeout", type=int, default=600, help="Polling timeout in seconds")
    args = parser.parse_args()

    api_key = os.environ.get("MUAPI_API_KEY")
    if not api_key:
        parser.error("Set MUAPI_API_KEY in the environment first")
    if not re.fullmatch(r"[a-z0-9-]+", args.model):
        parser.error("Model must be a lowercase endpoint slug from the README table")

    try:
        submitted = request_json(
            f"{API_ROOT}/api/v1/{args.model}",
            api_key,
            method="POST",
            payload={"prompt": args.prompt, "max_tokens": args.max_tokens},
        )
        request_id = submitted.get("request_id")
        if not request_id:
            raise RuntimeError(f"Submit response did not contain request_id: {submitted}")
        print(f"Submitted request {request_id}; waiting for completion…", file=sys.stderr)

        deadline = time.monotonic() + args.timeout
        while time.monotonic() < deadline:
            result = request_json(
                f"{API_ROOT}/api/v1/predictions/{request_id}/result", api_key
            )
            status = result.get("status")
            if status == "completed":
                print(json.dumps(result, indent=2))
                return
            if status == "failed":
                print(json.dumps(result, indent=2), file=sys.stderr)
                raise SystemExit(1)
            time.sleep(2)
        raise TimeoutError(f"Request {request_id} did not complete within {args.timeout}s")
    except HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        print(f"Muapi returned HTTP {exc.code}: {details}", file=sys.stderr)
        raise SystemExit(1)
    except (URLError, TimeoutError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
