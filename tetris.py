import pygame
import random
pygame.init()

#Gmae Constants
GAME_FONT = pygame.font.Font(r'C:\Users\Rajeswar Sharma\Documents\python\tetrisFont.ttf',32)
OVER_FONT = pygame.font.Font(r'C:\Users\Rajeswar Sharma\Documents\python\tetrisFont.ttf',60)
Start_FONT = pygame.font.Font(r'C:\Users\Rajeswar Sharma\Documents\python\tetrisFont.ttf',16)


TETRIS_GREEN = pygame.image.load(r'C:\Users\Rajeswar Sharma\Documents\python\TETRIS_Green.png')
TETRIS_BLUE = pygame.image.load(r'C:\Users\Rajeswar Sharma\Documents\python\TETRIS.png')
CLOCK = pygame.time.Clock()
MARGIN = 2
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
DISPLAY_WIDTH = 480
DISPLAY_HEIGHT= 640
display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
SINGLE_BLOCK = 36 # dimension of a single tile

CLR_WHITE = (225,225,225)
CLR_BLACK = (0,0,0)
CLR_GRAY = (110, 110, 110)
CLR_GREEN=(65, 222, 44)
CLR_BLUE=(52, 152, 235)
CLR_ORANGE = (255, 66, 3)
ROWS = 16
COLUMNS = 12

SHAPES={'B':[[0,1,2],
            [1,5,9]],

        'T':[[0,1,2,5],
             [1,4,5,9],
             [1,4,5,6],
             [1,5,6,9]],

        'L': [[1,5,8,9], 
              [0,4,5,6], 
              [1,2,5,9], 
              [4,5,6,10]],
        
        'S':[[1,2,4,5], 
            [1,5,6,10]]}

#Util functions
 
def init():
    global Score
    global block_update 
    global grid  
    global block_stack
    Score = 0 
    block_update = pygame.USEREVENT
    pygame.time.set_timer(block_update,500)
    grid = [[False for i in range(COLUMNS)] for j in range(ROWS)] 
    block_stack=[[False for i in range(COLUMNS)] for j in range(ROWS)]
    
 # convert the shape list to Tile value
 # Each x,y values of the tile are the coordinate of the tile in the grid
def convert_shape_to_Tile(shape_list):
    shape_tile=list()
    for i in shape_list:
        if i >= 4:
            index_x = i//4
            index_y = i%4
        else:
            index_x=0
            index_y=i
        shape_tile.append([index_x,index_y])
    return shape_tile

