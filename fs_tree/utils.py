import collections
from datetime import datetime
import os
import random
import string
import shutil


def path_size(path):
    size = os.path.getsize(path)
    if os.path.isdir(path):
        for file in os.listdir(path):
            child = os.path.join(path, file)
            size += path_size(child)
    print('{0: < 7}'.format(size), path)
    return size


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


def random_string(n=5):
    return ''.join(random.choices(string.ascii_lowercase, k=n))
