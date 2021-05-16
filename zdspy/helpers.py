from . import dataio as d
import ndspy.lz10
import ndspy.narc
import os

class ZDS_PH_AREA:
    """An object that represents a single `mapXY.bin` file."""
    filename: str
    narc: ndspy.narc.NARC
    identification: str = "-1"
    file_compression_type: int = 0

    def getName(self):
        """Returns the entire original filename `mapXY.bin`"""
        return self.filename

    def getArchive(self) -> ndspy.narc.NARC:
        """Returns the NARC archive (`ndspy.narc.NARC`)"""
        return self.narc

    def getID(self) -> str:
        """The double digits (XY part) in `mapXY.bin` as a string"""
        return self.identification

    def __init__(self, filename: str, data: bytearray, file_compression_type: int):
        self.filename = filename
        if "map" in filename:
            self.identification = str(filename[3:4]) + str(filename[4:5])
        else:
            self.identification = "-1"
        
        self.file_compression_type = file_compression_type
        if file_compression_type == 10:
            self.narc = ndspy.narc.NARC(ndspy.lz10.decompress(data))
        else:
            self.narc = ndspy.narc.NARC(data)

    def save(self) -> bytearray:
        # LZ10 compression
        if self.file_compression_type == 10:
            return ndspy.lz10.compress(self.narc.save())
        
        # No compression
        return self.narc.save()

class ZDS_PH_ILB: # Island Binary
    """island.ilb - todo"""
    data: bytearray

    def __init__(self, data: bytearray):
        self.data = data
    
    def save(self):
        return self.data

class ZDS_PH_MAP:
    """An object representing a single folder (and all its files) in the games `/Map/` directory."""
    name: str
    children: list = []
    map_count: int = 1
    course_bin: ZDS_PH_AREA
    is_island: bool = False
    island_ilb: ZDS_PH_ILB

    def getName(self):
        """The name of the folder in the `/Map/` directory, aka the Map name."""
        return self.name

    def __init__(self, name: str, nummaps: int, coursebin: ZDS_PH_AREA, children: list, island_ilb: ZDS_PH_ILB = None):
        self.name = name
        self.map_count = nummaps
        self.course_bin = coursebin

        self.children = children
        if not (island_ilb == None):
            self.is_island = True
        else:
            self.is_island = False
        self.island_ilb = island_ilb

    def __init__(self, folderpath: str, debug_print: bool=True):
        count = -1
        if debug_print:
            print(folderpath)
        self.name = os.path.basename(os.path.normpath(folderpath))
        self.children = []
        for r, di, f in os.walk(folderpath):
            for file in f:
                if debug_print:
                    print(" - "+file)
                count = count + 1
                if file == "course.bin":
                    self.course_bin = ZDS_PH_AREA( file, d.ReadFile(os.path.join(r, file)) , 10)
                elif file == "island.ilb":
                    # print("Island Binary!")
                    count = count - 1
                    self.island_ilb = ZDS_PH_ILB( d.ReadFile(os.path.join(r, file)) )
                elif "map" in file:
                    self.children.append( ZDS_PH_AREA( file, d.ReadFile( os.path.join(r, file) ) , 10) )

    def saveToFolder(self, save_path: str):
        """Saves `course.bin`, all map files `mapXY.bin` and if it's an island also its `island.ilb` file to disk into `save_path`."""

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
        child: ZDS_PH_AREA
        for child in self.children:
            with open(save_path + self.name + "/" + child.filename, 'w+b') as f:
                f.write(child.save())

    def addMap(self, narcdata):
        pass