from typing import List


class HashFunction:
    def __init__(self, table: List[int]):
        self._table = table
        self._n = len(self._table)

    def create_hash(self, string: str) -> int:
        next_hash = len(string) % self._n
        for letter in string:
            next_hash = self._table[(next_hash + ord(letter)) % self._n]
        return next_hash
