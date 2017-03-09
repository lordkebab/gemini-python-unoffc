# gemini-python-unoffc
Unofficial Python library for the [Gemini Exchange](https://gemini.com) REST API.  This library has methods for all public, private, and order execution methods.  The API documentation can be found [here](https://docs.gemini.com/rest-api/).

Installation
------------
We're on PyPi!  This library is only compatible with Python 3 (right now, see "Future Enhancements" below).

```
pip install gemini-python-unoffc
```

Usage
-----
You need to complete two steps before you can use the library:

1. Register for a [Gemini Exchange Account](https://exchange.gemini.com/register). They also offer a [Sandbox](https://exchange.sandbox.gemini.com/register) for testing purposes.
2. Once registered, obtain an API key and API secret.

Now you are ready to use the library.  Everything is called via a `Client` object:

```python
from gemini.client import Client

c = Client(api_key='API_KEY', api_secret='API_SECRET', sandbox=True)
```

Note the `sandbox` argument.  The default is `False`, so if you want to test on the exchange's sandbox, you need to override this argument and excplicitly set it to `True`.

The `Client` object returns JSON from the exchange's API.  

Example
--------
```python
from gemini.client import Client

c = Client('API_KEY','API_SECRET')
print(c.get_symbols())

print(c.get_balance())
```

Future Enhancements
-------------------
Some feautres planned for later releases include:
- 100% test coverage
- Python 2.x compatibility
- Websocket interface
- Travis CI builds (goes along with 100% test coverage)
- Those neat lil' icons showing "Build Passing," and "100% test coverage"
