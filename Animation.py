import pygame
import random
import time
import math
import glob
from options import SCREENSIZE, SUCCESS, FAILED, CustomColor

customcolor = CustomColor()

class Rain(object):

    def __init__(self, screen, stage = 1, height = 160, speed = 3, color = (180, 215, 228, 255), numdrops = 10):
        'Create and reuse raindrop particles'
        self.screen     = screen
        self.drops      = []
        self.height     = height
        self.speed      = speed
        self.color      = color
        self.numdrops   = numdrops
        self.asset_path = "/Users/gimjian/3학년2학기/visualArt/final_project/asset"
        self.stage = stage
        self.stage_count = 0
        self.mans = self.select_stage(self.stage)
        print(self.mans)
        for i in range(self.numdrops):
            # Randomize the size of the raindrop.
            raindropscale = random.randint(40, 100) / 100.0
            w, h = 3, int(raindropscale * self.height)
            # The bigger the raindrop, the faster it moves.
            velocity = raindropscale * self.speed/10.0
            pic = pygame.Surface((w, h), pygame.SRCALPHA, 32).convert_alpha()
            colorinterval = float(self.color[3] * raindropscale)/h
            r, g, b = self.color[:3]
            for j in range(h):
                # The smaller the raindrop, the dimmer it is.
                a = int(colorinterval * j)
                pic.fill( (r, g, b, a), (1, j, w-2, 1) )
                #pygame.draw.circle(pic, (r, g, b, a), (1, h-2), 2)
                pic = self.randomly_selected_person(self.mans)

            drop = Rain.Drop(self.speed, velocity, pic)
            self.drops.append(drop)

    def select_stage(self, stage):
        print(f"changed stage : {stage}")
        # select the current stage
        if stage == 1:
            ret = glob.glob("/Users/gimjian/3학년2학기/visualArt/final_project/asset/image/ten/*.jpeg")
        elif stage == 2:
            ret = glob.glob("/Users/gimjian/3학년2학기/visualArt/final_project/asset/image/twenty/*.jpeg")
        return ret

    def randomly_selected_person(self, filenames):
        # choose the random person image from path, and return it
        index = random.randint(0, len(filenames)-1)
        file = filenames[index]
        man = pygame.image.load(file)
        man = pygame.transform.scale(man, (40, 40))
        return man

    def Timer(self, now):
        ' Render the rain'
        dirtyrects = []
        for drop in self.drops:
            r = drop.Render(self.screen, now)
            if r:
                i = r.collidelist(dirtyrects)
                if i > -1:
                    dirtyrects[i].union_ip(r)
                else:
                    dirtyrects.append(r)
        return dirtyrects


    def AdjustSpeed(self, adj):
        newspeed = self.speed + adj
        newspeed = max(1, newspeed)
        newspeed = min(100, newspeed)
        self.speed = newspeed
        for drop in self.drops:
            drop.SetSpeed(newspeed)
        print ('Rain speed: %d' % newspeed)
    
    def touch(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for drop in self.drops:
            touch_result = drop.touch(mouse_x, mouse_y)
            if touch_result == SUCCESS:
                self.stage_count += 1
                

    class Drop(object):
        ' Rain drop used by rain generator'
        nexttime = 0   # The next time the raindrop will draw
        interval = .01 # How frequently the raindrop should draw

        def __init__(self, speed, scale, pic):
            ' Initialize the rain drop'
            self.speed = speed
            self.scale = scale
            self.pic = pic
            self.size = pic.get_size()
            self.SetSpeed(speed)
            self.pos = [random.random() * SCREENSIZE[0], -random.randint(-SCREENSIZE[1], SCREENSIZE[1])]
            self.currentspeed = speed

        def SetSpeed(self, speed):
            ' Speed up or slow down the drop'
            self.speed = speed
            self.velocity = self.scale * self.speed/10.0

        def Reset(self):
            ' Restart the drop at the top of the screen.'
            self.pos = [random.random() * SCREENSIZE[0], -random.random() * self.size[1] - self.size[1]]
            self.currentspeed = self.speed

        def Render(self, screen, now):
            ' Draw the rain drop'
            if now < self.nexttime:
                return None
            self.nexttime = now + self.interval
            oldrect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]+self.currentspeed)
            self.pos[1] += self.currentspeed
            newrect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
            r = oldrect.union(newrect)
            screen.blit(self.pic, self.pos)
            self.currentspeed += self.velocity
            if self.pos[1] > SCREENSIZE[1]:
                self.Reset()
            return r

        def touch(self, x_pos, y_pos):
            if self.objectInRange(x_pos, y_pos):
                self.Reset()
                return True
        def objectInRange(self, mouse_x, mouse_y, d = 50):

            distance = math.sqrt((self.pos[0] - mouse_x) ** 2 + (self.pos[1] - mouse_y) ** 2)
            # if rain in range, remove it. 
            if distance < d:
                return True
            else:
                return False

