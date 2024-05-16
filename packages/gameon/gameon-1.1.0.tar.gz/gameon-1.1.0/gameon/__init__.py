import pygame
import random as r
import sys
import time as t
import keyboard as kb
import os
pygame.init()

#screen
screen = None
screen_once = True

#colors
screen_color = (255,255,255)
color_map = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "orange": (255, 165, 0),
    "pink": (255, 192, 203),
    "purple": (128, 0, 128),
    "brown": (165, 42, 42),
    "turquoise": (64, 224, 208),
    "lime": (0, 255, 0),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "gray": (128, 128, 128),
    "indigo": (75, 0, 130),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0)
}

#time
clock = pygame.time.Clock()
frames = 120

#window
package_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(package_dir, 'icon.ico')
icon_img = pygame.image.load(icon_path)
pygame.display.set_icon(icon_img)
pygame.display.set_caption('GameOn')

#mouse_click
left_click = False
right_click = False

#key_pressed
keys = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','space','1','2','3','4','5','6','7','8','9','0']
pygame_keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_SPACE,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,pygame.K_0]
keys_boolean = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]

def fill(color):
    global screen,screen_color
    if not isinstance(color,tuple):
        if color.lower() in color_map:
            screen_color = color_map[color.lower()]
    elif isinstance(color, tuple):
        screen_color = color
    pass

def window(width, height):
    global screen,left_click,right_click,screen_color,screen_once

    #define the screen once
    if screen_once:
        screen = pygame.display.set_mode((width,height))
        screen_once = False

    #fill the background color
    screen.fill(screen_color)

    #handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True   
            if event.button == 3:
                right_click = True
        for i in range(len(keys)):
            if event.type == pygame.KEYDOWN:
                if event.key == pygame_keys[i]:
                    keys_boolean[i] = True
    pass

def fps(frames=120):
    clock.tick(frames)
    return clock.get_fps()
    pass

def icon(image):
    if isinstance(image, str):
        pygame.display.set_icon(pygame.image.load(image))
    else:
        pygame.display.set_icon(image)
    pass

def title(title):
    pygame.display.set_caption(title)
    pass

def update():
    pygame.display.flip()
    pass

def delay(time):
    pygame.time.delay(time)
    pass

import time as t

class Timer:
    def __init__(self, seconds, countdown=False):
        self.sec = seconds
        self.start_time = None
        self.run_timer = True
        self.timer = 0
        self.start_timer = True
        self.countdown = countdown
        self.run_once = True
    def start(self, seconds='default'):
        if self.run_once:
            if seconds != 'default':
                self.sec = seconds
            self.run_once = False
        if self.start_timer:
            self.start_time = t.time()
            self.start_timer = False
        self.current_time = t.time()
        if self.run_timer:
            if self.start_time != None:
                if not self.countdown:
                    self.timer = self.current_time - self.start_time
                else:    
                    self.timer = self.sec - (self.current_time - self.start_time)

        if not self.countdown:
            if self.timer >= self.sec:
                self.run_timer = False
                self.timer = self.sec
        else:
            if self.timer <= 0:
                self.run_timer = False
                self.timer = 0
    def stop(self):
        self.run_timer = False
        pass
    def restart(self, seconds='default'):
        self.new_time = seconds
        self.start_time = None
        self.run_timer = True
        if self.new_time != 'default':
            self.sec = self.new_time
        self.start_timer = True
        pass
    def time(self, integer=True):
        if integer:
            return int(self.timer)
        else:
            return self.timer   
        pass
    def __bool__(self):
        if not self.countdown:
            if self.timer != self.sec:
                return False
            else:
                return True
        else:
            if self.timer != 0:
                return False
            else:
                return True
    pass

def circle(x,y,color,radius,border_radius=0):
    global screen
    if border_radius == 0:
        if not isinstance(color, tuple):
            if color.lower() in color_map:
                pygame.draw.circle(screen, color_map[color.lower()], (x,y), radius)
        elif isinstance(color, tuple):
            pygame.draw.circle(screen, color, (x,y), radius)
    else:
        if not isinstance(color, tuple):
            if color.lower() in color_map:
                pygame.draw.circle(screen, color_map[color.lower()], (x,y), radius, border_radius)
        elif isinstance(color, tuple):
            pygame.draw.circle(screen, color, (x,y), radius, border_radius)
    pass

