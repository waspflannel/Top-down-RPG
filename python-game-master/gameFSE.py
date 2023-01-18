from pygame import *
import math
import random
init()
#Global variables
width, height = 800, 600
screen = display.set_mode((width, height))
RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DGREEN = (0, 170, 0)
YELLOW = (255, 255, 0)
WALL = (0, 0, 0, 255)
room = 1 #Current room
oldRoom=1
roomChange=True
game = True     #used to detrirmine if the game is running(other things that could be running are different cutscenes)
controldisplay = False    #Used to display controls
cutscene = False       #Used to display cutscene
cutscenecooldown = 0
loadscreen = True
arrowDirection=None  #Used to display the arrow in the correct orientation
endDeath=True    #used to display death screen
arrowx=0
arrowy=0
instakill=0
arrowRect=Rect(-1002,23121,31231,31312)
originalBackgroundx=0
originalBackgroundy=0
end=False
countdown=0
bossAlive=True

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Random pictures are loaded and assigned to their lists
Inventroytemplate = image.load("pics/Inventory2.png")

Background = image.load("pics/background.png")
Control = image.load("pics/control.png")
Cut = image.load("pics/cutscene.png")

pallet = image.load('pics/Rooms/1/pallet.png')
Pallet = transform.scale(pallet, (800, 600))
Palletmask = image.load("pics/Rooms/1/palletmask.png")
Palletcover = image.load("pics/Rooms/1/Room1Cover.png")


Route1=image.load("pics/Rooms/1/Route_1.png")
Route1mask=image.load("pics/Rooms/1/Route_1_mask.png")
Route1cover=image.load("pics/Rooms/1/Route_1_cover.png")

ViridianCity=image.load("pics/Rooms/1/Viridian_City.png")
Viridianmask=image.load("pics/Rooms/1/Viridian_City_Mask.png")
Viridiancover=image.load("pics/Rooms/1/Viridian_City_Cover.png")

Route_22=image.load("pics/Rooms/1/Route_22.png")
Route_22_mask=image.load("pics/Rooms/1/Route_22_mask.png")
Route_22_cover=image.load("pics/Rooms/1/Route_22_cover.png")

Route_23=image.load("pics/Rooms/1/Route_23.png")
Route_23_mask=image.load("pics/Rooms/1/Route_23_mask.png")
Route_23_cover=image.load("pics/Rooms/1/Route_23_cover.png")

arrowup=image.load("pics/arrowup.png")
arrowdown=image.load("pics/arrowdown.png")
arrowleft=image.load("pics/arrowleft.png")
arrowright=image.load("pics/arrowright.png")

deathscreenpic=image.load("pics/deathscreen.png")

lastRoom=image.load("pics/Rooms/1/VictoryRoad.png")
lastRoomMask=image.load("pics/Rooms/1/VictoryRoad_Mask.png")
lastRoomCover=image.load("pics/Rooms/1/VictoryRoad_Cover.png")

endscreen=image.load("pics/endscreen.png")
credits=image.load("pics/credits.png")

swordswing=mixer.Sound("sounds/swingsound.wav.wav")
skeletonDeath=mixer.Sound("sounds/skeledeathsound.wav")
bossdeathsound=mixer.Sound("sounds/boss1deathsound.wav")
boss2deathsound=mixer.Sound("sounds/boss2deathsound.wav")
boss3deathsound=mixer.Sound("sounds/finalbossdeathsound.wav")
bowsound=mixer.Sound("sounds/bowshotsound.wav")

menuMusic=mixer.music.load("sounds/menumusic.mp3")
mixer.music.play(-1)
rooms = [Pallet,Route1,ViridianCity,Route_22,Route_23,lastRoom]
masks = [Palletmask,Route1mask,Viridianmask,Route_22_mask,Route_23_mask,lastRoomMask]
covers = [Palletcover,Route1cover,Viridiancover,Route_22_cover,Route_23_cover,lastRoomCover]
exits=[0,Rect(350,0,105,1),Rect(284,135,65,1),Rect(0,300,1,50),Rect(179,140,1,70),Rect(200,145,30,1),Rect(0,0,0,0)]
Backgroundx = 0
Backgroundy = 0

playerSprite = sprite.Group()
enemySprite = sprite.Group()
deadsprite= sprite.Group()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Sprite loading
def loadSprites(path):
    'loadSprites(path)- takes file path and returns list of each sprite in folder'
    picList = []
    for i in range(50):
        try:
            picList.append(image.load(path + str(i) + '.png').convert_alpha())
        except:
            return picList