def select_background_image(stage):
    # need to modify 
    if stage == 1:
        return pygame.image.load('/Users/gimjian/3학년2학기/visualArt/final_project/asset/image/sky/8am.jpeg')
    elif stage == 2:
        return pygame.image.load('/Users/gimjian/3학년2학기/visualArt/final_project/asset/image/sky/10am.jpeg')

def update_stage(original_rain, original_background, screen):
    new_rain = Rain(screen, original_rain.stage + 1)
    if new_rain.stage > 2 : # max stage 
        new_rain.stage = 1
    new_rain.stage_count = 0

    # change background image
    new_bg = select_background_image(new_rain.stage)

    # resize the background image to screen size 
    new_bg = pygame.transform.scale(new_bg, SCREENSIZE)
    return new_rain, new_bg

def select_time(stage, font_ = 'freesansbold.ttf', fontsize = 15):
    font = pygame.font.Font(font_, fontsize)

    if stage  == 1:
        text = font.render('8AM', True, customcolor.yellow)
        textRect = text.get_rect()
        textRect.center = (20, 10)
        return text, textRect

    elif stage == 2:
        text = font.render('10AM', True, customcolor.yellow)
        textRect = text.get_rect()
        textRect.center = (20, 10)
        return text,textRect

def update_count_display(screen, rain):
    count, countRect = display_count_time(rain.stage, rain.stage_count)
    screen.blit(count, countRect)

def display_count_time(stage, stage_count, font_ = 'freesansbold.ttf', fontsize = 15):
   font = pygame.font.Font(font_, fontsize)
   # font = pygame.font.Font(font = font_, fontsize = fontsize)
   text = font.render(f'{(stage-1)*10 + stage_count}/{stage * 10} years last', True, customcolor.yellow)
   textRect = text.get_rect()
   textRect.center = (60, 30)
   return text, textRect
    
def set_intermediate_screen(screen, stage, wait = 1):
    
    inter_bg = pygame.image.load('/Users/gimjian/3학년2학기/visualArt/final_project/asset/image/inter/black.png')
    screen.blit(inter_bg, (0, 0))

    font_ ='freesansbold.ttf'
    fontsize = 100 
    font = pygame.font.Font(font_, fontsize)
    text = font.render(f'stage : {stage}', True, customcolor.yellow)
    textRect = text.get_rect()
    textRect.center = (320, 240)
    screen.blit(text, textRect)
    pygame.display.flip()
    pygame.time.delay(wait * 3000)

def main():
    # Initialize pygame
    pygame.init()
    pygame.key.set_repeat(500, 30)
    screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
    
    # Create rain generator
    rain = Rain(screen)
    print ('right arrow to increase speed, left arrow to decrease speed.')
    
    bg_image = select_background_image(rain.stage)
    bg_image = pygame.transform.scale(bg_image, SCREENSIZE)

    # Main loop
    quitgame = 0
    
    set_intermediate_screen(screen, 1)
   
    while not quitgame:

        # Emulate CPU usage.
        # Commenting this out will no longer matter,
        # as the raindrops update on a timer.
        time.sleep(.01)

        # Draw rain
        dirtyrects = rain.Timer(time.time())

        # Update the screen for the dirty rectangles only
        pygame.display.update(dirtyrects)
        
        # Fill the background with the dirty rectangles only
        
        screen.blit(bg_image, (0, 0))
        text, textrect = select_time(rain.stage)
        screen.blit(text, textrect)
        update_count_display(screen, rain)

        # Look for user events
        pygame.event.pump()
        for e in pygame.event.get():
            if e.type in [pygame.QUIT]:
                quitgame = 1
                break
            elif e.type == pygame.KEYDOWN:
                if e.key == 27:
                    quitgame = 1
                    break
                elif e.key in [pygame.K_LEFT, pygame.K_UP]:
                    rain.AdjustSpeed(-1)
                elif e.key in [pygame.K_RIGHT, pygame.K_DOWN]:
                    rain.AdjustSpeed(1)
           
            if e.type in [pygame.MOUSEBUTTONDOWN]:
                rain.touch()
                print(f"count of touch in stage {rain.stage} : {rain.stage_count}")
                update_count_display(screen, rain)
                if rain.stage_count >= 10:
                    set_intermediate_screen(screen, rain.stage + 1)
                    rain, bg_image = update_stage(rain, bg_image, screen)
    
    # Terminate pygame
    pygame.quit()

if __name__ == "__main__":
    main()