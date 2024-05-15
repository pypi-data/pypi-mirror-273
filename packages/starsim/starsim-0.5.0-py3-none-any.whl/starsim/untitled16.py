import numpy as np
np.random.seed(1)


class LittlePeople:
    # keys = ['age', 'sex', 'uid'] # Causes recurison error
    def __init__(self, n=0):
        self.n = n
        self.uid = np.arange(n)
        self.age = np.random.uniform(0, 100, n)
        self.sex = np.random.rand(n) < 0.5
        self.inds = np.arange(n)
        self.is_view = False
        
    def __getattribute__(self, key):
        if key in ['age', 'sex', 'uid']:
            return super().__getattribute__(key)[self.inds]
        else:
            return super().__getattribute__(key)
    
    def get(self, key, inds):
        return super().__getattribute__(key)[inds]
        
    def reset(self):
        self.inds = np.arange(self.n)
        
    def view(self):
        if not self.is_view:
            new = self.__class__.__new__(self.__class__)
            new.__dict__.update(self.__dict__)
            new.inds = new.inds.copy()
            new.is_view = True
            return new
        else:
            return self
        
    def filter(self, cond, verbose=True):
        view = self.view()
        if verbose:
            print(f'Running filter: n={len(self.inds)}, len={len(cond)}, true={sum(cond)}')
        view.inds = view.inds[cond]
        return view
    
    def __call__(self, cond):
        return self.filter(cond)
        

n = 100
pre = 50
max_age = 20
sex = 1

ppl = LittlePeople(n)
ppl.inds = np.arange(pre)
print(ppl.age)

view = ppl.view()
uids = view.filter(view.age < max_age).filter(view.sex==sex).uid

assert all(ppl.age[uids] < max_age)
assert all(ppl.sex[uids] == sex)