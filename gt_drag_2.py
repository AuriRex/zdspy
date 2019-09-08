# gt_drag_2.py
import random
import os
import pyglet
from pyglet.gl import *
from getinfo import ZDS_PH_MAP
from zdspy import zmb as zzmb

# label = pyglet.text.Label('Hello, world',
#                           font_name='Times New Roman',
#                           font_size=12,
#                           x=window.width//2, y=window.height//2,
#                           anchor_x='center', anchor_y='center')

tx = 0
ty = 0

frame = 0
def update_frame(x, y):
    global frame
    frame += 1


class Color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b

class Line:
    def __init__(self,x,y,ex,ey):
        self.x = x
        self.y = y
        self.ex = ex
        self.ey = ey
        self.color = None
        self.vc1 = None
        self.vc2 = None
    
    def computeTranslation(self,x,y):
        self.cx = self.x + x
        self.cy = self.y + y
        self.cex = self.ex + x
        self.cey = self.ey + y

class Quad:
    def __init__(self,x,y,sx,sy):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.color = None
    
    def computeTranslation(self,x,y):
        self.ctlx = self.x + x
        self.ctly = self.y + y

        self.ctrx = self.x + self.sx + x
        self.ctry = self.ctly

        self.cbrx = self.ctrx
        self.cbry = self.y + self.sy + y

        self.cblx = self.ctlx
        self.cbly = self.cbry

class EQuad:
    def __init__(self,x,y,sx,sy):
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.color = None
    
    @classmethod
    def fromABounds(self, ab):
        tmp = self(ab.x,ab.y,ab.w,ab.h)
        tmp.color = Color(1,0,1)
        return tmp

    def computeTranslation(self,x,y):
        self.ctlx = self.x + x
        self.ctly = self.y + y

        self.ctrx = self.x + self.sx + x
        self.ctry = self.ctly

        self.cbrx = self.ctrx
        self.cbry = self.y + self.sy + y

        self.cblx = self.ctlx
        self.cbly = self.cbry


class Label:
    def __init__(self, label):
        self.label = label
        self.x = label.x
        self.y = label.y
        self.color = None

    def computeTranslation(self,x,y):
        self.label.x = self.x + x
        self.label.y = self.y + y

    def draw(self):
        self.label.draw()

class GMap:
    def __init__(self, mapname,x,y):
        self.name = mapname
        self.levelname = mapname[:-3]
        self.x = x
        self.y = y
        self.size = len(mapname) * 10
        self.equad = EQuad(x,y, self.size, 20)
        self.fontColor = Color(1,1,1)
        self.num_warps = 0
        self.connections = {}
        self.id = 0
        self.label = pyglet.text.Label(self.name + " 0",
                          font_name='Arial',
                          font_size=12,
                          x=x, y=y)
        self.color = None
        self.lines = []

    def setPos(self,x,y):
        self.x = x
        self.y = y
        self.equad.x = x
        self.equad.y = y

    def addConnection(self, remoteLevel, remoteMap):
        try:
            if self.connections[remoteLevel] == None:
                self.connections[remoteLevel] = [remoteMap]
                # self.connections[remoteLevel].append(remoteMap)
            else:
                self.connections[remoteLevel].append(remoteMap)
        except KeyError:
            self.connections[remoteLevel] = [remoteMap] # lol

    def resLabelText(self):
        self.label.text = self.name + " " + self.num_warps

    def drawLines(self):
        for l in self.lines:
            drawLine(l, 0.25)
        self.drawConnections()

    def drawConnections(self):
        for rLvl, rMaps in self.connections.items():
            for m in rMaps:
                if m.levelname == self.levelname:
                    # print("Neat:",self.name)
                    l = Line(self.x+1+self.id*5,self.y,m.x+1+self.id*5,m.y)
                    if self.id % 2 == 0:
                        l.color = Color(0.5,0.9,0.9)
                    else:
                        l.color = Color(0.9,0.9,0.5)
                    drawLine(l, 0.25)
                else:
                    twoway = False
                    # try:
                    for rl, rmp in m.connections.items():
                        # print("nya", rLvl.name)
                        if rl.name == self.levelname:
                            # print("Neat: ",self.levelname, rLvl.name)
                            for mp in rmp:
                                if mp.name == self.name:
                                    print("Twoway enabled:",self.levelname,rl.name)
                                    twoway = True
                                    break
                    # except AttributeError:
                    #     pass
                    l = Line(self.x,self.y,m.x,m.y)

                    # if "isle_" in self.levelname:
                    #     l.vc1 = Color(0.2,1,0.2)
                    # if "sea" in self.levelname:
                    #     l.vc1 = Color(0.2,0.2,1)

                    # if "isle_" in rLvl.name:
                    #     l.vc2 = Color(0.2,1,0.2)
                    # if "sea" in rLvl.name:
                    #     l.vc2 = Color(0.2,0.2,1)
                    if not twoway:
                        l.vc1 = Color(0.2,1,0.2)
                        l.vc2 = Color(1,0.2,0.2)
                    else:
                        l.color = Color(0.2,0.2,1)

                    drawLine(l, 0.25)

    def drawEQuad(self):
        drawEQuad(self.equad, 0.25)

    def computeTranslation(self,x,y):
        self.label.x = self.x + 3 + x
        self.label.y = self.y + 3 + y
    
    def drawLabel(self):
        glColor3f(self.fontColor.r, self.fontColor.g, self.fontColor.b)
        self.label.draw()