characterList = [[loadSprites('pics/Movements/Move Up/Move Up'), 3, 26],
                 [loadSprites('pics/Movements/Move Down/Move Down'), 3, 26],
                 [loadSprites('pics/Movements/Move Left/Move Left'), 3, 26],
                 [loadSprites('pics/Movements/Move Right/Move Right'), 3, 26],
                 [[image.load('pics/Standing.png')], 1, 0],  # 4
                 [loadSprites('pics/Sword/SwordSwingUp/SwordSwingUp'), 2, 11],
                 [loadSprites('pics/Sword/SwordSwingDown/SwordSwingDown'), 2, 11],
                 [loadSprites('pics/Sword/SwordSwingLeft/SwordSwingLeft'), 2, 11],
                 [loadSprites('pics/Sword/SwordSwingRight/SwordSwingRight'), 2, 11],
                 [loadSprites('pics/Death/Death'), 7, 41]]

characterhbList = [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [loadSprites('pics/Sword/SwordSwingUp/swordswingupmask/swingswordmaskup'),2, 11],
                   [loadSprites('pics/Sword/SwordSwingDown/swordmask/swordmask'), 2, 11],
                   [loadSprites('pics/Sword/SwordSwingLeft/swordleftmask/swordswingleft'), 2, 11],
                   [loadSprites('pics/Sword/SwordSwingRight/swordswingrightmasks/sworswingrightmask'), 2, 11],
                   [0, 0, 0, 0]]  # 9

skeleList = [[loadSprites('pics/Skele/SkeleWalkUp/SkeleWalkUp'), 3, 26],
             [loadSprites('pics/Skele/SkeleWalkDown/SkeleWalkDown'), 3, 26],
             [loadSprites('pics/Skele/SkeleWalkLeft/SkeleWalkLeft'), 3, 26],
             [loadSprites('pics/Skele/SkeleWalkRight/SkeleWalkRight'), 3, 26],
             [0, 0, 0, 0],
             [loadSprites('pics/Skele/skeleswingup/skeleswingup'),5,39],
             [loadSprites('pics/Skele/skeleswingdown/skeleswingdown'),5,39],
             [loadSprites('pics/Skele/skeleswingleft/skeleswingleft'),5,39],
             [loadSprites('pics/Skele/skeleswingright/skeleswingright'),5,39],
             [loadSprites('pics/Skele/skeledeath/skeledeath'),7,41]]#9

bossList = [[loadSprites('pics/Movements/bossmoveup/bossmoveup'),5,44],
            [loadSprites('pics/Movements/bossmovedown/bossmovedown'),5,44],
            [loadSprites('pics/Movements/bossmoveleft/bossmoveleft'),5,44],
            [loadSprites('pics/Movements/bossmoveright/bossmoveright'),5,44],
            [0, 0, 0, 0],
            [loadSprites('pics/Sword/bswingup/bswingup'), 3, 17],
            [loadSprites('pics/Sword/bswingdown/bswingdown'), 3, 17],
            [loadSprites('pics/Sword/bswingleft/bswingleft'), 3, 17] ,
            [loadSprites('pics/Sword/bswingright/bswingright'), 3, 17],
            [loadSprites('pics/Movements/bossdeath/bossdeath'),7,41]]

boss2list= [[[image.load("pics/boss2/boss2walkup/boss2walkup0.png")],1,1],
            [[image.load("pics/boss2/boss2walkdown/boss2walkdown0.png")],1,1],
            [[image.load("pics/boss2/boss2walkleft/boss2walkleft0.png")],1,1],
            [[image.load("pics/boss2/boss2walkright/boss2walkright0.png")],1,1],
            [0,0,0,0],
            [loadSprites("pics/boss2/boss2shootup/boss2shootup"),2,25],
            [loadSprites("pics/boss2/boss2shootdown/boss2shootdown"),2,25],
            [loadSprites("pics/boss2/boss2shootleft/boss2shootleft"),2,25],
            [loadSprites("pics/boss2/boss2shootright/boss2shootright"),2,25],
            [loadSprites("pics/boss2/boss2death/boss2death"),7,41]]

finalboss=[[[image.load('pics/finalboss/orkmoveup/orkmoveup0.png')],1,1],
           [[image.load('pics/finalboss/orkmovedown/orkmovedown0.png')],1,1],
           [[image.load('pics/finalboss/orkmoveleft/orkmoveleft0.png')],1,1],
           [[image.load('pics/finalboss/orkmoveright/orkmoveright0.png')],1,1],
           [0,0,0,0],
           [loadSprites('pics/finalboss/orkswingup/orkswingup'),5,29],
           [loadSprites('pics/finalboss/orkswingdown/orkswingdown'),5,29],
           [loadSprites('pics/finalboss/orkswingleft/orkswingleft'),5,29],
           [loadSprites('pics/finalboss/orkswingright/orkswingright'),5,29],
           [loadSprites('pics/finalboss/orkdeath/orkdeath'),7,41],
           [loadSprites('pics/finalboss/spellcast/spellcast'),7,41]]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# player class
