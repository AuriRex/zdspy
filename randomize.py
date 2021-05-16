import random
import os
from zdspy.helpers import ZDS_PH_MAP, ZDS_PH_AREA
from zdspy import zmb as zds

def randomize(seed, workdir, outdir, enableBanlist=True, randoType="nll"):

    random.seed( seed )

    error_log = []

    banlist = ["battle00","battle01","battle02","battle03","battle04","battle05","battle06","battle07","battle08","battle09","battle10","battle11","player_dngn","demo_op","demo_chase","demo_end","demo_title"]

    # Beta maps:
    banlist.append("isle_first")
    banlist.append("isle_ice")

    # Horrible things
    banlist.append("sea_salvage")
    banlist.append("sea_fishing")

    # Types:
    #   nl -> no logic
    #   nld -> no logic dual
    #   nll -> no logic linked

    dirs = []
    # r=root, d=directories, f = files
    for root, directories, _ in os.walk(workdir):
        for name in directories:
            dirs.append(os.path.join(root, name))


    loaded_maps_list: list[type("ZDS_PH_MAP")] = []

    print("Loading maps...")

    for directory in dirs:
        print("[Reading] " + directory)
        loaded_maps_list.append( ZDS_PH_MAP( directory, debug_print=False ) )

    # w_mapl = loaded_maps_list.copy() # Used to write the new Values to

    zmb_cache: dict[str, type("ZMB")] = {}

    warpcountl = {}
    warpl = {}

    phantom_map: ZDS_PH_MAP
    for phantom_map in loaded_maps_list:
        print(phantom_map.getName())

        map_area: ZDS_PH_AREA
        for map_area in phantom_map.children:
            filename = "zmb/" + phantom_map.getName() + "_" + map_area.getID() + ".zmb"
            print(filename)
            try:
                zmb = zds.ZMB( map_area.getArchive().getFileByName(filename) )
                zmb_cache[filename] = zmb
                warph = zmb.get_child("WARP")
                if not (warph == None):
                    warpcountl[filename] = len(warph.children)
                    for i, wrp in enumerate(warph.children):
                        print(wrp)
                        if not (filename+str(i) in warpl):
                            warpl[filename+str(i)] = wrp
                        else:
                            raise Exception("Duplicate filename: \"" + filename + str(i) + "\".")
            except Exception as err:
                error_log.append(repr(err) + " | " + filename)

    # Saved for later:
    # random_item = random.choice(list)

    # print(zmb_cache)

    # print(warpl)


    # for m, w in warpl.items():
    #     if int(m.split(".zmb")[1]) == 0:
    #         mapname = m.split(".zmb")[0][4:]
    #         levelname = mapname[:-3]
    #         print()
    #         print(levelname + ": " + mapname)
    #     print(m.split(".zmb")[1] + ": " + m.split(".zmb")[0] + " --- " + str(w))

    # print(warpcountl)

    # Create a list of tuples sorted by index 1 i.e. value field     
    listofTuples = sorted(warpcountl.items() ,  key=lambda x: x[1])
    # Iterate over the sorted sequence
    for elem in listofTuples:
        #out_str = str(elem[0]) + " " + str(elem[1]) + "\n" + out_str
        print(elem[0] , " ::" , elem[1] )

    runBanList(warpl, banlist, enableBanlist)
    runBanList(warpcountl, banlist, enableBanlist)

    if randoType == "nl":
        n_warpl = nologic(warpl)
    elif randoType == "nld":
        n_warpl = nologicdual(warpl)
    elif randoType == "nll":
        n_warpl = nologiclinked(warpl)
    else:
        raise ValueError("Error. "+randoType+" not found!")

    print("#######################################################################")
    print("#######################################################################")
    print("#######################################################################")

    for m, w in n_warpl.items():
        if int(m.split(".zmb")[1]) == 0:
            mapname = m.split(".zmb")[0][4:]
            levelname = mapname[:-3]
            print()
            print(levelname + ": " + mapname)
        print(m.split(".zmb")[1] + ": " + m.split(".zmb")[0] + ": " + str(w))


    print("Writing changes ...")

    # Write new Warps to maplist
    phantom_map: ZDS_PH_MAP
    for phantom_map in loaded_maps_list:
        print(phantom_map.getName() + " ...")

        map_area: ZDS_PH_AREA
        for map_area in phantom_map.children:
            filename = "zmb/" + phantom_map.getName() + "_" + map_area.getID() + ".zmb"
            # print(filename)

            try:
                numofwarps = warpcountl[filename]
            except KeyError:
                numofwarps = 0
            
            warp_list = []

            if not (numofwarps == 0):
                for i in range(numofwarps):
                    warp_list.append(n_warpl[filename+str(i)])
                    
                zmb = zmb_cache[filename]
                warph: zds.ZMB_WARP = zmb.get_child("WARP")
                if not (warph == None):
                    warph.randoReplace(warp_list)
                    
                map_area.getArchive().setFileByName(filename, zmb.save())


        phantom_map.saveToFolder(outdir)
        # input("Neat Break Point :)")

    error_path = os.path.join(outdir, "../", "RANDOMIZER_ERROR_LOG.txt")
    print("Writing Errors to file ... (" + error_path + ")")
    err_string = ""
    for err in error_log:
        err_string += err + "\n"

    with open(error_path, 'wt', encoding='utf-8') as f:
        f.write(err_string[:-1])