class ABounds:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def insideX(self, x, w):
        return (self.x > x > self.x + self.w) or (self.x > x + w > self.x + self.w) or (self.x < x < self.x + self.w) or (self.x < x + w < self.x + self.w)

    def insideY(self, y, h):
        return (self.y > y > self.y + self.h) or (self.y > y + h > self.y + self.h) or (self.y < y < self.y + self.h) or (self.y < y + h < self.y + self.h)

    def isObstructing(self, ab):
        return self.insideX(ab.x, ab.w) and self.insideY(ab.y,ab.h)

class GLevel:
    def __init__(self, levelname,x,y):
        self.name = levelname
        self.x = x
        self.y = y
        self.maps = []
        self.color = None
        self.size = 30
        self.height = 50
        self.quad = Quad(x,y,20,50)
        self.quad.color = Color(0.1,0.1,0.1)
        self._col = Color(0.1,0.1,0.1)
        self.selected = False
        self.label = pyglet.text.Label(self.name,
                          font_name='Arial',
                          font_size=12,
                          x=x + 30, y=y)
    
    def setX(self, x):
        oldx = self.x
        self.x = x
        self.quad.x = x
        for i, m in enumerate(self.maps):
            m.setPos(self.x, m.y + i * 30)

    def setY(self, y):
        oldy = self.y
        self.y = y
        self.quad.y = y
        for i, m in enumerate(self.maps):
            m.setPos(m.x, self.y + i * 30)

    def computeSize(self):
        biggest = 0
        for m in self.maps:
            if m.size > biggest:
                biggest = m.size
        self.size = biggest
        self.quad.sx = self.size
        self.quad.sy = len(self.maps) * 30 + 20
        self.height = self.quad.sy

    def hasMap(self, mname):
        for m in self.maps:
            if m.name == mname:
                return True
        return False

    def getMap(self, mname):
        for m in self.maps:
            if m.name == mname:
                return m
        return None

    def select(self, bo, col, force=False):
        if bo:
            #select
            if self.selected == False or force:
                self._col = self.quad.color
                self.quad.color = col
                self.selected = True
        else:
            if self.selected or force:
                self.quad.color = self._col
                self.selected = False
            #deselect

    def addMap(self, mapname):
        nmap = GMap(mapname,self.x,self.y + len(self.maps)*30)
        nmap.id = len(self.maps)
        self.maps.append(nmap)
        self.computeSize()

    def drawLines(self):
        for m in self.maps:
            m.drawLines()

    def drawMaps(self):
        for m in self.maps:
            m.drawEQuad()

    def drawLabels(self):
        for m in self.maps:
            m.drawLabel()
        
        self.label.draw()

    def getAreaBounds(self):
        return ABounds(self.x-5, self.y-5, self.size + 10, self.height + 10)

    def computeTranslation(self,x,y):
        self.cx = self.x + x
        self.cy = self.y + y
        self.label.x = self.cx + 3
        self.label.y = self.y + len(self.maps)*30 + 5 + y
        for m in self.maps:
            m.computeTranslation(x,y)

    def drawQuad(self):
        drawQuad(self.quad, -0.25)



lines = []
quads = []
equads = []
labels = []

mapl = []

# mapl.append(GMap("TestLevel",0,0))

