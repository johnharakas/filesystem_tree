from fs_tree.tree import make_random_tree
from fs_tree.utils import BFS


def main():
    # Make a random tree
    path = '../files'
    tree = make_random_tree(path, max_depth=2, max_files=2, max_folders=2)
    traversed = BFS(tree)
    print(traversed)  # TODO: prettify tree for printing


main()
