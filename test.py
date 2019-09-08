from zdspy import nsbmd
from zdspy import dataio as d


# f = d.ReadFile("../../DS/dngn_main_f_00.nsbmd")

# z = zcab.ZCAB(f)
z = nsbmd.fromFile("../../DS/dngn_main_f_00.nsbmd")

print(z)