class player(sprite.Sprite):  # put everything in a class, can be used for multiple players, stops the use of multiple global variables for different players(x1,x2)
    def __init__(self, char, hitbox, x, y, width, height, HP, atk, defense,damage):
        sprite.Sprite.__init__(self)
        self.atk = atk      #basic character info
        self.char = char
        self.x = x
        self.y = y
        self.endx=x
        self.endy=y
        self.width = width
        self.height = height
        self.vel = 4
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.health = HP
        self.max_hp = HP
        self.alive = True
        self.deathPic = 0
        self.sword = False
        self.bow = False
        self.position = Rect((self.x, self.y, 31, 51))
        self.rect = Rect((self.x, self.y, 31, 51))
        self.action = 2
        self.old_action = self.action
        self.cooldown = 0
        self.timer = char[0][2]      #Max timer for the current animation
        self.image = self.char[self.action][0][self.cooldown // self.char[self.action][1]]   #The current animation
        self.hitbox = hitbox
        self.skelehbList = skeleList
        self.damage=damage
        self.jotaroRect= Rect((self.x,self.y,31,51))
        self.rangebox = Rect(self.endx +10, self.endy +10, 11, 75)     #Used to determine if your in an Ai's attack range
        self.adjustx = [30, 45, 70, 20]     #Used to adjust certain animations
        self.adjusty = [20, 5, 0, 5]
        self.originalx=x
        self.originaly=y
        self.shootcooldown=0

    #Used to update basic things like positions
    def update(self):
        if self.shootcooldown !=0:
            self.shootcooldown -=1

        if room==5 and self.char !=characterList:
            self.positionUpdate()

        if self.health <=0 and self.char != characterList:
            if self.alive:
                self.action=9
                if self.char == skeleList:
                    skeletonDeath.play()
                elif self.char == bossList:
                    bossdeathsound.play()
                elif self.char == boss2list:
                    boss2deathsound.play()
                elif self.char == finalboss:
                    boss3deathsound.play()
                deadsprite.add(self)
                enemySprite.remove(self)
                enemylist.remove(self)
                self.cooldown=0
                self.alive=False
            self.aideath()
        elif self.char==characterList and not self.alive:
            self.alive=False

        if self.alive or self.char == characterList:
            self.endx=self.x+Backgroundx
            self.endy=self.y+Backgroundy
            self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)
            self.cooldown += 1
            if self.old_action != self.action:
                self.cooldown = 0
            self.timer = self.char[self.action][2]
            if self.cooldown >= self.timer:
                if self.action==10:
                    self.spell=False
                    instakillRect = Rect(self.endx - 30, self.endy - 30, 111, 131)
                    if jotaro.rect.colliderect(instakillRect):
                        jotaro.health = 0
                self.cooldown = 0
                self.sword = False
            if self.action < 5 :
                if self.char==characterList:
                    self.rect = Rect(self.x, self.y, 31, 51)
            self.image = self.char[self.action][0][self.cooldown // self.char[self.action][1]]  # takes player action and determines the right sprite from characterList, determines which sprite from self.cooldown
            self.old_action = self.action

    #This is how the character moves
    def move(self):
        global Backgroundy
        global Backgroundx
        if self.alive:
            mask = masks[room - 1]
            if self.sword == False:
                if keys[K_a] and clear(self.x - self.vel, self.y):
                    if Backgroundx >= 0 or self.x >= 400:
                        self.x -= self.vel
                    else:
                        Backgroundx += self.vel
                    self.action = 2

                elif keys[K_d] and clear(self.x + self.vel, self.y):
                    if Backgroundx <= mask.get_width() * -1 + 800 or self.x < 400:
                        self.x += self.vel
                    else:
                        Backgroundx -= self.vel
                    self.action = 3

                elif keys[K_w] and clear(self.x, self.y - self.vel):
                    if Backgroundy >= 0 or self.y >= 300:
                        self.y -= self.vel
                    else:
                        Backgroundy += self.vel
                    self.action = 0

                elif keys[K_s] and clear(self.x, self.y + self.vel):
                    mask = masks[room - 1]
                    if Backgroundy == mask.get_height() * -1 + 600 or self.y < 300:
                        self.y += self.vel
                    else:
                        Backgroundy -= self.vel
                    self.action = 1

                else:
                    self.action = 4

        else:
            self.action = 9

    #Healthbar display
    def healthbar(self):
        mhealthRect = Rect((self.x - 10, self.y - 15, 50, 10))
        draw.rect(screen, RED, mhealthRect, 0)
        if self.health > 0:
            healthRect = Rect((self.x - 10, self.y - 15, 50 - (5 * (10 - self.health)), 10))
            draw.rect(screen, DGREEN, healthRect, 0)

    #Determines damage
    def hit(self):
        if self.health > 0:
            self.health -= self.damage
        else:
            self.alive = False

    #Used to trigger lose screen
    def respawn(self, x, y):
        global game
        time.wait(1000)
        lossMusic = mixer.music.load("sounds/loss sound.mp3")
        mixer.music.play(-1)
        game = False

    #Attack
    def SwingSword(self):
        if self.alive:
            if self.sword:   #Player attack
                if self.cooldown + 1 >= self.char[self.action][2]:
                    self.cooldown = 0
                    self.sword = False
            if self.char==characterList:
                if self.action < 4:
                    self.action += 5

                if self.action == 4:
                    self.action = 6

                if self.char==characterList:
                    self.rect = Rect(self.x - self.adjustx[self.action - 5], self.y - self.adjusty[self.action - 5], 31, 51)
                else:
                    self.endy = self.y + Backgroundy
                    self.endx = self.x + Backgroundx
                    self.rect = Rect(self.endx - self.adjustx[self.action - 5],self.endy - self.adjusty[self.action - 5], 31, 51)
                    self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)

            else:
                #Ai attack
                if self.endx > jotaro.x and jotaro.y+15>=self.endy and jotaro.y<=self.endy:
                    self.action=7
                elif self.endx < jotaro.x and jotaro.y+15>=self.endy and jotaro.y<=self.endy:
                    self.action=8
                elif self.endy < jotaro.y:
                    self.action=6
                elif self.endy > jotaro.y:
                    self.action=5

                self.endy = self.y + Backgroundy
                self.endx = self.x + Backgroundx
                self.rect = Rect(self.endx - self.adjustx[self.action - 5], self.endy - self.adjusty[self.action - 5],31, 51)
                self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)

        else:
            self.action==9

    #Checks collision between player and Ai
    def checkHit(self, image, hit, i, hurt, mode):
        self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)
        if room==3 and self.char != characterList and self.sword==True:
            self.rect = Rect(self.endx - self.adjustx[self.action - 5],self.endy - self.adjusty[self.action - 5], 31, 51)
        if self.char==characterList or self.endx <= 800 and self.endy <=600 and self.endx >=0 and self.endy >=0:
            if self.action != 10 and self.hitbox[self.action][2] > 0:
                if self.hitbox[self.action][2] > 0:
                    if self.old_action != self.action:
                        self.cooldown = 0
                    self.image = self.hitbox[self.action][0][self.cooldown // self.hitbox[self.action][1]]
                    if mode == "enemy":
                        hit.image = hit.char[hit.action][0][hit.cooldown // hit.char[hit.action][1]]#Takes an image from the hitbox list and checks if it collides
                        x = hurt
                        if hurt.action > 5 and hurt.action < 8 + 1:
                            hurt.image = hurt.char[hurt.action - 5][0][hurt.cooldown // hurt.char[hurt.action - 5][1]]
                    else:
                        playerSprite.clear(screen, rooms[room-1])
                        playerSprite.draw(screen)

                    if sprite.collide_mask(hit, hurt) is not None and self.action < 9:
                        if hurt.health > 0:
                            hurt.health -= self.damage
                        else:
                            hurt.alive = False
        self.image = image

    #Checks to see if you leave the room
    def exitCheck(self):
        global room
        position = Rect(self.x, self.y, 31, 51)
        if position.colliderect(exits[room]):
            room += 1

    #Used to reposition
    def positionChange(self,x,y):
        self.x=x
        self.y=y

    #Used to update positions with camera movement
    def positionUpdate(self):
        self.endy = self.y + Backgroundy
        self.endx = self.x + Backgroundx
        self.rect = Rect((self.endx, self.endy, 31, 51))
        self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)

    #Used to display large healthbars
    def bosshealthbar(self):
        if self.alive:
            mhealthRect = Rect((self.x -(self.max_hp/2)+15, self.y  - 15, self.max_hp, 10))
            draw.rect(screen, RED, mhealthRect, 0)
            if self.health > 0:
                healthRect = Rect((self.x - (self.max_hp / 2) + 15, self.y- 15, self.health, 10))
                draw.rect(screen, DGREEN, healthRect, 0)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Enemy class
class enemy(player):  # class for enemies and monsters.s
    def __init__(self, char, hitbox, x, y, width, height, HP, end, atk, defense,damage,adjustx,adjusty):
        player.__init__(self, char, hitbox, x, y, width, height, HP, atk, defense,damage)
        self.end = end
        self.path = [self.x, self.end]
        self.image = self.char[self.action][0][self.cooldown // self.char[self.action][1]]
        self.action = 2
        self.vel = 3
        self.alive = True
        self.endy = y
        self.endx = x
        self.damage=damage
        self.bossRect=Rect((self.x,self.y,1,51))
        self.sword=False
        self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)
        self.maxhealth=HP
        self.originalx=x
        self.originaly=y
        self.adjustx = adjustx
        self.adjusty = adjusty
        self.oldHP=HP
        self.shootcooldown=0
        self.bow=False
        self.spell=False

    #Ai movement
    def move(self):
        if self.alive:
            self.endy = self.y + Backgroundy
            self.endx = self.x + Backgroundx
            self.rect = Rect((self.endx, self.endy, 31, 51))
            self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)
            #Move in a direction until they get to their end position then they walk the other way
            if self.vel > 0:
                if self.x + self.vel < self.path[1] and aiClear(self.x - self.vel, self.y):
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                self.action = 3
            else:
                if self.x - self.vel > self.path[0] and aiClear(self.x - self.vel, self.y):
                    self.x += self.vel
                else:
                    self.vel = self.vel * -1
                self.action = 2

        else:

            self.action==9

    #Used to swing boss sword
    def BossSwingSword(self):
        if self.alive:
            if self.cooldown + 1 >= self.char[self.action][2]:
                self.cooldown = 0
                self.sword = False
                return
            if self.action < 4:
                self.action += 5
            if self.action == 4:
                self.action = 6
            self.endy = self.y + Backgroundy
            self.endx = self.x + Backgroundx
            self.rangebox = Rect(self.endx + 1, self.endy + 1, 29, 49)
            self.rect = Rect(self.endx - self.adjustx[self.action - 5],self.endy - self.adjusty[self.action - 5], 31, 51)

    #The boss paths towards the player
    def bossMove(self):
        if self.alive:
            self.endy = self.y + Backgroundy
            self.endx = self.x + Backgroundx
            self.rect = Rect((self.endx, self.endy, 31, 51))

            x = self.endx + self.vel
            if x < jotaro.x:
                self.x += self.vel
                self.action = 3
                self.bossRect = Rect(self.x, self.y, 31, 51)
                return

            x = self.endx - self.vel
            if x > jotaro.x:
                self.x -= self.vel
                self.action = 2
                self.bossRect = Rect(self.x, self.y, 31, 51)
                return

            y = self.endy + self.vel
            if y < jotaro.y:
                self.y += self.vel
                self.action = 1
                self.bossRect = Rect(self.x, self.y, 31, 51)
                return

            y = self.endy - self.vel
            if y > jotaro.y:
                self.y -= self.vel
                self.action = 0
                self.bossRect = Rect(self.x, self.y, 31, 51)
                return

        else:

            self.action=9
    #Used to display smaller healthbars
    def healthbar(self):

        if self.alive:
            mhealthRect = Rect((self.endx, self.endy - 15, 25, 10))
            draw.rect(screen, RED, mhealthRect, 0)

            if self.health > 0:
                healthRect = Rect((self.endx, self.endy - 15, 50 - (5 * (10 - self.health)), 10))
                draw.rect(screen, DGREEN, healthRect, 0)

    def bosshealthbar(self):
        if self.alive:
            mhealthRect = Rect((self.x + Backgroundx-(self.maxhealth/2)+15, self.y + Backgroundy - 15, self.maxhealth, 10))
            draw.rect(screen, RED, mhealthRect, 0)

            if self.health > 0:
                healthRect = Rect((self.x + Backgroundx - (self.maxhealth / 2) + 15, self.y + Backgroundy - 15, self.health, 10))
                draw.rect(screen, DGREEN, healthRect, 0)
    #Used to diplay death animations
    def aideath(self):
        self.endy = self.y + Backgroundy
        self.endx = self.x + Backgroundx
        self.rect = Rect((self.endx, self.endy, 31, 51))
        self.cooldown+=1
        self.timer = self.char[self.action][2]

        if self.cooldown >= self.timer:
            deadsprite.remove(self)
            self.alive = False

        self.image = self.char[self.action][0][self.cooldown // self.char[self.action][1]]

    #Used for boss 2 to teleport around
    def boss2move(self):
        if self.bow==False:
            if self.oldHP != self.health and self.char == boss2list:
                mask=masks[room-1]
                newx = random.randint(0, 800)
                newy = random.randint(Backgroundy*-1,Backgroundy*-1+600)

                if math.sqrt((jotaro.x - newx)**2+(jotaro.y-newy)**2) > 100 and aiClear(newx,newy):
                    self.x = newx
                    self.y = newy
                else:
                    self.boss2move()
            if jotaro.y>self.endy-50 and jotaro.y < self.endy+101 and jotaro.x < self.x+15:
                self.action=2

            elif jotaro.y>self.endy-50 and jotaro.y < self.endy+101 and jotaro.x > self.x+15:
                self.action=3

            elif jotaro.y > self.endy:
                self.action = 1

            else:
                self.action = 0

            self.oldHP=self.health

    #Used to determine boss 2 rects
    def fourDirection(self):
        self.shootdown=Rect(self.endx,self.endy+51,31,3000)
        self.shootup=Rect(self.endx,self.endy-3000,31,3000)
        self.shootright=Rect(self.endx+31,self.endy,3000,51)
        self.shootleft = Rect(self.endx-3000, self.endy, 3000, 51)

    #Used to trigger boss 2 shoot animations
    def shoot(self):
        global arrowDirection
        global arrowx
        global arrowy
        global originalBackgroundx
        global originalBackgroundy
        if self.cooldown + 1 >= self.char[self.action][2]:
            self.cooldown = 0
            self.bow = False


        if jotaro.rect.colliderect(boss2.shootdown) and  self.shootcooldown == 0:
            bowsound.play()
            arrowDirection="Down"
            self.bow=True
            self.action=6
            self.shootcooldown=75
            arrowx=self.endx
            arrowy=self.endy+51
            originalBackgroundx =Backgroundx
            originalBackgroundy =Backgroundy

        elif jotaro.rect.colliderect(boss2.shootup) and  self.shootcooldown == 0:
            bowsound.play()
            arrowDirection="Up"
            self.bow=True
            self.action=5
            self.shootcooldown=100
            arrowx=self.endx
            arrowy=self.endy
            originalBackgroundx =Backgroundx
            originalBackgroundy =Backgroundy

        elif jotaro.rect.colliderect(boss2.shootleft) and  self.shootcooldown == 0:
            bowsound.play()
            arrowDirection="Left"
            self.bow=True
            self.action=8
            self.shootcooldown=100
            arrowx=self.endx
            arrowy=self.endy
            originalBackgroundx =Backgroundx
            originalBackgroundy =Backgroundy

        elif jotaro.rect.colliderect(boss2.shootright) and  self.shootcooldown == 0:
            bowsound.play()
            arrowDirection="Right"
            self.bow=True
            self.action=7
            self.shootcooldown=100
            arrowx=self.endx+31
            arrowy=self.endy
            originalBackgroundx =Backgroundx
            originalBackgroundy =Backgroundy
    #Used to efficiently update enemy info
    def generalupdate(self):
        self.positionUpdate()
        if jotaro.rect.colliderect(self.rangebox) and self.sword == False:
            self.sword = True
        if self.sword == True:
            self.SwingSword()
        elif self.sword == False:
            self.move()
    #Used for final boss instakill mechanic
    def finalAttack(self):
        global instakill
        instakill += 1
        if instakill == 300:
            self.spell=True
            instakill = 0
            self.action = 10

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Different characters
jotaro = player(characterList, characterhbList, 380, 500, 31, 51, 25, 10,10,1)  # instance class, these go into class (x,y,width,height)
playerSprite.add(jotaro)

#------------------------------------------------------------------------------
#room1
skeleton = enemy(skeleList, skeleList, 60, 230, 31, 51, 5, 450, 1, 10,0.1,[0,0,0,0],[0,0,0,0])
skeleton1 = enemy(skeleList, skeleList, 350, 50, 31, 51, 5, 650, 1, 10,0.1,[0,0,0,0],[0,0,0,0])
skeleton2=enemy(skeleList,skeleList,400+Backgroundx,400+Backgroundy,31,51,5,700,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton3=enemy(skeleList,skeleList,70+Backgroundx,370+Backgroundy,31,51,5,400,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton4=enemy(skeleList,skeleList,75+Backgroundx,40+Backgroundy,31,51,5,350,1,10,0.1,[0,0,0,0],[0,0,0,0])

#room2
skeleton5=enemy(skeleList,skeleList,150+Backgroundx,1200+Backgroundy,31,51,5,650,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton6=enemy(skeleList,skeleList,270+Backgroundx,980+Backgroundy,31,51,5,670,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton7=enemy(skeleList,skeleList,100+Backgroundx,700+Backgroundy,31,51,5,450,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton8=enemy(skeleList,skeleList,450+Backgroundx,540+Backgroundy,31,51,5,600,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton9=enemy(skeleList,skeleList,300+Backgroundx,300+Backgroundy,31,51,5,600,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton10=enemy(skeleList,skeleList,100+Backgroundx,325+Backgroundy,31,51,5,150,1,10,0.1,[0,0,0,0],[0,0,0,0])

#room3
boss1=enemy(bossList,bossList,825+Backgroundx,600+Backgroundy,31,51,30,450,1,1,1,[35,28,60,15],[20,0,0,0])

#room4
skeleton11=enemy(skeleList,skeleList,470+Backgroundx,525+Backgroundy,31,51,5,1150,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton12=enemy(skeleList,skeleList,1025+Backgroundx,350+Backgroundy,31,51,5,1150,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton13=enemy(skeleList,skeleList,600+Backgroundx,220+Backgroundy,31,51,5,820,1,10,0.1,[0,0,0,0],[0,0,0,0])
skeleton14=enemy(skeleList,skeleList,475+Backgroundx,350+Backgroundy,31,51,5,660,1,10,0.1,[0,0,0,0],[0,0,0,0])

#room5
boss2=enemy(boss2list,boss2list,280+Backgroundx,2250+Backgroundy,31,51,10,0,1,1,0.35,[0,0,0,0],[0,0,0,0])

#room6
finalboss=enemy(finalboss,finalboss,450+Backgroundx,200+Backgroundy,31,51,50,500,1,1,0.17,[35,30,70,20],[60,20,0,0])


enemylist = []
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Makes sure way your moving is clear
def clear(x, y):
        mask = masks[room - 1]
        if x < 0 or x + 31 - Backgroundx >= mask.get_width() or y < 0 or y + 50 - Backgroundy >= mask.get_height():
            return False

        else:

            for i in range(31):
                if mask.get_at((x + i - Backgroundx, y + 50 - Backgroundy)) == WALL:
                    return False
            return True

#Takes into consideration camera movement when checking clear
def aiClear(x, y):
    mask = masks[room - 1]
    if x < 0 or x + 31 >= mask.get_width() or y < 0 or y + 50 >= mask.get_height():
        return False

    else:

        for i in range(31):
            if mask.get_at((x + i , y + 50)) == WALL:
                return False
        return True
#Used to display starting screen
def Loadscreen():
    global running
    global controldisplay
    global cutscene
    play = Rect(300, 171, 200, 64)
    controls = Rect(300, 296, 200, 46)
    notcontrols = Rect(0, 0, 50, 50)
    exit = Rect(300, 409, 200, 62)
    if cutscene:
        Cutscene()

    elif controldisplay:
        screen.blit(Control, (0, 0))
        if notcontrols.collidepoint(mx, my) and mb[0] == 1:
            controldisplay = False

    else:

        if exit.collidepoint(mx, my) and mb[0] == 1:
            running = False
        elif controls.collidepoint(mx, my) and mb[0] == 1:
            controldisplay = True
        elif play.collidepoint(mx, my) and mb[0] == 1:
            cutscene = True
        screen.blit(Background,(0,0))

#Used for blitting cutscene
def Cutscene():
    global cutscene
    global cutscenecooldown
    global loadscreen
    cutscenecooldown += 1
    if cutscenecooldown == 200:
        loadscreen = False
    else:
        screen.blit(Cut,(0,0))

#Used to change certain variables when entering a new room
def roomUpdate():
    global Backgroundx
    global Backgroundy
    global enemylist

    if room==1:
        backgroundMusic = mixer.music.load("sounds/background.mp3")
        mixer.music.play(-1)
        enemylist = [skeleton, skeleton1,skeleton2,skeleton3,skeleton4]

    if room==2:
        backgroundMusic = mixer.music.load("sounds/background.mp3")
        mixer.music.play(-1)
        enemylist=[skeleton5,skeleton6,skeleton7,skeleton8,skeleton9,skeleton10]
        jotaro.positionChange(400,550)
        Backgroundy = -924

    if room == 3:
        battleMusic = mixer.music.load("sounds/battlemusic.mp3")
        mixer.music.play(-1)
        jotaro.health = jotaro.max_hp
        enemylist = [boss1]
        jotaro.positionChange(400, 10)
        Backgroundx = -424
        Backgroundy = 0

    if room == 4:
        backgroundMusic = mixer.music.load("sounds/background.mp3")
        mixer.music.play(-1)
        enemylist = [skeleton11,skeleton12,skeleton13,skeleton14]
        jotaro.positionChange(740, 210)
        Backgroundx = -450
        Backgroundy = 0

    if room == 5:
        battleMusic = mixer.music.load("sounds/battlemusic.mp3")
        mixer.music.play(-1)
        enemylist = [boss2]
        jotaro.positionChange(275, 400)
        Backgroundx = 0
        Backgroundy = -2207

    if room==6:
        battleMusic = mixer.music.load("sounds/battlemusic.mp3")
        mixer.music.play(-1)
        jotaro.health=jotaro.max_hp
        enemylist=[finalboss]
        jotaro.positionChange(380,500)
        Backgroundy=-107
        Backgroundx=0

    enemySprite.empty()
    for enemy in enemylist:
        enemySprite.add(enemy)
#Used to update mobs
def aiattack():
    if room == 1:
        skeleton.generalupdate()
        skeleton1.generalupdate()
        skeleton2.generalupdate()
        skeleton3.generalupdate()
        skeleton4.generalupdate()

    if room == 2:
        skeleton5.generalupdate()
        skeleton6.generalupdate()
        skeleton7.generalupdate()
        skeleton8.generalupdate()
        skeleton9.generalupdate()
        skeleton10.generalupdate()

    if room == 3:
        boss1.positionUpdate()
        if bossRect.colliderect(jotaro.rect) and boss1.sword == False:
            boss1.sword = True
        if boss1.sword == True and boss1.alive:
            swordswing.play()
            boss1.BossSwingSword()
        elif boss1.sword == False and boss1.alive:
            boss1.bossMove()

    if room == 4:
        skeleton11.generalupdate()
        skeleton12.generalupdate()
        skeleton13.generalupdate()
        skeleton14.generalupdate()

    if room == 5:
        if boss2.alive:
            boss2.positionUpdate()
            boss2.fourDirection()
            boss2.shoot()
            boss2.boss2move()

    if room == 6:
        finalboss.positionUpdate()

        finalboss.bossRect=Rect(finalboss.x+Backgroundx-10,finalboss.endy+Backgroundy-10,61,81)
        if finalboss.bossRect.colliderect(jotaro.rect) and finalboss.sword == False:
            finalboss.sword = True

        if finalboss.sword == True and not finalboss.spell:
            swordswing.play()
            finalboss.SwingSword()
        elif finalboss.sword == False and finalboss.alive and not finalboss.spell:
            finalboss.boss2move()

        if finalboss.alive:
             finalboss.finalAttack()
#Used to move the arrow rect
def arrowShoot():
    global arrowDirection
    global arrowx
    global arrowy
    global arrowRect
    ydiff=originalBackgroundy-Backgroundy
    vel=10

    if arrowDirection == "Up":
        arrowy-=vel
        arrowRect = Rect(arrowx+10, arrowy-ydiff-106,10,106)
        screen.blit(arrowup,(arrowRect))

    if arrowDirection == "Down":
        arrowy+=vel
        arrowRect = Rect(arrowx+10, arrowy-ydiff,10,106)
        screen.blit(arrowdown,(arrowRect))

    if arrowDirection == "Left":
        arrowx-=vel
        arrowRect = Rect(arrowx-106, arrowy+20-ydiff,106,10)
        screen.blit(arrowleft,(arrowRect))

    if arrowDirection == "Right":
        arrowx +=vel
        arrowRect = Rect(arrowx, arrowy+20-ydiff,106,10)
        screen.blit(arrowright,(arrowRect))

    if arrowRect.colliderect(jotaro.rect):
        jotaro.health-=boss2.damage
#Draws all the healthbars
def healthbarupdate():
    if room==1:
        skeleton.healthbar()
        skeleton1.healthbar()
        skeleton2.healthbar()
        skeleton3.healthbar()
        skeleton4.healthbar()

    if room==2:
        skeleton5.healthbar()
        skeleton6.healthbar()
        skeleton7.healthbar()
        skeleton8.healthbar()
        skeleton9.healthbar()
        skeleton10.healthbar()

    if room==3:
        boss1.bosshealthbar()

    if room==4:
        skeleton11.healthbar()
        skeleton12.healthbar()
        skeleton13.healthbar()
        skeleton14.healthbar()

    if room==5:
        boss2.bosshealthbar()

    if room==6:
        finalboss.bosshealthbar()

#Used for ending screens
def endingScreen():
    global countdown
    global running
    countdown+=1
    if countdown <=200:
        screen.blit(endscreen,(0,0))
    elif countdown <=400:
        screen.blit(credits,(0,0))
    else:
        running=False

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Main screen updates while game is running
def redrawGameWindow():
    mixer.music.set_volume(1)
    if len(enemylist)==0:
        jotaro.exitCheck()
    screen.blit(rooms[room - 1], (Backgroundx, Backgroundy))
    healthbarupdate()
    jotaro.bosshealthbar()
    playerSprite.draw(screen)
    enemySprite.draw(screen)
    deadsprite.draw(screen)
    screen.blit(covers[room - 1], (Backgroundx, Backgroundy))
    display.update()
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
clock = time.Clock()
# main loop
running = True
while running:
    clock.tick(27)
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()

    if loadscreen:
        Loadscreen()
    elif game:
        if jotaro.health <= 0:
            jotaro.alive = False

        deadsprite.update()

        if not jotaro.alive:
            if jotaro.cooldown == 40:
                jotaro.respawn(100, 100)

        if mb[0] == 1 and jotaro.sword == False and jotaro.action != 4:
            swordswing.play()
            jotaro.sword = True
            jotaro.SwingSword()

        bossRect = Rect(boss1.x+Backgroundx-40,boss1.y+Backgroundy-20,111,111)
        jotaro.move()
        #checks collision for all enemies in enemysprite
        for i in range(len(enemySprite)):
            jotaro.checkHit(jotaro.image, jotaro, i, enemylist[i - 1], "player")
            enemylist[i - 1].checkHit(enemylist[i - 1].image, enemylist[i - 1], i, jotaro, "enemy")

        if room != oldRoom:
            roomChange = True
        if roomChange:
            roomUpdate()
            roomChange = False

        oldRoom=room
        playerSprite.update()
        aiattack()
        redrawGameWindow()
        enemySprite.update()

        if room==5 and boss2.alive:
            arrowShoot()
        #Initiates ending screen
        if not finalboss.alive:
           bossAlive=False
        if not finalboss.alive and len(deadsprite)==0:
            menuMusic = mixer.music.load("sounds/menumusic.mp3")
            mixer.music.play(-1)
            game = False
            end = True

    elif end:
        endingScreen()

    elif endDeath:
        screen.blit(deathscreenpic,(0,0))
        exitRect=Rect(330,450,140,50)
        if exitRect.collidepoint(mx,my) and mb[0]==1:
            running=False

    mask = masks[room - 1]
    display.flip()
quit()