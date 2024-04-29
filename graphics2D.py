from tkinter import *
from math import *

root = Tk()
myCanvas = Canvas(root, width=800, height=800, borderwidth=0, highlightthickness=0)
myCanvas.pack()
#text   canvasName.create_text(x+pad, y+pad, anchor=W, font="Purisa",text=name)
#circle canvasName.create_oval(x0, y0, x1, y1, fill="black")
#line   canvasName.create_line(p1[0]+ w/2, p1[1]+ h/2, p2[0]+ w/2, p2[1]+ h/2)
global center
global u
center = [myCanvas.winfo_reqheight()/2, myCanvas.winfo_reqwidth()/2]
u = 100

def planoCartesiano(uni):
    w = myCanvas.winfo_reqwidth()
    h = myCanvas.winfo_reqheight()
    t = 5
    for i in range(w//uni):
        myCanvas.create_line(i*uni, 0, i*uni ,h, fill = rgb(200,200,200))
        myCanvas.create_line(i*uni, center[1]-t,i*uni ,center[1]+t )
    for i in range(h//uni):
        myCanvas.create_line(0, i*uni, w, i*uni, fill = rgb(200,200,200))
        myCanvas.create_line(center[0]-t, i*uni, center[0]+t, i*uni)
    myCanvas.create_line(w/2, 0, w/2, h)
    myCanvas.create_line(0, h/2, w, h/2)        

def rgb(r,g,b):
    """r,g,b are intensities of red, green, and blue in range(256)
    Returns color specifier string for the resulting color"""
    return "#%02x%02x%02x" % (r,g,b)

class dot:
   def __init__(self, x, y):
       self.x = float(x)
       self.y = float(y)
   def draw(self, canvasName = myCanvas, color='black', r = 3):
       x = self.x + center[0]
       y = -self.y + center[1]
       print(x,y)
       myCanvas.create_oval(x - r, y - r, x + r, y + r, fill=color)
   def position(self):
       return self.x, self.y
   def x(self): return self.x
   def y(self): return self.y

class origin:
    def __init__(self):
        return None
    def dot(self):
        return dot(0,0)
    def position(self):
        return 0.0, 0.0
    def draw(self, color=rgb(0,0,0)):
        o = dot(0,0)
        o.draw(color=color)

class vector:
    def __init__(self, a, b):
        if type(a) == type(dot(0,0)):self.a = a
        else: self.a = dot(a[0],a[1])
        if type(b) == type(dot(0,0)):self.b = b
        else: self.b = dot(b[0],b[1])
        self.x = self.b.x - self.a.x
        self.y = self.b.y - self.a.y
        self.mod = sqrt(self.x**2 + self.y**2)
    def x(self):
        return self.x
    def y(self):
        return self.y
    def mod(self):
        return self.mod
    def showVector(self):
        print('Vector: (',self.b.x,',',self.b.y,')-('
                         ,self.a.x,',',self.a.y,')=('
                         ,self.x,',',self.y,')')
    def draw(self, color=rgb(0,0,0)):
        x0 = self.b.x + center[0]
        y0 = -self.b.y + center[1]
        x1 = self.a.x + center[0]
        y1 = -self.a.y + center[1]
        myCanvas.create_line(x0, y0, x1, y1, fill = color, arrow=FIRST)
    def drawOnOrigin(self, color=rgb(0,0,0)):
        x0 = 0 + center[0]
        y0 = 0 + center[1]
        x1 = self.x + center[0]
        y1 = -self.y + center[1]
        myCanvas.create_line(x0, y0, x1, y1, fill = color, arrow=LAST)
    def drawVecAng(self, color=rgb(0,0,0)):
        x0 = -u/3 + self.a.x + center[0]
        y0 = -u/3 - self.a.y + center[1]
        x1 = u/3 + self.a.x + center[0]
        y1 = u/3 - self.a.y + center[1]
        A = dot(u,0)
        o = origin()
        vx0 = vector(o.dot(), A)
        a1 = degrees(vecOrientedAng(vx0,vector(self.a,self.b)))
        myCanvas.create_arc(x0, y0, x1, y1, extent = a1, fill = color)        
        
        
def clear():
    myCanvas.delete("all")

#recebe vetores X e Y e retorna o produto escalar
def vecEscProd(x, y):
   return x.x*y.x+x.y*y.y

#recebe vetores X e Y e retorna o ângulo entre eles
def vecAng(x, y):
    return acos( vecEscProd(x, y)/(x.mod*y.mod) )

def vecOrientedAng(x, y):
    A = dot(u,0)
    o = origin()
    vx0 = vector(o.dot(), A)
    angx = vecAng(vx0, x)
    angy = vecAng(vx0, y)
    if x.y<0: angx*=-1
    if y.y<0: angy*=-1
    return angy - angx

def drawDifAngleOnOrigin(x, y, color='black'):
    x0 = -u/2 + center[0]
    y0 = -u/2 + center[1]
    x1 = u/2 + center[0]
    y1 = u/2 + center[1]
    A = dot(u,0)
    o = origin()
    vx0 = vector(o.dot(), A)
    a1 = degrees(vecOrientedAng(vx0,x))
    a2 = degrees(vecOrientedAng(vx0,y))
    myCanvas.create_arc(x0, y0, x1, y1, extent = a2-a1, fill = color, start = a1)

def drawDifAngleAngOnVec(x, y, color='black'):
    xpos = x.a.x
    ypos = x.a.y
    x0 = -u/3 + center[0] + xpos  
    y0 = -u/3 + center[1] - ypos
    x1 = u/3 + center[0] + xpos
    y1 = u/3 + center[1] - ypos
    A = dot(u,0)
    o = origin()
    vx0 = vector(o.dot(), A)
    a1 = degrees(vecOrientedAng(vx0,x))
    a2 = degrees(vecOrientedAng(vx0,y))
    myCanvas.create_arc(x0, y0, x1, y1, extent = a2-a1, fill = color, start = a1)

class polygon:
    def __init__(self, dots):
        self.dots = list(dots)
    def draw(self, color=rgb(0,0,0)):
        coords = []
        for d in self.dots:
            coords.append(d.x + center[0])
            coords.append(-d.y + center[1])
        myCanvas.create_polygon(coords, fill = color)
    def drawAng(self, color = 'black'):
        
        for i in range(len(self.dots)):
            v1 = vector(self.dots[i],self.dots[i-1])
            try:
                v2 = vector(self.dots[i+1],self.dots[i])
            except:
                v2 = vector(self.dots[i+1  - len(self.dots)],self.dots[i])
            print(v1.x,v1.y)
            print(v2.x,v2.y)
            v1.drawOnOrigin()
            v2.drawOnOrigin()
            drawDifAngleAngOnVec(v1, v2, color = 'black')








    