lvl = GLevel("dngn_main",100, 100)
lvl.addMap("dngn_main_00")
lvl.addMap("dngn_main_01")
lvl.addMap("dngn_main_02")
lvl.addMap("dngn_main_03")

# lvl2 = GLevel("dngn_flame",100, 100)
# lvl2.addMap("dngn_flame_00")

# lvl3 = GLevel("isle_main",100, 100)
# lvl3.addMap("isle_main_00")
# lvl3.addMap("isle_main_01")
# lvl3.addMap("isle_main_02")
# lvl3.addMap("isle_main_03")

# lvl4 = GLevel("dngn_ice",100, 100)
# lvl4.addMap("dngn_ice_00")

# lvl5 = GLevel("isle_wisdom",100, 100)
# lvl5.addMap("isle_wisdom_00")

# lvl6 = GLevel("isle_flame",100, 100)
# lvl6.addMap("isle_flame_00")

left = 1
right = 1
up = 1
down = 1

levellist = []

def levelExists(lname):
    for lvl in levellist:
        if lvl.name == lname:
            return lvl
    return None

random.seed(406)

direction = 0
def addLevel(glevel):
    # 0 1 2 3
    global left,right,up,down,levellist,direction

    if "sea" in glevel.name:
        glevel.quad.color = Color(0,0,0.2)
    elif "isle_" in glevel.name:
        glevel.quad.color = Color(0.1,0.2,0.1)
    elif "battle" in glevel.name:
        glevel.quad.color = Color(0.02,0.02,0.02)
    elif "ship" in glevel.name:
        glevel.quad.color = Color(0.2,0.2,0)
    elif "boss" in glevel.name:
        glevel.quad.color = Color(0.2,0,0)
    elif "demo" in glevel.name:
        glevel.quad.color = Color(0.15,0.3,0.3)

    again = True
    
    while again:
        again = False
        for lvl in levellist:
            # direction = random.randint(0,4)
            if lvl.getAreaBounds().isObstructing(ABounds(glevel.x, glevel.y, 100, 100)):
                print(lvl.name, "obstructing",glevel.name, direction)
                if direction == 0:
                    #left
                    glevel.setX(glevel.x - 200 * left)
                    glevel.setY(glevel.y + 10 * left * left / 2)
                    left += 1
                    direction += 1
                elif direction == 1:
                    #Right
                    glevel.setX(glevel.x + 200 * right)
                    glevel.setY(glevel.y + 10 * right * right / 2)
                    right += 1
                    direction = 0 # += 1
                elif direction == 2:
                    #Up
                    glevel.setY(glevel.y + 200 * up)
                    up += 1
                    direction += 1
                elif direction == 3:
                    #down
                    glevel.setY(glevel.y - 200 * down)
                    down += 1
                    direction = 0
                again = True
                break

    levellist.append(glevel)

def getLevelByName(name):
    global levellist
    for lvl in levellist:
        if lvl.name == name:
            return lvl
    return None

##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################

# """
# workdir = "./extracted/data/Map/"

workdir = "../../DS/randomize/data/Map/"

enableBanlist = True
banlist = ["battle00","battle01","battle02","battle03","battle04","battle05","battle06","battle07","battle08","battle09","battle10","battle11","player_dngn","demo_op","demo_chase","demo_end","demo_title","isle_first"]

banlist.append("isle_ice")

dirs = []
# r=root, d=directories, f = files
for r, d, f in os.walk(workdir):
    for directory in d:
        dirs.append(os.path.join(r, directory))


mapl = []

print("Loading maps...")

for d in dirs:
    mapl.append( ZDS_PH_MAP( d, p=False ) )

zmbl = {}

warpcountl = {}
warpl = {}

# Add Maps based on Warps - not all Maps have Warps so not all are visualized!

for mp in mapl:
    mp_name = mp.getName()
    print(mp_name)
    for c in mp.children:
        iden = c.getID()
        filename = "zmb/" + mp_name + "_" + iden + ".zmb"
        print(filename)
        zmb = zzmb.ZMB( c.getData().getFileByName(filename) )
        zmbl[filename] = zmb
        warph = zmb.get_child("WARP")
        if not (warph == None):
            warpcountl[filename] = len(warph.children)
            for i, wrp in enumerate(warph.children):
                print(wrp)
                warpl[filename+str(i)] = wrp



