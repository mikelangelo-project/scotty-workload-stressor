import sys
import os

test_dir_path = os.path.abspath(__file__ )
test_parent_dir = os.path.dirname(test_dir_path)
root_dir = os.path.dirname(test_parent_dir)
sys.path.append(root_dir)
