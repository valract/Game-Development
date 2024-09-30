import pygame
import random
from pygame.locals import(RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, K_z, K_x)

pygame.init()
WIDTH, HEIGHT = 1366, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Fight')
missile_sound = pygame.mixer.Sound('images/missile.wav')
enemy_sound = pygame.mixer.Sound('images/enemy.wav')
laser_sound = pygame.mixer.Sound('images/laser.wav')

def update():
    player.update_1(pressed_key)
    enemies.update()
    misiles.update()
    score_text.update(frames)
    laser_text.update(f'LASER: {player.laser_timer}')


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.lasers = [
            pygame.image.load("images/laser1.png").convert_alpha(),
            pygame.image.load("images/laser2.png").convert_alpha(),
            pygame.image.load("images/laser3.png").convert_alpha(),
            pygame.image.load("images/laser4.png").convert_alpha(),
        ]
        self.surf = pygame.image.load("images/player3.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.collide_rect = pygame.Rect(0, 0, 0, 0)
        self.laser_timer = 700
        self.laser_bool1 = False
        self.laser_bool2 = False

    def update_1(self, pressed_keys):
        global total_frames
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_key[K_z] and total_frames > 30:
            missile_sound.play()
            missile = Missile(self.rect)
            all_sprites.add(missile)
            misiles.add(missile)
            total_frames =  0
        if self.laser_bool1:
            self.laser_timer += 1
            if self.laser_timer == 700:
                self.laser_bool1 = False
        elif self.laser_bool2 and self.laser_timer > 0:
            self.x = self.rect[0] + 85
            self.y = self.rect[1] + 5
            self.collide_rect = pygame.Rect(self.x, self.y, self.lasers[0].get_rect()[2], self.lasers[0].get_rect()[3])
            screen.blit(random.choice(self.lasers), (self.x, self.y)); self.laser_timer -= 1
            if self.laser_timer == 0:
                self.laser_bool1 = True
                self.laser_bool2 = False
        elif pressed_keys[K_x]:
            laser_sound.play()
            self.laser_bool2 = True


        if self.rect.top <= 20:
            self.rect.top = 20
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT


class Stars(pygame.sprite.Sprite):
    def __init__(self):
        super(Stars, self).__init__()
        self.surf = pygame.Surface((1, 1))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(random.randint(0, 1366), random.randint(0, 768))
        )


class Missile(Player, pygame.sprite.Sprite):
    def __init__(self, player_pos):
        super(Missile, self).__init__()
        self.missile_len = 10
        self.missile_hei = 5
        self.surf = pygame.Surface((self.missile_len, self.missile_hei))
        self.rect = player_pos.copy()
        self.rect[:] = (player_pos[0] + 80, player_pos[1] + 15, self.missile_len, self.missile_hei) # Avoids Dimension Changing

    def update(self):
        self.rect.move_ip(5, 0)
        self.surf.fill((255, 255, 255))
        if self.rect.left > WIDTH:
            self.kill()


class Lives(pygame.sprite.Sprite):
    def __init__(self, x_axis):
        super(Lives, self).__init__()
        self.surf = pygame.Surface((x_axis, 15))
        self.surf.fill((255, 255, 255))
        self.surf.fill((255, 0, 0), pygame.Rect(1, 1, x_axis-2, 13))
        self.rect = self.surf.get_rect(
            center=(
                x_axis/2, 15
            )
        )


class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.id = "ENEMY"
        self.surf = pygame.image.load("images/astriod.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH + 20, WIDTH + 100),
                random.randint(40, HEIGHT-10),
        ))
        self.speed = random.randint(5, 10) * 0.8

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


font_obj = pygame.font.Font("freesansbold.ttf", 32)

class Text(pygame.sprite.Sprite):
    def __init__(self, l, h, color, txt):
        super(Text, self).__init__()
        self.color = color
        self.surf = font_obj.render("", True, self.color, (0, 0, 0))
        self.rect = self.surf.get_rect(
            center=(
                l, h
            )
        )
        self.txt = txt

    def update(self, to_frames):
        self.surf = font_obj.render(self.txt + str(to_frames), True, self.color, (0, 0, 0))

# Number of Lives
super_constant, lives_main = 500, 0
lives = Lives(super_constant)
score_text = Text(10, HEIGHT-20, (255, 255, 255), "Score: ")
laser_text = Text(600, 25, (0, 255, 0), "")
clock = pygame.time.Clock()
player = Player()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
misiles = pygame.sprite.Group()
all_sprites.add(player, lives, score_text, laser_text)

for i in range(600):
    stars = Stars()
    all_sprites.add(stars)

image = pygame.image.load("images/laser1.png").convert_alpha()
image = pygame.Surface((10, 15))
ADD_EVENT = pygame.USEREVENT + 1
LASER_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_EVENT, 250)

run = True
total_frames = 0
frames = 0

while run:
    if lives.surf.get_at((3, 3)) == (0, 0, 0):
        lives.surf.fill((255, 255, 255), pygame.Rect(0, 0, 1, 13))
        player.kill()
        run = False
    for events in pygame.event.get():
        if events.type == QUIT:
            run = False
        elif events.type == ADD_EVENT:
            new_enemy = Enemy()
            ids = random.randint(0, 50)
            if ids >= 48:
                new_enemy.surf = pygame.image.load("images/Health.png").convert_alpha()
                new_enemy.id = "HEALTH"
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
    pressed_key = pygame.key.get_pressed()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    for enemy in enemies:
        if player.collide_rect.colliderect(enemy):
            enemy.kill()
            player.collide_rect = pygame.Rect(0, 0, 0, 0)
    if pygame.sprite.spritecollideany(player, enemies):
        en = pygame.sprite.spritecollide(player, enemies, True)
        if en[0].id == "HEALTH":
            lives.surf.fill((255, 0, 0), pygame.Rect(1, 1, super_constant - 2, 13))
            lives_main = 0

        else:
            constant = super_constant - int(en[0].speed * 10)
            lives.surf.fill((0, 0, 0), pygame.Rect(constant-lives_main, 1, super_constant-constant-1, 13))
            clock.tick(30)
            screen.fill((255, 0, 0))
            lives_main += super_constant-constant-1

    if pygame.sprite.groupcollide(misiles, enemies, True, True):
        enemy_sound.play()
    update()
    pygame.display.flip()
    clock.tick(140)
    screen.fill((0, 0, 0))
    total_frames += 1; frames += 1


pygame.quit()
print("YOUR SCORE:", frames)
