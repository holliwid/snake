# need to update: score when you play, possible to go in option on dead_screen


import random
import pygame
import tkinter as tk
from tkinter import messagebox
import os
from sortedcontainers import SortedDict


class TextBox(pygame.sprite.Sprite):
    global validChars, shiftChars
    validChars = "`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./"
    shiftChars = '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.text = ""
        self.font = pygame.font.Font('freesansbold.ttf', 35)
        self.font1 = pygame.font.Font('freesansbold.ttf', 100)
        self.st1 = self.font1.render("YOU WIN", False, [255, 0, 0])
        self.st2 = self.font.render("Enter your name", False, [255, 255, 255])
        self.name = self.font.render(self.text,False, [255, 255, 255])
        self.rect = self.st2.get_rect()
        self.rect = self.st2.get_rect()
        self.rect = self.name.get_rect()

    def add_chr(self, char):
        global shiftDown, capsDown
        if char in validChars and not shiftDown and len(self.text) < 3:
            self.text += char
        elif char in validChars and (shiftDown or capsDown) and len(self.text) < 3:
            self.text += shiftChars[validChars.index(char)]
        self.update()

    def update(self):
        old_rect_pos = self.rect.center
        self.name = self.font.render(self.text, False, [255, 255, 255])
        self.rect = self.name.get_rect()
        self.rect.center = old_rect_pos