def rect(x,y,width,height,color='black',border_radius=0):
    global screen
    if border_radius == 0:
        if not isinstance(color, tuple):
            if color.lower() in color_map:
                pygame.draw.rect(screen, color_map[color.lower()], (x,y,width,height))
        elif isinstance(color, tuple):
            pygame.draw.rect(screen, color, (x,y,width,height))
    else:
        if not isinstance(color, tuple):
            if color.lower() in color_map:
                pygame.draw.rect(screen, color_map[color.lower()], (x,y,width,height), border_radius)
        elif isinstance(color, tuple):
            pygame.draw.rect(screen, color, (x,y,width,height), border_radius)
    pass

def line(x1,y1,x2,y2,color,thickness):
    if not isinstance(color, tuple):
        if color.lower() in color_map:
            pygame.draw.line(screen, color_map[color.lower()], (x1,y1), (x2,y2), thickness)
    elif isinstance(color, tuple):
        pygame.draw.line(screen, color, (x1,y1), (x2,y2), thickness)
    pass

def image(image,x,y):
    global screen
    if isinstance(image, str):
        screen.blit(pygame.image.load(image), (x,y))
    elif isinstance(image, pygame.Surface):
        screen.blit(image, (x,y))
    pass

def rotate(image, angle):
    if isinstance(image, str):
        return pygame.transform.rotate(pygame.image.load(image), angle)
    elif isinstance(image, pygame.Surface):
        return pygame.transform.rotate(image, angle)
    pass

def resize(image, width, height):
    if isinstance(image, str):
        return pygame.transform.scale(pygame.image.load(image), (width, height))
    elif isinstance(image, pygame.Surface):
        return pygame.transform.scale(image, (width, height))
    pass

def click(button='left',one=False):
    global left_click, right_click
    mouse = pygame.mouse.get_pressed()
    if button == 'left':
        if not one:
            if mouse[0] == True:
                return True
            if mouse[0] == False:
                return False
        if one:
            if left_click:
                left_click = False
                return True
            else:
                return False
            
    if button == 'right':
        if not one:
            if mouse[2] == True:
                return True
            if mouse[2] == False:
                return False
        if one:
            if right_click:
                right_click = False
                return True
            else:
                return False
    pass

def press(key,one=False):
    for i in range(len(keys)):
        if one:
            if key == keys[i]:
                if keys_boolean[i] == True:
                    keys_boolean[i] = False
                    return True
                else:
                    return False
    if not one:
        if kb.is_pressed(key):
            return True
        else:
            return False
    pass 

def pos(xy='xy'):
    mx,my = pygame.mouse.get_pos()
    if xy == 'x':
        return mx
    if xy == 'y':
        return my
    if xy == 'xy':
        return [mx,my]
    pass

def text(text, color, x, y, size=50 , font='Calibri', show=True):
    if not isinstance(color, tuple):
        if color.lower() in color_map:
            screen.blit(pygame.font.SysFont(font, size).render(text, show, color_map[color.lower()]), (x,y))
    elif isinstance(color, tuple):
        screen.blit(pygame.font.SysFont(font, size).render(text, show, color), (x,y))
    pass