def draw_grid(display):
    global DISPLAY_WIDTH
    for i in range(0,DISPLAY_HEIGHT//40):
        for j in range(0,DISPLAY_WIDTH//40):
            if grid[i][j]==True:
                pygame.draw.rect(display,CLR_GREEN,[j*40+MARGIN,i*40+MARGIN,SINGLE_BLOCK,SINGLE_BLOCK])

def draw_shape(vertical_shift,horizontal_shift,shape_list,shape_number,shape_tile):
    global grid 
    grid = [x[:]for x in block_stack]
    for x,y in shape_tile:
        grid[x+vertical_shift][y+horizontal_shift]=True

def restart(display,Score):
    font_text = OVER_FONT.render("GAME OVER!",False,CLR_BLUE,CLR_BLACK)
    font_rect = font_text.get_rect()
    font_rect.center = 640,200
    display.blit(font_text,font_rect)
    restart_text = Start_FONT.render("Press Space to Restart",False,CLR_ORANGE,CLR_BLACK)
    restart_rect = restart_text.get_rect()
    restart_rect.center = 640,550
    display.blit(restart_text,restart_rect)

def start(display):
    start_text = Start_FONT.render("Press Space to Start",False,CLR_ORANGE,CLR_BLACK)
    start_rect = start_text.get_rect()
    start_rect.center = 640,550
    display.blit(start_text,start_rect)

vertical_shift=0                                                    # Its value will be changed by 1 to move the shape 1 block down 
horizontal_shift= 4                                                 # 4 = Center of the game screen , initially shape will appear at the center of the screen
shape_list = random.choice(list(SHAPES.values()))                   # selecting a random shape from the shape dict
shape_number = random.randint(0,len(shape_list)-1)
shape_tile = convert_shape_to_Tile(shape_list[shape_number])

next_shape_list = random.choice(list(SHAPES.values()))              # geting the next shape
next_shape_number = random.randint(0,len(next_shape_list)-1)
next_shape_tile = convert_shape_to_Tile(next_shape_list[next_shape_number])

text_next = GAME_FONT.render("Next Shape",False,CLR_WHITE,CLR_BLACK)    # Fonts and texts
text_next_rect = text_next.get_rect()
text_next_rect.center = (640,500)

score_text = GAME_FONT.render("SCORE: 0",False,CLR_ORANGE,CLR_BLACK)
score_rect = score_text.get_rect()
score_rect.center=640,300 

hit_flag = False # To detect collision of shape with fixed shapes
IMAGE = TETRIS_BLUE #Tetris logo
IMAGE_Ctr = 0
game_started = False
game_over = False

#Game Loop
init()
while True:
    
    if game_started == True:
        display.fill(CLR_BLACK)
        pygame.draw.line(display,CLR_BLUE,(480,0),(480,640))                                #Line to separate playable area and score screen
        
        display.blit(IMAGE,(510,0))                                                         #Tetris Logo
        draw_shape(vertical_shift,horizontal_shift,shape_list,shape_number,shape_tile)
        
        display.blit(text_next,text_next_rect)

        score_text = GAME_FONT.render("SCORE: "+str(Score),False,CLR_ORANGE,CLR_BLACK)
        score_rect = score_text.get_rect()
        score_rect.center=640,300 
        display.blit(score_text,score_rect)
        
        
        for x,y in next_shape_tile:                                                         #Displaying the next shape
            pygame.draw.rect(display,CLR_GREEN,[y*40+580,x*40+360,SINGLE_BLOCK,SINGLE_BLOCK])
        
        draw_grid(display)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT:
                vertical_shift+=1
                if IMAGE_Ctr == 0: 
                    IMAGE = TETRIS_GREEN
                else: IMAGE = TETRIS_BLUE
                IMAGE_Ctr= (IMAGE_Ctr+1)%2
            
            if event.type == pygame.KEYDOWN:  
                if (event.key == pygame.K_UP or event.key == pygame.K_SPACE): # Rorate Shape
                    temp_number = (shape_number+1)%len(shape_list) # temp number/shape number maps to the next rotation of the shape 
                    temp_tile = convert_shape_to_Tile(shape_list[temp_number])
                    T = True
                    for x,y in temp_tile: #checking if rotaion is possible
                        if y+horizontal_shift <0 or y+horizontal_shift > 11 or block_stack[x+vertical_shift][y+horizontal_shift] == True:
                            T=False
                            break   
                    if T: # if rotation is possible, update the tiles and shape number 
                        shape_number=temp_number
                        shape_tile = temp_tile

                if event.key == pygame.K_RIGHT:
                    R = True
                    for x,y in shape_tile:
                        if y+horizontal_shift >= 11 or block_stack[x+vertical_shift][y+horizontal_shift+1] == True:
                            R=False
                            break
                    if R:
                        horizontal_shift+=1
                    
                if event.key == pygame.K_LEFT:
                    L = True
                    for x,y in shape_tile:
                        if y+horizontal_shift <= 0 or block_stack[x+vertical_shift][y+horizontal_shift-1] == True:
                            L=False
                            break
                    if L:
                        horizontal_shift-=1
                                            
        for x,y in shape_tile: # checking of collision 
            if block_stack[x][y+horizontal_shift] == True: #GameOver condition
                game_over=True
                game_started=False
                hit_flag = True
                break
            if x+vertical_shift > 14:
                hit_flag = True
                break
            if block_stack[x+vertical_shift+1][y+horizontal_shift] == True:
                hit_flag = True
                break

        if hit_flag == True: # if collide = true  fix the shape in block_stack array
            for x,y in shape_tile:
                block_stack[x+vertical_shift][y+horizontal_shift]=True
            vertical_shift=0
            horizontal_shift=4 #random.randint(0,8)
            
            shape_tile = next_shape_tile #Getting new shapes
            shape_number = next_shape_number  
            shape_list = next_shape_list
            
            next_shape_list = random.choice(list(SHAPES.values()))
            next_shape_number = random.randint(0,len(next_shape_list)-1)
            next_shape_tile = convert_shape_to_Tile(next_shape_list[next_shape_number])
            
            hit_flag = False

        for i in reversed(range(ROWS)): # checking for filled rows
            flag = True
            for j in range(COLUMNS):
                if block_stack[i][j] == False:
                    flag = False
                    break
            if flag == True: # if true increase the score and shift the upper blocks down
                Score+=2
                for k in reversed(range(0,i+1)): # Shifting upper blocks down
                    for j in range(COLUMNS):
                        if  k-1 > 0:
                            block_stack[k][j]=block_stack[k-1][j]      
                        else:
                            block_stack[k][j]=False
                                            
    else: # Game is not started or Game Over
        if game_over == True:
            restart(display,Score)
        else :
            start(display)
        pygame.draw.line(display,CLR_BLUE,(480,0),(480,640))
        display.blit(IMAGE,(510,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.USEREVENT:
                if IMAGE_Ctr == 0: 
                    IMAGE = TETRIS_GREEN
                else: IMAGE = TETRIS_BLUE
                IMAGE_Ctr= (IMAGE_Ctr+1)%2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    init()
                    display.fill(CLR_BLACK)
                    game_over=False
                    game_started=True
    
    pygame.display.update()