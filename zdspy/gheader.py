


from abc import ABC, abstractmethod
from . import dataio as d

class ZDS_GenericElementHeaderIDO(ABC):
    def __init__(self, data):
        self.data = data
        self.identification = d.Decode(data[:4])
        # print("Loading Element: " + self.identification)
        self.init()

    @abstractmethod
    def init(self):
        pass

class ZDS_GenericElementHeaderRaw(ABC):
    def __init__(self, data):
        self.data = data
        self.identification = d.Decode(data[:4])
        # print("Loading Element: " + self.identification)
        self.size = d.UInt32(data, 4)
        self.init()

    @abstractmethod
    def init(self):
        pass

class ZDS_GenericElementHeaderRawNR(ABC):
    def __init__(self, data):
        self.data = data
        self.identification = data[:4].decode()
        # print("Loading Element: " + self.identification)
        self.size = d.UInt32(data, 4)
        self.init()

    @abstractmethod
    def init(self):
        pass

class ZDS_GenericElementHeader(ABC):
    def __init__(self, data):
        self.data = data
        self.identification = d.Decode(data[:4])
        # print("Loading Element: " + self.identification)
        self.size = d.UInt32(data, 4)
        self.children_count = d.UInt16(data, 8)
        self.children = []
        self.padding = d.UInt16(data, 10)
        self.pointer = 12
        if not self.padding == 65535:
            print("Padding with NON 0xFFFF Value: "+str(self.padding))
        self.init()

    @abstractmethod
    def init(self):
        pass

class ZDS_GenericFileHeader(ABC): # TODO
    def __init__(self, data):
        self.data = data
        self.identification = data[:4].decode()
        # print("Loading Element: " + self.identification)
        self.bom = str(data[4:6].hex())
        if self.bom == "feff": # FEFF
            print("Big Endian")
        elif self.bom == "fffe": # FFFE
            print("Little Endian")
        else:
            print("BOM is wrong!")
        self.unknwn1 = d.UInt16(data, 6)
        print("Unknwn1 (0x06): "+str(self.unknwn1))
        self.children = []
        self.size = d.UInt32(data, 8)

        self.header_size = d.UInt16(data, 12)
        if not (self.header_size == 16):
            print("Header Size not 16 !!!")

        self.children_count = d.UInt16(data, 14)

        self.pointer = 16
        self.init()

    @abstractmethod
    def init(self):
        pass


# Programm Related:
class NDS_GenericTempContainer(ZDS_GenericElementHeaderRaw):
    def init(self):
        self.size2 = d.UInt32(self.data, 8) # Might be unused in some cases.

class NDS_GenericTempContainerNR(ZDS_GenericElementHeaderRawNR):
    def init(self):
        self.size2 = d.UInt32(self.data, 8) # Might be unused in some cases.
