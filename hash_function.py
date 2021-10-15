from typing import List


class HashFunction:
    def __init__(self, table: List[int]):
        self.table = table

    def create_hash(self, string: str) -> int:
        next_hash = len(string) % 180
        for letter in string:
            next_hash = self.table[(next_hash + ord(letter)) % 180]
        return next_hash
