#GLOBAL IMPORTS
import numpy as np
import pygame

#PACKAGE IMPORTS
from colearning.game import gameobjects
from colearning.utils import clip_to_dim, clip_array_to_dim, TeamColors

class BasePlayer(gameobjects.GameObject):
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
    next_move = None

    def __init__(self, net, ):
        super(BasePlayer, self).__init__(CoopPlayer.RADIUS)

    def initialize_player(team, individual_id):
        """ Setup the player's external attributes """
        self.team = team
        self.individual_id = individual_id

    def setup(self, pos, heading, fov_angle):
        """ Setup the player's game state """
        self.position = pos
        self.heading = heading
        self.fov_angle = fov_angle
        self.past_moves = set()

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
        """ Returns whether a given location is in the FOV"""
        angle = np.atan2(*list(pos - self.position))
        return abs((heading - angle)%(2*np.pi)) < self.fov_angle/2

    def select_move(self, move):
        assert(Move.contains(move) and self._next_move is None)
        self._next_move = move
        if(move not in self._past_moves):
            self.score += 3*(len(self.past_moves))
            self.past_moves.add(move)

    def get_next_move(self, move):
        assert(self._next_move is not None)
        ret = self._next_move
        self._next_move = None
        return ret

    #----Overrides
    #----------------------------------------------------
    def render(self, win):
        """ Renders the player on the screen """

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
        """ Get a move from the model """
        in_vals = self.get_view(objects)
        self.select_move(self.get_move(in_vals))

    def update(self, objects, dim, dt):
        """
        Act on input chosen in pre_update
        """
        if(self.current_cooldown > 0):
            self.current_cooldown -= dt
        #print(gameobjects.Move.to_text(self.next_move), self.next_move)

        move = self.get_next_move()
        if(move == gameobjects.Move.FORWARD):
            self.position += self.get_components(self.heading)*CoopPlayer.VELOCITY*dt
        elif(move == gameobjects.Move.TURN_LEFT):
            self.heading += CoopPlayer.ANGULAR_VELOCITY*dt
        elif(move == gameobjects.Move.TURN_RIGHT):
            self.heading -= CoopPlayer.ANGULAR_VELOCITY*dt
        elif(move == gameobjects.Move.WIDEN_FOV):
            self.fov_angle += CoopPlayer.FOV_INCREMENT*dt
        elif(move == gameobjects.Move.NARROW_FOV):
            self.fov_angle -= CoopPlayer.FOV_INCREMENT*dt
        elif(move == gameobjects.Move.SHOOT):
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

    #----VIRTUAL FUNTIONS
    #----------------------------------------------------
    def get_move(self, in_vals):
        raise NotImplementedError('BasePlayer subclasses must reimplement get_move')

    def initialize_model(self, params):
        raise NotImplementedError('BasePlayer subclasses must reimplement initialize_model')

    def param_dim(self):
        raise NotImplementedError('BasePlayer subclasses must reimplement param_dim')
