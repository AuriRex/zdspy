
from . import dataio as d
import sys

class MAP2D_PAL_CE:

    def __init__(self, data):
        self.data = data

        # Little Endian
        self.bitstring = (bin(int(str(self.data.hex()[2:]), base=16))[2:].zfill(8) +""+ bin(int(str(self.data.hex()[:2]), base=16))[2:].zfill(8))

        # http://www.romhacking.net/documents/%5B469%5Dnds_formats.htm#Graphics
        # Format ^ (BGR555)
        # X = Nothing
        # B = Blue bits
        # G = Green Bits
        # R = Red bits
        # XBBBBBGG GGGRRRRR

        self.x = self.bitstring[0]

        self.blue = self.bitstring[1:6]

        self.green = self.bitstring[6:11]

        self.red = self.bitstring[11:16]

    def get_rgb(self):
        return (int((int(self.red, base=2) / 31) * 255), int((int(self.green, base=2) / 31) * 255), int((int(self.blue, base=2) / 31) * 255))

    def __str__(self):
        return "<M2D_Pc Red="+self.red + " Green="+self.green + " Blue="+self.blue+" >"

class MAP2D_PAL: # .nbfp

    def __init__(self, data):
        self.data = data

        self.size = len(self.data)

        self.palette = []

        offset = 0
        for i in range(int(self.size/2)):
            np = MAP2D_PAL_CE(self.data[offset:offset+2])
            self.palette.append(np)
            offset = offset + 2

    def bitmap(self):

        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Module \"PIL\" not installed!")
            return None

        image = Image.new('RGB', (16, 16), color = 'black')
        drawing_image = ImageDraw.Draw(image)
        x = 0
        y = 0
        for i, c in enumerate(self.palette):
            y = int(i / 16)
            x = i - int(y * 16)
            drawing_image.point((x, y), c.get_rgb())
        
        del drawing_image

        return image

    def __str__(self):
        return "<M2D_P colors="+str(int(self.size / 2))+" >"


class MAP2D_SCREEN_CE:

    def __init__(self, data):
        self.data = data

        # Little endian
        self.bitstring = (bin(int(str(self.data.hex()[2:]), base=16))[2:].zfill(8) +""+ bin(int(str(self.data.hex()[:2]), base=16))[2:].zfill(8))

        # Format:
        # Y  = palette number (always zero)
        # X0 = Flip Tile on Y axis
        # X1 = Flip Tile on X axis
        # N  = Tile number / index from .nbfc file
        # YYYYXXNNNNNNNNNN

        self.pal_num = int(self.bitstring[0:4], base=2)

        self.flip_y = bool(int(self.bitstring[4]))
        self.flip_x = bool(int(self.bitstring[5]))

        
        self.tile_num = int(self.bitstring[6:].rjust(16, '0'), base=2)

    def get_graphic(self, ts):
        # ts = tile_set
        
        try:
            tile = ts.tiles[self.tile_num]
        except IndexError:
            print("INDEX ERROR: Tile Num:",self.tile_num)
            print("HEX: 0x"+self.data.hex())
            print("BS:  "+self.bitstring)
            input("BreakPoint :> (This should not happen.)")
            tile = ts.tiles[0]
            return tile.get_tile()

        if tile.color_data == []:
            raise TypeError('Tile has no palette!')

        tile_size = tile.tile_size

        wdata = tile.get_tile()

        if self.flip_x:
            wdata = tile.flip_x(wdata, tile_size)

        if self.flip_y:
            wdata = tile.flip_y(wdata, tile_size)

        return wdata

    def __str__(self):
        return "<M2D_Sc pal_num="+str(self.pal_num) + " FlipX="+str(self.flip_x) + " FlipY="+str(self.flip_y) + " tile_num="+str(self.tile_num)+" >"

class MAP2D_SCREEN: # .nbfs

    def __init__(self, data):
        self.data = data

        self.size = len(self.data)

        self.data_size = int(self.size / 2)

        self.gfx = []

        offset = 0
        for i in range(self.data_size):
            ns = MAP2D_SCREEN_CE(self.data[offset:offset+2])
            self.gfx.append(ns)
            offset = offset + 2

    def set_tiles(self, tile_set):
        self.tile_set = tile_set

    def bitmap(self):

        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Module \"PIL\" not installed!")
            return None

        if self.tile_set == None:
            raise TypeError('No tileset set!')

        tile_size = self.tile_set.tile_size

        # Create a new Image with the NDSes screen rosolution (256x192  |  4:3)
        image = Image.new('RGB', (256, 192), color = 'black')
        drawing_image = ImageDraw.Draw(image)
        
        # TODO: Turn off debug vars
        debug = False
        debug_draw_flips = False

        for i, gfx in enumerate(self.gfx):
            offset_y = int(i / int(256 / tile_size))
            offset_x = i - (offset_y * int(256 / tile_size))
            if debug:
                print("Drawing ScreenGFX #"+str(i)+" (Offset: "+str(hex(i*2))+") x="+str(offset_x)+" y="+str(offset_y))
            tile_gfx = gfx.get_graphic(self.tile_set)
            for index, tile in enumerate(tile_gfx):
                y = int(index / tile_size + offset_y * tile_size)
                x = index - int(int(index / tile_size) * tile_size) + offset_x * tile_size
                if debug:
                    print(" - x="+str(x)+" y="+str(y)+" index="+str(index)+" i="+str(i)+" TileLength="+str(len(tile_gfx)))
                if (gfx.flip_x or gfx.flip_y) and debug_draw_flips:
                    # Debug: draw tiles with checker pattern to see which tiles have the flip_x and/or flip_y bit set
                    if gfx.flip_x and gfx.flip_y:
                        if (x + y) % 2 == 0:
                            drawing_image.point((x, y), (255,0,255))
                        else:
                            drawing_image.point((x, y), (0,255,255))
                    elif gfx.flip_x:
                        if (x + y) % 2 == 0:
                            drawing_image.point((x, y), (255,0,0))
                        else:
                            drawing_image.point((x, y), (0,0,255))
                    elif gfx.flip_y:
                        if (x + y) % 2 == 0:
                            drawing_image.point((x, y), (0,255,0))
                        else:
                            drawing_image.point((x, y), (0,0,255))
                else:
                    # Draw Tile Pixels
                    drawing_image.point((x, y), tile)
        
        del drawing_image

        return image

    def __str__(self):
        return "<M2D_S data_size=" + str(self.data_size) + ">"

