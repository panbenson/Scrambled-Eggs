"""Author: Benson Pan
   Date: April 20, 2014
   Description: Scrambled Eggs - A Flappy Bird Remake
"""
import pygame, random

#Load all levels
top_pipe = pygame.image.load("./Resources/toppipe.png")
bot_pipe = pygame.image.load("./Resources/botpipe.png")
cracked = pygame.image.load("./Resources/cracked.png")
splat1 = pygame.image.load("./Resources/splat1.png")
splat2 = pygame.image.load("./Resources/splat2.png")
splat3 = pygame.image.load("./Resources/splat3.png")
splat4 = pygame.image.load("./Resources/splat4.png")
splat5 = pygame.image.load("./Resources/splat5.png")
splat6 = pygame.image.load("./Resources/splat6.png")
splat7 = pygame.image.load("./Resources/splat7.png")
splat8 = pygame.image.load("./Resources/splat8.png")
splat9 = pygame.image.load("./Resources/splat9.png")
background = pygame.image.load("./Resources/background.PNG")
title = pygame.image.load("./Resources/title.png")
game_over = pygame.image.load("./Resources/game_over.png")

class Top_pipe(pygame.sprite.Sprite):
    def __init__(self, width, height):
    #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.image = top_pipe
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.__width = width
        self.__height = height
        self.__dx = 0
        self.rect.bottom = (self.__height / 2) - 50
        self.rect.left = self.__width

    def move_pipe(self):
        self.__dx = 2

    def get_bottom(self):
        #Returns the y value of the bottom of this image, for relative distance for bottom pipe
        return self.rect.bottom

    def get_x(self):
        #returns the x value of the image, to check if it has reached half the screen
        return self.rect.right

    def check_boundaires(self):
        #The method checks if the image reaches the end, stops and resets if it has, and return a boolean value if it has
        if self.rect.right <= 0:
            self.reset() #Calls the reset method
            self.rect.bottom = random.randrange(50, (self.__height - 150))
            return True
        else:
            return False

    def pause(self):
        #Pauses animation
        self.__dx = 0

    def reset(self):
        #The method is called by the check_boundaries method or by the main program to reset the pipe
        self.__dx = 0
        self.rect.left = self.__width
        self.rect.bottom = random.randrange(50, (self.__height - 150)) #randomize pipe for next game

    def update(self):
        if self.__dx != 0:
            self.rect.centerx -= self.__dx

class Bottom_pipe(pygame.sprite.Sprite):
    def __init__(self, width, height, top_pipe):
    #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.image = bot_pipe
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.__width = width
        self.__height = height
        self.__dx = 0
        self.rect.top = top_pipe + 125
        self.rect.left = self.__width

    def move_pipe(self):
        self.__dx = 2

    def pause(self):
        #Pauses animation
        self.__dx = 0

    def reset(self, top_pipe):
        #The method only runs in main if the Top_pipe's check_boundaires is true. It stops the pipe and positions it
        self.__dx = 0
        self.rect.left = self.__width
        self.rect.top = top_pipe + 125

    def update(self):
        if self.__dx != 0:
            self.rect.centerx -= self.__dx

class Egg(pygame.sprite.Sprite):
    def __init__(self):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.image = cracked
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.__y = 0 #Used to store y value later
        self.__x = 250 #Used to store x value
        self.__dy = 0
        self.__gravity = 0
        self.__pic_num = 1
        self.__animate = False
        self.rect.centerx = self.__x
        self.rect.bottom = 240

    def start(self):
        self.__gravity = 0.5

    def jump(self):
        self.__dy = -5

    def get_top(self):
        #Returns the y value of the top of the egg for screen boder collisions
        return self.rect.top

    def get_bot(self):
        #Returns the y value of the bottom of the egg for screen boder collisions
        return self.rect.bottom

    def update(self):
        if self.__animate and self.__pic_num < 10:
            self.animate_splat()
        elif not self.__animate and self.__dy >= -5:
            self.__dy += self.__gravity
        self.rect.centery += self.__dy

    def set_animate(self):
        #sets the self.__animate attribute to True
        self.__animate = True

    def get_pic_num(self):
        #Returns the animation pic_num attribute
        return self.__pic_num

    def reset(self):
        #resets all attributes to original when called
        self.__dy = 0
        self.__gravity = 0
        self.image = cracked
        self.rect = self.image.get_rect()
        self.rect.bottom = 240
        self.rect.centerx = 250
        self.__animate = False
        self.__pic_num = 1

    def get_image(self):
        #uses a dictionary as a case to find the correct image
        return {
            1 : splat1,
            2 : splat2,
            3 : splat3,
            4 : splat4,
            5 : splat5,
            6 : splat6,
            7 : splat7,
            8 : splat8,
            9 : splat9
            }.get(self.__pic_num, splat9) #returns splat9 when the image number is not there

    def animate_splat(self):
        #animates the splat of the egg
        if self.__pic_num == 1:
            #Saves the first y value of the egg before to be used
            self.__y = self.rect.centery

        #calls the get_image method
        self.image = self.get_image()

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = self.__x
        self.rect.centery = self.__y

        self.__pic_num += 1

