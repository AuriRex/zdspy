import os
from zdspy import dataio as d
import ndspy.lz10
import ndspy.narc
from zdspy import nsbmd as znsbmd
from zdspy import zmb as zzmb
from zdspy import rom_util

rompath = "./Zelda_PH.nds"
workdir = "./extracted/root/"
outdir = "./infodump/"

class ZDS_PH_NARC:

    def getName(self):
        return self.name

    def getData(self):
        return self.data

    def getID(self):
        return self.id

    def __init__(self, name, data, comp):
        self.name = name
        if "map" in name:
            self.id = str(name[3:4]) + str(name[4:5])
        else:
            self.id = "-1"
        
        if comp == 10:
            self.data = ndspy.narc.NARC(ndspy.lz10.decompress(data))
        else:
            self.data = ndspy.narc.NARC(data)
        # print(self.data.filenames)

    def save(self):
        return ndspy.lz10.compress(self.data.save())

class ZDS_PH_ILB: # Island Binary

    def __init__(self, data):
        self.data = data
    
    def save(self):
        return self.data

class ZDS_PH_MAP:

    def getName(self):
        return self.name

    def __init__(self, name, nummaps, coursebin, children, island_ilb = None):
        self.name = name
        self.map_count = nummaps
        self.course_bin = coursebin

        self.children = children
        if not (island_ilb == None):
            self.is_island = True
        else:
            self.is_island = False
        self.island_ilb = island_ilb

    def __init__(self, folderpath, p=True):
        count = -1
        if p == True:
            print(folderpath)
        self.name = os.path.basename(os.path.normpath(folderpath))
        self.children = []
        for r, di, f in os.walk(folderpath):
            for file in f:
                if p == True:
                    print(" - "+file)
                count = count + 1
                if file == "course.bin":
                    self.course_bin = ZDS_PH_NARC( file, d.ReadFile(os.path.join(r, file)) , 10)
                elif file == "island.ilb":
                    # print("Island Binary!")
                    count = count - 1
                    self.island_ilb = ZDS_PH_ILB( d.ReadFile(os.path.join(r, file)) )
                elif "map" in file:
                    self.children.append( ZDS_PH_NARC( file, d.ReadFile( os.path.join(r, file) ) , 10) )

    def save(self, save_path):
        #Save course.bin

        try:
            os.makedirs(save_path + self.name + "/")
        except FileExistsError:
            # directory already exists
            pass

        with open(save_path + self.name + "/course.bin", 'w+b') as f:
            f.write(self.course_bin.save())


        #Save island.ilb
        try:
            if not (self.island_ilb == None):
                with open(save_path + self.name + "/island.ilb", 'w+b') as f:
                    f.write(self.island_ilb.save())
        except AttributeError:
            pass

        #Save Maps

        for child in self.children:
            with open(save_path + self.name + "/" + child.name, 'w+b') as f:
                f.write(child.save())

    def addMap(self, narcdata):
        pass



