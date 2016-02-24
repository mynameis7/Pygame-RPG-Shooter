from base import Base


class Enemy(Base):
    def __init__(self):
        Base.__init__(self)
        self.drop = None

    def update(self, td, *args, **kwargs):
        self.time += td

    def hit(self, bullet):
        self.shields -= bullet.damage