
from . import dataio as d
from . import gheader as gh


################################################################
## .clb  (ZCLB) File START
###############################################################

# Course List Binary

class ZCLB_CE:

    def __init__(self, data, num):
        self.data = data

        self.size = len(self.data)
        self.read_size = d.UInt32(self.data[:4],0)
        if self.size != self.read_size:
            print("[ERROR] Size doesnt match!")

        self.level_name = self.data[4:20].decode()
        self.level_name_translation = self.data[20:36]#.decode("UTF-16")

        print("Size: "+str(self.size))
        print("ZCLB_CE:"+" LevelName:"+self.level_name + " Translation?(UTF-16?):" + str(self.level_name_translation.hex()) + " HEX:"+self.data[36:].hex()+" [:"+str(num)+"]")

    def calculate_size(self):
        self.size = len(self.data)
        return self.size

    def save(self):
        buffer = bytearray(self.calculate_size())
        pointer = 0

        buffer = d.w_UInt32(buffer, 0,self.size)

        buffer = d.w_UTF8String(buffer,4,16, self.level_name)
        buffer[20:36] = self.level_name_translation

        buffer[36:] = self.data[36:]

        return buffer

class CLB(gh.ZDS_GenericElementHeaderRaw): # ZCLB():

    def init(self):
        if self.identification != "BLCZ": # Spaghetti :P
            print("Not a .clb File!")
            return
        
        self.wrongsize = d.UInt32(self.data, 4)

        self.children_count = d.UInt32(self.data, 8)
        self.children_count_2 = d.UInt32(self.data, 12)

        self.children = []

        self.pointer = 16

        for i in range(self.children_count):
            print("-------------- NEW ELEMENT --------------")
            self.child_size = d.UInt32(self.data, self.pointer)
            self.children.append( ZCLB_CE(self.data[self.pointer:self.pointer+self.child_size], i) )
            self.pointer = self.pointer + self.child_size

    def calcHeaderSize(self):
        return 16

    def calculate_size(self):
        return self.wrongsize # Investigate!

    def save(self):
        hs = self.calcHeaderSize()
        buffer = bytearray(hs)
        buffer[:4] = bytearray.fromhex("5a434c42") # ZCLB
        buffer = d.w_UInt32(buffer, 4, self.calculate_size()) # Wrong Size
        buffer = d.w_UInt32(buffer, 8, len(self.children)) # Children Count #1
        buffer = d.w_UInt32(buffer, 12, len(self.children)) # Children Count #2

        for child in self.children:
            buffer = buffer + child.save()

        return buffer

################################################################
## .clb  (ZCLB) File END
###############################################################

def fromFile(path):
    return CLB(d.ReadFile(path))