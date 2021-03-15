import os
from os import path

class InvertedIndexDictionary:
    word = ''
    doc_ids = set()
    next = None

    def __init__(self, doc_id: int, new_word: str):
        self.doc_ids = set(doc_id)
        self.word = new_word

    @staticmethod
    def create_new_item(doc_id: int, head: "InvertedIndexDictionary", word: str):
        same_word_element = InvertedIndexDictionary.search(head, word)
        if same_word_element is not None:
            same_word_element.doc_ids.Add(doc_id)
            return same_word_element
        else:
            tail = InvertedIndexDictionary.get_tail(head)
            new_item = InvertedIndexDictionary(doc_id, word)
            tail.next = new_item
            return new_item

    @staticmethod
    def search(node: "InvertedIndexDictionary", word: str):
        if node.word == word:
            return node
        next = node.next
        if next is not None:
            return InvertedIndexDictionary.search(next, word)
        return None

    @staticmethod
    def get_tail(head: "InvertedIndexDictionary"):
        next = head.next
        if next is None:
            return head
        return InvertedIndexDictionary.get_tail(next)


def create_index():
    punctuation_marks = [
        ",",
        ":",
        ";",
        " - ",
        " \"",
        "\" ",
        "!",
        "...",
        "?",
        "."
    ]
    sentence_end_marks = [
        "!",
        "...",
        "?",
    ]
    numbers = {
        "0": "ноль",
        "1": "один",
        "2": "два",
        "3": "три",
        "4": "четыре",
        "5": "пять",
        "6": "шесть",
        "7": "семь",
        "8": "восемь",
        "9": "девять"
    }
    folder_name = "documents/"
    all_files = os.listdir(folder_name)
    txt_files = filter(lambda x: x[-4:] == '.txt', all_files)
    basepath = path.dirname(__file__)
    for filename in txt_files:
        filepath = path.abspath(path.join(basepath, "..", f'{folder_name}{filename}'))


create_index()
