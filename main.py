import pygame,sys
from random import randint

def display_score():
    current_time=int(pygame.time.get_ticks()/1000) - start_time
    score_surface=game_font.render(f'Score : {current_time}',False,(64,64,64))
    score_rect=score_surface.get_rect(center=(400,50))
    SCREEN.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:
                SCREEN.blit(snail_surface,obstacle_rect)
            else:
                SCREEN.blit(fly_surface,obstacle_rect)

        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > 0]

        return obstacle_list
    else:
        return []


def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface,player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index=0
        player_surface = player_walk[int(player_index)]

pygame.init()

SCREEN=pygame.display.set_mode((800,400))
pygame.display.set_caption("runner game(amir hossein)")
Clock=pygame.time.Clock()
game_font=pygame.font.Font('font/Pixeltype.ttf', 50)

jump_sound=pygame.mixer.Sound('audio/jump.mp3')
jump_sound.set_volume(0.5)

bg_music=pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1)


sky_surface=pygame.image.load("graphics/Sky.png")
ground_surface=pygame.image.load("graphics/ground.png")

# Snail 
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]


obstacle_rect_list=[]

player_walk_1=pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2=pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0
player_jump=pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surface=player_walk[player_index]
player_rect=player_surface.get_rect(midbottom=(80,300))
player_gravity=0

player_stand=pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand=pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect=player_stand.get_rect(center=(400,200))

game_name=game_font.render('Runner(amir hossein soltan poor) ',False,(111,196,169))
game_name_rect=game_name.get_rect(center=(400,80))

game_message=game_font.render('press space to run ',False,(111,196,169))
game_message_rect=game_message.get_rect(center=(400,330))

game_active=False
start_time=0

score=0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer=pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer=pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300: 
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
                    jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surface = snail_frames[snail_frame_index] 

            if event.type == fly_animation_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surface = fly_frames[fly_frame_index] 

    if game_active:
        SCREEN.blit(sky_surface,(0,0))
        SCREEN.blit(ground_surface,(0,300))
        score = display_score()
        
        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # SCREEN.blit(snail_surf,snail_rect)

        # Player 
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        player_animation()
        SCREEN.blit(player_surface,player_rect)


        # Obstacle movement 
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision 
        game_active = collisions(player_rect,obstacle_rect_list)
        
    else:
        SCREEN.fill((94,129,162))
        SCREEN.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = game_font.render(f'Your score: {score}',False,(111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        SCREEN.blit(game_name,game_name_rect)

        if score == 0: SCREEN.blit(game_message,game_message_rect)
        else: SCREEN.blit(score_message,score_message_rect)

    pygame.display.update()
    Clock.tick(60)