class Score_keeper(pygame.sprite.Sprite):
    def __init__(self, width):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font('./Resources/Quicksand-Regular.ttf', 50)
        self.__text = ""
        self.__score = 0
        self.__width = width

    def add_score(self):
        #Adds 1 to the score everytime it is called
        self.__score += 1

    def reset(self):
        #Reset the score attribute to 0 when called
        self.__score = 0

    def update(self):
        self.__text = str(self.__score)
        self.image = self.__font.render(self.__text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.centerx = self.__width / 2

    def get_score(self):
        #returns the score for highscore checking
        return self.__score

class Background(pygame.sprite.Sprite):
        def __init__(self, width):
            #Calls the parent class' method
            pygame.sprite.Sprite.__init__(self)

            self.image = background
            self.image = self.image.convert()
            self.rect = self.image.get_rect()

            self.__dy = 1
            self.__width = width
            #The following variable is to control the movement of the background
            #to every other update method called
            self.__every_other = True

        def set_x_zero(self):
            self.rect.left = self.__width

        def update(self):
            if self.rect.right <= 0:
                self.rect.left = self.__width
            if self.__every_other:
                self.rect.left -= self.__dy
            self.__every_other = not self.__every_other

class Title_overlay(pygame.sprite.Sprite):
    def __init__(self, width, height):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.image = title
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.__width = width
        self.__height = height

        self.rect.centerx = self.__width / 2
        self.rect.centery = self.__height / 2

class Button(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y, text):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font('./Resources/Quicksand-Regular.ttf', 40)
        self.__hover_font = pygame.font.Font("./Resources/Quicksand-Bold.ttf", 40)
        self.__text = ""
        self.__x = 0
        self.__y = 0
        self.image = self.__font.render(self.__text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()

        self.__width = width
        self.__height = height
        self.__x = x
        self.__y = y
        self.__text = text

    def hover(self, is_hover):
        if is_hover:
            self.image = self.__hover_font.render(self.__text, 1, (255, 255, 204))
        else:
            self.image = self.__font.render(self.__text, 1, (255, 255, 255))

    def update(self):
        self.rect = self.image.get_rect()

        self.rect.centery = self.__height / 2 + self.__y
        self.rect.centerx = self.__width / 2 + self.__x

    def get_rect(self):
        #returns the rect, used for mouse collision
        return self.rect

class Game_over_overlay(pygame.sprite.Sprite):
    def __init__(self, width, height):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.image = game_over
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.__width = width
        self.__height = height

        self.rect.centerx = self.__width / 2
        self.rect.centery = self.__height / 2

class Score_label(pygame.sprite.Sprite):
    def __init__(self, width, height, identity):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font('./Resources/Quicksand-Regular.ttf', 30)
        self.__text = ""
        self.__score = 0
        self.__highscore = 0
        self.__width = width
        self.__height = height
        self.__type = identity #Updates as either a score or highscore label

    def update_highscore(self, score):
        #Checks if the current score is greater than the high score and stores it
        self.__score = score

        if self.__score > self.__highscore:
            self.__highscore = score

    def update(self):
        #Renders the text base on the self.__type attribute
        if self.__type == "score":
            self.__text = "Score: %d"%(self.__score)
            self.image = self.__font.render(self.__text, 1, (255, 255, 255))
            self.rect = self.image.get_rect()

            self.rect.centerx = self.__width / 2
            self.rect.centery = self.__height / 2 - 50

        else:
            self.__text = "Highscore: %d" %(self.__highscore)
            self.image = self.__font.render(self.__text, 1, (255, 255, 255))
            self.rect = self.image.get_rect()

            self.rect.centerx = self.__width / 2
            self.rect.centery = self.__height / 2

class Instructions(pygame.sprite.Sprite):
    def __init__(self, width, height):
        #Calls the parent class' method
        pygame.sprite.Sprite.__init__(self)

        self.__font = pygame.font.Font('./Resources/Quicksand-Regular.ttf', 20)
        self.__text = "Press space to fly!"
        self.__visible = True

        self.image = self.__font.render(self.__text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = width
        self.rect.centery = height