class cube(object):
    rows = 20
    w = 500


    def __init__(self, start, dirnx=1, dirny=0, color = (255, 0, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            keys = pygame.key.get_pressed()
          
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1

    def addCube(self):
        tail = self.body[-1]
        dx , dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i,c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def redrawWindow(surface):
    surface.fill((0,0,0))
    s.draw(surface)
    snack.draw(surface)
    pygame.display.update()

def randomSnack(rows, item):
    positions = item.body

    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)

def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

def main(mod = "hard", score_table = {53 : "BBT", 40 : "XYZ", 1 : "LIT"}): #hard mode
    if mod == "hard":
        delay = 100
        tick = 10
    elif mod == "easy":
        delay = 50
        tick = 5


    global width, rows, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    global s
    s = snake((255, 0, 0), (10, 10))
    snack = cube(randomSnack(rows, s), color=(0, 255, 0))
    flag = True


    clock = pygame.time.Clock()




    while flag:
        pygame.time.delay(delay)
        clock.tick(tick)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(0, 255, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                resent_result = len(s.body)
                print(len(s.body))
                ls = list(score_table)[-1]
                if resent_result > ls:
                    SCORE_NAME()
                print(len(s.body))
                dead_screen(score_table,resent_result)
                resent_result = 0
                s.reset(((10,10)))
                break




        redrawWindow(win)

def start_screen(mod = "hard"):
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    size = (500, 500)
    sc = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    img = pygame.image.load("snake image.jpg")
    pygame.display.set_icon(img)


    start_surf = pygame.image.load("start.png")
    start_surf = pygame.transform.scale(start_surf,(300,100))
    x_image = 250
    y_image = 100
    start_rect = start_surf.get_rect(center=(x_image,y_image))
    sc.blit(start_surf, start_rect)

    options_surf = pygame.image.load("options.png")
    options_surf = pygame.transform.scale(options_surf, (300, 100))
    x_image = 250
    y_image = 250
    options_rect = options_surf.get_rect(center=(x_image, y_image))
    sc.blit(options_surf, options_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                print(mouse)
                if (150 < mouse[0] < 450) and 50 < mouse[1] < 150:
                    main(mod)
                elif (150 < mouse[0] < 450) and 200 < mouse[1] < 300:
                    option_screen()
            if event.type == pygame.KEYDOWN:
                main(mod)




def option_screen():
    global delay, tick
    pygame.init()
    size = (500, 500)
    sc = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    img = pygame.image.load("snake image.jpg")
    pygame.display.set_icon(img)


    speed_surf = pygame.image.load("speed.png")
    speed_surf = pygame.transform.scale(speed_surf, (300, 100))
    x_image = 260
    y_image = 100
    speed_rect = speed_surf.get_rect(center=(x_image, y_image))
    sc.blit(speed_surf, speed_rect)


    easy_surf = pygame.image.load("easy.png")
    easy_surf = pygame.transform.scale(easy_surf, (100, 50))
    x_image = 145
    y_image = 250
    easy_rect = easy_surf.get_rect(center=(x_image, y_image))
    sc.blit(easy_surf, easy_rect)

    hard_surf = pygame.image.load("hard.png")
    hard_surf = pygame.transform.scale(hard_surf, (100, 50))
    x_image = 375
    y_image = 250
    hard_rect = hard_surf.get_rect(center=(x_image, y_image))
    sc.blit(hard_surf, hard_rect)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                print(mouse)
                if (94 < mouse[0] < 200) and 225 < mouse[1] < 275:
                    start_screen("easy")

                elif (320 < mouse[0] < 500) and 225 < mouse[1] < 275:
                    start_screen("hard")

def dead_screen(score_table,resent_result):
    print(resent_result)
    pygame.init()
    size = (500, 500)
    sc = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
    img = pygame.image.load("snake image.jpg")
    pygame.display.set_icon(img)

    gameover_surf = pygame.image.load("game over.jpg")
    gameover_surf = pygame.transform.scale(gameover_surf, (600, 300))
    x_image = 260
    y_image = 100
    gameover_rect = gameover_surf.get_rect(center=(x_image, y_image))
    sc.blit(gameover_surf, gameover_rect)


    font = pygame.font.Font('freesansbold.ttf',32)
    text = font.render('SCORE TABLE',False, (255,255,255))
    textRect = text.get_rect()
    textRect.center = (260, 200)
    sc.blit(text, textRect)



    #score tablle
    global name_win
    score_table.update({resent_result : name_win})
    score_table = SortedDict(score_table)
    print(score_table)

    font = pygame.font.Font('freesansbold.ttf',20)
    name1 = font.render(score_table[list(score_table.keys())[-1]],False, (255,255,255))
    score = str(list(score_table.keys())[-1])
    score1 = font.render(score,False, (255,255,255))
    name1Rect = name1.get_rect()
    score1Rect = score1.get_rect()
    name1Rect.center = (230, 250)
    score1Rect.center = (300,250)
    sc.blit(name1, name1Rect)
    sc.blit(score1, score1Rect)


    name2 = font.render(score_table[list(score_table.keys())[-2]],False, (255,255,255))
    score = str(list(score_table.keys())[-2])
    score2 = font.render(score,False, (255,255,255))
    name2Rect = name2.get_rect()
    score2Rect = score2.get_rect()
    name2Rect.center = (230, 290)
    score2Rect.center = (300,290)
    sc.blit(name2, name2Rect)
    sc.blit(score2, score2Rect)


    name3 = font.render(score_table[list(score_table.keys())[-3]],False, (255,255,255))
    score = str(list(score_table.keys())[-3])
    score3 = font.render(score,False, (255,255,255))
    name3Rect = name3.get_rect()
    score3Rect = score3.get_rect()
    name3Rect.center = (230, 330)
    score3Rect.center = (300,330)
    sc.blit(name3, name3Rect)
    sc.blit(score3, score3Rect)



    pygame.display.update()


    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.K_ESCAPE:
                start_screen()
            elif event.type == pygame.KEYDOWN:
                waiting = False


def SCORE_NAME():
    screen = pygame.display.set_mode([500, 500])
    textBox = TextBox()
    global shiftDown, capsDown
    shiftDown = False
    capsDown = False
    #textBox.rect.center = [340, 260]

    running = True
    while running:
        screen.fill([0, 0, 0])
        screen.blit(textBox.st1, (25, 50))
        screen.blit(textBox.st2, (120, 250))
        screen.blit(textBox.name, (230, 400))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYUP:
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = False
                if e.key == pygame.K_CAPSLOCK:
                    capsDown = False
            if e.type == pygame.KEYDOWN:
                textBox.add_chr(pygame.key.name(e.key))
                if e.key in [pygame.K_RSHIFT, pygame.K_LSHIFT]:
                    shiftDown = True
                if e.key in [pygame.K_CAPSLOCK]:
                    shiftDown = True
                if e.key == pygame.K_BACKSPACE:
                    textBox.text = textBox.text[:-1]
                    textBox.update()
                if e.key == pygame.K_RETURN:
                    if len(textBox.text) > 0:
                        print(textBox.text)
                        running = False
            global name_win
            name_win = textBox.text

start_screen()