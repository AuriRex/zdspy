


from . import dataio as d
from . import gheader as gh
from abc import ABC, abstractmethod

################################################################
## .nsbmd  (MDL0) File Start
###############################################################

class NSBMD_MDL0_HEADER:
    def __init__(self, data):
        self.data = data

        self.dummy = d.UInt8(self.data, 0)
        
        self.total_models_num = d.UInt8(self.data, 1)

        self.size = d.UInt16(self.data, 2)


        self.sub_header_size = d.UInt16(self.data, 4)
        self.sub_header_unknwn_size = d.UInt16(self.data, 6)
        self.sub_header_constant = d.UInt32(self.data, 8) # Always 0x00 00 01 7F (UInt32: 383)
        if not (self.sub_header_constant == 383):
            print("MDL Sub-Header Constant not 0x0000017F !: ", self.sub_header_constant)
        self.sub_header_data = []
        self.pointer = 12
        for i in range(self.total_models_num):
            self.sub_header_data.append( ( d.UInt32( self.data, self.pointer+(4*i) ) , d.UInt32(self.data, self.pointer+4+(4*i) ) ) )
        
        self.pointer = 12 + (4 * self.total_models_num)

        self.data_size = d.UInt16(self.data, self.pointer)
        if not (self.data_size == 4):
            print("MDL0 Header data_size != 4:", self.data_size)
        
        self.data_block_size = d.UInt16(self.data, self.pointer + 2)
        self.mdl_offsets = []

        for i in range(self.total_models_num):
            self.mdl_offsets.append( d.UInt32(self.data, self.pointer + 4 + (4 * i) ) )

        self.pointer = self.pointer + 4 + (4 * self.total_models_num)
        self.mdl_names = []
        for i in range(self.total_models_num):
            self.tmp = self.data[self.pointer + (16 * i):self.pointer+16 + (16 * i)].decode()
            self.mdl_names.append( self.tmp )
            print("MDL_"+str(i)+" : "+self.tmp)


        
