
from . import dataio as d
from . import gheader as gh

################################################################
## .zmb  (ZMB) File END
###############################################################

class ZMB_WARP(gh.ZDS_GenericElementHeader):

    def init(self):
        print("Loading Section: " + self.identification)
        # print(data.hex())
        print("Children: "+str(self.children_count))
        self.child_size = 24

        self.deny_save = False

        if not (self.children_count == 0):
            self.calc_cs = int((len(self.data) - 12) / self.children_count)
            self.deny_save = False
            if not (self.calc_cs == self.child_size):
                print("[NPCA] Children Size is messed up! There are only "+str(self.calc_cs)+" bits but the Header said "+str(self.children_count)+"bit. File might be corrupt, saving disabled!")
                self.child_size = self.calc_cs # TODO: WTF ? Hack - Remove later
                self.deny_save = True
                # self.children_count = self.calc_cs

        for _ in range(self.children_count):
            self.children.append( ZMB_WARP_CE.fromBinary( self.data[self.offset:self.offset+self.child_size]) )
            self.offset = self.offset + self.child_size

    def addWarp(self, fade_type, map_id, destination_warp_id, str16_destination, run_direction):
        largest_uid = 0
        for c in self.children:
            if c.UID >= largest_uid:
                largest_uid = c.UID + 1

        print("Added Warp:")
        self.children.append( ZMB_WARP_CE( largest_uid, fade_type, map_id, destination_warp_id, str16_destination, run_direction ) )

    def randoReplace(self, warp_list):
        self.children = warp_list

    def calculate_size(self):
        self.size = 12 + self.child_size * len(self.children)
        return self.size

    def save(self):
        if self.deny_save == True:
            print("[WARP] can not save corrupted file!")
            return bytearray(0)
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("50524157") # PRAW
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZMB_WARP_CE:

    def __init__(self, uid, ft, mid, dwid, dest, rundir):
        self.UID = uid
        self.fade_type = ft
        self.map_id = mid
        self.destination_warp_id = dwid
        self.destination = dest
        self.run_direction = rundir

        print("WUID:"+str(self.UID)+ " FadeType:"+str(self.fade_type)+ " MapID:"+str(self.map_id)+ " DestWUID-1:"+str(self.destination_warp_id) + " WDest:"+self.destination + " RunDir(Rotation):"+str(self.run_direction))

    @classmethod
    def fromBinary(self, data):
        
        UID = d.UInt8(data, 0)
        fade_type = d.UInt8(data, 1)
        map_id = d.UInt8(data, 2)
        destination_warp_id = d.UInt8(data, 3)

        # Max 16 Byte / Characters
        destination = data[4:20].decode()

        if (len(data) < 24):
            print("[ZMB_WARP_CE] Warp too short! Beta file ?")
            run_direction = 0
        else:
            run_direction = d.UInt32(data, 20)

        print("WUID:"+str(UID)+ " FadeType:"+str(fade_type)+ " MapID:"+str(map_id)+ " DestWUID-1:"+str(destination_warp_id) + " WDest:"+destination + " RunDir(Rotation):"+str(run_direction))

        return self(UID, fade_type, map_id, destination_warp_id, destination, run_direction)

    def cleanDestination(self):
        out = ""
        for c in self.destination:
            if c in "abcdefghijklmnopqrstuvwxyz_":
                out += c
        return out

    def __str__(self):
        return ("WUID:"+str(self.UID)+ " FadeType:"+str(self.fade_type)+ " MapID:"+str(self.map_id)+ " DestWUID-1:"+str(self.destination_warp_id) + " WDest:"+self.destination + " RunDir(Rotation):"+str(self.run_direction))

    def save(self):
        buffer = bytearray(24) # COMPLETE! :)

        buffer = d.w_UInt8(buffer, 0, self.UID)
        buffer = d.w_UInt8(buffer, 1, self.fade_type)
        buffer = d.w_UInt8(buffer, 2, self.map_id)
        buffer = d.w_UInt8(buffer, 3, self.destination_warp_id)

        buffer = d.w_UTF8String(buffer, 4, 16, self.destination)

        buffer = d.w_UInt32(buffer, 20, self.run_direction)

        return buffer

