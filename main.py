import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Walking/1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Walking/2.png').convert_alpha()
        player_walk_3 = pygame.image.load('Walking/3.png').convert_alpha()
        player_walk_4 = pygame.image.load('Walking/4.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4]
        self.player_index = 0
        self.player_jump = pygame.image.load('Walking/1.png').convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 550))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 550:
            self.gravity = -22

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 550:
            self.rect.bottom = 550

    def animation_state(self):
        if self.rect.bottom < 550:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "worm":
            worm_frame1 = pygame.image.load("worm/skyll-frame1.png").convert_alpha()
            worm_frame2 = pygame.image.load("worm/skyll-frame2.png").convert_alpha()
            worm_frame3 = pygame.image.load("worm/skyll-frame3.png").convert_alpha()
            self.frames = [worm_frame1, worm_frame2, worm_frame3]
            y_pos = 450
        else:
            poop_1 = pygame.image.load('dung1.png').convert_alpha()
            poop_2 = pygame.image.load('dung2.png').convert_alpha()
            poop_3 = pygame.image.load('dung3.png').convert_alpha()
            self.frames = [poop_1, poop_2, poop_3]
            y_pos = 550

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames): self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self):
            self.animation_state()
            self.rect.x -= 6
            self.destroy()

    def destroy(self):
            if self.rect.x <= -100:
                self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'Score:{current_time}', False, "White")
    score_rect = score_surface.get_rect(center=(528, 105))
    screen.blit(score_surface, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((1056, 672))
pygame.display.set_caption("UNDERCROFT")
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0
test_font = pygame.font.Font("static/PixelifySans-Bold.ttf", 50)
test_font2 = pygame.font.Font("static/PixelifySans-Medium.ttf", 50)

# GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

background_surface = pygame.image.load("bulkhead-wallsx3.png").convert_alpha()
# INTRO SCREEN
player_stand = pygame.image.load("Walking/1.png").convert_alpha()
player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(490, 250))

game_name = test_font.render("UNDERCROFT", False, 'black')
game_name_rect = game_name.get_rect(center=(525, 90))

game_namex = test_font.render("UNDERCROFT", False, "white")
game_namex_rect = game_namex.get_rect(center=(530, 95))

game_text = test_font2.render("PRESS  SPACE  TO  RUN", False, "black")
game_text_rect = game_text.get_rect(center=(525, 485))

game_textx = test_font2.render("PRESS  SPACE  TO  RUN", False, "white")
game_textx_rect = game_textx.get_rect(center=(525, 490))

# TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

# MUSIC
# /usx-qqnx-jgg

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["worm", "poop", "poop", "poop"])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(background_surface, (0, 0))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)

        screen.blit(game_namex, game_namex_rect)
        screen.blit(game_name, game_name_rect)

        score_message = test_font.render(f'Your score: {score}', False, "Black")
        score_message_rect = score_message.get_rect(center=(525, 485))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_textx, game_textx_rect)
            screen.blit(game_text, game_text_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