class NSBMD_MDL0_MDL:
    def __init__(self, data, size):
        self.data = data
        self.size = size

        self.offset_add_mdl_data = d.UInt32(self.data, 4)

        self.offset_tex_pal_data = d.UInt32(self.data, 8)

        self.offset_display_list = d.UInt32(self.data, 12)

        self.offset_display_list_end = d.UInt32(self.data, 16)

        print("Offsets:")
        print("  add_mdl_data:",self.offset_add_mdl_data)
        print("  tex_pal_data:",self.offset_tex_pal_data)
        print("  display_list:",self.offset_display_list)
        print("  display_list_end:",self.offset_display_list_end)

        self.dummy1 = d.UInt8(self.data, 20)
        self.dummy2 = d.UInt8(self.data, 21)
        self.dummy3 = d.UInt8(self.data, 22)

        self.object_count = d.UInt8(self.data, 23)
        self.material_count = d.UInt8(self.data, 24)
        self.polygon_count = d.UInt8(self.data, 25)

        print("Object count:",self.object_count)
        print("Material count:",self.material_count)
        print("Polygon count:",self.polygon_count)

        self.unknwns = [] # 10 Unknown Values!

        for i in range( 10 ):
            self.unknwns.append(d.UInt8(self.data, 26 + i))

        print("Unknown values:",self.unknwns)

        self.total_vertex_count = d.UInt16(self.data, 36)
        self.total_polygon_count = d.UInt16(self.data, 38)
        self.total_triangle_count = d.UInt16(self.data, 40)
        self.total_quad_count = d.UInt16(self.data, 42)

        print("Total Vertex count:",self.total_vertex_count)
        print("Total Polygon count:",self.total_polygon_count)
        print("Total Triangle count:",self.total_triangle_count)
        print("Total Quad count:",self.total_quad_count)

        # Bounding Box
        self.bb_x = self.data[44:46]
        self.bb_y = self.data[46:48]
        self.bb_z = self.data[48:50]

        self.bb_w = self.data[50:52]
        self.bb_h = self.data[52:54]
        self.bb_d = self.data[54:56]

        print("Bounding Box:")
        print("  X:",self.bb_x.hex())
        print("  Y:",self.bb_y.hex())
        print("  Z:",self.bb_z.hex())
        print("  w:",self.bb_w.hex())
        print("  h:",self.bb_h.hex())
        print("  d:",self.bb_d.hex())

        self.rt_use1 = self.data[56:60]
        self.rt_use2 = self.data[60:64]

        # self.objects = []

        self.pointer = 64
        

        self.tmp_offset = self.object_count * 4 + d.UInt16(self.data, self.pointer + 2)
        self.object = NSBMD_MDL0_MDL_OBJ( self.data[self.pointer:self.pointer + self.tmp_offset])

        # print(self.object.data.hex())

        self.additional_mdl_data = self.data[self.offset_add_mdl_data:self.offset_tex_pal_data]

        print("Additional_MDL_Data (Bone & Skeleton stuff):",self.additional_mdl_data.hex())

        self.texture_block_offset = d.UInt16(self.data, self.offset_tex_pal_data)
        self.palette_block_offset = d.UInt16(self.data, self.offset_tex_pal_data+2)

        print("Tex & Pal offsets:")
        print("  Tex:",self.texture_block_offset)
        print("  Pal:",self.palette_block_offset)
        # Offsets are relative to self.offset_tex_pal_data

        self.material = NSBMD_MDL0_MDL_MAT( self.data[self.offset_tex_pal_data+4:self.offset_tex_pal_data+self.texture_block_offset] )

        self.texture = NSBMD_MDL0_MDL_TEX( self.data[ self.offset_tex_pal_data + self.texture_block_offset : self.offset_tex_pal_data + self.palette_block_offset ] )

        self.pal_len = d.UInt16(self.data, self.offset_tex_pal_data + self.palette_block_offset + 2)

        self.palette = NSBMD_MDL0_MDL_PAL( self.data[ self.offset_tex_pal_data + self.palette_block_offset : self.offset_tex_pal_data + self.palette_block_offset + self.pal_len] ) # TODO IMPROVE --> End of Pal section

        self.material_definitions = []

        print("Material Definition:")
        print("num | Offset | Size | Data")
        for i, off in enumerate(self.material.data_offsets):
            noff = self.offset_tex_pal_data + off
            size = d.UInt16(self.data, noff+2)
            matdef = self.data[ noff : noff + size ]
            self.material_definitions.append(matdef)
            print(" ",i,"|",off,"|",size,"|",matdef.hex())

        # print(self.data[self.offset_display_list:self.offset_display_list+48].hex())

        self.polygon = NSBMD_MDL0_MDL_POL( self.data[ self.offset_display_list : self.offset_display_list_end ] )

        # self.tmp_object_size = 0
        # self.tmp_total_obj_offset = 0
        # print(str(self.data[self.pointer:self.pointer+48].hex()))
        # for i in range(self.object_count): # FLawed implementation TODO: Fix
        #     self.tmp_object_size = self.calcObjSize(self.data, self.pointer+self.tmp_total_obj_offset)
        #     print("TMPOBJSize:",self.tmp_object_size)
        #     self.tmp_total_obj_offset_old = self.tmp_total_obj_offset
        #     self.tmp_total_obj_offset += self.tmp_object_size
        #     print("OBJ_"+str(i)+": Size: ",self.tmp_object_size)
        #     self.objects.append( NSBMD_MDL0_MDL_OBJ( self.data[self.pointer+self.tmp_total_obj_offset_old:self.pointer+self.tmp_total_obj_offset] , self.tmp_object_size ) )
        #     break # TODO Remove ?
        # for i, o in enumerate(self.objects):
        #     print("List_OBJ_"+str(i)+": "+str(o.data.hex())+"\n\n")

    # Removed because i over complicated stuff ...   
    # def calcObjSize(self, data, header_offset):
    #     pointer = header_offset

    #     obj_num = d.UInt8(data, pointer + 1)

    #     obj_header_size = d.UInt16(data, pointer + 2)

    #     obj_sub_header_size = d.UInt16(data, pointer + 4)

    #     obj_sub_unknown_size = d.UInt16(data, pointer + 6)
    #     print(str(data[pointer:pointer+48].hex()))
    #     print("HeaderSize:",obj_header_size)
    #     print("NumObjs:",obj_num)
    #     print("OBJSUS: ",obj_sub_unknown_size)
    #     # Update pointer location
    #     print("Pointer: ",pointer)
    #     pointer = pointer + 4 + obj_sub_unknown_size
    #     print("Pointer: ",pointer)
    #     print(str(data[pointer:pointer+48].hex()))
    #     # data_sec_size = d.UInt16(data, pointer + 2)

    #     data_offsets = []
    #     total_offset_additional = 0
    #     # Data is always 4 Byte long!
    #     for i in range(obj_num):
    #         data_offsets.append( d.UInt32(data, pointer + (4 * i) ) )
    #         total_offset_additional += 4 # Add 4 Bytes for every Num Object

        

    #     for off in data_offsets:
    #         print("Offset:",off)
    #         trans_flag = d.UInt8(data, header_offset + off)

    #         print("TransformationFlag:",trans_flag)

    #         if trans_flag&1 != 0: # If 1th Bit is Set
    #             print("Translation bit set.") # + 12 Byte
    #             # total_offset_additional += 12
    #         if trans_flag&2 != 0: # If 2th Bit is Set
    #             print("Rotation bit set.")
    #         if trans_flag&4 != 0: # If 3th Bit is Set
    #             print("Scale bit set.")
    #         if trans_flag&8 != 0: # If 4th Bit is Set
    #             print("Pivot bit set.") # + 4 Bytes
    #             # total_offset_additional += 4

    #     # TODO: Object ends with 0x 06 00 00 00 ??? (Num Offsets * 4 + 4)

    #     return obj_header_size + total_offset_additional # <-- flag offsets + content length


