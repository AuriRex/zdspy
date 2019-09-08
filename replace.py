import os
import ndspy.rom
import ndspy.fnt
import ndspy.lz10
import ndspy.narc

romname = '1514 - Legend of Zelda - Phantom Hourglass, The (E)(EXiMiUS).nds'
# romname = '4544 - Legend of Zelda - Spirit Tracks, The (EU)(M5)(EXiMiUS).nds'

rom = ndspy.rom.NintendoDSRom.fromFile(romname)

print(rom)
print("Number of Files: "+str(len(rom.files)))

for i, file in enumerate(rom.files):
    # if file.startswith(b'ZCLB'):
    fname = rom.filenames.filenameOf(i)
    fname = str(fname)
    print(str(i) + " " + fname)
    # if "course.bin" in fname:
    #     print("Found One: "+fname)
    #     if not os.path.exists("output/" + fname):
    #         os.makedirs("output/" + fname[:-10])
    #     with open("output/" + fname, 'wb') as f:
    #         f.write(file)
    #     dcpfile = ndspy.lz10.decompressFromFile("output/" + fname)
    #     with open("output/" + fname + "_dcp", 'wb') as f:
    #         f.write(dcpfile)
    #     narc = ndspy.narc.NARC(dcpfile)
    #     # print(narc)
    #     for i_d, narcfile in enumerate(narc.files):
    #         nfn = narc.filenames.filenameOf(i_d)
    #         print("[NARC] "+nfn)
    #         if not os.path.exists("output/" + fname + "_file/" + nfn):
    #             os.makedirs("output/" + fname + "_file/" + nfn[:-2])
    #         with open("output/" + fname + "_file/" + nfn, 'wb') as f:
    #             f.write(narcfile)

with open('mod_map02.bin', 'rb') as f:
    cbin = f.read()

rom.setFileByName('Map/dngn_main/map02.bin', cbin)

with open('ph_modified.nds', 'wb') as f:
    f.write(rom.save())
        