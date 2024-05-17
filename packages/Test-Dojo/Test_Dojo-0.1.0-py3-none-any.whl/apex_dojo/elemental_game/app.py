import pygame

pygame.init()
pygame.display.set_caption("Elemental Game")

screen_width, screen_height = 1280, 720
player_width, player_height = 40, 40
player_1_x, player_1_y = 0, screen_height - player_height
player_2_x, player_2_y = screen_width - player_width, screen_height - player_height
ball_size = 10
player_velocity, ball_velocity = 10, 50

screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

player_1 = pygame.Surface((player_width, player_height))
player_1.fill("red")
player_2 = pygame.Surface((player_width, player_height))
player_2.fill("blue")
player_1_hp = 1
player_2_hp = 1

player_1_ball = []
player_2_ball = []

run = True


def move_left(x: int):
    if x > 0:
        x -= player_velocity
    return x


def move_right(x: int):
    if x < screen_width - player_width:
        x += player_velocity
    return x


def move_up(y: int):
    if y > 0:
        y -= player_velocity
    return y


def move_down(y: int):
    if y < screen_height - player_height:
        y += player_velocity
    return y


while run:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            run = False

        if event.type == pygame.KEYDOWN:
            if player_1_hp > 0 and event.key == pygame.K_e:
                player_1_ball_x = player_1_x + player_width
                player_1_ball_y = player_1_y + (player_height - ball_size) / 2
                player_1_ball.append((player_1_ball_x, player_1_ball_y))
            if player_2_hp > 0 and event.key == pygame.K_l:
                player_2_ball_x = player_2_x + player_width
                player_2_ball_y = player_2_y + (player_height - ball_size) / 2
                player_2_ball.append((player_2_ball_x, player_2_ball_y))

    if player_1_hp > 0:
        if keys[pygame.K_a]:
            player_1_x = move_left(player_1_x)
        if keys[pygame.K_d]:
            player_1_x = move_right(player_1_x)
        if keys[pygame.K_w]:
            player_1_y = move_up(player_1_y)
        if keys[pygame.K_s]:
            player_1_y = move_down(player_1_y)

    if player_2_hp > 0:
        if keys[pygame.K_LEFT]:
            player_2_x = move_left(player_2_x)
        if keys[pygame.K_RIGHT]:
            player_2_x = move_right(player_2_x)
        if keys[pygame.K_UP]:
            player_2_y = move_up(player_2_y)
        if keys[pygame.K_DOWN]:
            player_2_y = move_down(player_2_y)

    screen.fill("black")

    for idx, (player_1_ball_x, player_1_ball_y) in enumerate(player_1_ball):
        player_1_ball_x += ball_velocity
        player_1_ball[idx] = (player_1_ball_x, player_1_ball_y)
        if (
            player_2_x + player_width >= player_1_ball[idx][0] >= player_2_x
            and player_2_y <= player_1_ball[idx][1] <= player_2_y + player_width
        ):
            player_1_ball.pop(idx)
            player_2_hp -= 1
            if player_2_hp == 0:
                player_2.fill("white")

    for idx, (player_2_ball_x, player_2_ball_y) in enumerate(player_2_ball):
        player_2_ball_x -= ball_velocity
        player_2_ball[idx] = (player_2_ball_x, player_2_ball_y)
        if (
            player_1_x <= player_2_ball[idx][0] <= player_1_x + player_width
            and player_1_y <= player_2_ball[idx][1] <= player_1_y + player_width
        ):
            player_2_ball.pop(idx)
            player_1_hp -= 1
            if player_1_hp == 0:
                player_1.fill("white")

    player_1_balls = [(x + ball_velocity, y) for x, y in player_1_ball]
    player_2_balls = [(x - ball_velocity, y) for x, y in player_2_ball]

    player_1_balls = [(x, y) for x, y in player_1_balls if x < screen_width]
    player_2_balls = [(x, y) for x, y in player_2_balls if x > 0]

    for player_1_ball_x, player_1_ball_y in player_1_ball:
        pygame.draw.rect(
            screen, "yellow", (player_1_ball_x, player_1_ball_y, ball_size, ball_size)
        )

    for player_2_ball_x, player_2_ball_y in player_2_ball:
        pygame.draw.rect(
            screen, "white", (player_2_ball_x, player_2_ball_y, ball_size, ball_size)
        )

    pygame.draw.rect(
        player_1,
        "yellow",
        (
            (player_width - ball_size) / 2,
            (player_height - ball_size) / 2,
            ball_size,
            ball_size,
        ),
    )
    screen.blit(player_1, (player_1_x, player_1_y))

    pygame.draw.rect(
        player_2,
        "white",
        (
            (player_width - ball_size) / 2,
            (player_height - ball_size) / 2,
            ball_size,
            ball_size,
        ),
    )

    screen.blit(player_2, (player_2_x, player_2_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
