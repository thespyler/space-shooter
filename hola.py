import pygame
from pygame.locals import *
from random import randrange

height, width = 600, 600
display = pygame.display.set_mode((height, width))
pygame.display.set_caption('game')
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (height // 20, width - 40)
        self.speed = 0

    def update(self):
        keys = pygame.key.get_pressed()
        keylift = not pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.speed = -8

        elif keys[K_RIGHT]:
            self.speed = 8

        if keylift:
            self.speed = 0
        self.rect.x += self.speed
        if self.rect.left > height:
            self.rect.left = 0

        if self.rect.right <= 0:
            self.rect.right = height


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, 400)
        self.rect.y = width
        self.speedx = randrange(-1, 1)
        self.speedy = randrange(1, 9)

    def update(self):
        if self.rect.bottom > width or self.rect.left < 0 or self.rect.right > height:
            self.rect.x = randrange(100, height)
            self.rect.y = randrange(-10, 0)
        self.rect.x += self.speedx
        self.rect.y += self.speedy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed


def main():
    pygame.init()
    player = Player()
    mob = Mob()
    bullet = Bullet(player.rect.x, player.rect.y)
    mobs = pygame.sprite.Group()
    mobs.add(mob)
    players = pygame.sprite.Group()
    players.add(player)
    bullets = pygame.sprite.Group()
    bullets.add(bullet)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(bullet)
    all_sprites.add(player)
    all_sprites.add(mob)
    for i in range(10):
        m = Mob()
        mobs.add(m)
        all_sprites.add(m)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for b in range(5):
                        b = Bullet(player.rect.x, player.rect.y)
                        bullets.add(b)
                        all_sprites.add(b)

            if event.type == KEYUP:
                player.speed = 0
        display.fill(BLACK)
        hits = pygame.sprite.groupcollide(players, mobs, False, False)
        bullethit = pygame.sprite.groupcollide(bullets, mobs, True, True)
        if bullethit:
            m = Mob()
            mobs.add(m)
            all_sprites.add(m)
        if hits:
            pygame.quit()
            quit()
        all_sprites.update()
        all_sprites.draw(display)
        pygame.display.update()
        pygame.time.Clock().tick(60)


if __name__ == '__main__':
    main()