def button(image, x,y, retract=True, retract_length=10, button='left', one=False, show=True):
    mouse_pos = pygame.mouse.get_pos()
    if show:
        if not retract:
            if isinstance(image, str):
                screen.blit(pygame.image.load(image), (x,y))
                if pygame.Rect(x,y,pygame.image.load(image).get_width(),pygame.image.load(image).get_height()).collidepoint(mouse_pos):
                    if click(button, one):
                        return True
                    else:
                        return False
            elif isinstance(image, pygame.Surface):
                screen.blit(image, (x,y))
                if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                    if click(button, one):
                        return True
                    else:
                        return False

        if retract:
            if isinstance(image, str):
                if not one:
                    if pygame.Rect(x,y,pygame.image.load(image).get_width(),pygame.image.load(image).get_height()).collidepoint(mouse_pos):
                        if click(button):
                            screen.blit(resize(image,pygame.image.load(image).get_width()-retract_length,pygame.image.load(image).get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                            return True
                        else:
                            screen.blit(pygame.image.load(image), (x,y))
                            return False
                    else:
                        screen.blit(pygame.image.load(image), (x,y))
                        return False
                    
                if one:
                    if pygame.Rect(x,y,pygame.image.load(image).get_width(),pygame.image.load(image).get_height()).collidepoint(mouse_pos):
                        if click(button):
                            screen.blit(resize(image,pygame.image.load(image).get_width()-retract_length,pygame.image.load(image).get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                            return click(button, one)
                        else:
                            screen.blit(pygame.image.load(image), (x,y))
                            return click(button, one)
                    else:
                        screen.blit(pygame.image.load(image), (x,y))
                        return False
                    
            elif isinstance(image, pygame.Surface):
                if not one:
                    if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                        if click(button):
                            screen.blit(resize(image,image.get_width()-retract_length,image.get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                            return True
                        else:
                            screen.blit(image, (x,y))
                            return False
                    else:
                        screen.blit(image, (x,y))
                        return False
                    
                if one:
                    if pygame.Rect(x,y,image.get_width(),image.get_height()).collidepoint(mouse_pos):
                        if click(button):
                            screen.blit(resize(image,image.get_width()-retract_length,image.get_height()-retract_length), (x+(retract_length/2),y+(retract_length/2)))
                            return click(button, one)
                        else:
                            screen.blit(image, (x,y))
                            return click(button, one)
                    else:
                        screen.blit(image, (x,y))
                        return False
    pass

class Player:
    def __init__(self,image,x,y,left=None,right=None,up=None,down=None,jump=False,speed=3,height=20,sides=True):
        self.image = image
        self.x = x
        self.y = y
        self.left = left
        self.right = right
        self.up = up
        self.down  = down
        self.jump = jump
        self.speed = speed
        self.height = height
        self.sides = sides
        self.player_width = 0
        self.player_width = 0
        self.jumped = True
        self.jump_velocity = self.height
        pass
    def move(self):
        if not self.sides:
            if self.left != None:
                if kb.is_pressed(self.left):
                    self.x -= self.speed
            if self.right != None:
                if kb.is_pressed(self.right):
                    self.x += self.speed
            if self.up != None:
                if kb.is_pressed(self.up):
                    self.y -= self.speed
            if self.down != None:
                if kb.is_pressed(self.down):
                        self.y += self.speed
            if self.jump != None:
                if self.jumped:
                    self.y -= self.jump_velocity
                    self.jump_velocity -= 1
                    if self.jump_velocity < -self.height:
                        self.jumped = False
                        self.jump_velocity = self.height
        if self.sides:
            if self.left != None:
                if kb.is_pressed(self.left) and self.x > 0:
                    self.x -= self.speed
            if self.right != None:
                if kb.is_pressed(self.right) and self.x < screen.get_width() - self.player_width:
                    self.x += self.speed
            if self.up != None:
                if kb.is_pressed(self.up) and self.y > 0:
                    self.y -= self.speed
            if self.down != None:
                if kb.is_pressed(self.down) and self.y < screen.get_height() - self.player_height:
                    self.y += self.speed
            if self.jump != None:
                if self.jumped:
                    self.y -= self.jump_velocity
                    self.jump_velocity -= 1
                    if self.jump_velocity < -self.height:
                        self.jumped = False
                        self.jump_velocity = self.height
        if isinstance(self.image, str):
            screen.blit(pygame.image.load(self.image), (self.x,self.y))
            self.player_width = pygame.image.load(self.image).get_width()
            self.player_height = pygame.image.load(self.image).get_height()
        elif isinstance(self.image, pygame.Surface):
            screen.blit(self.image, (self.x,self.y))
            self.player_width = self.image.get_width()
            self.player_height = self.image.get_height()
        pass
    pass

def box(image,x,y,collision=True):
    global player_x,player_y,player_width,player_height,player_speed
    player_rect = pygame.Rect(player_x,player_y,player_width,player_height)
    col_box = pygame.Rect(x,y,image.get_width(),image.get_height())
    if collision:
        if player_rect.colliderect(col_box):
            if player_rect.right >= col_box.x and player_rect.right <= col_box.x + (player_speed + 2) :
                player_x = col_box.x - player_rect.width
            if player_rect.left >= col_box.right - (player_speed + 2) and player_rect.left <= col_box.right:
                player_x = col_box.right
            if player_rect.top <= col_box.bottom and player_rect.top >= col_box.bottom - (player_speed + 2):
                player_y = col_box.bottom
            if player_rect.bottom >= col_box.top and player_rect.bottom <= col_box.top + (player_speed + 2):
                player_y = col_box.top - player_rect.height
    screen.blit(image, (x,y))
    pass

def collide(rect1, rect2):
    mx,my = pygame.mouse.get_pos()
    if isinstance(rect1, tuple) and isinstance(rect2, tuple):
        if pygame.Rect(rect1).colliderect(pygame.Rect(rect2)):
            return True
        else:
            return False
    elif isinstance(rect1, tuple) and rect2 == 'mouse':
        if pygame.Rect(rect1).collidepoint((mx,my)):
            return True
        else:
            return False
    elif isinstance(rect2, tuple) and rect1 == 'mouse':
        if pygame.Rect(rect2).collidepoint((mx,my)):
            return True
        else:
            return False
    pass

def load(image):
    return pygame.image.load(image)
    pass