class ZMB_MPOB(gh.ZDS_GenericElementHeader):

    def init(self):
        print("Loading Section: " + self.identification)
        print("Children: "+str(self.children_count))

        

        self.child_size = 28

        if not (self.child_size == 0):
            self.calc_cs = int((len(self.data) - 12) / self.child_size)

            if not (self.calc_cs == self.children_count):
                print("[MPOB] Children count is messed up! There are only "+str(self.calc_cs)+" but the Header said: "+str(self.children_count))
                self.children_count = self.calc_cs

        for i in range(self.children_count):
            self.children.append( ZMB_MPOB_CE(self.data[self.offset:self.offset+self.child_size], i) )
            self.offset = self.offset + self.child_size

    def addObject(self, objid, posx, posy, rdata):
        buffer = bytearray(28)

        buffer = d.w_UInt32(buffer, 0, objid)
        buffer = d.w_UInt8(buffer, 4, posx)
        buffer = d.w_UInt8(buffer, 5, posy)

        buffer[6:] = bytearray.fromhex(rdata)

        self.children.append(ZMB_MPOB_CE(buffer ,-1))
        # OBJID:10 XPos:30 YPos:25 HEX:

    def calculate_size(self):
        self.size = 12 + self.child_size * len(self.children)
        return self.size

    def save(self):
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("424f504d") # BOPM
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZMB_MPOB_CE:

    def __init__(self, data, num):
        self.data = data
        self.mapobjectid = d.UInt32(self.data, 0)
        self.position_x = d.UInt8(self.data, 4)
        self.position_y = d.UInt8(self.data, 5)

        self.rotation = d.SInt16(self.data, 6)

        print("OBJID:"+str(self.mapobjectid) + " XPos:"+str(self.position_x)+ " YPos:"+str(self.position_y)+ " HEX:" + str(self.data[8:].hex()) + " [:"+str(num)+"] ")
    
    def __str__(self):
        return "OBJID:"+str(self.mapobjectid) + " XPos:"+str(self.position_x)+ " YPos:"+str(self.position_y)+ " HEX:" + str(self.data.hex())

    def save(self):
        buffer = self.data

        buffer = d.w_UInt32(buffer, 0, self.mapobjectid)
        buffer = d.w_UInt8(buffer, 4, self.position_x)
        buffer = d.w_UInt8(buffer, 5, self.position_y)

        return buffer


class ZMB_NPCA(gh.ZDS_GenericElementHeader):

    def init(self):
        print("Loading Section: " + self.identification)
        print("Children: "+str(self.children_count))

        self.child_size = 32

        if not (self.child_size == 0):
            self.calc_cs = int((len(self.data) - 12) / self.child_size)
            self.deny_save = False
            if not (self.calc_cs == self.children_count):
                print("[NPCA] Children count is messed up! There are only "+str(self.calc_cs)+" but the Header said: "+str(self.children_count)+". File might be corrupt, saving disabled!")
                self.child_size = int((len(self.data) - 12) / self.children_count) # TODO: WTF ? Hack XP
                self.deny_save = True
                # self.children_count = self.calc_cs

        for i in range(self.children_count):
            self.children.append( ZMB_NPCA_CE(self.data[self.offset:self.offset+self.child_size], i) )
            self.offset = self.offset + self.child_size

    def addNPCRaw(self, data):
        if len(data) != self.child_size:
            print("[NPCA] Could not create new NPC")
            return None
        new_npc = ZMB_NPCA_CE(data, -1)
        self.children.append( new_npc)
        return new_npc

    def addNPC(self, npctype, xpos, ypos, link, data): # TODO Unique fields as inputs
        new_data = bytearray(self.child_size)

        new_data[:4] = bytearray.fromhex(npctype) 
        new_data = d.w_UInt16(new_data, 4, xpos)
        new_data = d.w_UInt16(new_data, 6, ypos)
        new_data = d.w_UInt16(new_data, 8, link)


        new_data[10:] = data # FLags

        self.children.append( ZMB_NPCA_CE(new_data, -1))

    def calculate_size(self):
        self.size = 12 + self.child_size * len(self.children)
        return self.size

    def save(self):
        if self.deny_save == True:
            print("[NPCA] can not save corrupted section!")
            return bytearray(0)
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("4143504e") # ACPN
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer


