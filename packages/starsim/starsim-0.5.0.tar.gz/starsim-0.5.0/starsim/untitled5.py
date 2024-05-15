import sciris as sc
import starsim as ss

# Make HIV
hiv = ss.HIV(
    pars = dict(
        beta = {'mf': [0.0008, 0.0004]},
        init_prev = ss.bernoulli(0.05),
    )
)

# Make syphilis
syph = ss.Syphilis(
    pars = dict(
        beta = {'mf': [0.5, 0.2]},
        init_prev = ss.bernoulli(0.05),
    )
)

sim = ss.Sim(pars=dict(networks='mf'), diseases=[hiv, syph])
sim.initialize()



sim.diseases.hiv.pars.init_prev.disp()
# sim.diseases.syphilis.pars.init_prev.disp()

hiv_inf = sim.diseases.hiv.infectious.uids
# syph_inf = sim.diseases.syphilis.infectious.uids
# diff = hiv_inf.remove(syph_inf)

print(ss.__version__)
sc.pp(sim.diseases.hiv.pars.init_prev.state)
# sc.pp(sim.diseases.syphilis.pars.init_prev.state)

sc.options(dpi=200)
sim.run()
sim.plot()
print(sim.summary)