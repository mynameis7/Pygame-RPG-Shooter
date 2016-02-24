from random import choice
import constants as C
import math


def DEFAULT_PATH(t, dir, vel, *args):
    dx_t = 0
    dy_t = vel #pixels per second
    return dx_t, dy_t

def DIRECTED_PATH(t, dir, vel, *args):
    dx_t = math.cos(dir) * vel
    dy_t = math.sin(dir) * vel
    return dx_t, dy_t

def FANCY_PATH(t, dir, vel, *args):
    dx_t = math.cos(dir + math.radians(t/10)) * vel
    dy_t = math.sin(dir + math.radians(t/10)) * vel
    return dx_t, dy_t


def ARC_PATH(t, dir, vel, *args):
    dx_t = math.cos(dir) * vel
    dy_t = math.sin(dir) * vel
    if dx_t > 0:
        dx_t += math.pow(t/10, 1.2)
    elif dx_t < 0:
        dx_t -= math.pow(t/10, 1.2)
    dy_t += math.pow(t/20, 1.2)
    return dx_t, dy_t


def WAVE_PATH(t, dir, vel, *args):
    d = math.cos(dir)
    dx_t = 0
    if d > 0:
        dx_t = math.sin(dir + math.radians(t/2)) * vel * 5
    if d < 0:
        dx_t = math.sin(dir + math.radians(t/2)) * vel * 5

    dy_t = vel + math.pow(t/10, 1.8)#math.cos(dir + math.radians(t/10)) * vel + math.pow(t/50, 2)
    return dx_t, dy_t


class Weapon(object):

    def __init__(self, name, rate, damage, bullet):
        self.name = name                         #weapon name
        self.rate = rate                         #firerate of the weapon as time between shots in milliseconds
        self.damage = damage                     #Damage of the bullet
        self.bullet = bullet
        self.last_shot = -10000
        self.time = 0

    def update(self, td):
        self.time += td

    def can_shoot(self):
        if self.time - self.last_shot > self.rate:
            return True
        return False

    def __str__(self):
        return "%s \n\tRate=%s Damage=%s"%(self.name, self.rate, self.damage)


class GenWeapon(Weapon):

    def __init__(self, name, rate, damage, attrib, bullet):
        super(GenWeapon, self).__init__(name, rate, damage, bullet)
        self.aoe = attrib["aoe"]
        self.seeking = attrib["Seeking"]
        self.piercing = attrib["Piercing"]
        self.leeching = attrib["Leeching"]
        self.pack = attrib

    def shoot(self, player):
        self.last_shot = self.time
        return [self.bullet(self, player, Bullet.UP, 800, DEFAULT_PATH)]

    def __str__(self):
        return super(GenWeapon, self).__str__() + "\n\tAoe=%s Piercing=%s Seeking=%s Leeching=%s\n" % (self.aoe,
                                                                                                       self.piercing,
                                                                                                       self.seeking,
                                                                                                       self.leeching)


class SP_WEAPON(Weapon):
    def __init__(self, name, rate, damage, attrib):
        super(SP_WEAPON, self).__init__(name, rate, damage)
        self.aoe = attrib["aoe"]
        self.seeking = attrib["Seeking"]
        self.piercing = attrib["Piercing"]
        self.leeching = attrib["Leeching"]
        self.pack = attrib
        self.seeking = False

    def shoot(self, player):
        self.last_shot = self.time
        return [self.bullet(self, player, math.radians(i*45 + 22.5), 200, FANCY_PATH, 500) for i in xrange(8)]


class MissleLauncher(GenWeapon):

    def __init__(self, name, rate, damage, attrib, level = 1):
        self.base_rate = 1000.0
        self.base_damage = 100
        rate *= self.base_rate
        damage *= self.base_damage
        super(MissleLauncher, self).__init__(name, rate, damage, attrib, Bullet)
        self.missle_cnt = 4
        self.seeking = True
        self.aoe += 50
        self.level = level

    def shoot(self, player):
        self.last_shot = self.time
        base = (180/self.missle_cnt)
        return [self.bullet(self, player, math.radians(i*base + 180 + base/2), 200, DIRECTED_PATH, 500) for i in xrange(self.missle_cnt)]


class MachineGun(GenWeapon):
    def __init__(self, name, rate, damage, attrib, level = 1):
        self.base_rate = 250.0
        self.base_damage = 100
        rate *= self.base_rate
        damage *= self.base_damage
        super(MachineGun, self).__init__(name, rate, damage, attrib, Bullet)
        self.bull_count = 1

    def shoot(self, player):
        self.last_shot = self.time
        base = (70.0/self.bull_count)
        dirs = [math.radians(90 + (i - self.bull_count/2) * base + (self.bull_count + 1) % 2*base/2.0) for i in xrange(self.bull_count)]
        return [self.bullet(self, player, i, 800, DIRECTED_PATH, 0) for i in dirs]


