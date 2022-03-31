import copy
import itertools

from BinNumber import BinNumber
from BST import BST, Node


class HanoiWrapper(object):
    def __init__(self, hanoi):
        self.hanoi = hanoi
        self.captures = []

    def __repr__(self):
        repr_str = str(self.hanoi.tower_number())
        if len(self.captures) > 0:
            repr_str += ' ' + str(self.captures)

        return repr_str

    @property
    def t(self):
        return self.hanoi.t

    def __eq__(self, other):
        return self.t == other.t


class Hanoi(object):
    def __init__(self, towers=None, disks=4, size=None):
        if size is None:
            size = disks

        assert size >= disks
        self.size = size

        if towers is not None:
            self.towers = towers
        else:
            start_tower = [0] * (size - disks) + [1] * disks
            self.towers = [BitNumber(start_tower, num_bits=size)]

            for k in range(2):
                # initialise the other 2 towers
                self.towers.append(BitNumber(
                    [0] * size, num_bits=size
                ))

        self.towers = tuple(self.towers)
        # print(self.towers)
        # print(self.towers[0].solo_msb())
        # print(self.state)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return self.t == other.t

    @property
    def t(self):
        return self.tower_number()

    @property
    def state(self):
        state = 0
        for tower in self.towers:
            state = state << self.size
            state += tower.value

        return state

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}({self.towers})'

    @staticmethod
    def move(hanoi, start, end):
        # make new hanoi towers from previous one after moving
        towers = copy.deepcopy(hanoi.towers)
        towers = list(towers)

        solo_msb = towers[start].solo_msb()
        if solo_msb < towers[end]:
            # other tower has larger disks
            return None

        # remove msb bit from start tower and add it to other tower
        # print('SOLOMSB', towers[start], solo_msb, towers[start].msb_index())
        towers[start] = towers[start] & ~solo_msb
        towers[end] = towers[end] | solo_msb
        return Hanoi(towers)

    def tower_number(self):
        """
        return a number where each digit is the tower no
        for the corresponding disk (starts from 1)
        """
        tower_bits = []
        i = 0

        for k in range(len(self.towers[0])):
            for i in range(len(self.towers)):
                tower = self.towers[i]
                if tower[tower.invert_index(k)] == 1:
                    break

            tower_bits.append(i + 1)

        return ''.join([str(bit) for bit in tower_bits])

    def make_fsm(
        self, bst=None, node=None, hanoi=None, states=None
    ):
        if hanoi is None:
            hanoi = self
        if states is None:
            states = []

        def wrap(hanoi_towers):
            return hanoi_towers.tower_number()

        if bst is None:
            bst = BST()
            node = bst.add_node(HanoiWrapper(self))
            states = [hanoi.state]

        for k in range(3):
            for i in range(3):
                if k == i:
                    continue

                # print('')
                # print(f'k,i: {(k,i)}')
                new_hanoi = self.move(hanoi, k, i)
                # print('NEW', new_hanoi)

                if new_hanoi is None:
                    continue
                elif new_hanoi.state in states:
                    continue

                new_node = Node(HanoiWrapper(new_hanoi))

                if node.left is None:
                    node.left = new_node
                else:
                    assert node.right is None
                    node.right = new_node

                states.append(new_hanoi.state)
                self.make_fsm(
                    bst, new_node, new_hanoi, states
                )

        print(len(states))
        return bst

    def make_bfs_fsm(
        self, bst=None, hanoi=None
    ):
        if hanoi is None:
            hanoi = self

        states = []
        bfs_nodes = []

        if bst is None:
            bst = BST()
            node = bst.add_node(HanoiWrapper(self))
            states = [hanoi.t]
            bfs_nodes.append(node)

        while len(bfs_nodes) > 0:
            new_bfs_nodes = []

            for node in bfs_nodes:
                hanoi = node.value.hanoi
                product = itertools.product(range(3), range(3))
                children, captures = [], []

                if node.parent is not None:
                    parent_hanoi = node.parent.value.hanoi
                else:
                    parent_hanoi = None

                for k, i in product:
                    if k == i:
                        continue

                    # print('')
                    # print(f'k,i: {(k,i)}')
                    new_hanoi = self.move(hanoi, k, i)
                    wrapped_new_hanoi = HanoiWrapper(new_hanoi)
                    if new_hanoi is not None:
                        print('NEW', new_hanoi.t, hanoi.t)

                    if new_hanoi is None:
                        print('BAD-STATE')
                        continue
                    elif new_hanoi.t in states:
                        print('IN-STATE')
                        captures.append(wrapped_new_hanoi)
                        continue

                    new_node = Node(wrapped_new_hanoi)

                    if node.left is None:
                        node.left = new_node
                    elif node.right is None:
                        node.right = new_node
                    else:
                        assert (
                            (new_node.value == node.left.value) or
                            (new_node.value == node.right.value)
                        )

                    # connect parent node
                    new_node.parent = node
                    states.append(new_hanoi.t)
                    new_bfs_nodes.append(new_node)
                    children.append(new_node)

                # if len(children) == 0:
                node.value.captures = [
                    capture for capture in captures
                    if (capture.hanoi != parent_hanoi) and
                    (capture.hanoi != hanoi)
                ]

            bfs_nodes = new_bfs_nodes
            print(new_bfs_nodes)

        print(len(states))
        return bst


if __name__ == '__main__':
    a = BitNumber(20, num_bits=5)
    b = BitNumber(5, num_bits=5)
    print('test')
    print('a', a)
    print('b', b)
    print(a & b, a | b)

    h = Hanoi(disks=4)
    print(h.state)
    bst = h.make_bfs_fsm()
    print('\n\n')
    bst.show()
    print('\n\n')