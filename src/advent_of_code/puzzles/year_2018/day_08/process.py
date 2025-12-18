import collections
import dataclasses
import timeit
import typing


@dataclasses.dataclass
class Node:
    children: typing.Sequence['Node']
    metadata: typing.Sequence[int]

    @property
    def metadata_sum(self):
        return sum([node.metadata_sum for node in self.children]) + sum(self.metadata)

    @property
    def value(self):
        if self.children:
            values = []
            for metadatum in self.metadata:
                try:
                    values.append(self.children[metadatum - 1].value)
                except IndexError:
                    pass
            return sum(values)
        else:
            return sum(self.metadata)


class TreeParser:

    def __init__(self, raw_nodes):
        nodes = [int(node) for node in raw_nodes.split()]
        self._nodes = collections.deque(nodes)

    @classmethod
    def read_file(cls):
        with open('input.txt') as f:
            return cls(f.read())

    def parse(self):
        children_no = self._nodes.popleft()
        metadata_no = self._nodes.popleft()
        children = [self.parse() for _ in range(children_no)]
        metadata = [self._nodes.popleft() for _ in range(metadata_no)]
        return Node(children, metadata)


def main():
    tree_parser = TreeParser.read_file()
    tree = tree_parser.parse()
    print(f'Metadata sum: {tree.metadata_sum}')
    print(f'Root node value: {tree.value}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')
