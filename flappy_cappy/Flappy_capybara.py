#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[2]:





# In[1]:


import pygame
import random
FPS = 30
pygame.init()

if True:
    WIN_WIDTH = 600
    WIN_HEIGHT = 600
    WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Flappy Capybara")

    # load the capybara image
    CAPYBARA_IMG = pygame.image.load('capybara.png')
    CAPYBARA_IMG = pygame.transform.scale(CAPYBARA_IMG, (60, 45))

    # load the background image
    BG_IMG = pygame.image.load('background.png')
    BG_IMG = pygame.transform.scale(BG_IMG, (WIN_WIDTH, WIN_HEIGHT))

    # load the pipe image
    PIPE_IMG = pygame.image.load('pipe.png')
    PIPE_IMG = pygame.transform.scale(PIPE_IMG, (70, 400))

    # set the font for the score
    SCORE_FONT = pygame.font.SysFont('comicsans', 30)


PIPE_GAP = 150   # spacing between pipes
PIPE_VEL = 3   # speed of pipes moving to the left
PIPE_DISTANCE = 140  # horizontal distance between pipes


class Capybara:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.gravity = 1
        self.jump_vel = -10
        self.height = self.y
        self.image = CAPYBARA_IMG

    def jump(self):
        self.vel = self.jump_vel

    def move(self):
        self.vel += self.gravity
        self.y += self.vel

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.image)

class Pipe:
    def __init__(self, x, minimum=50):
        self.x = x
        self.height = 0
        self.gap = PIPE_GAP
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        self.passed = False
        self.set_height(minimum=minimum)

    def set_height(self,minimum=50):
        self.height = random.randrange(minimum, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= PIPE_VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, capybara):
        capybara_mask = capybara.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - capybara.x, self.top - round(capybara.y))
        bottom_offset = (self.x - capybara.x, self.bottom - round(capybara.y))

        b_point = capybara_mask.overlap(bottom_mask, bottom_offset)
        t_point = capybara_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

    def passed_pipe(self, capybara):
        if capybara.x > self.x and not self.passed:
            self.passed = True
            return True

        return False

    @staticmethod
    def add_pipe(pipes):
        pipes.append(Pipe(WIN_WIDTH))


class Score:
    def __init__(self):
        self.score = 0
        self.x = 10
        self.y = 10

    def draw(self, window):
        score_label = SCORE_FONT.render(f'Score: {self.score}', 1, (255, 255, 255))
        window.blit(score_label, (self.x, self.y))

    def update(self):
        self.score += 1


# In[2]:


import tkinter as tk

import pygame

def try_again():
    # Initialize Pygame
    pygame.init()

    # Create the main window
    root = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Capy ded :(")

    # Create a font object
    font = pygame.font.SysFont(None, 48)

    # Render the text
    text = font.render("Try again?", True, (255, 255, 255))

    # Get the dimensions of the text
    text_width = text.get_width()
    text_height = text.get_height()

    # Get the center of the screen
    screen_center = (root.get_width() // 2, root.get_height() // 2)

    # Create a rectangle for the text
    text_rect = text.get_rect(center=screen_center)

    # Create a rectangle for the "Yes" button
    button1_rect = pygame.Rect(0, 0, 100, 50)
    button1_rect.center = (screen_center[0] - 75, screen_center[1] + 50)

    # Create a rectangle for the "No" button
    button2_rect = pygame.Rect(0, 0, 100, 50)
    button2_rect.center = (screen_center[0] + 75, screen_center[1] + 50)

    # Set up a loop to handle events
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the "Yes" button was clicked
                if button1_rect.collidepoint(event.pos):
                    running = False
                    return False
                # Check if the "No" button was clicked
                elif button2_rect.collidepoint(event.pos):
                    running = False
                    return True

        # Draw the background
        root.fill((0, 20, 80))

        # Draw the text
        root.blit(text, text_rect)

        # Draw the buttons
        pygame.draw.rect(root, (0, 255, 0), button1_rect)
        pygame.draw.rect(root, (255, 0, 0), button2_rect)

        # Draw the text on the buttons
        button1_text = font.render("Yes!", True, (255, 255, 255))
        button2_text = font.render("No", True, (255, 255, 255))
        root.blit(button1_text, button1_rect.move(5, 5))
        root.blit(button2_text, button2_rect.move(10, 5))

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()



def main():
    pygame.init()
    done = False
    capybara = Capybara(100, 200)
    pipes = [Pipe(400)]
    score = Score()
    dead = False
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Cappy!")
    while not dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #pygame.quit()
                dead = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if pipes and capybara.y - CAPYBARA_IMG.get_height() > 0:
                        capybara.jump()

        # move the capybara
        capybara.move()

        # move the pipes and check for collisions
        add_pipe = False
        pipes_to_remove = []
        for pipe in pipes:
            if pipe.collide(capybara):
                dead = True
                #pygame.quit()
                

            if pipe.x + PIPE_IMG.get_width() < 0:
                pipes_to_remove.append(pipe)
            
            if pipe.passed_pipe(capybara):
                score.update()

            pipe.move()
        if pipes[-1].x + PIPE_IMG.get_width() < WIN_WIDTH - PIPE_DISTANCE:
                add_pipe = True

        if add_pipe:
            if pipes[-1].height > 375:
                minimum = 150
            else:
                minimum = 50
            pipes.append(Pipe(WIN_WIDTH,minimum))
            add_pipe = False

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # check for capybara hitting the ground or ceiling
        if capybara.y + CAPYBARA_IMG.get_height() >= WIN_HEIGHT or capybara.y < 0:
            dead = True
         
        if dead:
            done = try_again()
            if done:
                pygame.quit()
                return False
            if not done:
                main()

        # draw the window
        WINDOW.blit(BG_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(WINDOW)

        score.draw(WINDOW)
        capybara.draw(WINDOW)

        pygame.display.update()
        clock.tick(30)


        
        
if __name__ == "__main__":
    playing = True
    while playing:
        playing = main()
    quit()


# In[ ]:





# In[ ]:




