"""
Traverse a given filepath with os.walk() and return a tree.

Set max_depth to limit the tree size.
"""
import os

from fs_tree.utils import *
from tree import Node, File, Folder, find_node


# Traverses the given path. Returns a tree.
def traverse(root_dir, path, max_depth=10):
    root = Folder(root_dir, path, None)
    current_node = root
    queue = collections.deque([])

    if not os.path.exists(path):
        print('Not found: {}'.format(path))

    # MUST BE TOPDOWN
    for rootdir, dirs, files in os.walk(path, topdown=True):  # Loop through directories
        try:
            for dir in dirs:
                # print('depth: {} {} {}'.format(current_node.depth, rootdir, dirs))
                # print('{} {} {}'.format(rootdir, dirs, files))
                node = Folder(name=dir,
                              path=os.path.join(rootdir, dir),
                              parent=current_node
                              )
                queue.append(node)
                current_node.children.append(node)
        except FileNotFoundError as e:
            print(e)
            pass

        try:
            for file in files:  # Loop through files
                # print('depth: {} {} {}'.format(current_node.depth, rootdir, dirs))
                # print('{} {} {}'.format(rootdir, dirs, files))
                # path = os.path.join(rootdir, file)
                node = File(name=file,
                            path=os.path.join(rootdir, file),
                            parent=current_node,
                            )
                current_node.children.append(node)
        except FileNotFoundError as e:
            print(e)
            pass

        if len(queue) > 0:
            current_node = queue.popleft()

        if current_node.depth == max_depth:
            break
    return root
