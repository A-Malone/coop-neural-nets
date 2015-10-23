import numpy as np
import pygame


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

    @classmethod
    def contains(cls, move):
        return cls.to_text(move) != None


class GameObject(object):
    """docstring for GameObject"""

    OBJECT_ID = 0

    # State
    position = None
    heading = None
    active = True

    # hitbox
    radius = None

    def __init__(self, radius):
        #Increments the global id, but not our ID
        self.object_id = GameObject.OBJECT_ID
        GameObject.OBJECT_ID += 1

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

    def pre_update(self, players, bullets):
        pass

    # Pure virtual
    def update(self, players, bullets, dim, dt):
        raise NotImplementedError('Not implemented')
