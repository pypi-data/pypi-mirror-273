# cleanse-speech 🚀

[![PyPI version](https://badge.fury.io/py/cleanse_speech.svg)](https://badge.fury.io/py/cleanse_speech)
[![Downloads](https://pepy.tech/badge/cleanse_speech)](https://pepy.tech/project/cleanse_speech)
[![Downloads](https://pepy.tech/badge/cleanse_speech/month)](https://pepy.tech/project/cleanse_speech)

Python🐍 3.9+ support.

A library for cleansing sensitive words in speech.

> [!NOTE]
> This library is designed with the intent to promote a harmonious online environment by identifying and
> addressing offensive language. It is **not** intended to enforce strict censorship or infringe upon free speech. Our
> goal is to foster respectful communication and ensure that all users feel safe and included in online communities. By
> using this library, developers can help create spaces where open dialogue is encouraged while maintaining a level of
> decency and mutual respect.

## Installation

```shell
pip install cleanse-speech
```

## Usage

```python
import io

from cleanse_speech import DLFA
from cleanse_speech import SpamShelf

if __name__ == '__main__':
    dfa = DLFA(words_resource=[
        ['你好'],
        io.BytesIO(b'sensitive'),
        SpamShelf.CN.ADVERTISEMENT,
    ])
    print(dfa.contains_illegal('This is a 你好 word.'))
    print(dfa.censor_all('This is a 你好 word.'))
    print(dfa.extract_illegal_words('This is a 你好 word.'))
    dfa.update_words(['sensitive', 'word', 'new'])
    print(dfa.extract_illegal_words('This is a new sensitive word.'))
```