import numpy as np
import pygame

import gameobjects
from utils import clip_to_dim, clip_array_to_dim, TeamColors

class CoopPlayer(gameobjects.GameObject):
    """docstring for CoopPlayer"""

    #----Constants
    VELOCITY = 40
    RADIUS = 15
    ANGULAR_VELOCITY = np.pi/5

    SHOOT_COOLDOWN = 2

    MAX_FOV = np.pi/4
    FOV_INCREMENT = np.pi/20

    #----Fields
    team = None
    individual_id = None
    # State
    fov_angle = None
    ping = False

    current_cooldown = 0

    #Score
    score = 0

    #Update
    next_move = None

    def __init__(self, net, team, individual_id):
        super(CoopPlayer, self).__init__(CoopPlayer.RADIUS)
        score = 0
        self.nn = net
        self.team = team
        self.individual_id = individual_id

    def setup(self, pos, heading, fov_angle):
        self.position = pos
        self.heading = heading
        self.fov_angle = fov_angle

    def get_view(self, objects):
        """
        Returns what the player is able to see
        Outputs:
            Fov (in rad)
            Num enemy
            Num Ally in view
                Num Ally ping in view
            Enemy bullets in view
        """
        output = np.zeros(5)
        output[0] = self.fov_angle

        for obj in objects:
            if(obj is CoopPlayer):
                if(self.is_in_fov(obj.position)):
                    if(obj.team != self.team):
                        output[1] += 1
                    else:
                        output[2] += 1
                        if(obj.ping):
                            output[3] += 1
            elif(obj is gameobjects.Bullet):
                if(self.is_in_fov(obj)):
                    output[4] += 1

        return output

    def is_in_fov(self, pos):
        angle = np.atan2(*list(pos - self.position))
        return abs((heading - angle)%(2*np.pi)) < self.fov_angle/2

    # Overrides
    def render(self, win):
        super(CoopPlayer, self).render(win)

        #Draw FOV
        team_colour = TeamColors.get(self.team)
        pygame.draw.line(
            win,
            team_colour,
            [int(x) for x in np.rint(self.position)],
            [int(x) for x in np.rint(self.position + self.get_components(self.heading - self.fov_angle/2)*self.radius*3)],
            1)

        pygame.draw.line(
            win,
            team_colour,
            [int(x) for x in np.rint(self.position)],
            [int(x) for x in np.rint(self.position + self.get_components(self.heading + self.fov_angle/2)*self.radius*3)],
            1)

        if(self.ping):
            pygame.draw.circle(
                win,
                (255, 255, 100),
                [int(x) for x in np.rint(self.position)],
                int(self.radius*1.2),
                1)

    def pre_update(self, objects):
        in_vals = self.get_view(objects)
        results = self.nn.activate(in_vals)
        self.next_move = np.argmax(results)

    def update(self, objects, dim, dt):
        """
        Act on input chosen in pre_update
        """
        if(self.current_cooldown > 0):
            self.current_cooldown -= dt
        #print(gameobjects.Move.to_text(self.next_move), self.next_move)

        if(self.next_move == gameobjects.Move.FORWARD):
            self.position += self.get_components(self.heading)*CoopPlayer.VELOCITY*dt
        elif(self.next_move == gameobjects.Move.TURN_LEFT):
            self.heading += CoopPlayer.ANGULAR_VELOCITY*dt
        elif(self.next_move == gameobjects.Move.TURN_RIGHT):
            self.heading -= CoopPlayer.ANGULAR_VELOCITY*dt
        elif(self.next_move == gameobjects.Move.WIDEN_FOV):
            self.fov_angle += CoopPlayer.FOV_INCREMENT*dt
        elif(self.next_move == gameobjects.Move.NARROW_FOV):
            self.fov_angle -= CoopPlayer.FOV_INCREMENT*dt
        elif(self.next_move == gameobjects.Move.SHOOT):
            if(self.current_cooldown <= 0):
                objects.append(gameobjects.Bullet(self.object_id, np.copy(self.position), self.heading))
                self.current_cooldown = CoopPlayer.SHOOT_COOLDOWN

        # Ping?
        self.ping = (self.next_move == gameobjects.Move.PING)

        # Truncate heading to bounds
        self.heading %= np.pi*2

        # Truncate FOV to bounds
        self.fov_angle = clip_to_dim(self.fov_angle, CoopPlayer.MAX_FOV)

        #Truncate position to bounds
        clip_array_to_dim(self.position, dim)
