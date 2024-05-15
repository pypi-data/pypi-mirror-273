import numpy as np


class SmallPeople:
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
        
    def reset(self):
        self.inds = np.arange(self.n)
    
    def filter(self, cond):
        print('hi', len(cond), sum(cond))
        self.inds = self.inds[cond]
        return self
    
    def __call__(self, cond):
        return self.filter(cond)
        

# class View:
#     def __init__(self, ppl):
        

ppl = SmallPeople(100)

ppl(ppl.age < 20)(ppl.sex==1)

# ppl.inds = np.arange(50)
# print(ppl.age)
# ppl.filter(ppl.age < 50).filter(ppl.sex==True)
print(ppl.age)


# pf = ppl.filter()
# f_uids = pf(pf.female)(pf.age < upper_age).uid

# f_uids = people.female & (self.risk_group == rg) & (people.age < upper_age)
# m_uids = people.male & (self.risk_group == rg) & (people.age < upper_age)