for m, w in warpl.items():
    # if int(m.split(".zmb")[1]) == 0:
    mapname = m.split(".zmb")[0][4:]
    levelname = mapname[:-3]
    lvl = levelExists(levelname)
    if not (lvl == None):
        if not lvl.hasMap(str(mapname)):
            lvl.addMap(str(mapname))
    else:
        lvl = GLevel(str(levelname),100,100)
        lvl.addMap(str(mapname))
        addLevel(lvl)
        
    print()
    print(levelname + ": " + mapname)
    print(m.split(".zmb")[1] + ": " + m.split(".zmb")[0] + ": " + str(w))

for m, w in warpl.items():
    # mapid = m.split(".zmb")[1]
    rlvl = None
    rmap = None
    # print("Test:",w.cleanDestination() + "_" + f'{w.map_id:02}')
    for lvl in levellist:
        # find remote map
        for ma in lvl.maps:
            
            if ma.name == w.cleanDestination() + "_" + f'{w.map_id:02}':
                rlvl = lvl
                rmap = ma
                break
    mapname = m.split(".zmb")[0][4:]
    levelname = mapname[:-3]
    lvl = getLevelByName(levelname)
    if not (lvl == None):
        mapobj = lvl.getMap(mapname)
        if not (mapobj == None):
            if not (rlvl == None) and not (rmap == None):
                mapobj.addConnection(rlvl, rmap)
                rlvl = None
                rmap = None


# """

##########################################################################################################################################################
##########################################################################################################################################################
##########################################################################################################################################################




# addLevel(lvl)
# addLevel(lvl2)
# addLevel(lvl3)
# addLevel(lvl4)
# addLevel(lvl5)
# addLevel(lvl6)


# lines.append(Line(100,100,200,200))
# labels.append(Label(label))

# qua = Quad(300,300,100,-200)
# qua.color = Color(0.1,0,0.25)
# quads.append(qua)

# eq = EQuad(300,340,100,20)
# eq.color = Color(0.4,0,1)
# equads.append(eq)

# for lvl in levellist:
#     equads.append(EQuad.fromABounds(lvl.getAreaBounds(tx,ty)))

window = pyglet.window.Window(resizable=True)

dbga = [None,None,None]

sticky = None
selected = None

qz = -0.25

def touchingLevel(lvl,x,y):
    global tx,ty
    return lvl.getAreaBounds().isObstructing(ABounds(x,y,5,5))

def move(x, y, dx, dy):
    global tx,ty, dbga, sticky
    x = x - tx
    y = y - ty
    # print(x,y)
    if not (sticky == None):
        ox = sticky.x - x
        oy = sticky.y - y
        sticky.setX(x + ox + dx)
        sticky.setY(y + oy + dy)
    else:
        for lvl in levellist:
            # lvl.computeTranslation(tx,ty)
            if touchingLevel(lvl,x,y):
                # dbga[0] = EQuad.fromABounds(ABounds(x,y,5,5))
                ox = lvl.x - x
                oy = lvl.y - y
                # dbga[1] = EQuad.fromABounds(ABounds(x+ox,y+oy,5,5))
                # dbga[2] = EQuad.fromABounds(lvl.getAreaBounds())
                # print(x,y," | O:",ox,oy," | FC:",x + ox + dx,y + oy + dy, " | ", lvl.name)
                lvl.setX(x + ox + dx)
                lvl.setY(y + oy + dy)
                sticky = lvl
                break



def drawLine(line, z):
    line.computeTranslation(tx,ty)
    if not (line.color == None):
        glColor3f(line.color.r, line.color.g, line.color.b)
    else:
        glColor3f(1.0, 1.0, 1.0)
    if not (line.vc1 == None):
        glColor3f(line.vc1.r, line.vc1.g, line.vc1.b)
    glVertex3f(line.cx,line.cy, z)
    if not (line.vc2 == None):
        glColor3f(line.vc2.r, line.vc2.g, line.vc2.b)
    glVertex3f(line.cex,line.cey, z)

def drawLineRaw(x,y,ex,ey,z):
    glVertex3f(x,y, z)
    glVertex3f(ex,ey, z)

def drawQuad(quad, qz):
    global tx,ty
    if not (quad.color == None):
        glColor3f(quad.color.r, quad.color.g, quad.color.b)
    else:
        glColor3f(1.0, 1.0, 1.0)
    quad.computeTranslation(tx,ty)
    glVertex3f(quad.ctlx,quad.ctly, qz) # Top Left
    glVertex3f(quad.ctrx,quad.ctry, qz) # Top Right
    glVertex3f(quad.cbrx,quad.cbry, qz) # Bottom Right
    glVertex3f(quad.cblx,quad.cbly, qz) # Bottom Left