def main():

    if not os.path.exists(workdir):
        print("No extracted files present, extracting rom first!")
        rom_util.extract(rompath, workdir, False)

    err_log = []

    dirs = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(workdir + "Map/"):
        for directory in d:
            dirs.append(os.path.join(r, directory))


    mapl = []

    for d in dirs:
        mapl.append( ZDS_PH_MAP( d ) )

    zmbl = {}

    nsbmdl = []

    for mp in mapl:
        mp_name = mp.getName()
        print(mp_name)
        for c in mp.children:
            map_num = c.getName()[3:4]
            map_num_2 = c.getName()[4:5]
            filename = "zmb/" + mp_name + "_" + str(map_num) + str(map_num_2) + ".zmb"
            print(filename)
            try:
                zmbl[ zzmb.ZMB( c.getData().getFileByName(filename) ) ] = filename
            except Exception as err:
                err_log.append(repr(err) + " | " + filename)
            filename = "nsbmd/" + mp_name + "_" + str(map_num) + str(map_num_2) + ".nsbmd"
            print(filename)
            try:
                nsbmdl.append( (znsbmd.NSBMD( c.getData().getFileByName(filename) ), filename) )
            except Exception as err:
                err_log.append(repr(err) + " | " + filename)

    npc_room_list = {}
    npc_type_list = {}

    warp_fade_type_list = {}

    entrance_unknown1_list = {}
    entrance_unknown1_file_list = {}

    obj_id_list = {}

    room_hex_list = {}
    environment_type_list = {}
    music_id_list = {}

    total_areas = 0
    for (zmb, fname) in zmbl.items():
        total_areas = total_areas + 1
        npch = zmb.get_child("NPCA")
        if not (npch == None):
            for npc in npch.children:
                if str(fname) not in npc_room_list:
                    npc_room_list[str(fname)] = {}
                else:
                    if npc.npctype not in npc_room_list[str(fname)]:
                        npc_room_list[str(fname)][str(npc.npctype)] = 1
                    else:
                        npc_room_list[str(fname)][str(npc.npctype)] = npc_room_list[str(fname)][str(npc.npctype)] + 1
                if npc.npctype not in npc_type_list:
                    npc_type_list[str(npc.npctype)] = 1
                else:
                    npc_type_list[str(npc.npctype)] = npc_type_list[str(npc.npctype)] + 1
        warph = zmb.get_child("WARP")
        if not (warph == None):
            for wrp in warph.children:
                if str(wrp.fade_type) not in warp_fade_type_list:
                    warp_fade_type_list[str(wrp.fade_type)] = 1
                else:
                    warp_fade_type_list[str(wrp.fade_type)] = warp_fade_type_list[str(wrp.fade_type)] + 1
        objh = zmb.get_child("MPOB")
        if not (objh == None):
            for obj in objh.children:
                if str(obj.mapobjectid) not in obj_id_list:
                    obj_id_list[str(obj.mapobjectid)] = 1
                else:
                    obj_id_list[str(obj.mapobjectid)] = obj_id_list[str(obj.mapobjectid)] + 1
        roomh = zmb.get_child("ROOM")
        if not (roomh == None):
            if str(roomh.data) not in room_hex_list:
                room_hex_list[str(roomh.data[4:].hex())] = fname
            if str(roomh.environment_type) not in environment_type_list:
                environment_type_list[str(roomh.environment_type)] = 1
            else:
                environment_type_list[str(roomh.environment_type)] = environment_type_list[str(roomh.environment_type)] + 1
            if str(roomh.music_id) not in music_id_list:
                music_id_list[str(roomh.music_id)] = 1
            else:
                music_id_list[str(roomh.music_id)] = music_id_list[str(roomh.music_id)] + 1
        plyrh = zmb.get_child("PLYR")
        if not (plyrh == None):
            for c in plyrh.children:
                if str(fname) not in entrance_unknown1_file_list:
                    entrance_unknown1_file_list[str(fname)] = {}
                else:
                    if c.id not in entrance_unknown1_file_list[str(fname)]:
                        entrance_unknown1_file_list[str(fname)][c.id] = str(c.unknown1)
                if str(c.unknown1) not in entrance_unknown1_list:
                    entrance_unknown1_list[str(c.unknown1)] = 1
                else:
                    entrance_unknown1_list[str(c.unknown1)] += 1


    #print(sorted(npc_type_list))

    #######################################################################################
    #               NPCs
    #######################################################################################

    out_str = ""
    for k, v in sorted(npc_type_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_used_npcs_list_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(npc_type_list.items() ,  key=lambda x: x[1])
    out_str = ""
    # Iterate over the sorted sequence
    for elem in listofTuples :
        out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )
    f = open(outdir + 'ph_used_npcs_list_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str[:-1])

    total_npcs = 0
    for k, v in sorted(npc_type_list.items()):
        total_npcs = total_npcs + v

    # NPC Listed By Room #

    # npc_room_list
    out_str_complete = ""
    for fname, npcr in npc_room_list.items():
        # Create a list of tuples sorted by index 1 i.e. value field     
        listofTuples = sorted(npcr.items() ,  key=lambda x: x[1])
        out_str = ""
        # Iterate over the sorted sequence
        for elem in listofTuples :
            out_str = "  " + str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
            # print(elem[0] , " ::" , elem[1] )
        out_str_complete += fname + ":\n" + out_str
    f = open(outdir + 'ph_used_npcs_in_rooms_list_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str_complete[:-1])

    #######################################################################################
    #               WARPs & Transition Types
    #######################################################################################

    out_str = ""
    for k, v in sorted(warp_fade_type_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_used_warp_fade_types_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(warp_fade_type_list.items() ,  key=lambda x: x[1])
    out_str = ""
    # Iterate over the sorted sequence
    for elem in listofTuples :
        out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )
    f = open(outdir + 'ph_used_warp_fade_types_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str[:-1])

    total_warps = 0
    for k, v in sorted(warp_fade_type_list.items()):
        total_warps = total_warps + v

    out_str = ""
    for k, v in sorted(entrance_unknown1_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_plyr_unknown1_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    out_str_complete = ""
    for fname, npcr in entrance_unknown1_file_list.items():
        # Create a list of tuples sorted by index 1 i.e. value field     
        listofTuples = sorted(npcr.items() ,  key=lambda x: x[1])
        out_str = ""
        # Iterate over the sorted sequence
        for elem in listofTuples :
            out_str = "  " + str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
            # print(elem[0] , " ::" , elem[1] )
        out_str_complete += fname + ":\n" + out_str
    f = open(outdir + 'ph_plyr_unknown1_files_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str_complete[:-1])

    #######################################################################################
    #               Object IDs
    #######################################################################################

    out_str = ""
    for k, v in sorted(obj_id_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_obj_id_list_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(obj_id_list.items() ,  key=lambda x: x[1])
    out_str = ""
    # Iterate over the sorted sequence
    for elem in listofTuples :
        out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )
    f = open(outdir + 'ph_obj_id_list_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str[:-1])

    total_obj_ids = 0
    for k, v in sorted(obj_id_list.items()):
        total_obj_ids = total_obj_ids + v


    #######################################################################################
    #               ROOM ZMB Header
    #######################################################################################

    # environment_type_list
    out_str = ""
    for k, v in sorted(environment_type_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_environment_type_list_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(environment_type_list.items() ,  key=lambda x: x[1])
    out_str = ""
    # Iterate over the sorted sequence
    for elem in listofTuples :
        out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )
    f = open(outdir + 'ph_environment_type_list_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str[:-1])

    total_environment_types = 0
    for k, v in sorted(environment_type_list.items()):
        total_environment_types = total_environment_types + v

    # music_id_list
    out_str = ""
    for k, v in sorted(music_id_list.items()):
        #print(k, v)
        out_str = out_str + "\n" + str(k) + " " + str(v)
    f = open(outdir + 'ph_music_id_list_abc.txt', 'wt', encoding='utf-8')
    f.write(out_str[1:])

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(music_id_list.items() ,  key=lambda x: x[1])
    out_str = ""
    # Iterate over the sorted sequence
    for elem in listofTuples :
        out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )
    f = open(outdir + 'ph_music_id_list_sbv.txt', 'wt', encoding='utf-8')
    f.write(out_str[:-1])

    total_music_ids = 0
    for k, v in sorted(music_id_list.items()):
        total_music_ids = total_music_ids + v


    #######################################################################################
    #               Model Files
    #######################################################################################

    total_vtx_count = 0

    print("NSBMD Stuff:")
    for i, (nsbmd, filename) in enumerate(nsbmdl):
        mdl = nsbmd.children[0].models[0]
        print("MDL_"+str(i)+" ("+filename+"):")
        print("  Obj count:", mdl.object_count) # Not very usefull info
        print("  Material count:", mdl.material_count) # same
        print("  Total Vertex count:", mdl.total_vertex_count)
        print("  Object Names:")
        for j, name in enumerate(mdl.object.names):
            print("  ",j, name)

        print("  Material Names:")
        for j, name in enumerate(mdl.material.names):
            print("  ",j, name)
        
        total_vtx_count += mdl.total_vertex_count

    #######################################################################################
    #               Summary
    #######################################################################################

    print("Error Log:")
    err_string = ""
    for err in err_log:
        print(" ",err)
        err_string += err + "\n"

    f = open(outdir + 'ERROR_LOG.txt', 'wt', encoding='utf-8')
    f.write(err_string[:-1])

    print("## The Legend of Zelda: Phantom Hourglass Rom Info ##")
    print("Number of Maps: "+str(len(mapl)))
    print("Number of Areas: "+str(total_areas))
    print("Number of Areas WITHOUT a Model File: "+str(total_areas - len(nsbmdl)))
    print("## Object Info ##")
    print("Number of total Objects used: "+str(total_obj_ids))
    print("Number of unique Objects used: "+str(len(obj_id_list)))
    print("## NPC Info ##")
    print("Number of total NPCs: "+str(total_npcs))
    print("Number of unique NPCs: "+str(len(npc_type_list)))
    print("## ROOM Header Info ##")
    print("Number of total lighting ids used: "+str(total_environment_types))
    print("Number of unique lighting ids used: "+str(len(environment_type_list)))
    print("Number of total music ids used: "+str(total_music_ids))
    print("Number of unique music ids used: "+str(len(music_id_list)))
    print("## Warp / Entrance Info ##")
    print("Number of Entrances / Warps placed in Levels: "+str(total_warps))
    print("Number of unique Fade / Transition types used: "+str(len(warp_fade_type_list)))
    print("## World / Static Model Info ##")
    print("Total Number of Vertecies: "+str(total_vtx_count))


    print("Room Hex List:")
    print("8 = Lighting ID")
    print("12 = Music ID")
    print("Offset           1                   2                   3")
    print(":)   4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1")
    for i, (ent, v) in enumerate(room_hex_list.items()):
        print(str(i).ljust(4), ent, v)

    print("###################################")

    print(npc_room_list)

if __name__ == '__main__':
    main()