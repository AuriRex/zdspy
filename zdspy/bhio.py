
from . import dataio as d
from . import gheader as gh


################################################################
## .bhio  (DNFH) File START
###############################################################

"""
BHIO is a file containing all objects in the game
"""

class HFND(gh.ZDS_GenericElementHeaderIDO):

    # Parameter Identifier ?
    olid_1 = "896582cc8c60"
    olid_2 = "896594bc8c61"
    olid_3 = "896594bc8c6181468f63"
    olid_4 = "835e836283608341834e8356"
    olid_5 = "835f8381815b83578eed97de"
    olid_6 = "8376838c83438384815b835f"
    olid_7 = "9347835f8381815b8357"
    olid_8 = "89c28e8b94bb92e8"
    olid = ["This Array Starts at 1 :)",olid_1,olid_2,olid_3,olid_4,olid_5,olid_6,olid_7,olid_8] # No Comment ...

    def init(self):

        self.unknwn1 = d.UInt32(self.data, 4)
        self.size = d.UInt32(self.data, 8)
        self.pointer = 16
        self.obj_id_string = d.Decode(self.data[16:20])

        print("Object Identifier: "+self.obj_id_string)

        self.add_offset = d.UInt32(self.data, self.pointer + 4)

        self.inbetween_data = self.data[self.pointer + 8:self.pointer + 8 + self.add_offset]

        for b in self.inbetween_data:
            if not b == 0:
                print("Non Zero Inbtwn: "+str(self.inbetween_data))
                break

        self.pointer = self.pointer + 8 + self.add_offset

        # method = getattr(self, method_name, lambda: "Invalid month")

        for i in range(1, 9):
            
            if str(self.data[self.pointer:self.pointer + (len(HFND.olid[i])//2) ].hex()) == HFND.olid[i]:
                self.tmp = self.data[self.pointer + (len(HFND.olid[i])//2) :self.pointer+16]
                for b in self.tmp:
                    if not b == 0:
                        print("OLine"+str(i)+": "+str(self.tmp.hex()))
                        break
            else:
                print("OL"+str(i)+": Wrong Identification! I wont stop you but things might break.")
            
            setattr(self, "obj_params_"+str(i), self.tmp)

            self.pointer = self.pointer + 16

    def calculate_size(self):
        self.size = 160 # LOL
        return self.size

    def save(self):
        buffer = bytearray(160)
        pointer = 32

        buffer[:4] = bytearray.fromhex("444e4648") # DNFH
        buffer = d.w_UInt32(buffer, 4, self.unknwn1)
        buffer = d.w_UInt32(buffer, 8, self.calculate_size())

        buffer[16:20] = bytearray(d.Encode(self.obj_id_string))
        addoff = bytearray(self.add_offset)

        buffer = d.w_UInt32(buffer, 20, self.add_offset)
        buffer[24:24+self.add_offset] = addoff
        
        for i in range(1, 9):
            line = bytearray.fromhex(HFND.olid[i]) + getattr(self, "obj_params_"+str(i), lambda: "Error?!")
            buffer[pointer:pointer + 16] = line
            pointer = pointer + 16

        return buffer
        
class BHIO(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        if self.identification != "HFND":
            print("Not a .bhio File!")
            return
        self.pointer = d.UInt32(self.data, 8)
        self.children_count = d.UInt32(self.data, 12)
        self.children = []
        self.inbetween_data = self.data[16:self.pointer]

        print("Inbtwn:"+str(self.inbetween_data.hex()))
        print("Children: "+str(self.children_count))

        for i in range(self.children_count):
            self.tmp = d.UInt32(self.data, self.pointer + 8)
            gen = gh.NDS_GenericTempContainer(self.data[self.pointer:self.pointer+self.tmp])
            self.pointer = self.pointer+self.tmp
            print("-------------- NEW OBJECT --------------")
            print("["+str(i)+"] "+gen.identification + " Size: "+str(gen.size2))
            if gen.identification == "HFND":
                self.children.append( HFND(gen.data) )

    def calculate_size(self):
        self.size = 16 + len(self.inbetween_data) + len(self.children) * 160
        return self.size

    def calcHeaderSize(self):
        return 16 + len(self.inbetween_data)

    def save(self):
        hs = self.calcHeaderSize()
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("444e4648") # DNFH
        buffer = d.w_UInt32(buffer, 4, self.calculate_size())
        buffer = d.w_UInt32(buffer, 8, hs)
        buffer = d.w_UInt32(buffer, 12, len(self.children))
        buffer[16:] = self.inbetween_data

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

################################################################
## .bhio  (DNFH) File END
###############################################################

def fromFile(path):
    return BHIO(d.ReadFile(path))