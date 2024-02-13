# Anycode

**Anycode** is a Python module that uses ChatGPT to automatically generate constants and functions based on their name.

Just import `anycode` and use its dynamically-generated attributs: `anycode.PI` is `3.14…`,
`anycode.SAMPLE_10_NAMES` is `['John', 'Jane', 'Adam', 'Eve', …]`, `anycode.SAMPLE_ISBN` is `"978-1-56619-909-4"` and
so on.

This works on functions, too:

```python
import anycode

anycode.fetch_wikipedia_article_intro("Angelina Mango")
# => "Angelina Mango is an Italian singer-songwriter. …"

anycode.get_random_number_between(1000, 2000)
# => 1241 (for example)

anycode.multiply(4, 5)
# => 20

anycode.say_hello("Baptiste")
# prints "Hello, Baptiste!"
```

**Note:** I wrote this module for fun, please don’t use it in production.

## Install

    pip install anycode

Or with Poetry:

    poetry add anycode

We support Python 3.9+.

## Usage

Note: you need a valid [OpenAI API key](https://platform.openai.com/api-keys). See below how to configure it.

Any attribute written in `UPPER_CASE` is assumed to be a single value:

```python
import anycode

print(anycode.PI)  # 3.141592...
print(anycode.SAMPLE_EAN13)  # 9780141036148
print(anycode.SAMPLE_ISBN)  # 978-1-56619-909-4

print(anycode.TWO + anycode.TWO)  # 4

print(anycode.ROT13_DICT)  # {'A': 'N', 'B': 'O', 'C': 'P', 'D': 'Q', 'E': 'R', ...}

print(anycode.TEN_RANDOM_QUOTES) # ['The only way to do great work is to love what you do. - Steve Jobs', ...]

print(anycode.OPENAI_API_KEY)  # raises a GenerationException("Cannot generate code for 'OPENAI_API_KEY'")
```

If you prefer can also import from the module:

```python
from anycode import HELLO, WORLD

print(HELLO + " " + WORLD)
```

Any other value is a function:

```python
import anycode

type(anycode.say_goodbye)
# => <class 'function'>

anycode.say_goodbye("John")
# prints "Goodbye, John!"
```

Note that only simple functions work; if you try complex things ChatGPT fails to generate valid code and/or tries to
import third-party modules.
The generated code is executed on your machine, so do not use this in production.

The function is generated when it’s called for the first time, so we know how many arguments it should take. Further
calls reuse the cached function. Once a function has been generated, you can access `._openai_fn` on it to get the
ChatGPT-generated function and `.openai_response` to get the ChatGPT text response.

### Exceptions

When OpenAI can’t generate a valid value, the module raises a `GenerationException` that you can inspect to
understand what went wrong.
Use its `query` attribute to get the query used to generate the code and `openai_response` to get the response text from
OpenAI.

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

## Configuration

### OpenAI API key

By default Anycode takes the value of the `OPENAI_API_KEY` from your environment or from a `.env` file.
You can also explicitly set it:

```python
import anycode

anycode.set_openai_api_key("your-api-key")

# or from an environment variable
anycode.set_openai_api_key_from_env("MY_OPENAI_API_KEY")
```

### Advanced configuration

The OpenAI client can be directly accessed and modified:

```python
from anycode.client import openai_client

openai_client.default_headers = {"x-foo": "true"}
```

## License

Copyright © 2024 – Baptiste Fontaine. See the [LICENSE](./LICENSE) file.
