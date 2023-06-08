[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?logo=githubactions&logoColor=white)](https://github.com/Sanchoyzer/caraconnect/actions)
![GitHub commit activity](https://img.shields.io/github/commit-activity/y/Sanchoyzer/caraconnect)
![GitHub last commit](https://img.shields.io/github/last-commit/Sanchoyzer/caraconnect)

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)

---

Implement the method `nextNum()` and an effective set of deterministic unit tests.
Make sure your code is exemplary, as if it was going to be shipped as part of a production system.

As a quick check, given Random Numbers are `[-1, 0, 1, 2, 3]` and
Probabilities are `[0.01, 0.3, 0.58, 0.1, 0.01]`
if we call nextNum() 100 times we may get the following results.

As the results are random, these particular results are unlikely.
```
-1: 1 times
0: 22 times
1: 57 times
2: 20 times
3: 0 times
```

You may use `random.random()` which returns a pseudo random number between 0 and 1.

You can use the following structure for your code.
If possible, make this structure more pythonic.

```python
import random

class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []

    # Probability of the occurence of random_nums
    _probabilities = []

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        """

```
