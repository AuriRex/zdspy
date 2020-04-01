from zdspy import nsbmd
from zdspy import zob
from zdspy import zmb
from zdspy import bhio
from zdspy import dataio as d


# f = d.ReadFile("../../DS/dngn_main_f_00.nsbmd")

# z = zcab.ZCAB(f)

# z = nsbmd.fromFile("../../DS/dngn_main_f_00.nsbmd")

# b = bhio.fromFile("../../DS/param.bhio")

# z = zob.ZOB_NPC(d.ReadFile("../../DS/z_ph_Map/isle_main/file_course.bin/objlist/npctype_1.zob"))

# print(bytearray.fromhex("00801f00"))
# print(d.SFix32_16(bytearray.fromhex("00801f00"), 0))
# print("ffff1f00")
# print(bin(int("ffff1f00", base=16))[2:])
# print(d.SFix(bytearray.fromhex("1f0f"), 0, 16, 12))
# shex = 0xF0FF

# 2^12
# 4096

# print(shex / 4096)


if False:
    # F000‬
    print(d.SFix(bytearray.fromhex("ffcb"), 0, 16, 5))
    while True:
        inp = input("Number:> ")
        print(float(inp))
        hex_num = d.w_SFix(bytearray(2), 0, float(inp), 16, 5)
        int_num = d.SFix(hex_num, 0, 16, 5)
        print(hex_num.hex())
        print(int_num)
    print()
    input("> ")

if False:
    print(d.w_SFix(bytearray(2), 0, -241.9375, 16, 12).hex()) # f180
    print(d.SFix(bytearray.fromhex("e1f0"), 0, 16, 12))
    # print(d.w_SFix(bytearray(2), 0, 241.9375, 16, 12, False).hex())
    print("---")
    print(d.w_SFix(bytearray(2), 0, -2.5, 8, 7).hex()) # f180
    print(d.SFix(bytearray.fromhex("fb00"), 0, 8, 7))



    input("> ")

_zmb = zmb.fromFile("../../DS/dngn_main_01.zmb")

ralbh = _zmb.get_child("RALB")

for child in ralbh.children:
    for node in child.nodes:
        node.position_x += 1
        node.position_y += 1

with open("../../DS/dngn_main_01.zmb" + "_savetest", 'w+b') as f:
    f.write(_zmb.save())

input(">")

_zmb = zmb.fromFile("../../DS/dngn_main_f_00.zmb_savetest")

npch = _zmb.get_child("NPCA")
# crps_npc = bytearray.fromhex("535052432002900100ff00000000000000000000000000002403780000010000")
# npch.addNPCRaw(crps_npc)

for c in npch.children:
    print(c.npctype)
    print(c.position_x)
    print(c.position_y)
    print(c.position_z)
    # c.position_x = 29
    # c.position_y = 23
    # c.position_z = 0
    print(c.save().hex())

input("AAAAA> ")

_zmb = zmb.fromFile("../../DS/demo_title_00.zmb")

plyrh = _zmb.get_child("PLYR")
for c in plyrh.children:
    print("Entrance with ID:"+str(c.id))
    print("X: "+str(c.position_x))
    print("Y: "+str(c.position_y)) # Automaticaly puts you down/up onto the ground ?
    # c.position_x = 20
    print("Z: "+str(c.position_z))
    print("Unknown1: "+str(c.unknown1))

warph = _zmb.get_child("WARP")

for c in warph.children:
    c.destination = "isle_main"
    c.map_id = 1
    c.destination_warp_id = 2


objh = _zmb.get_child("MPOB")

objh.addObject(10,0x1a,0x15,"000001000000000000000101000000000000ff010000")
objh.addObject(10,0x1b,0x15,"000002000000000000000101000000000000ff010000")
objh.addObject(10,0x1a,0x17,"000003000000000000000101000000000000ff010000")
objh.addObject(10,0x1a,0x19,"000005000000000000000101000000000000ff010000")

objh.addObject(9,0x1e,0x19,"000005000000000000000101000000000000ff010000")

# OBJID:101 XPos:31 YPos:34 HEX:650000001f22000001000000000000000101000000000000ff010000

objh.addObject(39,0x1a,0x12,"000001000000000000000101000000000000ff010000")
# objh.addObject(39,29,21,"000001000000000000000101000000000000ff010000")

def new_crps(posx, posy, posz):
    crps_npc = bytearray.fromhex("535052432002900100ff00000000000000000000000000002403780000010000")

    crps_npc = d.w_SFix(crps_npc, 4, posx, n_bits=16, n_bits_int=12)
    crps_npc = d.w_SFix(crps_npc, 6, posy, n_bits=16, n_bits_int=12)
    # crps_npc = d.w_SFix(crps_npc, 8, posz, n_bits=16, n_bits_int=8)
    crps_npc = d.w_SInt16(crps_npc, 8, posz)

    return crps_npc

npch = _zmb.get_child("NPCA")
# crps_npc = bytearray.fromhex("535052432002900100ff00000000000000000000000000002403780000010000")

# crps_npc = d.w_SFix(crps_npc, 4, 29, n_bits=16, n_bits_int=12)
# crps_npc = d.w_SFix(crps_npc, 6, 23, n_bits=16, n_bits_int=12)
# crps_npc = d.w_SFix(crps_npc, 8, 1, n_bits=16, n_bits_int=8)

npch.addNPCRaw(new_crps(29,23,1))
npch.addNPCRaw(new_crps(31,23,1))

for c in npch.children:
    print(c.npctype)
    print(c.position_x)
    print(c.position_y)
    print(c.position_z)
    # c.position_x = 29
    # c.position_y = 23
    # c.position_z = 10
    # print(c.save().hex())

