from tree import make_random_tree
from utils import BFS


def main():
    # Make a random tree
    path = '../files'
    tree = make_random_tree(path, max_depth=3, max_files=5, max_folders=3)
    traversed = BFS(tree)
    print(traversed)  # TODO: prettify tree for printing


main()
