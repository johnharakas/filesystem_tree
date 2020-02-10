"""
Create a file directory and represent it as a tree.
Currently only creates folders and txt files
"""
import collections
import os
import random


class Node:
    def __init__(self, name, type, path, parent=None, children=None, **kwargs):
        self.__dict__.update(kwargs)
        # TODO: Add more file information
        self.name = name
        self.type = type
        self.path = path
        self.parent = parent
        if children is None:
            self.children = []
        else:
            self.children = children
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
        if children:
            self.children = children

    def print_details(self):
        print('Node:{} depth:{}'.format(self.name, self.depth))

    def __repr__(self):
        # TODO: Maybe make it prettier?
        return "<Node {}>".format(self.path)

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    # TODO: can create_child() and add_child() be combined?
    def create_child(self, name, path, type):
        print(name, path, type)
        node = Node(name, path, type)
        self.children.append(node)

    def add_child(self, node):
        if node.type is 'folder':
            if not os.path.exists(node.path):
                os.mkdir(node.path + '/')
        if node.type is 'file':
            filepath = node.path + '.txt'
            with open(filepath, 'w') as file:
                file.write(node.path)
        self.children.append(node)


def make_random_tree(directory, max_depth=3, max_files=5, max_folders=3):  # TODO: utilize function arguments
    """
    Make a random directory tree.
    """
    path = directory + '/' + 'root/'  # TODO: Fix path and directory arguments.
    # For debugging/testing:
    import shutil
    shutil.rmtree(path)
    if not os.path.exists(path):
        os.mkdir(path)
    root = Node('root', 'dir', path)
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
                if child.type is 'folder':
                    make_random_nodes(child, max_files=max_files, max_folders=max_folders,
                                      max_depth=node.depth == max_depth)
                queue.append(child)
        explored.append(node)
    return root


def make_random_nodes(node, max_files=6, max_folders=4, max_depth=False):
    """
    Given a parent node, make random child nodes.
    Specify maximum number of files/folders
    """
    # If max_depth = True, not going to create any additional folders.
    if not max_depth:
        num_folders = random.randint(1, max_folders)
        for d in range(num_folders):
            new_name = '{}'.format(d)
            new_path = node.path + 'folder' + str(node.depth) + str(d) + '/'
            new_node = Node(name=new_name, type='folder', path=new_path, parent=node)
            node.add_child(new_node)

    num_files = random.randint(1, max_files)
    for d in range(num_files):
        new_name = '{}'.format(d)
        new_path = node.path + 'file' + str(d)
        new_node = Node(name=new_name, type='file', path=new_path, parent=node)
        node.add_child(new_node)
    return node
