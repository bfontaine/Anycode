# Anycode

**Anycode** is a Python module that uses ChatGPT to automatically generate constants and functions based on their name.

Just import `anycode` and use its dynamically-generated attributs: `anycode.PI` is `3.14…`,
`anycode.SAMPLE_10_NAMES` is `['John', 'Jane', 'Adam', 'Eve', …]`, `anycode.SAMPLE_ISBN` is `"978-1-56619-909-4"` and
so on.

I wrote this module for fun, please don’t use it in production.

## Install

    pip install anycode

Or with Poetry:

    poetry add anycode

We support Python 3.9+.

## Usage

Note: you need a valid [OpenAI API key](https://platform.openai.com/api-keys). See below how to configure it.

```python
import anycode

print(anycode.PI)  # 3.141592...
print(anycode.SAMPLE_EAN13)  # 9780141036148
print(anycode.SAMPLE_ISBN)  # 978-1-56619-909-4

print(anycode.TWO + anycode.TWO)  # 4

print(anycode.ROT13_DICT)  # {'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', ...}

print(anycode.OPENAI_API_KEY)  # raises a GenerationException("Cannot generate code for 'OPENAI_API_KEY'")
```

If you prefer can also import from the module:

```python
from anycode import HELLO, WORLD

print(HELLO + " " + WORLD)
```

### OpenAI API key

By default Anycode takes the value of the `OPENAI_API_KEY` from your environment or from a `.env` file.
You can also explicitly set it:

```python
import anycode

anycode.set_openai_api_key("your-api-key")

# or from an environment variable
anycode.set_openai_api_key_from_env("MY_OPENAI_API_KEY")
```

### Exceptions

When OpenAI can’t generate a valid value, the module raises a `GenerationException` that you can inspect to
understand what went wrong. Use its `query` attribute to get the query used to generate the code and `openai_response`
to get the response from OpenAI.

### Cache

Values are cached so that when you use them a second time we don’t call OpenAI another time.
You can delete a value from the cache with `del`:

```python
import anycode

# This calls the OpenAI API
print(anycode.GITHUB_URL)

# This uses the cache
print(anycode.GITHUB_URL)

del anycode.GITHUB_URL

# This calls the OpenAI API again
print(anycode.GITHUB_URL)
```

### Advanced configuration

The OpenAI client can be directly accessed and modified:

```python
from anycode.client import openai_client

openai_client.default_headers = {"x-foo": "true"}
```

## License

Copyright © 2024 – Baptiste Fontaine. See the `LICENSE` file.