with open("../../DS/demo_title_00.zmb" + "_savetest", 'w+b') as f:
    f.write(_zmb.save())

input("> ")


_zmb = zmb.fromFile("../../DS/dngn_main_f_00.zmb")



plyh = _zmb.get_child("PLYR")

for c in plyh.children:
    print("Entrance with ID:"+str(c.id))
    print("X: "+str(c.position_x))
    print("Y: "+str(c.position_y)) # Automaticaly puts you down/up onto the ground ?
    # c.position_x = 20
    print("Z: "+str(c.position_z))
    print("Unknown1: "+str(c.unknown1))
    # c.position_y = 32
    # print("from " + str(c.position_y) + " to " + str(c.position_y + 100000))
    # print(c.position_x)
    # c.position_x = 2064384 + 65536
    # c.position_x = 2147483648 - 1
    # print(c.position_y)
    # 16384 = 1/4 ?
    # 32768 = 1/2 !
    # FixedPoint -> 2 Byte int , 2 Byte fractions

room = _zmb.get_child("ROOM")

print("Unknown 1: " + str(room.unknown1))

print("Music ID: " + str(room.music_id))
print("Environment Type: " + str(room.environment_type))
print("Lighting Type: " + str(room.lighting_type))

room.music_id = 7
# room.environment_type = 4
room.lighting_type = 4
room.unknown1 = 4

# music_id:
# 7 = House
# 8 = Dungeon
# 9 = House
# 10 = Outside (Unsafe)

# environment_type
# 4 = Sunset colored Objects
# 5 = Smoke / Mist
# 6 = ?
# 7 = ?
# 8 = Blue Sky / Normal

arabh = _zmb.get_child("ARAB")

for c in arabh.children:
    print("ARAB ID: "+str(c.id))
    print("X1: " + str(c.position_x))
    print("Y1: " + str(c.position_y))
    # c.position_y = 276
    print("X2: " + str(c.position_x_secondary))
    print("Y2: " + str(c.position_y_secondary))
    print("Unknown1: " + str(c.unknown1))
    print("Unknown2: " + str(c.unknown2))

npch = _zmb.get_child("NPCA")



for c in npch.children:
    print("NPCID: "+str(c.npctype))
    print("X: " + str(c.position_x))
    print("Y: " + str(c.position_y))
    print("Z: " + str(c.position_z))
    print("Rot: " + str(c.rotation))
    print("BMGID: " + str(c.bmg_script_id))
    if str(c.npctype) == "CRPS":
        print("Hex[8:10]: " + str(c.data[8:10]))
        c.position_z = c.position_z + 2
        c.bmg_script_id = 7865132
        # print(c.data.hex())
    # c.position_y += 32
    # c.position_z += 2
    # c.position_x += 1
    # 16 Bit -> 12 Bit Int, 4 Bit Fraction

npch.addNPCRaw(new_crps(29,23,1))
npch.addNPCRaw(new_crps(29.5,23,2))
npch.addNPCRaw(new_crps(30,23,3))
npch.addNPCRaw(new_crps(30.5,23,4))
npch.addNPCRaw(new_crps(31,23,5))
npch.addNPCRaw(new_crps(31.5,23,6))

# zpos: 4, 8, 16, 32 == 1 ?


ncrps = bytearray.fromhex("535052432002900100ff00000000000000000000000000002403780000010000")

# ncrps = d.w_SFix(ncrps, 6, 25, n_bits=16, n_bits_int=12)
ncrps = d.w_UInt32(ncrps, 0x18, 0)

new_crps = npch.addNPCRaw(ncrps)


objh = _zmb.get_child("MPOB")


num = 32

objh.addObject(10,0x1a,0x15,"0000"+hex(num)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1b,0x15,"0000"+hex(num+1)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1c,0x15,"0000"+hex(num+2)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1d,0x15,"0000"+hex(num+3)[2:]+"000000000000000101000000000000ff010000")


objh.addObject(10,0x1f,0x15,"0000FF000000000000000101000000000000ff010000")
objh.addObject(10,0x20,0x15,"00001A000000000000000101000000000000ff010000")


num = 152

objh.addObject(10,0x1a,0x18,"0000"+hex(num)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1b,0x18,"0000"+hex(num+1)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1c,0x18,"0000"+hex(num+2)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1d,0x18,"0000"+hex(num+3)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1e,0x18,"0000"+hex(num+4)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x1f,0x18,"0000"+hex(num+5)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x20,0x18,"0000"+hex(num+6)[2:]+"000000000000000101000000000000ff010000")
objh.addObject(10,0x21,0x18,"0000"+hex(num+7)[2:]+"000000000000000101000000000000ff010000")

for c in objh.children:
    print(c)
    # c.position_x += 3
    # print(c)
#addObject

# new_crps.position_x += 1.5



warph = _zmb.get_child("WARP")

for c in warph.children:
    print(c)
    if c.UID == 1:
        c.destination = "demo_title"
        c.destination_warp_id = 0
        c.map_id = 0

with open("../../DS/dngn_main_f_00.zmb" + "_savetest", 'w+b') as f:
    f.write(_zmb.save())

print("Unknown 1: " + str(room.unknown1))

print("Music ID: " + str(room.music_id))
print("Environment Type: " + str(room.environment_type))
print("Lighting Type: " + str(room.lighting_type))

# _zmb = zmb.fromFile("../../DS/dngn_main_f_00.zmb_savetest")
# warph = _zmb.get_child("WARP")

# for c in warph.children:
#     print(c)
# for c in z.children:
#     print("------")
#     print(c)
#     try:
#         print(b.children[c._s16_0].obj_id_string)
#     except IndexError:
#         print("IndexError")


# print(z)