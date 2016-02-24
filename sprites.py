import pygame
import constants as C
import weapon


class Sprite(pygame.sprite.Sprite):
    # Sprite is a container for the base object in a game
    # Sprite will hold any visual information and acts as the
    # view for the model held in base
    def __init__(self, imagesrc, base):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load(imagesrc).convert()
        self.source.set_colorkey(self.source.get_at((0, 0)))
        self.dim = self.source.get_size()
        self.image_count = self.dim[1]/self.dim[0]
                            #width / height
        self.im_rect = pygame.Rect(0, 0, self.dim[0], self.dim[0])
        self.image = self.source.subsurface(self.im_rect)
        self.rect = self.image.get_rect()
        self.radius = abs(self.rect.center[0]-self.rect.left)
        self.base = base

    def update(self, td):
        self.base.update(td)
        self.rect.center = self.base.x, -self.base.y


class Effect(pygame.sprite.Sprite):
    def __init__(self, imagesrc):
        pygame.sprite.Sprite.__init__(self)
        self.source = pygame.image.load(imagesrc).convert()
        self.source.set_colorkey(self.source.get_at((0, 0)))
        self.dim = self.source.get_size()
        self.image_count = self.dim[1]/self.dim[0]
                            #width / height
        self.im_rect = pygame.Rect(0, 0, self.dim[0], self.dim[0])
        self.image = self.source.subsurface(self.im_rect)
        self.rect = self.image.get_rect()




class PlayerSpr(Sprite):
    def __init__(self, play):
        Sprite.__init__(self, "resources/images/sprites/player/player.png", play)
        self.bullets = pygame.sprite.Group()

    def update(self, td, *args, **kwargs):
        super(PlayerSpr, self).update(td)
        self.bullets.update(td)
        if self.base.shooting:
            bullets = self.base.equipped.shoot(self.base)
            if type(bullets) == list:
                wep = self.base.equipped
                #bullet = None
                if type(wep) == weapon.LaserGun:
                    bullet = LaserSpr
                elif type(wep) == weapon.MachineGun:
                    bullet = BulletSpr
                elif type(wep) == weapon.MissleLauncher:
                    bullet = BulletSpr
                else:
                    bullet = BulletSpr
                for b in bullets:
                    bull = bullet(b)
                    self.bullets.add(bull)
            else:
                raise Exception("object returned from shoot() is not a list of bullets")
        clamped = self.rect.clamp(C.GAME_RECT)
        if clamped != self.rect:
            self.rect = clamped
            x, y = self.rect.center
            self.base.x = x
            self.base.y = -y


class BulletTrail(Effect):
    def __init__(self, bullet, limit=1000):
        super(BulletTrail, self).__init__("resources/images/effects/bullet_trail.png")
        self.x = bullet.x
        self.y = bullet.y
        self.time = 0
        self.limit = limit

    def update(self, td):
        super(BulletTrail, self).update(td)
        index = (self.time/50) % self.image_count
        self.image = self.source.subsurface(self.im_rect.move(0, self.dim[0] * index))
        if self.time > self.limit:
            self.kill()


class BulletSpr(Sprite):

    def __init__(self, bullet):
        Sprite.__init__(self, "resources/images/sprites/bullets/bullet.png", bullet)

        self.rect.center = self.base.x,- self.base.y

    def update(self, td, *args, **kwargs):
        super(BulletSpr, self).update(td)
        index = (self.base.time/50) % self.image_count
        self.image = self.source.subsurface(self.im_rect.move(0, self.dim[0] * index))
        if not C.KILL_RECT.colliderect(self.rect):
            self.kill()


class LaserSpr(Sprite):

    def __init__(self, laser):
        Sprite.__init__(self, "resources/images/sprites/bullets/laser.png", laser)
        self.im_rect = pygame.Rect(0, 0, self.dim[0], self.dim[1])
        self.rect = self.image.get_rect()
        self.rect.center = self.base.x, self.base.y
        self.rect.move_ip(0,-128)
    def update(self, td, *args, **kwargs):
        super(LaserSpr, self).update(td)
        #self.rect.bottom = -self.base.y
        self.rect.move_ip(0,-64)
        index = (self.base.time/50) % self.image_count
        self.image = self.source.subsurface(self.im_rect.move(0, self.dim[0] * index))
        if not C.KILL_RECT.colliderect(self.rect):
            self.kill()


class EnemySpr(Sprite):
    def __init__(self, enemy):
        Sprite.__init__(self, "resources/images/sprites/enemies/enemy.png", enemy)

    def update(self, td, *args, **kwargs):
        super(EnemySpr, self).update(td)


if __name__ == "__main__":
    pass
