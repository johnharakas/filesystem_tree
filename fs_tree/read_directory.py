"""
Traverse a given filepath with os.walk() and return a tree.

Set max_depth to limit the tree size.
"""
import os

from node import Node
from fs_tree.utils import *


# Traverses the given path. Returns a tree.
def traverse(path, max_depth=20):
    root = Node(None, 'root', path)
    current_node = root
    queue = collections.deque([])

    # MUST BE TOPDOWN
    for rootdir, dirs, files in os.walk(path, topdown=True):
        # Loop through directories
        for dir in dirs:
            # print('depth: {} {} {}'.format(current_node.depth, rootdir, dirs))
            # print('{} {} {}'.format(rootdir, dirs, files))
            node = Node(name=dir, path=os.path.join(rootdir, dir), type="folder", parent=current_node)
            queue.append(node)
            current_node.children.append(node)

        # Loop through files
        for file in files:
            # print('depth: {} {} {}'.format(current_node.depth, rootdir, dirs))
            # print('{} {} {}'.format(rootdir, dirs, files))
            node = Node(name=file, path=os.path.join(rootdir, file), type="folder", parent=current_node)
            current_node.children.append(node)

        if len(queue) > 0:
            current_node = queue.popleft()

        if current_node.depth == max_depth:
            break
    return root


# Testing
def foo():
    path = '/home/user/.mozilla'
    root = traverse(path)
    BFS(root)
