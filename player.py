import controls
import math
from base import Base


class Player(Base):

    def __init__(self):
        Base.__init__(self)
        self.equipped = None
        self.weapons = []
        self.inventory = []
        self.buffs = []
        self.direction = 0
        self.controls = controls.Controls()
        self.dx = 0
        self.dy = 0
        self.shooting = False
        self.level = 1
        self.attack = 100
        self.defense = 100
        self.speed = 300 #pixels per second
        self.wep_index = 0

    def update(self, td):
        self.controls.update(td, self)
        if self.equipped:
            self.equipped.update(td)
        self.direction = self.controls.direction
        if self.controls.magnitude:
            mag = self.speed * td/1000.0 * self.controls.magnitude
            self.dx = math.cos(self.direction) * mag
            self.dy = math.sin(self.direction) * mag
            self.x += self.dx
            self.y += self.dy
        else:
            self.dx, self.dy = (0, 0)
        if self.controls.shoot and self.equipped and self.equipped.can_shoot():
            self.shooting = True
        else:
            self.shooting = False
        if self.controls.switch != 0:
            self.wep_index = (self.wep_index + self.controls.switch) % len(self.weapons)
            self.equipped = self.weapons[self.wep_index]
            print self.equipped


class HeavyPlayer(Player):
    def __init__(self):
        super(HeavyPlayer, self).__init__()
        self.attack = 200
        self.speed = 100
        self.defense = 200


class LightPlayer(Player):
    def __init__(self):
        super(LightPlayer, self).__init__()
        self.attack = 100
        self.speed = 200
        self.defense = 100


if __name__ == "__main__":
    import main
    import weapon
    main.init()
    p = LightPlayer()
    wep1 = weapon.generate_weapon("Machine Gun")
    p.weapons.append(wep1)
    wep2 = weapon.generate_weapon("Missle Launcher")
    p.weapons.append(wep2)
    wep3 = weapon.generate_weapon("Laser Gun")
    p.weapons.append(wep3)
    p.equipped = p.weapons[0]
    print p.equipped
    p.speed = 400
    main.test(p)
