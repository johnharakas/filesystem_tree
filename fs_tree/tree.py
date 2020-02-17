"""
Create a file directory and represent it as a tree.
Currently only creates folders and txt files
"""
import collections
import os
import random
from typing import Optional, Union
import utils


class Node:
    def __init__(self, name, path, parent=None, children=None):

        self.name = name
        self.path = path

        if children is None:
            self.children = []
        else:
            self.children = children

        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

        self.size = os.path.getsize(self.path)
        self.atime = os.path.getatime(self.path)
        self.ctime = os.path.getctime(self.path)
        self.mtime = os.path.getmtime(self.path)

        self.as_sting = ''

    def __repr__(self):
        # TODO: Maybe make it prettier?
        return "<Node {}>".format(self.name)

    def __str__(self):
        return self.path

    def __lt__(self, other):
        return self.path < other.path

    def get(self, item):
        return self.__dict__[item]

    def print_tree(self):
        """
        Recursively create a string representation of tree node
        """

        def _print_tree(node, level=0):
            branch = "\t" * level + repr(node.path) + "\n"
            for child in node.children:
                branch += _print_tree(child, level + 1)
            return branch

        self.as_string = _print_tree(self)
        print(self.as_string)
        return self.as_sting

    def print_details(self):
        print('Node:{} depth:{} size:{} atime:{}'.format(self.name, self.depth, self.size, self.atime))

    # Backtrack node to root
    def get_path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))


class Folder(Node):
    def __init__(self, name, path, parent):
        super().__init__(name, path, parent)

    def __repr__(self):
        return "<Folder {}>".format(self.path)

    def make_child(self, name, path, node_type):
        child = None
        if node_type is Folder:
            if not os.path.exists(path):
                os.mkdir(path + '/')
                child = Folder(name=name, path=path, parent=self)

        if node_type is File:
            filepath = path + '.txt'
            with open(filepath, 'w') as file:
                file.write(path)
            child = File(name=name, path=filepath, parent=self)
        self.children.append(child)
        self.children.sort()


class File(Node):
    def __init__(self, name, path, parent):
        super().__init__(name, path, parent)
        self.ext = os.path.splitext(self.path)[1]

    def __repr__(self):
        return "<File {}>".format(self.path)


def find_node_value(root, item):
    """
    Given a tree and class attribute returns a list.
    e.g. returns a list of all creation dates
    """
    queue = collections.deque([])
    queue.append(root)
    explored = []
    while len(queue) > 0:
        node = queue.popleft()
        for child in node.children:
            if child not in explored:
                queue.append(child)
        explored.append(node.get(item))
    return explored


def find_node(root: Node, target: str) -> Union[Node, Folder, File, None]:
    """
    Given a tree and path, returns a Node
    """
    queue = collections.deque([])
    queue.append(root)
    explored = []
    while len(queue) > 0:
        node = queue.popleft()
        for child in node.children:
            if child not in explored:
                queue.append(child)
        if node.name == target:
            return node
        explored.append(node)
    return None


def make_random_tree(directory, max_depth=2, max_files=2, max_folders=2):  # TODO: utilize function arguments
    """
    Make a random directory tree.
    """
    path = directory  # TODO: Fix path and directory arguments.

    # For debugging/testing:
    # utils.rm_directory(path)

    os.mkdir(path)

    root = Folder('root', path, None)
    make_random_nodes(root)

    # This is essentially the same as BFS:
    # Just adds a random number of children for each (file) node
    queue = collections.deque([])
    queue.append(root)
    explored = []
    while len(queue) > 0:
        node = queue.popleft()
        for child in node.children:
            if child not in explored:
                if type(child) is Folder:
                    make_random_nodes(child,
                                      max_files=max_files,
                                      max_folders=max_folders,
                                      max_depth=node.depth == max_depth
                                      )
                queue.append(child)
        explored.append(node)
    return root


def make_random_nodes(node, max_files=2, max_folders=2, max_depth=False):
    """
    Given a parent node, make random child nodes.
    Specify maximum number of files/folders
    """
    # If max_depth = True, not going to create any additional folders.
    if not max_depth:
        num_folders = random.randint(1, max_folders)
        for d in range(num_folders):
            new_name = '{}'.format(d)

            new_path = os.path.join(
                node.path,
                'dir' + str(node.depth) + str(d)
            )
            node.make_child(new_name, new_path, node_type=Folder)

    num_files = random.randint(1, max_files)
    for d in range(num_files):
        new_name = '{}'.format(d)
        new_path = os.path.join(
            node.path,
            'file' + str(d)
        )
        node.make_child(new_name, new_path, node_type=File)
    return node


# Breadth first traversal
def BFS(root):
    queue = collections.deque([])
    queue.append(root)
    explored = []
    while len(queue) > 0:
        node = queue.popleft()
        for child in node.children:
            if child not in explored:
                queue.append(child)
        explored.append(node)
    return explored


def tree_size(node):
    size = node.size
    if type(node) is Folder:
        for child in node.children:
            size += tree_size(child)
    print('{0: < 7}'.format(size), node.path)
    return size


def identical_tree(root1, root2):
    """
    Check if two trees are identical by comparing paths.
    Convert the child node paths into sets
    Check if the difference is empty
    """
    q1 = collections.deque([])
    q1.append(root1)
    q2 = collections.deque([])
    q2.append(root2)

    explored1 = []
    explored2 = []
    while len(q1) > 0 and len(q2) > 0:
        node1 = q1.popleft()
        node2 = q2.popleft()
        for c1, c2 in zip(sorted(node1.children), sorted(node2.children)):
            s1 = set(c.path for c in c1.children)
            s2 = set(c.path for c in c2.children)
            if len(s1 - s2) > 0:
                print(s1)
                print(s2)
                return False
            if c1 not in explored1:
                q1.append(c1)

            if c2 not in explored2:
                q2.append(c2)
        explored1.append(node1)
        explored2.append(node2)
    return True
