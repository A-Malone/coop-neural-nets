#GLOBAL IMPORTS
import numpy as np
import pygame

#PACKAGE IMPORTS
from .gameobjects import GameObject, Move
from .bullet import Bullet
from colearning.utils import clip_to_dim, clip_array_to_dim, TeamColors

class BasePlayer(GameObject):
    """ The base class for all players. Handles all game-related logic """

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

    # Moves
    past_moves = None

    def __init__(self):
        super(BasePlayer, self).__init__(BasePlayer.RADIUS)

    def initialize_player(self, team, individual_id):
        """ Setup the player's external attributes """
        self.team = team
        self.individual_id = individual_id

    def setup(self, pos, heading, fov_angle):
        """ Setup the player's game state """
        self.position = pos
        self.heading = heading
        self.fov_angle = fov_angle
        self.score = 0
        self.past_moves = set()

    def get_view(self, players, bullets):
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

        for obj in players:
            if(self.is_in_fov(obj.position)):
                if(obj.team != self.team):
                    output[1] += 1
                else:
                    output[2] += 1
                    if(obj.ping):
                        output[3] += 1

        for obj in bullets:
            if(self.is_in_fov(obj.position)):
                output[4] += 1

        return output

    def is_in_fov(self, pos):
        """ Returns whether a given location is in the FOV"""
        angle = np.arctan2(*list(pos - self.position))
        return abs((self.heading - angle)%(2*np.pi)) < self.fov_angle/2

    #----Overrides
    #----------------------------------------------------
    def render(self, win):
        """ Renders the player on the screen """

        super(BasePlayer, self).render(win)

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


    def pre_update(self, players, bullets):
        """ Get a move from the model """
        in_vals = self.get_view(players, bullets)
        return self.get_move(in_vals)

    def update(self, move, players, bullets, dim, dt):
        """
        Act on input chosen in pre_update
        """
        if(self.current_cooldown > 0):
            self.current_cooldown -= dt

        if(move == Move.FORWARD):
            self.position += self.get_components(self.heading)*BasePlayer.VELOCITY*dt
        elif(move == Move.TURN_LEFT):
            self.heading += BasePlayer.ANGULAR_VELOCITY*dt
        elif(move == Move.TURN_RIGHT):
            self.heading -= BasePlayer.ANGULAR_VELOCITY*dt
        elif(move == Move.WIDEN_FOV):
            self.fov_angle += BasePlayer.FOV_INCREMENT*dt
        elif(move == Move.NARROW_FOV):
            self.fov_angle -= BasePlayer.FOV_INCREMENT*dt
        elif(move == Move.SHOOT):
            if(self.current_cooldown <= 0):
                bullets.append(Bullet(self.object_id, np.copy(self.position), self.heading))
                self.current_cooldown = BasePlayer.SHOOT_COOLDOWN

        # Ping?
        self.ping = (move == Move.PING)

        # Truncate heading to bounds
        self.heading %= np.pi*2

        # Truncate FOV to bounds
        self.fov_angle = clip_to_dim(self.fov_angle, BasePlayer.MAX_FOV)

        #Truncate position to bounds
        clip_array_to_dim(self.position, dim)

    #----VIRTUAL FUNTIONS
    #----------------------------------------------------
    def on_game_start(self):
        raise NotImplementedError('BasePlayer subclasses must reimplement on_game_start')

    def on_game_end(self):
        raise NotImplementedError('BasePlayer subclasses must reimplement on_game_end')

    def get_move(self, in_vals):
        raise NotImplementedError('BasePlayer subclasses must reimplement get_move')

    def set_params(self, params):
        raise NotImplementedError('BasePlayer subclasses must reimplement set_params')

    def get_params(self):
        raise NotImplementedError('BasePlayer subclasses must reimplement set_params')

    def param_dim(self):
        raise NotImplementedError('BasePlayer subclasses must reimplement param_dim')

    def reward(self, amount):
        raise NotImplementedError('BasePlayer subclasses must reimplement reward')
