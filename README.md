# filesystem_tree
Represent a given filesystem directory as a tree. The scope of this project is not fully defined yet. However, there will be some interesting additions and functionalities.

As of right now, the currently defined features are reading a given directory struture into a tree and generating a random directory tree. 

### Creating a random tree
```python
from fs_tree import tree
path = 'files'
depth = 5
n_files = 5
n_folders = 5
t = tree.make_random_tree(path, max_depth=depth, max_files=n_files, max_folders=n_folders)
```
### Creating a tree for a given path
```python
from fs_tree import read_directory
path = 'files'
t = read_directory.traverse(path, path)
```
### Checking if two trees are identical
```python
from fs_tree import tree, read_directory, utils

path = 'files'
t1 = tree.make_random_tree(path, max_depth=1, max_files=2, max_folders=2)
t2 = read_directory.traverse(path, path)

print('Checking if t1 and t2 are identical.')

if utils.identical_tree(t1, t2):
    print('Trees are identical.')
else:
    print('Trees are not identical')
```
### Find a file
```python
from fs_tree import tree, read_directory

root_dir = '.mozilla'
path = '/home/user/.mozilla'
root = read_directory.traverse(root_dir, path)
target = 'profiles.ini'
node = tree.find_node(root, target)
if node:
    print('Found: %s' % target)
    node.print_details()
    # Backtrack up parent nodes
    node.get_path()
else:
    print('%s not found.' % target)
```
### Pretty print a tree
```python
from fs_tree import read_directory
root_dir = '.mozilla'
path = '/home/user/.mozilla'
t = read_directory.traverse(root_dir, path)
t.print_tree()
```
