import numpy as np
import pygame

from utils import clip_to_dim, clip_array_to_dim, out_of_bounds
import coopplayer

#POSSIBLE MOVES
class Move(object):
    FORWARD = 0
    TURN_LEFT = 1
    TURN_RIGHT = 2
    NARROW_FOV = 3
    WIDEN_FOV = 4
    PING = 5
    SHOOT = 6

    @classmethod
    def to_text(cls, move):
        for k, v in cls.__dict__.iteritems():
            if v == move:
                return k
        return None


class GameObject(object):
    """docstring for GameObject"""

    object_id = 0

    # State
    position = None
    heading = None
    active = True

    # hitbox
    radius = None

    def __init__(self, radius):
        #Increments the global id, but not our ID
        GameObject.object_id += 1

        self.radius = radius

    def __eq__(self, other):
        print(self.object_id, other.object_id)
        return self.object_id == other.object_id

    def __cmp__(self, other):
        print("cmp", self.object_id, other.object_id)
        return self.object_id == other.object_id

    def get_components(self, angle):
        return np.array([np.sin(angle), np.cos(angle)])

    def collision(self, pos):
        return np.linalg.norm(pos-self.position) <= self.radius

    # Overrideable
    def render(self, win):
        #Draw circle
        pygame.draw.circle(
            win,
            (255, 255, 255),
            [int(x) for x in np.rint(self.position)],
            self.radius,
            1)

        #Draw heading
        pygame.draw.line(
            win,
            (100, 255, 100),
            [int(x) for x in np.rint(self.position)],
            [int(x) for x in np.rint(self.position + self.get_components(self.heading)*self.radius)],
            1)

    def pre_update(self, objects):
        pass

    def post_update(self, objects):
        pass

    # Pure virtual
    def update(self, objects, dim, dt):
        raise NotImplementedError('Not implemented')

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

    def update(self, objects, dim, dt):
        self.position += self.get_components(self.heading)*Bullet.VELOCITY*dt
        if(out_of_bounds(self.position, dim)):
            self.active = False

    def post_update(self, objects):
        if(self.active):
            for obj in filter(lambda x: x is coopplayer.CoopPlayer, objects):
                if(self.collision(obj.pos)):
                    firer = filter(lambda x: x.object_id == firer_id, objects)[0]
                    obj.score -= 10
                    firer.score += 10 if obj.team != firer.team else -10
                    self.active = False
                    break