class MAP2D_TILES_CE:

    def __init__(self, data, tile_size):
        self.data = data
        self.tile_size = tile_size

        # 8x8 = 1 Tile (64 Byte)

        self.color_ref = []
        self.color_data = []

        for by in self.data:
            self.color_ref.append(int(by))


    def set_palette(self, pal):
        self.color_data = []
        for cr in self.color_ref:
            self.color_data.append(pal.palette[cr].get_rgb())

    def get_tile(self):
        return self.color_data

    def flip_x(self, wdata, tile_size):
        nwdata = []
        for i in range(tile_size):
            nwdata += (wdata[tile_size*(i):tile_size*(i+1)])[::-1]
        return nwdata

    def flip_y(self, wdata, tile_size):
        nwdata = []
        for i in range(tile_size):
            n = i * -1 + tile_size
            nwdata += wdata[tile_size*(n-1):tile_size*n]
        return nwdata

    def __str__(self):
        return "<M2D_Tc "+str(self.tile_size)+"x"+str(self.tile_size)+"Tile: PalIndex="+str(self.color_ref)+">"

class MAP2D_TILES: # .nbfc

    # 8x8 Tiles - 8 Byte for one TileRow (64 Byte for one Tile)

    def __init__(self, data):
        self.data = data

        self.size = len(self.data)

        self.tile_size = 8

        self.tile_size_sqd = self.tile_size * self.tile_size

        self.num_tiles = int(self.size / self.tile_size_sqd)

        self.tiles = []

        self.pal = None

        offset = 0
        for i in range(self.num_tiles):
            nt = MAP2D_TILES_CE(self.data[offset:offset+self.tile_size_sqd], self.tile_size)
            self.tiles.append(nt)
            offset = offset + self.tile_size_sqd
    
    def bitmap(self):

        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Module \"PIL\" not installed!")
            return None

        if self.pal == None:
            raise TypeError('No palette set!')

        tile_size = self.tile_size

        image = Image.new('RGB', (tile_size, self.num_tiles), color = 'black')
        drawing_image = ImageDraw.Draw(image)

        for i, t in enumerate(self.tiles):
            for index, tile in enumerate(t.get_tile()):
                y = int(index / tile_size + tile_size * i)
                x = index - int(int(index / tile_size) * tile_size)
                drawing_image.point((x, y), tile)
        
        del drawing_image

        return image

    def set_palette(self, pal):
        self.pal = pal
        for tile in self.tiles:
            tile.set_palette(self.pal)

    def __str__(self):
        return "<M2D_T num_tiles="+str(self.num_tiles)+" >"

class MAP2D:

    def __init__(self, data):
        # self.narc = data

        try:
            import ndspy
            import ndspy.lz10
            import ndspy.narc
        except ImportError:
            ndspy = None
        
        if ndspy:
            self.narc = ndspy.narc.NARC(ndspy.lz10.decompress(data))
        else:
            print("Please install ndspy to use this feature! (https://github.com/RoadrunnerWMC/ndspy)")
            return None

        try:
            self.palette = MAP2D_PAL(self.narc.getFileByName("map2d.nbfp"))
        except ValueError:
            print("map2d.nbfp (Palette File) not found!")
            self.palette = False

        try:
            self.tiles = MAP2D_TILES(self.narc.getFileByName("map2d.nbfc"))
        except ValueError:
            print("map2d.nbfc (Tiles File) not found!")
            self.tiles = False

        try:
            self.screen = MAP2D_SCREEN(self.narc.getFileByName("map2d.nbfs"))
        except ValueError:
            print("map2d.nbfs (Screen File) not found!")
            self.screen = False

        try:
            self.tiles.set_palette(self.palette)

            self.screen.set_tiles(self.tiles)
        except AttributeError:
            pass
        # TODO: Create main class

    def save_bitmap(self, path, name, export_map2d=True, export_tiles=True, export_palette=True, path_map2d="", path_tiles="", path_palette=""):

        #import PIL
        try:
            from PIL import Image, ImageDraw
        except ImportError:
            print("Please install PIL to use this feature!")
            return None

        if export_map2d and self.screen:
            self.screen.bitmap().save(path+path_map2d+name+"_map2d.png", "PNG")

        if export_tiles and self.tiles:
            self.tiles.bitmap().save(path+path_tiles+name+"_tiles.png", "PNG")

        if export_palette and self.palette:
            self.palette.bitmap().save(path+path_palette+name+"_palette.png", "PNG")


def dump_bitmap_all(input_path, output_path):

    workdir = input_path # "../../../DS/extracted/data/Map2D/"
    outdir = output_path # "../infodump/map2d/"

    import os

    dirs = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(workdir):
        for directory in d:
            dirs.append(os.path.join(r, directory))

    for d in dirs:
        for _r, _d, f in os.walk(d):
            for file in f:
                name = os.path.basename(os.path.normpath(d))
                print(d+"/"+file)
                MAP2D(d.ReadFile(d+"/"+file)).save_bitmap(outdir, name+"_"+file[:-4], path_tiles="tiles/", path_palette="palettes/")

