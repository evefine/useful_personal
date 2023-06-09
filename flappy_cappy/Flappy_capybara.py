#!/usr/bin/env python
# coding: utf-8

# In[1]:





# In[2]:





# In[1]:


import pygame
import random
FPS = 30
pygame.init()

# Can make it easier by increasing column gap and shorter jumps
#easy_mode = True
easy_mode = False

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
    def __init__(self, x, y,vel=-10):
        self.x = x
        self.y = y
        self.vel = 0
        self.gravity = 1
        self.jump_vel = vel
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
    def __init__(self, x, minimum=50,gap=150):
        self.x = x
        self.height = 0
        self.gap = gap
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


import pandas as pd
import pygame
import os
import csv

global mode
mode = 0

def write_new_highscore(score, mode,new=False):
    scores_csv = 'scores.csv'
    if not new:
        df_scores = pd.read_csv(scores_csv)
        scores = df_scores['High Score']
        # Change high score of appropriate mode
        scores[mode] = score
    else:
        # Set original high scores to 0 if new csv file
        scores = [0, 0]
        scores[mode] = score
    with open('scores.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Mode", "High Score"])
        writer.writerow([0, scores[0]])
        writer.writerow([1, scores[1]])

        
def check_highscore(score):
    scores_csv = 'scores.csv'
    # Check if have a scores.csv file
    if scores_csv not in os.listdir('.'):
        # If not, write a new one and return current score
        write_new_highscore(score,mode,new=True)
        return score
    else:
        df = pd.read_csv(scores_csv)
        # Check if your score is higher than the high score for that mode
        if int(df['High Score'][mode]) < int(score):
            write_new_highscore(score, mode)
            return score
        else:
            return df['High Score'][mode]

modes = ['easy', 'less easy']

def try_again(score):
    # Initialize Pygame
    pygame.init()

    # Create the main window
    root = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Capy ded :(")

    # Create a font object
    font = pygame.font.SysFont(None, 48)
    
    # Check the highscore
    high_score = check_highscore(score)

    # Render the text
    text = font.render("Try again?", True, (255, 255, 255))
    score_text = font.render("Score = {}".format(score), True, (255, 255, 255))
    highscore_text = font.render("High Score in {} mode = {}".format(modes[mode],high_score), True, (255, 255, 255))
    
    # Get the dimensions of the text
    text_width = text.get_width()
    text_height = text.get_height()
    
    score_text_width = score_text.get_width()
    score_text_height = score_text.get_height()
    
    highscore_text_width = highscore_text.get_width()
    highscore_text_height = highscore_text.get_height()

    # Get the center of the screen
    screen_center = (root.get_width() // 2, root.get_height() // 2)

    # Create a rectangle for the text
    text_rect = text.get_rect(center=screen_center)
    score_text_rect = score_text.get_rect(center = (screen_center[0], screen_center[1] - text_height))
    highscore_text_rect = highscore_text.get_rect(center = (screen_center[0], screen_center[1] - text_height - score_text_height))
    
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
                    ret = False
                # Check if the "No" button was clicked
                elif button2_rect.collidepoint(event.pos):
                    running = False
                    ret = True

        # Draw the background
        root.fill((0, 20, 80))

        # Draw the text
        root.blit(text, text_rect)
        root.blit(score_text, score_text_rect)
        root.blit(highscore_text, highscore_text_rect)
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
    return ret


def choose_mode():
    global mode
    # Initialize Pygame
    pygame.init()

    # Create the main window
    root = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Choose mode")

    # Create a font object
    font = pygame.font.SysFont(None, 48)

    # Render the text
    text = font.render("Choose mode", True, (255, 255, 255))

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
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the "Yes" button was clicked
                if button1_rect.collidepoint(event.pos):
                    running = False
                    mode = 0
                    return True
                # Check if the "No" button was clicked
                elif button2_rect.collidepoint(event.pos):
                    mode = 1
                    running = False
                    return False

        # Draw the background
        root.fill((0, 20, 80))

        # Draw the text
        root.blit(text, text_rect)

        # Draw the buttons
        pygame.draw.rect(root, (0, 255, 0), button1_rect)
        pygame.draw.rect(root, (255, 0, 0), button2_rect)

        # Draw the text on the buttons
        button1_text = font.render("Easy", True, (255, 255, 255))
        button2_text = font.render("Less easy", True, (255, 255, 255))
        root.blit(button1_text, button1_rect.move(5, 5))
        root.blit(button2_text, button2_rect.move(10, 5))

        # Update the display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()


# make screen for easy and hard mode selection

    
def main():
    easy = choose_mode()
    easy_gap = 200
    easy_dist = 180
    pygame.init()
    done = False
    if easy:
        capybara = Capybara(100, 200,vel=-8)
        pipes = [Pipe(400,gap=easy_gap)]
    else:
        capybara = Capybara(100, 200)
        pipes = [Pipe(400)]
    score = Score()
    dead = False
    clock = pygame.time.Clock()
    pygame.display.set_caption("Flappy Cappy!")

    while not dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
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
        if easy:
            distance = easy_dist
        else:
            distance = PIPE_DISTANCE
        if pipes[-1].x + PIPE_IMG.get_width() < WIN_WIDTH - distance:
                add_pipe = True

        if add_pipe:
            if pipes[-1].height > 375:
                minimum = pipes[-1].height - 250
            else:
                minimum = 50
            if easy:
                pipes.append(Pipe(WIN_WIDTH,minimum=minimum,gap=easy_gap))
            else:
                pipes.append(Pipe(WIN_WIDTH,minimum))
            add_pipe = False

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        # check for capybara hitting the ground or ceiling
        if capybara.y + CAPYBARA_IMG.get_height() >= WIN_HEIGHT or capybara.y < 0:
            dead = True


        # draw the window
        WINDOW.blit(BG_IMG, (0, 0))
        for pipe in pipes:
            pipe.draw(WINDOW)

        score.draw(WINDOW)
        capybara.draw(WINDOW)

        pygame.display.update()
        clock.tick(30)
        
        if dead:
            done = try_again(str(score.score))
            if done:
                pygame.quit()
                return False
            if not done:
                main()

        
if __name__ == "__main__":
    main()
    pygame.quit()
    quit()


# In[ ]:


score = 4
print("Score = {} \nTry again?".format(score))


# In[ ]:




