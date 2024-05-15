import io
import pathlib
import re
from typing import Union, List, Dict, Any


class DLFA:
    def __init__(self, words_resource: List[Union[List[str], io.BytesIO, pathlib.Path]]) -> None:
        """
        Initialize a DFA to detect and censor sensitive words.
        :param words_resource:  A list of sensitive words or a BytesIO object that contains sensitive words.
        """
        self.ban_words_set = set()
        self.ban_words_list: List[str] = []
        self.ban_words_dict: Dict[str, Any] = {}
        for resource in words_resource:
            self.extract_words(resource)

    def extract_words(self, words_resource: Union[List[str], io.BytesIO, pathlib.Path]) -> None:
        """
        Extract sensitive words from a list or a BytesIO object.
        :param words_resource: A list of sensitive words or a BytesIO object that contains sensitive words.
        :return: None
        """
        import base64

        if isinstance(words_resource, io.BytesIO):
            words = words_resource.getvalue().decode('utf-8').splitlines()
        elif isinstance(words_resource, pathlib.Path):
            if not words_resource.exists():
                raise FileNotFoundError(f"File {words_resource} not found.")
            with open(words_resource, 'r') as f:
                words = f.readlines()
        else:
            words = words_resource
        for word in words:
            word = word.strip()
            if word:
                try:
                    decoded_word = base64.b64decode(word).decode('utf-8')
                    word_to_add = decoded_word
                except (Exception, UnicodeDecodeError):
                    word_to_add = word
                if word_to_add not in self.ban_words_set:
                    self.ban_words_set.add(word_to_add)
                    self.ban_words_list.append(word_to_add)
        self.build_ban_words_dict(self.ban_words_list)

    def update_words(self, words_resource: Union[List[str], io.BytesIO]) -> None:
        """
        Update the sensitive words list.
        :param words_resource: A list of sensitive words or a BytesIO object that contains sensitive words.
        :return: None
        """
        self.ban_words_list.clear()
        self.ban_words_dict.clear()
        self.ban_words_set.clear()
        self.extract_words(words_resource)

    def build_ban_words_dict(self, word_list: List[str]) -> None:
        """
        Build a dictionary that represents the sensitive words.
        :param word_list:  A list of sensitive words.
        :return:  None
        """
        for word in word_list:
            self.add_word_to_DFA(word)

    def add_word_to_DFA(self, word: str) -> None:
        """
        Add a sensitive word to the DFA.
        :param word: A sensitive word.
        :return: None
        """
        current_dict = self.ban_words_dict
        for index, char in enumerate(word):
            current_dict = current_dict.setdefault(char, {'is_end': False})
            if index == len(word) - 1:
                current_dict['is_end'] = True

    def find_illegal_pos(self, text: str) -> int:
        """
        Find the position of the first illegal word in the text.
        :param text: A text.
        :return: The position of the first illegal word in the text.
        """
        current_dict = self.ban_words_dict
        i = 0
        word_start = -1
        word_starting = True
        while i < len(text):
            if text[i] not in current_dict:
                if not word_starting:
                    i = word_start + 1
                    word_start = -1
                    current_dict = self.ban_words_dict
                else:
                    i += 1
                word_starting = True
            else:
                if word_starting:
                    word_start = i
                    word_starting = False
                current_dict = current_dict[text[i]]
                if current_dict['is_end']:
                    return word_start
                else:
                    i += 1
        return -1

    def contains_illegal(self, text: str) -> bool:
        """
        Check if the text contains any illegal words.
        :param text: A text.
        :return: True if the text contains any illegal words, False otherwise.
        """
        stripped_text = re.sub('\W+', '', text).replace("_", '')
        return self.find_illegal_pos(stripped_text) != -1

    def censor_text(self, text: str, start_pos: int) -> str:
        """
        Censor the illegal word in the text.
        :param text: The text.
        :param start_pos: The position of the illegal word in the text.
        :return: The text with the illegal word censored.
        """
        end_pos = start_pos
        current_dict = self.ban_words_dict[text[start_pos]]
        while end_pos + 1 < len(text) and text[end_pos + 1] in current_dict and not current_dict['is_end']:
            end_pos += 1
            current_dict = current_dict[text[end_pos]]
        if current_dict['is_end']:
            end_pos += 1
        return text[:start_pos] + '*' * (end_pos - start_pos) + text[end_pos:]

    def censor_all(self, text: str) -> str:
        """
        Censor all illegal words in the text.
        :param text: The text.
        :return: The text with all illegal words censored.
        """
        illegal_pos = self.find_illegal_pos(text)
        while illegal_pos != -1:
            text = self.censor_text(text, illegal_pos)
            illegal_pos = self.find_illegal_pos(text)
        return text

    def extract_illegal_words(self, text: str) -> List[str]:
        """
        Extract all illegal words from the text.
        :param text: The text.
        :return: A list of illegal words.
        """
        illegal_words = []
        pos = 0
        while pos < len(text):
            start_pos = self.find_illegal_pos(text[pos:])
            if start_pos != -1:
                end_pos = start_pos
                current_dict = self.ban_words_dict[text[pos + start_pos]]
                while end_pos + 1 < len(text[pos:]) and text[pos + end_pos + 1] in current_dict and not current_dict[
                    'is_end']:
                    end_pos += 1
                    current_dict = current_dict[text[pos + end_pos]]
                if current_dict['is_end']:
                    end_pos += 1
                illegal_words.append(text[pos + start_pos: pos + end_pos])
                pos += end_pos
            else:
                break
        return illegal_words


if __name__ == '__main__':
    dfa = DLFA(words_resource=[
        ['你好'],
        io.BytesIO(b'sensitive'),
    ])
    print(dfa.contains_illegal('This is a 你好 word.'))
    print(dfa.censor_all('This is a 你好 word.'))
    print(dfa.extract_illegal_words('This is a 你好 word.'))
    dfa.update_words(['sensitive', 'word', 'new'])
    print(dfa.contains_illegal('This is a new sensitive word.'))
    print(dfa.censor_all('This is a new sensitive word.'))
    print(dfa.extract_illegal_words('This is a new sensitive word.'))
