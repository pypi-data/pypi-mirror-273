# Bland AI Python Library

[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)
[![pypi](https://img.shields.io/pypi/v/bland.svg)](https://pypi.python.org/pypi/bland)

The Bland AI Python Library provides convenient access to the Bland AI API from 
applications written in Python. 

The library includes type definitions for all 
request and response fields, and offers both synchronous and asynchronous clients powered by httpx.

## Installation

Add this dependency to your project's build file:

```bash
pip install bland
# or
poetry add bland
```

## Usage
Simply import `BlandAI` and start making calls to our API. 

```python
from blandai import PronunciationObject, SendCall
from blandai.client import BlandAI

client = BlandAI(
    api_key="YOUR_API_KEY"  # Defaults to your BLAND_API_KEY environment variable
)

client.call(
    request=SendCall(
        phone_number="29382721828",
        task="Would love for you to check out our AI API!",
        transfer_list={
            "default": "+1234567890",
            "sales": "+1234567890",
            "support": "+1234567890",
            "billing": "+1234567890",
        },
        model="enhanced",
        pronunciation_guide=[
            PronunciationObject(
                word="API",
                pronunciation="A P I",
            ),
            PronunciationObject(
                word="AI",
                pronunciation="ei ai",
            ),
        ],
    ),
)
```

## Async Client
The SDK also exports an async client so that you can make non-blocking
calls to our API. 

```python
from blandai import PronunciationObject, SendCall
from blandai.client import BlandAI

client = AsyncBlandAI(
  api_key="YOUR_API_KEY" # Defaults to your BLAND_API_KEY environment variable
)

async def main() -> None:
    await client.call(
        request=SendCall(
            phone_number="29382721828",
            task="Would love for you to check out our AI API!",
            transfer_list={
                "default": "+1234567890",
                "sales": "+1234567890",
                "support": "+1234567890",
                "billing": "+1234567890",
            },
            model="enhanced",
            pronunciation_guide=[
                PronunciationObject(
                    word="API",
                    pronunciation="A P I",
                ),
                PronunciationObject(
                    word="AI",
                    pronunciation="ei ai",
                ),
            ],
        ),
    )

asyncio.run(main())
```

## BlandAI Module
All of the models are nested within the BlandAI module. Let IntelliSense 
guide you! 

![Alt text](assets/module.png)

## Exception Handling
All errors thrown by the SDK will be subclasses of [`ApiError`](./src/blandai/core/api_error.py).

```python
import blandai

try:
  client.call(...)
except blandai.core.ApiError as e: # Handle all errors
  print(e.status_code)
  print(e.body)
```

## Advanced

### Timeouts
By default, requests time out after 60 seconds. You can configure this with a 
timeout option at the client or request level.

```python
from blandai.client import BlandAI

client = BlandAI(
    # All timeouts are 20 seconds
    timeout=20.0,
)

# Override timeout for a specific method
client.call(..., {
    timeout_in_seconds=20.0
})
```

### Custom HTTP client
You can override the httpx client to customize it for your use-case. Some common use-cases 
include support for proxies and transports.

```python
import httpx

from blandai.client import BlandAI

client = BlandAI(
    http_client=httpx.Client(
        proxies="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
```

## Beta Status

This SDK is in **Preview**, and there may be breaking changes between versions without a major 
version update. 

To ensure a reproducible environment (and minimize risk of breaking changes), we recommend pinning a specific package version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. 
Additions made directly to this library would have to be moved over to our generation code, 
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as
 a proof of concept, but know that we will not be able to merge it as-is. We suggest opening 
an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
