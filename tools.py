import itertools
import re
import string
from collections.abc import Generator
from typing import Iterable


def load_dicts(dicts: Iterable[str], min_lenth: int = 1) -> set[str]:
    """Carga palabras a partir de un listado de rutas de archivos."""
    words = set()
    for d in dicts:
        with open(d, "r") as x:
            content = x.readlines()
            new_words = (w.strip().lower() for w in content)
            words.update(set(w for w in new_words if len(w) >= min_lenth))
    return words


def find_words(text: str, words: Iterable[str]) -> float:
    """Encuentra coincidencias de palabras en un texto."""
    result_words = text.split()
    counter = sum(map(lambda item: re.sub(r'[^a-z]+', "", item) in words, result_words))
    accuracy = counter / len(result_words)
    return accuracy


def generate_permutations(max_len: int, alphabet: str = string.ascii_lowercase) -> Generator[str, None, None]:
    """Genera permutaciones de una longitud dada."""
    for length in range(1, max_len + 1):
        perms = itertools.product(alphabet, repeat=length)
        for perm in perms:
            yield ''.join(perm)


def decrypt(text: str, key: str, alphabet: str = string.ascii_lowercase) -> str:
    """Desencripta un texto usando una clave y un alfabeto especifico."""
    result = []
    pad = key * int(len(text) / len(key) + 1)
    j = 0
    for i in range(len(text)):
        if text[i] in alphabet:
            try:
                pos_t = alphabet.index(text[i])
                pos_p = alphabet.index(pad[j])
                pos_r = (pos_t - pos_p) % len(alphabet)
                result += alphabet[pos_r]
            except Exception:
                result += text[i]
            j += 1
        else:
            result += text[i]

    return ''.join(result)
