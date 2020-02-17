"""
Traverse a given filepath with os.walk() and return a tree.

Set max_depth to limit the tree size.

With os.walk(), traverse the directory structure (MUST BE TOPDOWN)


Set current_node = root node. For the first loop, rootdir == current_node.path
- Create nodes for all dirs and append them to current_node.children
- Add all directory nodes to the queue
- Create nodes for all files and append them to current_node.children

When the current_node.path != rootdir,
- find the child node whose path is the new rootdir
- the child_node becomes current_node
- Remove that node from the queue (Keep it small)

"""
import os

from fs_tree.utils import *
from tree import File, Folder


# Traverses the given path. Returns a tree.
def traverse(root_dir, path, max_depth=10):
    root = Folder('root', path, None)
    current_node = root
    queue = []
    if not os.path.exists(path):
        print('Not found: {}'.format(path))

    for rootdir, dirs, files in os.walk(path, topdown=True):  # Loop through directories

        # Update current_node
        if rootdir != current_node.path:
            for n in queue:
                if n.path == rootdir:
                    current_node = queue.pop(queue.index(n))

        for dir in dirs:
            node = Folder(name=dir,
                          path=os.path.join(rootdir, dir),
                          parent=current_node
                          )
            print(node.path, end='\t')
            queue.append(node)
            current_node.children.append(node)

        for file in files:  # Loop through files
            node = File(name=file,
                        path=os.path.join(rootdir, file),
                        parent=current_node,
                        )
            current_node.children.append(node)

        if current_node.depth == max_depth:
            break

    return root
