from colearning.utils import  out_of_bounds
from .gameobjects import GameObject

class Bullet(GameObject):
    """docstring for Bullet"""

    # Constants
    VELOCITY = 60
    RADIUS = 4

    firer_id = None

    def __init__(self, firer_id, pos, heading):
        super(Bullet, self).__init__(Bullet.RADIUS)
        self.position = pos
        self.heading = heading
        self.firer_id = firer_id

    def update(self, players, bullets, dim, dt):
        self.position += self.get_components(self.heading)*Bullet.VELOCITY*dt
        if(out_of_bounds(self.position, dim)):
            self.active = False
