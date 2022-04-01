"""
MG's Tower of Hanoi for Python - Main Module
"""
import pygame

import sys


# Color Constants class
class ColorConstants():
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)
        GREEN = (0, 255, 0)
        WHITE = (173, 216, 255)
        BACKGROUND = (240, 248, 255)
        BOARD_COLOR = (153, 76, 0)
		
# Generic Block class
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
# Game positions class
class Position(Block):
    def __init__(self, pos_index,color, width, height):
        Block.__init__(self,color, width, height)
        self.pos_index = pos_index
        self.discs = []
# Game discs class
class Disc(Block):
    def __init__(self,current_pos,id,color, width, height):
        Block.__init__(self,color, width, height)
        self.current_pos = current_pos
        self.id = id
# Buttons class
class Button(Block):
    def __init__(self,text,text_color,text_size,text_font,color, width, height):
        Block.__init__(self,color, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.SysFont(text_font, text_size, False, False)
        self.text_render = self.font.render(text, 1, text_color)
        self.value = None
    def set_value(self,value):
        self.value = value
    def render_text(self):
        w = (self.width/2-(self.text_render.get_width()/2))
        h = (self.height/2-(self.text_render.get_height()/2))
        self.image.blit(self.text_render,[w,h])
# Main Menu
class MainMenu(ColorConstants):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.sprites_list = pygame.sprite.Group()
        self.btn_discs = []
        self.label = Button("WANNA PLAY?",self.BLACK,30,'Calibri',self.WHITE,500,30)
        self.label.rect.x = self.SCREEN_WIDTH/4
        self.label.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.label.render_text()
        self.sprites_list.add(self.label)
        btn = Button('CLick Me!!!',self.BLACK,30,'Calibri',self.GREEN,300,80)
        btn.rect.x = 250
        btn.rect.y = 450
        btn.render_text()
        btn.set_value(3)
        self.btn_discs.append(btn)
        self.sprites_list.add(self.btn_discs)
        # Game over buttons
        self.btn_play_again = Button("Play Again",self.BLACK,15,'Calibri',self.GREEN,130,30)
        self.btn_return = Button("Return",self.BLACK,30,'Calibri',self.GREEN,150,30)
        self.btn_next_level = Button("Next Level? Press 'S'",self.BLACK,18,'Calibri',self.GREEN,150,30)
        self.btn_level_uno = Button("Level 1",self.BLACK,18,'Calibri',self.GREEN,150,30)
        self.btn_level_dos = Button("Level 2",self.BLACK,18,'Calibri',self.GREEN,150,30)
        self.btn_level_tres = Button("Level 3",self.BLACK,18,'Calibri',self.GREEN,150,30)
        self.btn_quit = Button("Quit",self.BLACK,20,'Calibri',self.RED,70,30)
        self.btn_play_again.rect.x = self.SCREEN_WIDTH/2 - (self.btn_return.image.get_width()*2)
        self.btn_play_again.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_play_again.render_text()
        self.btn_next_level.rect.x = 100
        self.btn_next_level.set_value(4)
        self.btn_level_uno.set_value(5)
        self.btn_level_dos.set_value(6)
        self.btn_level_tres.set_value(7)
        self.btn_next_level.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_level_uno.rect.x = 200
        self.btn_level_dos.rect.x = 400
        self.btn_level_tres.rect.x = 600
        self.btn_level_uno.rect.y = 400
        self.btn_level_dos.rect.y = 400
        self.btn_level_tres.rect.y = 400
        self.btn_next_level.render_text()
        self.btn_level_uno.render_text()
        self.btn_level_dos.render_text()
        self.btn_level_tres.render_text()
        self.btn_return.rect.x = 100
        self.btn_return.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_return.render_text()
        self.btn_quit.rect.x = 400
        self.btn_quit.rect.y = self.SCREEN_HEIGHT/2 - 40
        self.btn_quit.render_text()
# Game main class
class Game(ColorConstants):
    def __init__(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        # Game sprites groups
        self.sprites_list = pygame.sprite.Group()
        self.pos_sprites_list = pygame.sprite.Group()
        # Game constants
        self.BOARD_WIDTH = SCREEN_WIDTH/2
        self.BOARD_HEIGHT = 50
        self.BOARD_X = SCREEN_WIDTH * 0.25
        self.BOARD_Y = SCREEN_HEIGHT - 55
        self.POS_WIDTH = 20
        self.POS_HEIGHT = 200
        self.DISC_WIDTH = 200
        self.DISC_HEIGHT = self.POS_WIDTH
        # Positions and discs lists
        self.positions = []
        self.discs = []
        # Draw the game board and it's positions
        self.game_board = Block(self.BOARD_COLOR, self.BOARD_WIDTH,self.BOARD_HEIGHT)
        self.game_board.rect.x= self.BOARD_X
        self.game_board.rect.y= self.BOARD_Y
        first_pos = Position(0,self.BOARD_COLOR, self.POS_WIDTH,self.POS_HEIGHT)
        first_pos.rect.x = self.BOARD_X
        first_pos.rect.y=  self.BOARD_Y - self.POS_HEIGHT
        second_pos = Position(1,self.BOARD_COLOR, self.POS_WIDTH,self.POS_HEIGHT)
        second_pos.rect.x = (self.BOARD_X + (self.BOARD_WIDTH/2)) - (self.POS_WIDTH/2)
        second_pos.rect.y= self.BOARD_Y - self.POS_HEIGHT
        third_pos = Position(2,self.BOARD_COLOR,self.POS_WIDTH,self.POS_HEIGHT)
        third_pos.rect.x = (self.BOARD_X + self.BOARD_WIDTH) - self.POS_WIDTH
        third_pos.rect.y= self.BOARD_Y - self.POS_HEIGHT
        self.positions = [first_pos,second_pos,third_pos]
        self.sprites_list.add([self.game_board,self.positions])
        self.pos_sprites_list.add(self.positions)
    # Set discs number and mim movements
    def set_n_discs(self,n_discs):
        self.n_discs = n_discs
        self.min_moves = ((2**self.n_discs)-1)
    # Draw discs method
    def draw_discs(self):
        DISC_WIDTH = 200
        DISC_HEIGHT = self.POS_WIDTH
        for i in range(0,self.n_discs):
            if i % 2 == 0:
                disc = Disc(0,i,self.RED,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
            else:
                disc = Disc(0,i,self.GREEN,(DISC_WIDTH/(i+1)),DISC_HEIGHT)
            disc.rect.x = self.BOARD_X - ((DISC_WIDTH/(i+1)/2)-(DISC_HEIGHT/2))
            disc.rect.y = (self.BOARD_Y - DISC_HEIGHT) - (DISC_HEIGHT*i)
            self.discs.append(disc)
            self.positions[0].discs.append(disc)
        self.sprites_list.add(self.discs)


# Define screen constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
# Color constants object
color = ColorConstants()
# Init pygame
pygame.init()
# Define the screen (and it's properties)
# Create main menu object
menu = MainMenu(SCREEN_WIDTH,SCREEN_HEIGHT)
# Create game object
game = Game(SCREEN_WIDTH,SCREEN_HEIGHT)
# Discs' move variables
done = False
drag = False
drop = False
move = False
game_over = False
init_game = False
disc_index = None
last_pos = [0,0]
# Moves counter
moves_counter = 0

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Sisyphus Escapes")
# Manage how fast the screen updates
clock = pygame.time.Clock()

def loop_game_screen():
    global game
    global moves_counter
    global game_over
    global move
    screen.fill(game.WHITE)
    backgroundfile = pygame.image.load("skyline_large.png")
    screen.blit(backgroundfile,(0,0))
    # Title line
    pygame.draw.line(screen, game.BLACK, [0, 60], [SCREEN_WIDTH,60], 5)
    # Text font,size, bold and italic
    #Add two buttons with backgound color green
    menu.sprites_list.add([menu.btn_level_tres, menu.btn_level_dos,menu.btn_level_uno])
    font = pygame.font.SysFont('Calibri', 30, False, False)
    title_font = pygame.font.SysFont('Calibri', 50, False, False)
    # Info Texts
    game_title = title_font.render("Sisyphus Escapes", True, color.BLACK)
    screen.blit(game_title, [((SCREEN_WIDTH/2)-(game_title.get_width()/2)),20])
    if init_game:
        player_moves = font.render("Player moves: "+str(moves_counter), True, color.BLACK)
        min_moves = font.render("Max Moves: "+str(game.min_moves), True, color.BLACK)
        screen.blit(player_moves, [20, 80])
        screen.blit(min_moves, [20, 110])
        if moves_counter > game.min_moves:
            game_over = True
            game_over_text = font.render("Game Over!!!", True, color.RED)
            screen.blit(game_over_text, [((SCREEN_WIDTH/2)-(game_over_text.get_width()/2)),SCREEN_HEIGHT/2])
            menu.sprites_list.add([menu.btn_quit])
            menu.sprites_list.remove([menu.btn_discs,menu.label, menu.btn_level_uno, menu.btn_level_dos, menu.btn_level_tres])
        if game_over:
            menu.sprites_list.draw(screen)
            if len(game.positions[2].discs) == game.n_discs:
                if moves_counter == game.min_moves:
                    game_over_title = font.render("Congratulations! You Won! :)", True, color.BLACK)
                    screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
                    #add a button to direct user to next level
                    menu.sprites_list.add([menu.btn_next_level,menu.btn_quit])
                    #menu.sprites_list.remove([menu.btn_level_uno, menu.btn_level_dos, menu.btn_level_tres,menu.btn_discs,menu.btn_return,menu.btn_play_again,menu.label])
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                           if event.key == pygame.K_s:
                                game.sprites_list.remove([game.discs])
                                game.positions[2].discs = []
                                #game.set_n_discs()
                                moves_counter = 0
                                game.discs = []
                                game.set_n_discs(4)
                                game.draw_discs()
                                game_over = False
                                menu.sprites_list.remove([menu.btn_return,menu.btn_play_again, menu.label])
                                if moves_counter == game.min_moves:
                                    game_over_title = font.render("Congratulations! You Won! :)", True, color.BLACK)
                                    screen.blit(game_over_title, [((SCREEN_WIDTH/2)-(game_over_title.get_width()/2)),SCREEN_HEIGHT/2])
                                    #add a button to direct user to next level
                                    menu.sprites_list.add([menu.btn_next_level,menu.btn_quit])
                                    #menu.sprites_list.remove([menu.btn_level_uno, menu.btn_level_dos, menu.btn_level_tres,menu.btn_discs,menu.btn_return,menu.btn_play_again,menu.label])
                                    for event in pygame.event.get():
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_s:
                                                game.sprites_list.remove([game.discs])
                                                game.positions[2].discs = []
                                                #game.set_n_discs()
                                                moves_counter = 0
                                                game.discs = []
                                                game.set_n_discs(5)
                                                game.draw_discs()
                                                game_over = False
                                                menu.sprites_list.remove([menu.btn_return,menu.btn_play_again, menu.label])
                                                #models.MainMenu.btn_next_level.set_value(3)
                        
                
        else:
            if drag:
                if move:
                    pos = pygame.mouse.get_pos()
                    game.discs[disc_index].rect.x = pos[0] - (game.discs[disc_index].width/2)
                    game.discs[disc_index].rect.y = pos[1] - (game.discs[disc_index].height/2)
            elif drop:
                if move:
                    current_pos = game.discs[disc_index].current_pos
                    new_pos = None
                    change = False
                    turn_back = True
                    position = pygame.sprite.spritecollideany(game.discs[disc_index],game.pos_sprites_list)
                    if position != None:
                        new_pos = position.pos_index
                        if new_pos != current_pos:
                            disc_length = len(position.discs)
                            if disc_length == 0:
                                turn_back = False
                                change = True
                            elif game.discs[disc_index].id > position.discs[disc_length-1].id:
                                turn_back = False
                                change = True
                    if change:
                        moves_counter = moves_counter + 1
                        game.positions[current_pos].discs.remove(game.discs[disc_index])
                        game.discs[disc_index].current_pos = new_pos
                        game.positions[new_pos].discs.append(game.discs[disc_index])
                        new_pos_length = len(game.positions[new_pos].discs)
                        game.discs[disc_index].rect.x = game.positions[new_pos].rect.x - ((game.DISC_WIDTH/(game.discs[disc_index].id+1)/2)-(game.DISC_HEIGHT/2))
                        game.discs[disc_index].rect.y = (game.BOARD_Y - game.DISC_HEIGHT) - (game.DISC_HEIGHT*(new_pos_length-1))
                        #Check if the game is over
                        if (len(game.positions[2].discs) == game.n_discs):
                            game_over = True
                            menu.sprites_list.add([menu.btn_play_again,menu.btn_quit,menu.btn_return])
                            menu.sprites_list.remove([menu.label,menu.btn_discs])
                    if turn_back:
                        game.discs[disc_index].rect.x = last_pos[0]
                        game.discs[disc_index].rect.y = last_pos[1]
                    move = False
        game.sprites_list.draw(screen)
    else:
        menu.sprites_list.draw(screen)

# -------- Main Game Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            drop = False
            if init_game:
                if not game_over:
                    for i in range(0,game.n_discs):
                        if game.discs[i].is_clicked():
                            current_pos = game.discs[i].current_pos
                            pos_length = len(game.positions[current_pos].discs)
                            if game.discs[i] == game.positions[current_pos].discs[pos_length-1]:
                                disc_index = i
                                last_pos = [game.discs[i].rect.x,game.discs[i].rect.y]
                                move = True
                else:
                    if menu.btn_quit.is_clicked():
                        done = True
                    if menu.btn_play_again.is_clicked():
                        game.sprites_list.remove(game.discs)
                        game.positions[2].discs = []
                        moves_counter = 0
                        game.discs = []
                        game.draw_discs()
                        game_over = False
                    if menu.btn_return.is_clicked():
                        menu.sprites_list.remove([menu.btn_play_again,menu.btn_return,menu.btn_quit])
                        menu.sprites_list.add([menu.btn_discs,menu.label])
                        game.sprites_list.remove(game.discs)
                        init_game = False
            else:
                for i in range(0,1000):
                    if menu.btn_discs[i].is_clicked():
                        game.set_n_discs(menu.btn_discs[i].value)
                        game.sprites_list.remove(game.discs)
                        game.discs = []
                        game.positions[2].discs = []
                        moves_counter = 0
                        game.draw_discs()
                        init_game = True
                        game_over = False
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            drag = False
            drop = True
    loop_game_screen()

    # --- update  screen.
    pygame.display.flip()
    # --- Limit to 60 frames per second
    clock.tick(60)
pygame.quit()
