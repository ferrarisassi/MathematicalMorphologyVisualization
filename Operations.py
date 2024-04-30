import cv2
import numpy as np
import random
from graphics2D import *

u = 50
planoCartesiano(u)

def DesenhaImagem(imagem):
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        t = str(cor)
        
        A = dot(x*u+u/2, y*u+u/2)
        B = dot(x*u-u/2, y*u+u/2)
        C = dot(x*u-u/2, y*u-u/2)
        D = dot(x*u+u/2, y*u-u/2)
        P = polygon([A,B,C,D])
        P.draw(color = rgb(cor,cor,cor))
        
        if(u>15): myCanvas.create_text(x*u+center[0], -y*u+ center[1], text = t, fill=rgb(150,0,0))

def GetIndexFromPointInImage(x,y,image):
    a = 0
    for i in image:
        if(x==i[0] and y==i[1]):
            return a
        else:
            a+=1
    return -1

def Expansao(imagem, forma = 'quadrado'):
    novaImagem = []
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        if(forma == "quadrado"):
            pontosAdjacentes = [[x+1, y+1],
                                [x+1, y+0],
                                [x+1, y-1],
                                [x+0, y+1],
                                [x+0, y-1],
                                [x-1, y+1],
                                [x-1, y+0],
                                [x-1, y-1]]
        elif(forma == "x"):
            pontosAdjacentes = [[x+1, y+1],
                                [x+1, y-1],
                                [x-1, y+1],
                                [x-1, y-1]]
        elif(forma == "+"):
            pontosAdjacentes = [[x+1, y+0],
                                [x+0, y+1],
                                [x+0, y-1],
                                [x-1, y+0]]
        for xl,yl in pontosAdjacentes:
            if(GetIndexFromPointInImage(xl,yl,imagem)==-1):
                index = GetIndexFromPointInImage(xl,yl,novaImagem)
                if(index!=-1):
                    novaImagem[index][2]=(novaImagem[index][2]+cor)//2
                else:
                    novaImagem.append([xl,yl,cor])
    return novaImagem+imagem
                
def Encolhimento(imagem, limiar = 255, forma = 'quadrado'):
    novaImagem = []
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        if(forma == "quadrado"):
            pontosAdjacentes = [[x+1, y+1],
                                [x+1, y+0],
                                [x+1, y-1],
                                [x+0, y+1],
                                [x+0, y-1],
                                [x-1, y+1],
                                [x-1, y+0],
                                [x-1, y-1]]
        elif(forma == "x"):
            pontosAdjacentes = [[x+1, y+1],
                                [x+1, y-1],
                                [x-1, y+1],
                                [x-1, y-1]]
        elif(forma == "+"):
            pontosAdjacentes = [[x+1, y+0],
                                [x+0, y+1],
                                [x+0, y-1],
                                [x-1, y+0]]
        soma = 0
        for xl,yl in pontosAdjacentes:
            index = GetIndexFromPointInImage(xl,yl,imagem)
            if(index!=-1):
                if(imagem[index][2]<limiar):
                    soma+=1
        if(soma == len(pontosAdjacentes)):
            novaImagem.append([x,y,cor])
    return novaImagem

def Dilatacao(imagem, EE):
    novaImagem = []
    for pe in EE:
        for pi in imagem:
            nx = pi[0]+pe[0]
            ny = pi[1]+pe[1]
            cor = pi[2]+pe[2]
            if cor>255: cor = 255
            elif cor<0: cor = 0
            index = GetIndexFromPointInImage(nx,ny,novaImagem)
            if(index!=-1):
                corAntes = novaImagem[index][2]
                if(cor>corAntes): novaImagem[index][2] = cor
            else:
                novaImagem.append([nx,ny,cor])
    return novaImagem
        
def Erosao(imagem, EE, cinza = True):
    novaImagem = []
    cadaImagem = []
    a = 0
    for pe in EE:
        cadaImagem.append([])
        for pi in imagem:
            nx = pi[0]+pe[0]
            ny = pi[1]+pe[1]
            cor = pi[2]-pe[2]
            if cor>255: cor = 255
            elif cor<0: cor = 0
            index = GetIndexFromPointInImage(nx,ny,novaImagem) 
            if(index!=-1):
                corAntes = novaImagem[index][2]
                if(cor<corAntes): novaImagem[index][2] = cor
            else:
                cadaImagem[a].append([nx,ny,cor])
        a+=1
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        soma = 0
        for img in cadaImagem:
            index = GetIndexFromPointInImage(x,y,img)
            if(index!=-1):
                novaCor = img[index][2]
                if(novaCor<cor): cor = novaCor
                soma+=1
        if(soma == len(cadaImagem)):
            if(cinza):
                if(cor!=0):novaImagem.append([x,y,cor])
            else:
                novaImagem.append([x,y,cor])
    return novaImagem

