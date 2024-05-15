import numpy as np
import sciris as sc
np.random.seed(1)


class LittlePeople:
    def __init__(self, n):
        self.n = n
        self.uid = np.arange(n)
        self.age = np.random.uniform(0, 100, n)
        self.sex = np.random.rand(n) < 0.5
        self.inds = np.arange(n)
        
    def __getattribute__(self, key):
        if key in ['age', 'sex']:
            return super().__getattribute__(key)[self.inds]
        else:
            return super().__getattribute__(key)
    
    def get(self, key, inds):
        return super().__getattribute__(key)[inds]
        
    def reset(self):
        self.inds = np.arange(self.n)
        

class View:
    def __init__(self, ppl):
        self.ppl = ppl
        self.inds = sc.dcp(self.ppl.inds)
    
    def __getattribute__(self, key):
        if key in ['age', 'sex', 'uid']:
            return self.ppl.get(key, self.inds)
        else:
            return super().__getattribute__(key)
    
    def filter(self, cond, verbose=True):
        if verbose:
            print(f'Running filter: len={len(cond)}, true={sum(cond)}')
        self.inds = self.inds[cond]
        return self
    
    def __call__(self, cond):
        return self.filter(cond)
        

ppl = LittlePeople(100)
ppl.inds = np.arange(50)
vi = View(ppl)
print(vi.age)

max_age = 20
sex = 1
uids = vi(vi.age < max_age)(vi.sex==sex).uid

uids = view.filter(view.age < max_age).filter(view.sex==sex).uid

assert all(ppl.age[uids] < max_age)
assert all(ppl.sex[uids] == sex)