from MCTS import *


class Nim:

    def __init__(self, N = 10, K=3):
        self.player = 1
        self.K = K
        self.N = N

    def check_finished(self):
        if self.N == 0:
            return True
        return False

    def get_result(self):
        if self.check_finished():
            if self.player == 2:
                return 0

            elif self.player == 1:
                return 1
    """
    def move(self, n):
        if n < self.K and n < self.N:
            self.N -= n
            if self.check_finished():
                print("GAME OVER")
                return
            if self.player == 1:
                self.player = 2
            else:
                self.player = 1
        else:
            print("Move not valid")

    """

    def change_player(self):
        if self.player == 1:
            return 2
        else:
            return 1

    def generate_children(self):
        # make new state for every possible move
        # change player
        # change N
        # return list with all children states
        states = []
        for i in range (self.K):
            states.append(Nim(self.N-(i+1)))
            states[i].player = self.change_player()
        return states


def main():
    game = Nim(5, 3)
    mcts = MCTS(game)
    optimal_path = mcts.run(100)

    for node in optimal_path:
        print(node)

# Spill mot menneske
# Spill mot random bot