class NSBMD_MDL0_MDL_CONTAINER(ABC):
    def __init__(self, data):
        self.data = data

        self.name_c()

        self.dummy = d.UInt8(self.data, 0) # Always 0

        if self.dummy != 0:
            print("[MDL0] Dummy Byte not 0!")

        self.number_of_element = d.UInt8(self.data, 1)

        self.header_size = d.UInt16(self.data, 2)

        self.sub_header_size = d.UInt16(self.data, 4)

        self.sub_unknown_size = d.UInt16(self.data, 6)
        
        self.data_offsets = []

        self.data_size = d.UInt16(self.data, self.sub_unknown_size)
        if self.data_size != 4:
            print("[MDL0] Data Size is not 4!")

        self.data_sec_size = d.UInt16(self.data, self.sub_unknown_size + 2)

        self.offset_name_section = 0

        self.offset_name_section = self.sub_unknown_size + 4 + (4 * self.number_of_element)

        self.names = []

        # Data is always 4 Byte long!
        for i in range(self.number_of_element):
            self.data_offsets.append( d.UInt32(self.data, self.sub_unknown_size + 4 + (4 * i) ) )
            name = self.data[self.offset_name_section + (16 * i): self.offset_name_section + 16 + (16 * i)].decode()
            print(str(i)+"_Name:",name)
            self.names.append(name)

        self.init()
    
    @abstractmethod
    def init(self):
        pass
    
    @abstractmethod
    def name_c(self):
        pass

class NSBMD_MDL0_MDL_CONTAINER_LDS(ABC): # For Long Data Section TODO
    def __init__(self, data):
        self.data = data

        self.name_c()

        # print(self.data.hex()) # TODO Remove this line

        self.dummy = d.UInt8(self.data, 0) # Always 0

        if self.dummy != 0:
            print("[MDL0] Dummy Byte not 0!")

        self.number_of_element = d.UInt8(self.data, 1)

        self.header_size = d.UInt16(self.data, 2)

        self.sub_header_size = d.UInt16(self.data, 4)

        self.sub_unknown_size = d.UInt16(self.data, 6)
        
        self.data_offsets = []  # <-- Relative to self.offset_tex_pal_data
        self.data_no_associated_mats = []

        self.data_size = d.UInt16(self.data, self.sub_unknown_size)
        if self.data_size != 4:
            print("[MDL0] Data Size is not 4!")

        self.data_sec_size = d.UInt16(self.data, self.sub_unknown_size + 2)

        self.offset_name_section = 0

        self.offset_name_section = self.sub_unknown_size + 4 + (4 * self.number_of_element)

        self.names = []

        # Data is always 4 Byte long!
        for i in range(self.number_of_element):
            self.data_offsets.append( d.UInt16(self.data, self.sub_unknown_size + 4 + (4 * i) ) )
            self.data_no_associated_mats.append( d.UInt8(self.data, self.sub_unknown_size + 4 + (4 * i) + 2 ) )

            name = self.data[self.offset_name_section + (16 * i): self.offset_name_section + 16 + (16 * i)].decode()
            print(str(i)+"_Name:",name)
            self.names.append(name)

        print("Offset | No. of Associations")
        for o, a in zip(self.data_offsets, self.data_no_associated_mats):
            print(" ",o," | ",a)

        self.init()
    
    @abstractmethod
    def init(self):
        pass
    
    @abstractmethod
    def name_c(self):
        pass