class ZMB_NPCA_CE:

    def __init__(self, data, num):
        self.data = data
        self.npctype = d.Decode(self.data[:4])

        self.position_x = d.SFix(self.data, 4, n_bits=16, n_bits_int=12)
        self.position_y = d.SFix(self.data, 6, n_bits=16, n_bits_int=12)
        self.position_z = d.SInt16(self.data, 8)

        self.rotation = d.SInt16(self.data, 10)

        # print(str(len(self.data)) + ": " + self.data.hex())
        if len(self.data) < 0x1C:
            self.bmg_script_id = 0
        else:
            self.bmg_script_id = d.UInt32(self.data, 0x18)

        print("NPCID:"+str(self.npctype) + " HEX:" + str(self.data[4:].hex()) + " [:"+str(num)+"] ")

    def save(self):
        buffer = bytearray(self.data)

        buffer[:4] = d.Encode(self.npctype)
        buffer = d.w_SFix(buffer, 4, self.position_x, n_bits=16, n_bits_int=12)
        buffer = d.w_SFix(buffer, 6, self.position_y, n_bits=16, n_bits_int=12)
        buffer = d.w_SInt16(buffer, 8, self.position_z)

        buffer = d.w_SInt16(buffer, 10, self.rotation)

        buffer = d.w_UInt32(buffer, 0x18, self.bmg_script_id)

        return buffer

