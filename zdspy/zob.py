from . import dataio as d
from . import gheader as gh

class ZOB_NPC(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        self.unknown_1 = d.UInt16(self.data, 8)
        self.unknown_2 = d.UInt16(self.data, 10)
        self.children_count = d.UInt16(self.data, 12)
        self.children = []
        self.padding = d.UInt16(self.data, 14)

        print("Unknown_1:",self.unknown_1)
        print("Unknown_2:",self.unknown_2)

        self.pointer = 16
        for i in range(self.children_count):
            self.children.append( ZOB_NPC_CE(self.data[self.pointer:self.pointer+4]) )
            print(i,"-",self.children[len(self.children)-1])
            self.pointer = self.pointer + 4

class ZOB_NPC_CE:
    def __init__(self, data):
        self.data = data

        self.npc = d.Decode(self.data)

    def __str__(self):
        return str(self.npc)

class ZOB(gh.ZDS_GenericElementHeaderRaw):

    def init(self):
        self.unknown_1 = d.UInt16(self.data, 8)
        self.unknown_2 = d.UInt16(self.data, 10)
        self.children_count = d.UInt16(self.data, 12)
        self.children = []
        self.padding = d.UInt16(self.data, 14)

        print("Unknown_1:",self.unknown_1)
        print("Unknown_2:",self.unknown_2)

        self.pointer = 16
        for i in range(self.children_count):
            self.children.append( ZOB_CE(self.data[self.pointer:self.pointer+4]) )
            print(i,"-",self.children[len(self.children)-1])
            self.pointer = self.pointer + 4

class ZOB_CE:
    def __init__(self, data):
        self.data = data

        # temp code
        self._16_0 = d.UInt16(self.data, 0)
        self._s16_0 = d.SInt16(self.data, 0)

        self._16_2 = d.UInt16(self.data, 2)
        self._s16_2 = d.SInt16(self.data, 2)

        self._8_0 = d.UInt16(self.data, 0)
        self._s8_0 = d.SInt16(self.data, 0)

        self._8_1 = d.UInt8(self.data, 1)
        self._s8_1 = d.SInt8(self.data, 1)

    def __str__(self):
        return str(self._16_0) + " - " + str(self._s16_2)


