import copy

from BinNumber import BinNumber
from BST import BST, Node


class BitNumber(BinNumber):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, signed=False, **kwargs)

    def __repr__(self):
        name = self.__class__.__name__
        num = self.to_bin()
        return (
            f'{name}({num}, num_bits={self.num_bits})'
        )

    def msb_index(self):
        for k in range(self.num_bits):
            if self.bits[k] == 1:
                return self.invert_index(k)

        return None

    def solo_msb(self):
        # take out all bits except the MSB
        # i.e. 0b01011 becomes 0b01000
        msb_index = self.msb_index()
        new_num = BitNumber(num=0, num_bits=self.num_bits)
        if msb_index is None:
            return new_num

        new_num[msb_index] = 1
        return new_num


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
        print(self.towers)
        print(self.towers[0].solo_msb())
        print(self.state)

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

    def move(self, hanoi, start, end):
        # make new hanoi towers from previous one after moving
        towers = copy.deepcopy(hanoi.towers)
        towers = list(towers)

        solo_msb = towers[start].solo_msb()
        if solo_msb < towers[end]:
            # other tower has larger disks
            return None

        # remove msb bit from start tower and add it to other tower
        print('SOLOMSB', towers[start], solo_msb, towers[start].msb_index())
        towers[start] = towers[start] & ~solo_msb
        towers[end] = towers[end] | solo_msb
        return Hanoi(towers)

    def make_fsm(
        self, bst=None, node=None, hanoi=None, states=()
    ):
        if hanoi is None:
            hanoi = self

        if bst is None:
            bst = BST()
            node = bst.add_node(self)
            states = (hanoi.state,)

        for k in range(3):
            for i in range(3):
                if k == i:
                    continue

                print('')
                print(f'k,i: {(k,i)}')
                new_hanoi = self.move(hanoi, k, i)
                print('NEW', new_hanoi)

                if new_hanoi is None:
                    print('NONE', (k, i))
                    continue
                elif new_hanoi.state in states:
                    print('IN', (k, i), new_hanoi.state, states)
                    continue

                new_node = Node(new_hanoi)

                if node.left is None:
                    node.left = new_node
                else:
                    assert node.right is None
                    node.right = new_node

                states = states + (new_hanoi.state,)
                self.make_fsm(bst, new_node, hanoi, states)

        return bst


if __name__ == '__main__':
    a = BitNumber(20, num_bits=5)
    b = BitNumber(5, num_bits=5)
    print('test')
    print('a', a)
    print('b', b)
    print(a & b, a | b)

    h = Hanoi()
    print(h.state)
    bst = h.make_fsm()
    bst.show()
    print('TEST')