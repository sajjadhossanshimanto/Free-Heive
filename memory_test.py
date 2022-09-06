#%%
import pandas as pb
import json
from memory_profiler import profile


#%%
f="resource/subjects.json"

# %%
# @profile
def panda_json(fp):
    return pb.read_json(fp)

# %%
# @profile
def read_json(fp):
    with open(fp) as f:
        return json.load(f)

#%%
@profile
def test():
    a=4
    a=panda_json(f)

# read_json(f)
test()