def E(imagem1, imagem2):
    novaImagem = []
    for i in imagem1:
        x = i[0]
        y = i[1]
        cor = i[2]
        index1 = GetIndexFromPointInImage(x,y,imagem1)
        index2 = GetIndexFromPointInImage(x,y,imagem2)
        if(index1!=-1 and index2!=-1):
            cor = (imagem1[index1][2]+imagem2[index2][2])//2
            novaImagem.append([x,y,cor])
    return novaImagem

def OU(imagem1, imagem2):
    novaImagem = imagem2
    for i in imagem1:
        x = i[0]
        y = i[1]
        cor = i[2]
        index1 = GetIndexFromPointInImage(x,y,imagem1)
        index2 = GetIndexFromPointInImage(x,y,imagem2)
        if(index1!=-1):
            if(index2!=-1):
                cor = (imagem1[index1][2]+imagem2[index2][2])//2
                novaImagem.append([x,y,cor])
            else:
                cor = imagem1[index1][2]
                novaImagem.append([x,y,cor])
        elif(index2!=-1):
            cor = imagem1[index2][2]
            novaImagem.append([x,y,cor])
    return novaImagem

def Abertura(imagem, EE):
    novaImagem = Erosao(imagem,EE)
    novaImagem = Dilatacao(imagem,EE)
    return novaImagem

def Fechamento(imagem, EE):
    novaImagem = Dilatacao(imagem,EE)
    novaImagem = Erosao(imagem,EE)
    return novaImagem

def MenosBinario(imagem1, imagem2):
    novaImagem = []
    for i in imagem1:
        x = i[0]
        y = i[1]
        cor = i[2]
        index1 = GetIndexFromPointInImage(x,y,imagem1)
        index2 = GetIndexFromPointInImage(x,y,imagem2)
        if(index2==-1):
            novaImagem.append([x,y,cor])
    return novaImagem

def Menos(imagem1, imagem2):
    novaImagem = []
    for i in imagem1:
        x = i[0]
        y = i[1]
        index1 = GetIndexFromPointInImage(x,y,imagem1)
        index2 = GetIndexFromPointInImage(x,y,imagem2)
        cor = (imagem1[index1][2]-imagem2[index2][2])
        if(cor>0):
            novaImagem.append([x,y,cor])
    return novaImagem

def Translacao(imagem, xt, yt):
    novaImagem = []
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        novaImagem.append([x+xt,y+yt,cor])
    return novaImagem

def Conj2Img(imagem):
    h = 60
    w = 60
    newImage = np.ones((h,w,3), np.uint8)*255
    for i in imagem:
        x = i[0]
        y = i[1]
        cor = i[2]
        newImage[(h//2)+y][(w//2)+x] = [cor,cor,cor]
    cv2.imwrite("imagemNova.png",newImage)

def Img2Conj(imagem):
    imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) 
    h,w = imagem.shape
    newImage = []
    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            cor = imagem[i][j]
            if cor>140: newImage.append([-(w//2)+j,(h//2)-i,imagem[i][j]])
    return newImage



i1 = [[1,-1,114],[2,-1,128],[3,-1,101],[2,-2,74]]
i2 = [[1,-1,0],[2,-1,0],[3,-1,0],[2,-2,0]]
i3 = [[1,0,0],[1,-1,0],[1,-2,0],[1,-3,0],[2,-3,0],[3,-3,0]]
i4 = [[2,-1,3],[3,-1,40],[1,-4,30],[3,-4,55],[1,-8,120]]
i5 = [[3,0,66],[2,-1,3],[3,-1,40],[4,-1,7],[3,-2,150],[1,-4,30],[3,-4,55],[1,-7,70],[0,-8,95],[1,-8,120],[2,-8,12],[1,-9,40]]
i6 = [[3,0,66],[2,-1,3],[3,-1,40],[4,-1,7],[3,-2,150]]
EE = [[0,0,0],[1,0,0]]
EE2 = [[1,0,0],[0,-1,0],[0,0,0],[-1,0,0],[0,1,0]]
EE3 = [[0,0,0],[0,-1,0],[1,-1,0]]
imagem4 = []
for i in range(40):
    for j in range(40):
        imagem4.append([i-20,j-20,random.randint(0,255)])
EE4 = []
for i in range(10):
    for j in range(40):
        EE4.append([i-5,j-20,0])

img = OU(i2,i3)
imagemEro = Erosao(img,EE3,False)
DesenhaImagem(imagemEro)

#ima = Img2Conj(cv2.imread("mama.jpg"))
#DesenhaImagem(ima)

#imagemExp = Expansao(imagem4)
#DesenhaImagem(imagemExp)

#imagemEnc = Encolhimento(ima)
#DesenhaImagem(imagemEnc)

#imagemDil = Dilatacao(imagem4,EE2)
#DesenhaImagem(Menos(imagemDil,imagem4))

#imagemEro = Erosao(imagem4,EE4,False)
#DesenhaImagem(imagemEro)

#Conj2Img(Imagem2)

