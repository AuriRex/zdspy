from ndspy import soundArchive
from zdspy import dataio as d


sdat = soundArchive.SDAT(d.ReadFile("../../DS/snd.sdat"))

for i, (k, v) in enumerate(sdat.groups):
    print("\n", i)
    for ge in v:
        print(ge.id, ge)