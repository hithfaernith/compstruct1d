import textwrap


class Node(object):
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def length(self):
        return len(str(self.value))

    @property
    def balance(self):
        if self.left is None:
            left_height = 0
        else:
            left_height = self.left.height

        if self.right is None:
            right_height = 0
        else:
            right_height = self.right.height

        balance = left_height - right_height
        return balance

    @property
    def height(self):
        if not self.has_children:
            return 0

        if self.left is None:
            left_height = 0
        else:
            left_height = self.left.height

        if self.right is None:
            right_height = 0
        else:
            right_height = self.right.height

        return max(left_height, right_height) + 1

    @property
    def has_children(self):
        return (
            (self.left is not None) or
            (self.right is not None)
        )


class BST(object):
    def __init__(self, values=()):
        self.root = None
        self.size = 0

        for value in values:
            self.add_node(value)

    def __len__(self):
        return self.size

    def add_node(self, value):
        node = self.root
        new_node = Node(value)
        self.size += 1

        if self.root is None:
            self.root = new_node
            return new_node

        while True:
            if node.value > value:
                if node.left is None:
                    node.left = new_node
                    new_node.parent = node
                    return new_node
                else:
                    node = node.left
            else:
                if node.right is None:
                    node.right = new_node
                    new_node.parent = node
                    return new_node
                else:
                    node = node.right

    def delete(self, value):
        self.root = self.delete_node(self.root, value)

    def delete_node(self, root, value):
        if root is None:
            return root

        if value < root.value:
            root.left = self.delete_node(root.left, value)
        elif value > root.value:
            root.right = self.delete_node(root.right, value)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.sucessor_node(root.right)
            root.value = temp.value
            root.right = self.delete_node(root.right, temp.value)

        return root

    @staticmethod
    def sucessor_node(root):
        current = root

        while current.left is not None:
            current = current.left

        return current

    def get_nodes_at_depth(self, depth=0):
        if depth == 0:
            return [self.root]

        parent_nodes = self.get_nodes_at_depth(depth-1)
        return self.get_child_nodes(parent_nodes)

    @staticmethod
    def get_child_nodes(parent_nodes):
        child_nodes = []

        for parent_node in parent_nodes:
            if parent_node.left is not None:
                child_nodes.append(parent_node.left)
            if parent_node.right is not None:
                child_nodes.append(parent_node.right)

        return child_nodes

    def get_height(self):
        height = 0
        nodes = [self.root]

        while len(nodes) > 0:
            nodes = self.get_child_nodes(nodes)
            height += 1

        return height

    def make_lines(self, node=None):
        if node is None:
            node = self.root

        str_value = f' {node.value} '
        if not node.has_children:
            return [str_value], 0

        node_length = len(str_value) + 1
        left_lines, right_lines = [], []
        left_mid, right_mid = 0, 0

        if node.left is not None:
            left_lines, left_mid = self.make_lines(node.left)
        if node.right is not None:
            right_lines, right_mid = self.make_lines(node.right)

        new_lines = []
        for k, left_line in enumerate(left_lines):
            start_char = '<' if (k == left_mid) else ' '
            spacer = ' ' if (k < left_mid) else '|'
            new_lines.append(
                 ' ' * node_length + spacer + start_char + left_line
            )

        midpoint = len(new_lines)
        new_lines.append(str_value + '—|')

        for k, right_line in enumerate(right_lines):
            start_char = '>' if (k == right_mid) else ' '
            spacer = ' ' if (k > right_mid) else '|'
            new_lines.append(
                 ' ' * node_length + spacer + start_char + right_line
            )

        length = max([len(line) for line in new_lines])
        for k in range(len(new_lines)):
            new_lines[k] += ' ' * (length - len(new_lines[k]))

        return new_lines, midpoint

    def show(self):
        lines, midpoint = self.make_lines()
        for line in lines:
            print(line)

    @staticmethod
    def print_if(cond, *args, **kwargs):
        if cond:
            print(*args, **kwargs)

    def traverse_in_order(self, show=False):
        return self.traverse_bst_in_order(self, show=show)

    @classmethod
    def traverse_bst_in_order(cls, T, show=False):
        size = T.size
        node = T.root
        current_max = None
        values = []
        steps = 0

        while node is not None:
            steps += 1
            value = node.value
            parent = node.parent
            is_leaf = (
                (node.left is None) and (node.right is None)
            )

            no_descend_left = (
                (current_max is not None) and
                (node.left is not None) and
                (current_max >= node.left.value)
            )

            no_descend_right = (
                (current_max is not None) and
                (node.right is not None) and
                (current_max >= node.right.value)
            )

            if is_leaf:
                cls.print_if(show, 'LEAF REACH', node, current_max)
                cls.print_if(show, node.value)
                values.append(value)

                if current_max is None:
                    current_max = node.value
                else:
                    current_max = max(node.value, current_max)

                size -= 1
                node = parent
                continue

            if (node.left is not None) and not no_descend_left:
                cls.print_if(show, 'GO LEFT', node, current_max)
                node = node.left
                continue

            if (node.right is not None) and not no_descend_right:
                cls.print_if(show, 'GO RIGHT', node, current_max)
                cls.print_if(show, node.value)
                values.append(value)

                current_max = node.value
                node = node.right
                size -= 1
                continue

            if (current_max is not None) and (value > current_max):
                cls.print_if(show, 'LEFT JUMP UP', node, current_max)
                cls.print_if(show, node.value)
                current_max = node.value
                values.append(value)
                size -= 1
            else:
                cls.print_if(show, 'RIGHT JUMP UP', node, current_max)
                # traversing up right
                pass

            node = parent

        cls.print_if(show, 'steps taken', steps)
        return values

    def from_sorted_arr(self, values):
        if len(values) == 0:
            return None

        midpoint = len(values) // 2
        left_values = values[:midpoint]
        mid_value = values[midpoint]
        right_values = values[midpoint+1:]

        root = Node(mid_value)
        root.left = self.from_sorted_arr(left_values)
        root.right = self.from_sorted_arr(right_values)
        return root

    def tree_split(self, k):
        sorted_values = self.traverse_in_order()
        left_values, right_values = [], []

        for value in sorted_values:
            if value < k:
                left_values.append(value)
            elif value > k:
                right_values.append(value)

        left_bst = BST()
        right_bst = BST()
        left_bst.root = self.from_sorted_arr(left_values)
        right_bst.root = self.from_sorted_arr(right_values)

        print('left BST')
        left_bst.show()
        print('')
        print('right BST')
        right_bst.show()
        print('')


if __name__ == '__main__':
    a = BST([8, 3, 10, 1, 6, 14, 4, 7, 13])
    sorted_nodes = a.traverse_in_order()

    print(sorted_nodes)
    a.show()

    a.tree_split(9)

    a.delete(10)
    a.show()