class LaserGun(GenWeapon):
    def __init__(self, name, rate, damage, attrib, level = 1):
        self.base_rate = 50.0
        self.base_damage = 20
        damage *= self.base_damage
        rate *= self.base_rate
        super(LaserGun, self).__init__(name, rate, damage, attrib, Laser)
        self.aoe = 0
        self.seeking = False

    def shoot(self, player):
        self.last_shot = self.time
        return [self.bullet(self, player, Bullet.UP, 2400)]


class Bullet(object):
    UP = math.radians(90)

    def __init__(self, weapon, player, direc=0.0, velocity=800, path=None, delay = 1000):
        self.time = 0
        self.direc = direc
        self.x = player.x
        self.y = player.y
        self.path = path
        if not self.path:
            self.path = DEFAULT_PATH
        self.damage = weapon.damage
        self.dx = 0
        self.dy = 0
        self.velocity = velocity
        self.aoe = weapon.aoe
        self.seeking = weapon.seeking
        self.piercing = weapon.piercing
        self.leeching = weapon.leeching
        self.delay = delay

    def follow_nearest(self):
        near = None
        minim = 10000
        for enemy in C.ENEMIES:
            dist = math.hypot(self.x - enemy.base.x, self.y - enemy.base.y)
            if near:
                if dist < minim:
                    near = enemy
                    minim = dist
            else:
                near = enemy
                minim = dist
        if not near:
            return 0, 800
        dx = near.base.x - self.x
        dy = near.base.y - self.y
        return dx, dy

    def update(self, td, *args):
        self.time += td
        if self.seeking:
            if self.time < self.delay:
                self.dx, self.dy = self.path(self.time, self.direc, self.velocity)
            else:
                self.dx, self.dy = self.follow_nearest()
        else:
            self.dx, self.dy = self.path(self.time, self.direc, self.velocity)
        self.x += self.dx * td/1000.0
        self.y += self.dy * td/1000.0

class Laser(object):
    def __init__(self, weapon, player, direc=0.0, velocity=800, path=None, delay = 1000):
        self.time = 0
        self.direc = direc
        self.start_x = player.x
        self.start_y = player.y
        self.x = player.x
        self.y = player.y
        self.path = path
        if not self.path:
            self.path = DEFAULT_PATH
        self.damage = weapon.damage
        self.dx = 0
        self.dy = 0
        self.velocity = velocity
        self.aoe = weapon.aoe
        self.seeking = weapon.seeking
        self.piercing = weapon.piercing
        self.leeching = weapon.leeching
        self.delay = delay
        self.player = player

    def update(self, td, *args):
        self.dx, self.dy = self.path(self.time, self.direc, self.velocity)
        self.start_x += self.dx * td/1000.0
        self.start_y += self.dy * td/1000.0
        self.x = self.player.x
        self.y = self.start_y

style_tbl = {"Fast": {"rate": .5, "damage": .5},
             "Balanced": {"rate": 1.0, "damage": 1.0},
             "Heavy": {"rate": 2.0, "damage": 2.0}
             }

attrib_tbl = {"Exploding": {"aoe": 20, "Seeking": False, "Piercing": False, "Leeching": False},
              "Seeking": {"aoe": 0, "Seeking": True, "Piercing": False, "Leeching": False},
              "Piercing": {"aoe": 0, "Seeking": False, "Piercing": True, "Leeching": False},
              "Leeching": {"aoe": 0, "Seeking": False, "Piercing": False, "Leeching": True},
              "": {"aoe": 0, "Seeking": False, "Piercing": False, "Leeching": False}
              }

WEAPON_LIST = {"Missle Launcher": MissleLauncher,
               "Machine Gun": MachineGun,
               "Laser Gun": LaserGun}

def generate_weapon(wep_type):
    att = choice(list(attrib_tbl))
    sty = choice(list(style_tbl))
    name = att + " " + sty + " " + wep_type
    sty = style_tbl[sty]
    att = attrib_tbl[att]
    wep = WEAPON_LIST[wep_type](name, sty["rate"], sty["damage"], att)
    return wep

def make_SP_wep():
    sty = style_tbl["Fast"]
    att = attrib_tbl["Seeking"]
    print att
    wep = SP_WEAPON("STAR", int(sty["rate"] * 1000), sty["damage"], att)
    print wep
    return wep


if __name__ == "__main__":
    pass
