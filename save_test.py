from zdspy import zmb
from zdspy import dataio as d

og_file = d.ReadFile("../../DS/dngn_main_01.zmb")

_zmb = zmb.ZMB(og_file)

save_zmb = _zmb.save()

print("Same file: " + str(og_file == save_zmb))