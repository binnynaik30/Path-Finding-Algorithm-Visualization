import pygame
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import sys
import math

screen = pygame.display.set_mode((810, 580))

class points:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.n = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.value = 1

    def display(self, color, st):
        if self.closed == False :
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def steps(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def show(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[self.i + 1][j].obs == False:
            self.n.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.n.append(grid[self.i - 1][j])
        if j < row-1 and grid[self.i][j + 1].obs == False:
            self.n.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.n.append(grid[self.i][j - 1])


cols = 50
grid = [0 for i in range(cols)]
row = 50
opl = []
cl = []
c1 = (235, 229, 52)
c2 = (235, 128, 52)
c3 = (227, 9, 16)
w = 800 / cols
h = 800 / row

for i in range(cols):
    grid[i] = [0 for i in range(row)]

for i in range(cols):
    for j in range(row):
        grid[i][j] = points(i, j)


start = grid[12][5]
end = grid[3][6]

for i in range(cols):
    for j in range(row):
        grid[i][j].display((255, 255, 255), 1)

for i in range(0,row):
    grid[0][i].display(c3, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].display(c3, 0)
    grid[i][row-1].display(c3, 0)
    grid[i][0].display(c3, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True

def onClick():
    global start
    global end
    st = sBox.get().split(',')
    ed = eBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    window.quit()
    window.destroy()

window = Tk()
label = Label(window, text='Starting Point coordinates(x,y): ')
sBox = Entry(window)
label1 = Label(window, text='Ending Point coordinates(x,y): ')
eBox = Entry(window)
var = IntVar()
showSteps = ttk.Checkbutton(window, text='Show Procedure :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onClick)

showSteps.grid(columnspan=2, row=2)
submit.grid(columnspan=2, row=3)
label1.grid(row=1, pady=3)
eBox.grid(row=1, column=1, pady=3)
sBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
opl.append(start)

def onSpace(x):
    t = x[0]
    w = x[1]
    g1 = t // (800 // cols)
    g2 = w // (800 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.display((255, 255, 255), 0)

end.display((2, 18, 191), 0)
start.display((2, 18, 191), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                onSpace(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].show(grid)

def calc(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    return d


def main():
    end.display((2, 18, 191), 0)
    start.display((2, 18, 191), 0)
    if len(opl) > 0:
        minm = 0
        for i in range(len(opl)):
            if opl[i].f < opl[minm].f:
                minm = i

        current = opl[minm]
        if current == end:
            print('done', current.f)
            start.display((2, 18, 191),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.display((213, 42, 232), 0)
                current = current.previous
            end.display((2, 18, 191), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ('The program is finished, the shortest distance \n to the path is ' + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        opl.pop(minm)
        cl.append(current)

        n = current.n
        for i in range(len(n)):
            n1 = n[i]
            if n1 not in cl:
                ap = current.g + current.value
                if n1 in opl:
                    if n1.g > ap:
                        n1.g = ap
                else:
                    n1.g = ap
                    opl.append(n1)

            n1.h = calc(n1, end)
            n1.f = n1.g + n1.h

            if n1.previous == None:
                n1.previous = current
    if var.get():
        for i in range(len(opl)):
            opl[i].display(c2, 0)

        for i in range(len(cl)):
            if cl[i] != start:
                cl[i].display(c1, 0)
    current.closed = True


while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    main()