class NSBMD_MDL0_MDL_OBJ(NSBMD_MDL0_MDL_CONTAINER):
    def name_c(self):
        print("[ OBJ Data ]")
    def init(self):
        # self.data = data
        # self.size = size

        # self.dummy = d.UInt8(self.data, 0) # Always 0

        # self.number_of_element = d.UInt8(self.data, 1)

        # self.header_size = d.UInt16(self.data, 2)

        # self.sub_header_size = d.UInt16(self.data, 4)

        # self.sub_unknown_size = d.UInt16(self.data, 6)
        print("OBJ_HeaderSize:",self.header_size)
        print("OBJ_NumObjs:",self.number_of_element)
        print("OBJ_SUS: ",self.sub_unknown_size)

        self.trans_data = []

        for off in self.data_offsets:
            print("Offset:",off)
            trans_flag = d.UInt8(self.data, off)
            td = self.data[off:off + 4]
            self.trans_data.append( td )

            print("TransformationFlag:",trans_flag)
            print(" ",td.hex())
            if trans_flag&1 != 0: # If 1th Bit is Set
                print("  Translation bit set.") # + 12 Byte
            if trans_flag&2 != 0: # If 2th Bit is Set
                print("  Rotation bit set.")
            if trans_flag&4 != 0: # If 3th Bit is Set
                print("  Scale bit set.")
            if trans_flag&8 != 0: # If 4th Bit is Set
                print("  Pivot bit set.") # + 4 Bytes


#NSBMD_MDL0_MDL_MAT
class NSBMD_MDL0_MDL_MAT(NSBMD_MDL0_MDL_CONTAINER):
    def name_c(self):
        print("[ MAT Data ]")
    def init(self):
        print("MAT_HeaderSize:",self.header_size)
        print("MAT_NumMats:",self.number_of_element)
        print("MAT_SUS: ",self.sub_unknown_size)

        print("Material Definition Offsets:") # Relative to self.offset_tex_pal_data
        for off in self.data_offsets:
            print(" ",off)


class NSBMD_MDL0_MDL_TEX(NSBMD_MDL0_MDL_CONTAINER_LDS):
    def name_c(self):
        print("[ TEX Data ]")
    def init(self):
        print("TEX_HeaderSize:",self.header_size)
        print("TEX_NumTexs:",self.number_of_element)
        print("TEX_SUS: ",self.sub_unknown_size)

class NSBMD_MDL0_MDL_PAL(NSBMD_MDL0_MDL_CONTAINER_LDS):
    def name_c(self):
        print("[ PAL Data ]")
    def init(self):
        print("PAL_HeaderSize:",self.header_size)
        print("PAL_NumTexs:",self.number_of_element)
        print("PAL_SUS: ",self.sub_unknown_size)

class NSBMD_MDL0_MDL_POL_POL_DEF:
    def __init__(self, data, i=0):
        self.data = data
        
        self.unknown_bytes = self.data[ : 8]

        self.offset = d.UInt32(self.data, 8) # Relative to parents self.offset_poly_def

        self.display_list_size = d.UInt32(self.data, 12)

        print("Polygon"+str(i)+" Definition:")
        print("  Unknown Data:",self.unknown_bytes.hex())
        print("  Offset:",self.offset)
        print("  Size:",self.display_list_size)


class NSBMD_MDL0_MDL_POL(NSBMD_MDL0_MDL_CONTAINER):
    def name_c(self):
        print("[ POL Data ]")
    def init(self):
        # print(self.data.hex())
        print("POL_HeaderSize:",self.header_size)
        print("POL_NumTexs:",self.number_of_element)
        print("POL_SUS: ",self.sub_unknown_size)
        
        self.polygon_definitions = []
        
        self.offset_poly_def = self.data_offsets[0]

        for i, off in enumerate(self.data_offsets):
            self.polygon_definitions.append( NSBMD_MDL0_MDL_POL_POL_DEF( self.data[ off : off + 16 ] , i ) )

class NSBMD_MDL0(gh.ZDS_GenericElementHeaderIDO):
    def init(self):
        print("Done.")
        self.header_size = d.UInt16(self.data, 10)

        self.header = NSBMD_MDL0_HEADER(self.data[8:8+self.header_size])

        self.models = []

        for offset in self.header.mdl_offsets:
            # Offsets are relative to MDL0 Block here.
            self.tmp_mdl_size = d.UInt32(self.data, offset)
            self.models.append( NSBMD_MDL0_MDL( self.data[offset: offset + self.tmp_mdl_size] , self.tmp_mdl_size ) )


class NSBMD(gh.ZDS_GenericFileHeader):

    def init(self):
        
        self.pointer = d.UInt32(self.data, self.pointer) # Offset after header ? (14 00 00 00)

        for i in range(self.children_count):
            self.tmp = d.UInt32(self.data, self.pointer + 4)
            gen = gh.NDS_GenericTempContainerNR(self.data[self.pointer:self.pointer+self.tmp])
            self.pointer = self.pointer+self.tmp
            print(gen.identification + " Size: "+str(gen.size))
            if gen.identification == "DUMMY":
                pass
            elif gen.identification == "MDL0":
                self.children.append( NSBMD_MDL0(gen.data) )
            else:
                print("TODO! #############################################################################################")
                self.children.append( gen )


################################################################
## .nsbmd  (MDL0) File END
###############################################################

def fromFile(path):
    return NSBMD(d.ReadFile(path))