"""
Traverse a given filepath with os.walk() and return a tree.

Set max_depth to limit the tree size.
"""
import os

from fs_tree.utils import *
from tree import Node, find_node


# Traverses the given path. Returns a tree.
def traverse(root_dir, path, max_depth=5):
    root = Node(root_dir, 'root', path)
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
                node = Node(name=dir,
                            path=os.path.join(rootdir, dir),
                            ftype="folder",
                            parent=current_node,
                            size=os.path.getsize(path),
                            atime=os.path.getatime(path),
                            ctime=os.path.getctime(path),
                            mtime=os.path.getmtime(path)
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
                path = os.path.join(rootdir, file)
                # ext = os.path.splitext(path)[1]
                # print(ext)
                node = Node(name=file,
                            path=os.path.join(rootdir, file),
                            ftype="file",
                            parent=current_node,
                            size=os.path.getsize(path),
                            atime=os.path.getatime(path),
                            ctime=os.path.getctime(path),
                            mtime=os.path.getmtime(path),
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


# Testing
def foo():
    root_dir = '.mozilla'
    path = '/home/user/.mozilla'
    root = traverse(root_dir, path)
    traversed = BFS(root)
    print(traversed)
    target = 'profiles.ini'
    node = find_node(root, target)
    if node:
        print('Found: %s' % target)
        node.print_details()
    else:
        print('%s not found.' % target)


foo()
