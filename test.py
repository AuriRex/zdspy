from zdspy import nsbmd
from zdspy import zob
from zdspy import bhio
from zdspy import dataio as d


# f = d.ReadFile("../../DS/dngn_main_f_00.nsbmd")

# z = zcab.ZCAB(f)

# z = nsbmd.fromFile("../../DS/dngn_main_f_00.nsbmd")

# b = bhio.fromFile("../../DS/param.bhio")

z = zob.ZOB_NPC(d.ReadFile("../../DS/z_ph_Map/isle_main/file_course.bin/objlist/npctype_1.zob"))

# for c in z.children:
#     print("------")
#     print(c)
#     try:
#         print(b.children[c._s16_0].obj_id_string)
#     except IndexError:
#         print("IndexError")


print(z)