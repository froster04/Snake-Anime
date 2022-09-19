import pygame
from pygame.locals import *
import time,random

SIZE=40
BACKGROUND_COLOR=(0,0,0)


class Apple:
    def __init__(self,parent_screen):
        self.image=pygame.image.load("resources/food.gif").convert()
        self.parent_screen=parent_screen
        self.x=120
        self.y=120 #to align snake and apple the apple xoordinates are multiple of size(40)
#

    def draw(self):
        
            # self.parent_screen.fill((255,255, 255))
            # for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x, self.y))
            pygame.display.flip()  # to update screen

#



    def move(self):
        self.x=random.randint(0,10)*SIZE
        self.y=random.randint(0,10)*SIZE






class Snake:
    def __init__(self, parent_screen,length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/loli-2.png").convert()
        self.x = [40]*length
        self.y = [40]*length
        self.direction = 'down'
        self.length=length



    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)






    def draw(self):
        # so that drawed blocks don't leave trail behind, they get overwritten by the fill
        # self.parent_screen.fill(BACKGROUND_COLOR)
        for i in range(self.length):
            if i!=0:
                self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
            else:
                block1 = pygame.image.load("resources/loli-2.png").convert()
                self.parent_screen.blit(block1,(self.x[i], self.y[i]))

            pygame.display.flip()  # to update screen


    


    def move_up(self):
       # self.y-=10
        self.direction = 'up'  # check why moving up decreases y coordinate

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'


    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i]=self.x[i-1]
            self.y[i]=self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] +=SIZE 
        self.draw()

     


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake & Apple Game")
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((1000, 600))
        self.surface.fill((0, 0, 0))  # fill color in window
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple=Apple(self.surface)
        self.apple.draw

    def is_collision(self,x1,y1,x2,y2):
        if x1>=x2 and x1 < x2+SIZE:
            if y1 >= y2 and y1 < y2+SIZE:
                return True
        return False

    def play_sound(self,sound):
        sound=pygame.mixer.Sound(f"resources/{sound}.mp3") #how does pytho differentaiate btw sound and sound(in parameters)
        pygame.mixer.Sound.play(sound)



    def play_background_music(self):
        pygame.mixer.music.load("usada_bgm.mp3")
        pygame.mixer.music.play()


    def render_background(self):
        bg=pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))


    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip() 

        if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
            

        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.snake.x[i],self.snake.y[i]):
                self.play_sound("crash")
                raise ValueError("Game over")




    def display_score(self):
        font=pygame.font.SysFont('arial',30)
        score=font.render(f"SCORE: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (800,10))
        pygame.display.flip()


    def show_game_over(self):
        self.render_background()
        self.surface.fill(BACKGROUND_COLOR)
        font=pygame.font.SysFont('arial',30)
        line1=font.render(f"GAME OVER! SCORE:{self.snake.length}",True , (255,255,255))
        self.surface.blit(line1, (200,300))
        line2=font.render(f"PRESS ENTER TO PLAY AGAIN. ESC TO EXIT",True , (255,255,255))
        self.surface.blit(line2, (200,350))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake=Snake(self.surface,1)
        #self.snake.draw()
        self.apple=Apple(self.surface)

        

    def run(self):
        running = True
        pause=False
        while(running):

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause=False
                        pygame.mixer.music.unpause()


                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except ValueError:
                self.show_game_over()
                pause=True
                self.reset()

            time.sleep(0.2)
           

if __name__ == "__main__":

    game = Game()
    game.run()
    pygame.display.flip()
