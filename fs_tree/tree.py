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


class File(Node):
    def __init__(self, name, path, parent):
        super().__init__(name, path, parent)
        self.ext = os.path.splitext(self.path)[1]

    def __repr__(self):
        return "<File {}>".format(self.path)


def find_node(root: Node, target: str) -> Union[Node, Folder, File, None]:
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
