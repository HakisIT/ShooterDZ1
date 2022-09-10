from pygame import *
from pygame import image as img
import random
 
bg = "galaxy.jpg"
zsu = "rocket.png"
bullet = 'bullet.png'
enemy = 'zomb.png'
 
 
class Picture(sprite.Sprite):
    def __init__(self, x, y, image, width, height):
        super().__init__()
        self.image = img.load(image)
        self.image = transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Player(Picture):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x < 600:
            self.rect.x += 5
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 5
        if keys[K_SPACE]:
            self.fire()
 
    def fire(self):
        ballet = Bullet(player.rect.centerx, player.rect.top, bullet, 20, 50)
        bullets.add(ballet)
 
 
class Bullet(Picture):
    def update(self):
        self.rect.y -= 15

class UFO(Picture):
    def update(self):
        global failed
        self.rect.y += random.randint(2,5)
        if self.rect.y > 500:
            failed += 1
            self.rect.y = -100
            self.rect.x = random.randint(0,600)

bullets = sprite.Group()
enemies = sprite.Group()

for i in range(10):
    ufo = UFO(random.randint(0,400), -100, enemy, 400, 300)
    enemies.add(ufo)
    
win_width = 700
win_height = 500
display.set_caption("Moskali Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(bg), (win_width, win_height))
clock = time.Clock()
FPS = 60
 
player = Player(275, 350, zsu, 100, 100)

font.init()
font = font.Font(None, 30)

win = font.render(
   'Перемога!', True, (0, 255, 0)
)

lost = font.render(
    'Поразка...', True, (255, 0, 0)
)

count_d = font.render( 
    'Ворогів знищено: 0', True, (255, 255, 255)
)

count_l = font.render( 
    'Ворогів пропущено: 0', True, (255, 255, 255)
)

game = True
killed = 0
failed = 0
while game:
    clock.tick(FPS)
    window.blit(background, (0, 0))
    count_d = font.render('Ворогів знищено:' + str(killed), True, (255, 255, 255))
    count_l = font.render('Ворогів пропущено:' + str(failed), True, (255, 255, 255))
    window.blit(count_d, (50, 50))
    window.blit(count_l, (450, 50))
    player.draw()
    player.update()
    s_collide = sprite.spritecollide(player, enemies, False)
    s_list = sprite.groupcollide(enemies, bullets, False, True)
    for name in s_list.keys():
        name.rect.y = -100
        name.rect.x = random.randint(0,600)
        killed += 1
    #if len(s_collide) >= 1:
        #game = False
    if killed == 50:
        game = False
    bullets.draw(window)
    bullets.update()
    enemies.update()
    enemies.draw(window)
    display.update()
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.fire()