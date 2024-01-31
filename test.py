# importera nödvändiga moduler
import pygame, sys, math, time
from pygame.locals import *
from random import *


# Superklass "Ball"
# Vad ÄR en Boll? (attribut)  position, hastighet, utseende
# Vad GÖR en Boll? (metoder)  flyttar på sig, ritas ut
# Bollen påverkas av gravitation (i y-led)
# Bollen byter riktning vid fönsterkant
# Bollen har tidsstämpel som används för att inte vända håll för tidigt vid nedre kant där hastighet är hög
class Ball:
    def __init__(self,x,y,xvel,yvel,c,r):
        self.x_pos = x
        self.y_pos = y
        self.x_vel = xvel
        self.y_vel = yvel
        self.color = c
        self.radie = r
        self.x_time = 0
        
    def move(self):
        self.bordercheck()
        self.lifespan()
        if self.y_vel < 15:
             self.y_vel += 0.1         # gravitation
        self.x_pos += self.x_vel   # beräkna ny position
        self.y_pos += self.y_vel   # beräkna ny position
        
    def lifespan(self):
        for ref in drops:
            if self.x_time <= 600:
                drops.pop(ref)

        
    def draw(self):
        pygame.draw.circle(screen,
                          (self.color),
                          (int(self.x_pos),int(self.y_pos)),
                           self.radie)  # yta,(färg),(position),radie  
        
    def bordercheck(self):
        if self.x_pos > (w - self.radie) : self.x_vel *= -1
        elif self.x_pos < self.radie : self.x_vel *= -1
        elif self.y_pos > (h- self.radie) :
            if time.time() > self.x_time + 1:
                self.y_vel *= -1
                self.x_time = time.time()
        elif self.y_pos < self.radie : self.y_vel *= -1
    
# Subklass till Ball
# Attribut "keys" är en tupel som innehåller info angående vilka tangenter som styr denna boll
# Metoden (överskuggning) "move"         känner av styr-tangenter och flytta vid nertryckt
# Metoden (överskuggning) "bordercheck"  x-led:passerar till motstående     y-led:stannar vid kant                
class Ball_smooth_navigation2(Ball):
    def __init__(self, x, y, xvel, yvel, c, r, keys): 
        super(Ball_smooth_navigation2, self).__init__(x, y, xvel, yvel, c, r)  
        self.keys = keys

    def move(self,pressed_keys):
        self.keyboard_event(pressed_keys)
        self.bordercheck()

    def bordercheck(self):
        if self.y_pos > (h - self.radie):
            self.y_pos = h - self.radie
        if self.y_pos < self.radie:
            self.y_pos = self.radie
        if self.x_pos > (w - self.radie):
            self.x_pos = w - self.radie
        if self.x_pos < self.radie:
            self.x_pos = self.radie

    
    def keyboard_event(self, pressed_keys):
        if pressed_keys[K_RIGHT]:
            self.x_pos += 5
        if pressed_keys[K_LEFT]:
            self.x_pos -= 5
        if pressed_keys[K_UP]:
            self.y_pos -= 5
        if pressed_keys[K_DOWN]:
            self.y_pos += 5




def ball_collision(ball1,ball2):
    distance = math.sqrt((ball1.x_pos-ball2.x_pos)**2+(ball1.y_pos-ball2.y_pos)**2)
    if distance < (ball1.radie + ball2.radie):
        ball1.color = (255,0,0)
        return True
    else:     
        ball1.color = (255,255,255)



def build_random_drop():
    x = randint(40,w-40)
    y = 40
    xv = 5*(random() - 0.5)
    yv = 0
    col = (255 , 200 , 200)
    r = 40
    return Ball(x , y , xv , yv , col , r)


# ----- Start - sker en gång i uppstart av programkörning ----------------------------------------

# initiering av skärmen
wave_time = 0                                     
w = 800
h = 800
pygame.init()
pygame.display.set_caption('Skapa screen')
screen = pygame.display.set_mode((w,h),RESIZABLE) # screen är nu det buffer-fönster vi kan ritar i
mainClock = pygame.time.Clock()
                                            
# initiering av boll
b1 = Ball_smooth_navigation2(w/2 , h*2/3 , 0 , 0 , (255,255,255) , 20,('Up','Left','Down','Right'))  # vit boll att styra

# initiering av droppar
drops = []                  # lagrar alla bottar
delay_counter = 0           # räknare för att besluta om det är dags att skapa en ny droppe
delay_value = 200.00        # så här långt mellan varje droppe


# ----- Game-loop - körs om och om igen med viss maxfrekvens ----------------------------------------
while True:
    w, h = screen.get_size()
    pressed_keys = pygame.key.get_pressed()    # skapa lista med alla nertryckta tangenter
    key_events = pygame.event.get()   # alla händelser senaste varv i gameloop
    for event in key_events:        
        if event.type == QUIT:              
            pygame.quit()                   
            sys.exit()



    if delay_counter > delay_value:         #  är det dags att skapa en ny droppe?
          delay_counter = 0                 #  dvs har räknare nått till fördröjningsvärde
          new_drop = build_random_drop()
          drops.append(new_drop)            # japp
    else : delay_counter += 1               # nej, fortsätt räkna upp

    if delay_value > 10:                    # är minsta dropp-fördröjning uppnådd
         delay_value -= 0.025          # annars minska  ...det ska bli svårare och svårare
    

    # sudda        
    screen.fill((0,0,0))
    
    # flytta spelare och alla droppar
    b1.move(pressed_keys)
    for ref in drops:
         ref.move()

    # kontrollera om någon droppe träffat spelare
    for ref in drops:
         if ball_collision(b1,ref) : break     # om någon droppe träffat avslutas kollisionskontroll

    # rita
    b1.draw()
    for ref in drops:
         ref.draw()
                                 
    wave_time += 1
    print(wave_time)                                            
                                            
    pygame.display.update()                 
    mainClock.tick(60) 