def drawEQuad(equad, eqz):
    global tx,ty
    if not (equad.color == None):
        glColor3f(equad.color.r, equad.color.g, equad.color.b)
    else:
        glColor3f(1.0, 1.0, 1.0)
    equad.computeTranslation(tx,ty)
    glVertex3f(equad.ctlx,equad.ctly, eqz) # Top Left
    glVertex3f(equad.ctrx,equad.ctry, eqz) # Top Right

    glVertex3f(equad.ctrx,equad.ctry, eqz) # Top Right
    glVertex3f(equad.cbrx,equad.cbry, eqz) # Bottom Right

    glVertex3f(equad.cbrx,equad.cbry, eqz) # Bottom Right
    glVertex3f(equad.cblx,equad.cbly, eqz) # Bottom Left

    glVertex3f(equad.cblx,equad.cbly, eqz) # Bottom Left
    glVertex3f(equad.ctlx,equad.ctly, eqz) # Top Left

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global tx, ty, sticky
    if buttons in [2,4,6]:
        if buttons == 6: # mouse 2 + middle mouse button together
            dx += dx
            dy += dy
        tx += dx
        ty += dy
    if buttons == 1 or not (sticky == None):
        move(x,y,dx,dy)

@window.event
def on_mouse_press(x, y, button, modifiers):
    global tx, ty, selected
    if button == 1:
        if sticky == None:
            # Set selected
            for lvl in levellist:
                if touchingLevel(lvl,x-tx,y-ty):
                    if lvl == selected:
                        return
                    # lvl found
                    lvl.select(True,Color(1,0.2,0.2))
                    if not (selected == None):
                        selected.select(False, None)
                        print("deselected",selected.name)
                    print("selected",lvl.name)
                    selected = lvl
                    return
            # if no level has been touched
            if not (selected == None):
                selected.select(False, None)
                print("deselected",selected.name)
            selected = None
            
    

@window.event
def on_mouse_release(x, y, button, modifiers):
    global sticky
    # print(button)
    if button == 1:
        sticky = None

# DEBUG Variables ###########

drawAB = True

#############################

@window.event
def on_draw():
    global tx, ty, qz, drawAB
    glClear(GL_COLOR_BUFFER_BIT)

    for lvl in levellist:
        lvl.computeTranslation(tx,ty)

    glBegin(GL_POINTS)

    glColor3f(1,1,1)
    glVertex3f(tx,ty,0)

    glEnd()

    glBegin(GL_QUADS)

    for quad in quads:
        quad.computeTranslation(tx,ty)
        if not (quad.color == None):
            glColor3f(quad.color.r, quad.color.g, quad.color.b)
        else:
            glColor3f(1.0, 1.0, 1.0)
        drawQuad(quad, qz)

    for lvl in levellist:
        lvl.drawQuad()

    glEnd()

    # create a line context
    glBegin(GL_LINES)
    # create a line, x,y,z
    for line in lines:
        drawLine(line, 0.25)

    for equad in equads:
        equad.computeTranslation(tx,ty)
        if not (equad.color == None):
            glColor3f(equad.color.r, equad.color.g, equad.color.b)
        else:
            glColor3f(1.0, 1.0, 1.0)
        drawEQuad(equad, 0.25)

    for lvl in levellist:
        lvl.drawLines()
        lvl.drawMaps()
        if drawAB:
            drawEQuad(EQuad.fromABounds(lvl.getAreaBounds()),1)
    
    for db in dbga:
        if not (db == None):
            drawEQuad(db, 1)

    # for m in mapl:
    #     m.drawEQuad()

    glEnd()

    for la in labels:
        la.computeTranslation(tx,ty)
        if not (la.color == None):
            glColor3f(la.color.r, la.color.g, la.color.b)
        else:
            glColor3f(1.0, 1.0, 1.0)
        la.draw()
    # for m in mapl:
    #     if not (m.color == None):
    #         glColor3f(m.color.r, m.color.g, m.color.b)
    #     else:
    #         glColor3f(1.0, 1.0, 1.0)
    #     m.computeTranslation(tx,ty)
    #     m.drawLabel()
    for lvl in levellist:
        lvl.drawLabels()

# pyglet.clock.schedule(update_frame, 1/10.0)
pyglet.app.run()