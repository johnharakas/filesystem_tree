import collections
from datetime import datetime


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