def nologic(warpl):
    n_warpl = {}
    o_warpl = warpl.copy()
    print()
    p_fname, p_warp_ce = random.choice(list(warpl.items()))
    first = (p_fname, p_warp_ce)
    del warpl[p_fname]
    for i in range(len(warpl)):
        fname, warp_ce = random.choice(list(warpl.items()))
        del warpl[fname]

        # uid, ft, mid, dwid, dest, rundir
        n_warp_ce = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, p_warp_ce.map_id, p_warp_ce.destination_warp_id, p_warp_ce.destination, warp_ce.run_direction )
        n_warpl[fname] = n_warp_ce
        p_fname = fname
        p_warp_ce = warp_ce
    # Insert first warp
    fname, warp_ce = first
    n_warp_ce = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, p_warp_ce.map_id, p_warp_ce.destination_warp_id, p_warp_ce.destination, warp_ce.run_direction )
    n_warpl[fname] = n_warp_ce
    return n_warpl

def nologicdual(warpl): # Similar to nl
    n_warpl = {}
    o_warpl = warpl.copy()
    print()
    for i in range(int(round(len(warpl)/2))):
        fname, warp_ce = random.choice(list(warpl.items()))
        del warpl[fname]
        p_fname, p_warp_ce = random.choice(list(warpl.items()))
        del warpl[p_fname]

        # uid, ft, mid, dwid, dest, rundir
        n_warpl[fname] = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, p_warp_ce.map_id, p_warp_ce.destination_warp_id, p_warp_ce.destination, warp_ce.run_direction )
        n_warpl[p_fname] = zds.ZMB_WARP_CE( p_warp_ce.UID, p_warp_ce.fade_type, warp_ce.map_id, warp_ce.destination_warp_id, warp_ce.destination, p_warp_ce.run_direction )
    if len(n_warpl) < len(o_warpl):
        fname, warp_ce = random.choice(list(warpl.items()))
        n_warpl[fname] = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, warp_ce.map_id, warp_ce.destination_warp_id, warp_ce.destination, warp_ce.run_direction )
    print(len(o_warpl),len(n_warpl))
    # input("Breakpoint :)")
    return n_warpl

def splitMapInfo(fname):
    mapname = fname.split(".zmb")[0][4:]
    levelname = mapname[:-3]
    mapid = mapname[-2:]
    # print("Levelname:",levelname)
    # print("Mapname:  ",mapname)
    # print("Mapid:    ",mapid)
    return [mapname, levelname, mapid]

def nologiclinked(warpl):
    n_warpl = {}
    o_warpl = warpl.copy()
    print()
    for i in range(int(round(len(warpl)/2))):
        fname, warp_ce = random.choice(list(warpl.items()))
        info = splitMapInfo(fname)
        del warpl[fname]
        p_fname, p_warp_ce = random.choice(list(warpl.items()))
        p_info = splitMapInfo(p_fname)
        del warpl[p_fname]

        # uid, ft, mid, dwid, dest, rundir
        n_warpl[fname] = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, int(p_info[2]), p_warp_ce.destination_warp_id, p_info[1], warp_ce.run_direction )
        n_warpl[p_fname] = zds.ZMB_WARP_CE( p_warp_ce.UID, p_warp_ce.fade_type, int(info[2]), warp_ce.destination_warp_id, info[1], p_warp_ce.run_direction )
    if len(n_warpl) < len(o_warpl):
        fname, warp_ce = random.choice(list(warpl.items()))
        n_warpl[fname] = zds.ZMB_WARP_CE( warp_ce.UID, warp_ce.fade_type, warp_ce.map_id, warp_ce.destination_warp_id, warp_ce.destination, warp_ce.run_direction )
    print(len(o_warpl),len(n_warpl))
    # input("Breakpoint :)")
    return n_warpl


def runBanList(thelist, banlist, enableBanlist):
    if enableBanlist:
        removeList = []
        for f, w in thelist.items():
            for ban in banlist:
                if ban in f and f not in removeList:
                    print("[Banlist] Removing \""+f+"\"")
                    removeList.append(f)
        for f in removeList:
            del thelist[f]

if __name__ == "__main__":
    randomize(404, "../../DS/extracted/data/Map/", "../../DS/randomize/data/Map/")