class ZMB_ROOM(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        print("Loading Section: " + self.identification)

        self.unknown1 = d.UInt8(self.data, 8) # Do Not Touch -> does funky stuff with skybox, music, light and npc Z-Position
        # unknown1 may have something to do with terrys shop
        self.environment_type = d.UInt8(self.data, 9) # = Skybox Color & Mist / Fog effects & Object Coloring
        self.unknown2 = d.UInt8(self.data, 10) # Always 0x04
        self.unknown3 = d.UInt8(self.data, 11) # Always 0x03
        self.music_id = d.UInt8(self.data, 12)
        self.lighting_type = d.UInt8(self.data, 13)

        print("EnvType:"+str(self.environment_type)+" UNKNWN1:"+str(self.unknown1)+" UNKNWN2:"+str(self.unknown2)+" MUSICID:"+str(self.music_id)+ " HEX:"+str(self.data[13:].hex()))

    def calculate_size(self):
        self.size = len(self.data)
        return self.size

    def save(self):
        buffer = self.data

        buffer = d.w_UInt8(buffer, 8 , self.unknown1)
        buffer = d.w_UInt8(buffer, 9 , self.environment_type)
        buffer = d.w_UInt8(buffer, 10 , self.unknown2)
        buffer = d.w_UInt8(buffer, 11 , self.unknown3)
        buffer = d.w_UInt8(buffer, 12 , self.music_id)
        buffer = d.w_UInt8(buffer, 13 , self.lighting_type)

        return buffer

class ZMB_ARAB(gh.ZDS_GenericElementHeader):

    def init(self):
        print("Loading Section: " + self.identification)
        print("Children: "+str(self.children_count))

        self.child_size = 12
        for i in range(self.children_count):
            self.children.append( ZMB_ARAB_CE(self.data[self.offset:self.offset+self.child_size], i) )
            self.offset = self.offset + self.child_size

    def calculate_size(self):
        self.size = 12 + self.child_size * len(self.children)
        return self.size

    def save(self):
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("42415241") # BARA
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt16(buffer, 10, 65535) # Write 0xFFFF

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZMB_ARAB_CE:

    def __init__(self, data, num):
        self.data = data

        self.id = d.UInt8(self.data, 0)
        self.unknown1 = d.UInt8(self.data, 1)

        self.unknown2 = d.SInt16(self.data, 2)

        self.position_y = d.SInt16(self.data, 4)
        self.position_x = d.SInt16(self.data, 6)
        if len(self.data) < 10:
            self.position_y_secondary = 0
            self.position_x_secondary = 0
        else:
            self.position_y_secondary = d.SInt16(self.data, 8)
            self.position_x_secondary = d.SInt16(self.data, 10)

        print("ARAB_CE:"+" HEX:" + str(self.data.hex()) + " [:"+str(num)+"] ")

    def save(self):
        hs = 12
        buffer = bytearray(hs)

        buffer = d.w_UInt8(buffer, 0, self.id)
        buffer = d.w_UInt8(buffer, 1, self.unknown1)

        buffer = d.w_SInt16(buffer, 2, self.unknown2)

        buffer = d.w_SInt16(buffer, 4, self.position_y)
        buffer = d.w_SInt16(buffer, 6, self.position_x)
        buffer = d.w_SInt16(buffer, 8, self.position_y_secondary)
        buffer = d.w_SInt16(buffer, 10, self.position_x_secondary)

        return buffer

class ZMB_PLYR(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        print("Loading Section: " + self.identification)

        
        self.children_count = d.UInt16(self.data, 8)
        self.children = []
        print("Children: "+str(self.children_count))

        self.unknwn1 = d.UInt8(self.data, 10)
        self.unknwn2 = d.UInt8(self.data, 11)
        self.offset = 12

        self.child_size = 16
        for i in range(self.children_count):
            self.children.append( ZMB_PLYR_CE(self.data[self.offset:self.offset+self.child_size], i) )
            self.offset = self.offset + self.child_size
        #print("LightingID:"+str(self.lighting_id)+" UNKNWN1:"+str(self.unknwn1)+" UNKNWN2:"+str(self.unknwn2)+" MUSICID:"+str(self.music_id)+ " HEX:"+str(self.data[13:].hex()))

    def calculate_size(self):
        self.size = 12 + self.child_size * len(self.children)
        return self.size

    def save(self):
        hs = 12
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("52594c50") # RYLP
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt8(buffer, 10, self.unknwn1) # Unknown #1
        buffer = d.w_UInt8(buffer, 11, self.unknwn2) # Unknown #2
        # NO 0xFFFF !!!

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

class ZMB_PLYR_CE:

    def __init__(self, data, num):
        self.data = data

        self.position_x = d.SFix32_16(self.data, 0)
        self.position_z = d.SFix32_16(self.data, 4)
        self.position_y = d.SFix32_16(self.data, 8)
        self.rotation = d.SInt16(self.data, 0xC)

        self.id = d.UInt8(self.data, 0xE)
        self.unknown1 = d.UInt8(self.data, 0xF)

        print(self)
        # print("PLYR_CE:"+" HEX:" + str(self.data.hex()) + " [:"+str(num)+"] ")

    def save(self):
        hs = 0x10
        buffer = bytearray(hs)
        buffer = d.w_SFix32_16(buffer, 0, self.position_x) # X
        buffer = d.w_SFix32_16(buffer, 4, self.position_z) # Z
        buffer = d.w_SFix32_16(buffer, 8, self.position_y) # Y
        buffer = d.w_SInt16(buffer, 0xC, self.rotation) # Rotation

        buffer = d.w_UInt8(buffer, 0xE, self.id) # ID
        buffer = d.w_UInt8(buffer, 0xF, self.unknown1) # Unknown1

        return buffer

    def __str__(self):
        return "<ZMB_PLYR_CE ID:"+str(self.id)+" X:" + str(self.position_x) + " Y:" + str(self.position_y) + " Z:" + str(self.position_z) + " Rot:" + str(self.rotation) + " Unknown1:" + str(self.unknown1) + ">"

class ZMB_CAME(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        print("Loading Section: " + self.identification)
        if len(self.data) > 12:
            print("[CAMERA] SECTION HAS DATA! WOOOOH!")

        self.children_count = d.UInt16(self.data, 8)

        self.child_size = 28

        self.offset = 12

        self.children = []

        for _ in range(self.children_count):
            self.children.append( ZMB_CAME_CE( self.data[ self.offset : self.offset + self.child_size ] ) )
            self.offset += self.child_size

    def calculate_size(self):
        self.size = 12 + (len(self.children) * 28)
        return self.size

    def save(self):
        # TODO GETBACK
        buffer = bytearray(12)
        buffer[:4] = bytearray.fromhex("454D4143") # EMAC
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Size
        buffer = d.w_UInt16(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt8(buffer, 10, int(0xFF))
        buffer = d.w_UInt8(buffer, 11, int(0xFF))

        for c in self.children:
            buffer += c.save()
        return self.data

class ZMB_CAME_CE(gh.ZDS_GenericElementHeaderIDO):
    def init(self):
        print("CAMERA_CE:",self.identification , self.data[4:].hex() )

    def save(self):
        return self.data

class ZMB_RALB(gh.ZDS_GenericElementHeader): # Seems to Contain Movement Paths (Phantoms)

    def init(self):
        print("Loading Section: " + self.identification)
        print("Children: "+str(self.children_count))

        self.child_size = 12

        self.total_node_count = int( (len(self.data)-12) / 12) - self.child_size

        self.offset = 12

        self.children = []

        for i in range(self.children_count):
            path_end_offset = d.UInt8(self.data, self.offset+1)*self.child_size + 12
            self.children.append( ZMB_RALB_PATH( self.data[ self.offset : self.offset + path_end_offset ] , i) )
            self.offset += path_end_offset

    def calculate_size(self):
        size = 0
        for child in self.children:
            size += child.number_of_nodes * 12 + 12
        size += 12
        self.size = size
        return self.size

    def save(self):
        hs = 12
        buffer = bytearray(hs)

        buffer[:4] = bytearray.fromhex("424c4152") # BLAR

        buffer = d.w_UInt16(buffer, 8, len(self.children))

        buffer[10:12] = bytearray.fromhex("FFFF")

        for child in self.children:
            buffer += child.save()

        buffer = d.w_UInt32(buffer, 4, len(buffer))

        return buffer

class ZMB_RALB_PATH:

    def __init__(self, data, num):
        self.data = data[12:]

        self.head = data[:12]

        self.nodes = []

        self.node_size = 12

        self.number_of_nodes = d.UInt8(self.head, 1)
        self.number_of_nodes_calculated = int( len(self.data) / self.node_size )

        if not self.number_of_nodes == self.number_of_nodes_calculated:
            print("Warning! Number of Nodes missmatch between read and calculated!")

        self.offset = 0

        print("RALB_PATH:"+" HEX:" + str(self.head.hex()) + " [:"+str(num)+"] #Nodes:" + str(self.number_of_nodes) + " #NodesCalc:" + str(self.number_of_nodes_calculated))

        for i in range(self.number_of_nodes):
            self.nodes.append( ZMB_RALB_NODE( self.data[self.offset : self.offset + self.node_size] , i) )
            self.offset += self.node_size


    def save(self):
        buffer = self.head

        for node in self.nodes:
            buffer += node.save()

        return buffer

class ZMB_RALB_NODE: # TODO
    def __init__(self, data, num):
        self.data = data

        self.position_x = d.SFix(self.data, 0, 16, 12)
        self.position_y = d.SFix(self.data, 2, 16, 12)

        print(" RALB_NODE:"+" PosX:"+str(self.position_x)+" PosY:"+str(self.position_y)+" HEX:" + str(self.data[4:].hex()) + " [:"+str(num)+"] ")

    def save(self):
        hs = 12
        buffer = self.data
        buffer = d.w_SFix(buffer, 0, self.position_x, 16, 12) # PosX
        buffer = d.w_SFix(buffer, 2, self.position_y, 16, 12) # PosY

        return buffer

class ZMB_ROMB(gh.ZDS_GenericElementHeaderRaw): # TODO Investigate!
    # Read Only Memory Binary ???
    def init(self):
        print("Loading Section: " + self.identification)

        self.unknwn1 = d.UInt16(self.data, 8)
        self.unknwn2 = d.UInt16(self.data, 10)

        print("ROMB: "+"Unknwn1: "+str(self.unknwn1)+" Unknwn2: "+str(self.unknwn2))
    
    def calculate_size(self):
        self.size = len(self.data)
        return self.size

    def save(self):
        return self.data # TODO

class ZMB:
    def __init__(self, data):
        self.data = data
        self.identification = data[:8].decode()
        if self.identification != "BPAM1BMZ":
            print("Not a ZMB File!")
            return
        print("ZMB File: "+self.identification)
        self.size = d.UInt32(self.data, 8)
        print("Size: "+str(self.size))
        self.unknown1 = self.data[16:32]
        print("Unknown1: "+ str(self.unknown1.hex()))

        self.offset = 32

        self.children_count = d.UInt32(self.data, 12)
        self.children = []

        for _ in range(self.children_count):
            # print("Pointer:",self.offset,"HEX:",self.data[self.offset:].hex())
            if self.offset >= len(self.data):
                raise Exception('Not enough children in file and EOF reached. The children count must be {} but it was: {}'.format(self.children_count, len(self.children)))
            self.tmp = d.UInt32(self.data, self.offset + 4)
            gen = gh.NDS_GenericTempContainer(self.data[self.offset:self.offset+self.tmp])
            self.offset = self.offset+self.tmp
            print(gen.identification + " Size: "+str(gen.size))
            if gen.identification == "DUMMY":
                pass
            elif gen.identification == "ROMB":
                self.children.append( ZMB_ROMB(gen.data) )
            elif gen.identification == "ARAB":
                self.children.append( ZMB_ARAB(gen.data) )
            elif gen.identification == "PLYR":
                self.children.append( ZMB_PLYR(gen.data) )
            elif gen.identification == "CAME":
                self.children.append( ZMB_CAME(gen.data) )
            elif gen.identification == "RALB":
                self.children.append( ZMB_RALB(gen.data) )
            elif gen.identification == "ROOM":
                self.children.append( ZMB_ROOM(gen.data) )
            elif gen.identification == "WARP":
                self.children.append( ZMB_WARP(gen.data) )
            elif gen.identification == "MPOB":
                self.children.append( ZMB_MPOB(gen.data) )
            elif gen.identification == "NPCA":
                self.children.append( ZMB_NPCA(gen.data) )
            else:
                print("TODO! #############################################################################################")
                self.children.append( gen )

        self.npctypes = { # TODO Add More NPC Types and/or remove/relocate this
            "Corpse": "53505243", # Corpse / Skelleton | CRPS
            "Spikeroller": "4C525053", # Rolling Spikes | LRPS
            "Navimessage": "47534D4E", # Message that Ceila says? | GMSN | ExNPC: 47534D4ED401B40100FF00000000000000000000010100007100780000010000  |  ( copied a corpse switched npc type to this and ceila said its text upon entering the room )
            "Camerahighlight": "52415441", # Camera Highlight | RATA | Camera scrolls to location of npc and back to link
            "CHOB": "424F4843", # Something todo with Paths ? | BOHC
            "Bluephantom": "52534843", # Blue Phantom / Chaser? | RSHC
            "SWOB": "424F5753", # Unknown | BOWS
            "Redphantom": "32534843", # Red Phantom | CHS2
            "ITGE": "45475449", # Unknown3
        }

    def getNPCType(self, type):
        if type in self.npctypes:
            return self.npctypes[type]

        print("NPC Type not found: \"" + type + "\"")
        raise ValueError("NPC Type not found: \"" + type + "\"")


    def get_child(self, child_idnetification):
        try:
            for child in self.children:
                if child.identification == child_idnetification:
                    return child
        except AttributeError:
            print("[ZMB] get_child() -> Attribute 'self.children' does not exist!")
            return None

        print("[ZMB] Child not found: \"" + child_idnetification + "\"")

    def calculate_size(self):
        tmp_size = 32
        
        for child in self.children:
            tmp_size = tmp_size + child.calculate_size()

        self.size = tmp_size
        return self.size

    def save(self):
        hs = 31
        buffer = bytearray(hs)
        buffer[:8] = bytearray.fromhex("4250414d31424d5a") # BPAM1BMZ
        buffer = d.w_UInt32(buffer, 8, self.calculate_size()) # Size
        buffer = d.w_UInt32(buffer, 12, len(self.children)) # Children Count

        buffer[16:31] = bytearray.fromhex("04030201040302010403020104030201")

        for child in self.children:
            buffer = buffer + child.save()

        return buffer


################################################################
## .zmb  (ZMB) File END
###############################################################


def fromFile(path):
    return ZMB(d.ReadFile(path))