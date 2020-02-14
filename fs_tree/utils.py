import collections
from datetime import datetime
import os
import shutil


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
        for c1, c2 in zip(node1.children, node2.children):
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


def get_file_sizes(root):
    queue = collections.deque([])
    queue.append(root)
    explored = []
    num_bytes = 0
    while len(queue) > 0:
        node = queue.popleft()
        for child in node.children:
            if child not in explored:
                queue.append(child)
        if node.ftype == 'file':
            num_bytes += node.size
        explored.append(node)
    return num_bytes


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S:%f')


def convert_bytes(n_bytes, unit):
    factor = {
        'KB': 1 << 10,
        'MB': 1 << 20,
        'GB': 1 << 30
    }
    return n_bytes / factor[unit]


def rm_directory(path, prompt=True):
    if os.path.exists(path) and prompt:
        print('---- WARNING ----')
        y = input('About to delete %s. Continue? (y/n)' % path)
        if y.lower() != 'y':
            return
        shutil.rmtree(path)
