from fs_tree import tree
from fs_tree import read_directory
from fs_tree import utils


def test_tree_structure(path):
    """
    Test tree generation and tree reading.
    Generate a random tree: t1
    Read the directory of t1: t2
    Check if t1 and t2 are identical trees
    """

    t1 = tree.make_random_tree(path, max_depth=1, max_files=2, max_folders=2)
    if t1:
        print('t1 created at %s' % t1.path)

    t2 = read_directory.traverse(path, path)
    if t2:
        print('t2 reated at %s' % t2.path)

    print('Checking if t1 and t2 are identical.')

    if utils.identical_tree(t1, t2):
        print('Trees are identical.')
    else:
        print('Trees are not identical')

    return t1, t2


def test_random_tree():
    print('Testing: make random tree')
    path = 'files'
    t = tree.make_random_tree(path, max_depth=1, max_files=2, max_folders=2)
    traversed = utils.BFS(t)
    print(traversed)


def test_read_directory():
    root_dir = '.mozilla'
    path = '/home/modp/.mozilla'
    root = read_directory.traverse(root_dir, path)
    traversed = utils.BFS(root)
    print(traversed)
    target = 'profiles.ini'
    node = tree.find_node(root, target)
    if node:
        print('Found: %s' % target)
        node.print_details()
    else:
        print('%s not found.' % target)
    return root
