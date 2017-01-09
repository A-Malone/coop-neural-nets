#GLOBAL IMPORTS
import numpy as np
import pygame

#PACKAGE IMPORTS
from .gameobjects import GameObject, Move
from .bullet import Bullet
from colearning.utils import clip_to_dim, clip_array_to_dim, TeamColors

class Player(GameObject):
    """ The base class for all players. Handles all game-related logic """

    #----Constants
    VELOCITY = 40
    RADIUS = 15
    ANGULAR_VELOCITY = np.pi/5

    SHOOT_COOLDOWN = 2

    MAX_FOV = np.pi/4
    FOV_INCREMENT = np.pi/20

    # State
    fov_angle = None
    ping = False
    current_cooldown = 0

    # Moves
    past_moves = None

    def __init__(self):
        super(Player, self).__init__(Player.RADIUS)

    def setup(self, pos, heading, fov_angle):
        """ Setup the player's game state """
        self.position = pos
        self.heading = heading
        self.fov_angle = fov_angle
        self.past_moves = set()


    def is_in_fov(self, pos):
        """ Returns whether a given location is in the FOV"""
        angle = np.arctan2(*list(pos - self.position))
        return abs((self.heading - angle)%(2*np.pi)) < self.fov_angle/2

    #----Overrides
    #----------------------------------------------------
    def render(self, win):
        """ Renders the player on the screen """

        super(Player, self).render(win)

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

    def update(self, move, players, bullets, dim, dt):
        """
        Act on input chosen in pre_update
        """
        if(self.current_cooldown > 0):
            self.current_cooldown -= dt

        if(move == Move.FORWARD):
            self.position += self.get_components(self.heading)*Player.VELOCITY*dt
        elif(move == Move.TURN_LEFT):
            self.heading += Player.ANGULAR_VELOCITY*dt
        elif(move == Move.TURN_RIGHT):
            self.heading -= Player.ANGULAR_VELOCITY*dt
        elif(move == Move.WIDEN_FOV):
            self.fov_angle += Player.FOV_INCREMENT*dt
        elif(move == Move.NARROW_FOV):
            self.fov_angle -= Player.FOV_INCREMENT*dt
        elif(move == Move.SHOOT):
            if(self.current_cooldown <= 0):
                bullets.append(Bullet(self.object_id, np.copy(self.position), self.heading))
                self.current_cooldown = Player.SHOOT_COOLDOWN

        # Ping?
        self.ping = (move == Move.PING)

        # Truncate heading to bounds
        self.heading %= np.pi*2

        # Truncate FOV to bounds
        self.fov_angle = clip_to_dim(self.fov_angle, Player.MAX_FOV)

        #Truncate position to bounds
        clip_array_to_dim(self.position, dim)
