import json


class SquaredleSolver:
    def __init__(self):
        data = self.get_table()
        self.table = data
        self.answers = set()
        self.size = len(data)

    def read_words(self):
        with open("words.json", "r") as words:
            return json.load(words)

    def build_words(self):
        words = self.read_words()

        trie = {}

        for w in words:
            node = trie
            for ch in w:
                if ch not in node:
                    node[ch] = {}
                node = node[ch]

            node["end"] = True

        return trie

    def get_table(self):
        raw_size = input("provide size:")

        if not raw_size.isnumeric():
            raise SystemExit("Invalid size")

        size = int(raw_size)

        raw_table = input(f"provide table: example abc,def,ghi: ")

        table = [item.strip() for item in raw_table.split(",")]

        if len(table) != size or any(len(item) != size for item in table):
            raise SystemExit(f"Invalid table. Expected {size} rows of {size} letters")

        return [list(row) for row in table]

    def coordinates(self, address: list[int]):
        [row, col] = address
        return self.size * row + col + 1

    def solver(self, address: list[int], word: str, path: set, trie: dict):
        [row, col] = address
        letter = self.table[row][col]
        next_trie = trie.get(letter)

        if next_trie is None:
            return

        updated_word = word + letter

        if next_trie.get("end"):
            self.answers.add(updated_word)

        cell = self.coordinates(address)
        path.add(cell)

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                x = row + dx
                y = col + dy

                if x < 0 or x >= self.size or y < 0 or y >= self.size:
                    continue

                if self.coordinates([x, y]) in path:
                    continue

                self.solver([x, y], updated_word, path, next_trie)

        path.remove(cell)

    def solve(self):
        words = self.build_words()

        for i in range(self.size):
            for j in range(self.size):
                self.solver([i, j], "", set(), words)

        print(self.answers)


if __name__ == "__main__":
    SquaredleSolver().solve()
