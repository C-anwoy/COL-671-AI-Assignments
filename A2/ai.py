import random
import numpy as np
from typing import List, Tuple, Dict
from connect4.utils import get_pts, get_valid_actions, Integer
import copy
import sys
import time
import signal

class AIPlayer:
    def __init__(self, player_number: int, time: int):
        """
        :param player_number: Current player number
        :param time: Time per move (seconds)
        """
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        self.time = time
        # Do the rest of your implementation here
        self.opponent_number = 2
        if player_number == 2:
            self.opponent_number = 1
        self.stateMap = {}

    def pop_from_board(self, board, action):
        new_board = copy.deepcopy(board)
        rows = board.shape[0]
        new_board[1:,action] = new_board[:rows-1,action]
        new_board[0,action] = 0
        return new_board

    def add_to_board(self, board, action, player_number):
        new_board = copy.deepcopy(board)
        row_ind = np.where(new_board[:,action]==0)[0][-1]
        new_board[row_ind, action] = player_number
        return new_board

    def get_intelligent_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move
        This will play against either itself or a human player
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        class TimeoutException(Exception):
            pass
        def handler(signum, stack):
            raise TimeoutException

        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, self.time-0.5)
        try:
            max_depth = 10
            best_action = None
            for depth in range(1, max_depth+1):
                best_action, _ = self.get_best_move_minimax(state, self.player_number, -sys.maxsize, sys.maxsize, depth)
        except TimeoutException:
            pass

        return best_action

    def fill_entire_board(self, board, player_number):
        new_board = copy.deepcopy(board)
        new_board[np.where(new_board == 0)] = player_number
        return new_board

    def get_optimal_score(self, state):
        return get_pts(self.player_number, self.fill_entire_board(state[0], self.player_number)) - get_pts(self.opponent_number, self.fill_entire_board(state[0], self.opponent_number))

    def get_best_move_minimax(self, state, player_number, alpha, beta, depth):

        board_in_key = tuple([tuple(item) for item in sorted(state[0].tolist())])
        list_of_dict_items = sorted(list(state[1].items()))
        list_of_dict_items = [(key,value.get_int()) for key,value in list_of_dict_items]
        dict_in_key = tuple(list_of_dict_items)
        state_in_key = tuple( (board_in_key, dict_in_key) )
        key = tuple((state_in_key, player_number))

        valid_actions = get_valid_actions(player_number, state)   

        if key in self.stateMap:
            beta = min(self.stateMap[key], beta)

        if len(valid_actions) == 0 or depth <= 0:
            return (None,self.get_optimal_score(state))

        opponent_number = 2
        if player_number == 2:
            opponent_number = 1

        best_worst_score = beta
        if player_number == self.player_number:
            best_worst_score = alpha

        best_worst_action = None
        for action in valid_actions:
            new_state = self.perform_action(state, action, player_number)
            _, score = self.get_best_move_minimax(new_state, opponent_number, alpha, beta, depth-1)
            if player_number == self.player_number:
                alpha = max(alpha, score)
                if(best_worst_score < score):
                    best_worst_score = score
                    best_worst_action = action
            else:
                beta = min(beta, score)
                if(best_worst_score > score):
                    best_worst_action = action
                    best_worst_score = score
            if(alpha >= beta):
                break

        self.stateMap[key] = best_worst_score
        return best_worst_action, best_worst_score

    def perform_action(self, state, action, player_number):
        is_popout = action[1]
        num_popout = copy.deepcopy(state[1])
        if is_popout:
            num_popout[player_number].decrement()
            new_board = self.pop_from_board(state[0], action[0])
        else:
            new_board = self.add_to_board(state[0], action[0], player_number)
        return (new_board, num_popout)

    def get_best_move_expectimax(self, state, player_number, depth):
        valid_actions = get_valid_actions(player_number, state)
        if len(valid_actions)==0 or depth<=0:
            return (None,self.get_optimal_score(state))
        
        opponent_number = 2
        if player_number == 2:
            opponent_number = 1

        if(player_number == self.player_number):
            best_score = -sys.maxsize
            best_action = None
            for action in valid_actions:
                new_state = self.perform_action(state, action, player_number)
                _, score = self.get_best_move_expectimax(new_state, opponent_number, depth-1)
                if(score > best_score):
                    best_score = score
                    best_action = action
            return (best_action,best_score)
        else:
            avg_score = 0
            for action in valid_actions:
                new_state = self.perform_action(state, action, player_number)
                _, score = self.get_best_move_expectimax(new_state, opponent_number, depth-1)
                avg_score += score
            avg_score /= len(valid_actions)
            return (random.choice(valid_actions), avg_score)

    def get_expectimax_move(self, state: Tuple[np.array, Dict[int, Integer]]) -> Tuple[int, bool]:
        """
        Given the current state of the board, return the next move based on
        the Expecti max algorithm.
        This will play against the random player, who chooses any valid move
        with equal probability
        :param state: Contains:
                        1. board
                            - a numpy array containing the state of the board using the following encoding:
                            - the board maintains its same two dimensions
                                - row 0 is the top of the board and so is the last row filled
                            - spaces that are unoccupied are marked as 0
                            - spaces that are occupied by player 1 have a 1 in them
                            - spaces that are occupied by player 2 have a 2 in them
                        2. Dictionary of int to Integer. It will tell the remaining popout moves given a player
        :return: action (0 based index of the column and if it is a popout move)
        """
        # Do the rest of your implementation here
        MAX_DEPTH = 10
        best_action = None
        class TimeoutException(Exception):
            pass
        def handler(signum, stack):
            raise TimeoutException

        signal.signal(signal.SIGALRM, handler)
        signal.setitimer(signal.ITIMER_REAL, self.time-0.5)
        try:
            for depth in range(1, MAX_DEPTH+1):
                best_action, _ = self.get_best_move_expectimax(state, self.player_number, depth)
        except TimeoutException:
            pass
        return best_action
        
