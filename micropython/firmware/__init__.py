import os
import sys

# Add the micropython dir to the path so that `import lib.dsp` etc will work in firmware scripts.
# This is needed because we can't do relative imports in micropython / on hardware, so we have to
# import everything relative to the the root dir instead of relative to the current file.
this_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(this_dir, '..'))
sys.path.insert(0, root_dir)
