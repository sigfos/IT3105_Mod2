import math
import random


class Node:

    def __init__(self, state):
        self.visits = 0
        self.parent = None
        self.children =[]
        self.wins = 0
        self.state = state


class MCTS:

    def __init__(self, state):
        self.root_node = Node(state)

    def selection(self):
        current_node = self.root_node
        max_node = self.root_node

        # check if not a leaf node and that game is not over
        while len(current_node.children) == len(
                current_node.state.generate_children()) and not current_node.state.check_finished():
            max_value = -1
            for child in current_node.children:
                exploitation_value = child.wins/child.visits
                exploration_value = math.sqrt(2)*math.sqrt(math.log(child.parent.visits)/child.visits)
                if child.state.player == 1:
                    node_value = exploitation_value + exploration_value
                else:
                    node_value = 1 - (exploitation_value + exploration_value)
                if node_value > max_value:
                    max_node = child
                    max_value = node_value
            current_node = max_node
        # print(">>>The returned node has ", len(current_node.children), "children and N = ", current_node.state.N)
        return current_node

    def expansion(self, leaf):
        num = len(leaf.children)
        expanded_node = None
        generated_children = leaf.state.generate_children()
        if len(generated_children) > 0:
            if num == 0:
                expanded_node = Node(generated_children[0])
            else:
                expanded_node = Node(generated_children[num])
            expanded_node.parent = leaf
            leaf.children.append(expanded_node)
        return expanded_node

    def simulation(self, expanded_node):
        # do 1 simulation by a random sequence of moves
        if not expanded_node:
            return
        current_state = expanded_node.state
        while not current_state.check_finished():
            children = current_state.generate_children()
            child = random.choice(children)
            current_state = child
        return current_state.get_result()

    def backprop(self, expanded_node, result_from_simulation):
        # add result to leaf and all parents
        if not expanded_node:
            # print ("No expanded node")
            return
        current_node = expanded_node
        current_node.wins += result_from_simulation
        current_node.visits += 1
        while current_node.parent:
            current_node = current_node.parent
            current_node.wins += result_from_simulation
            current_node.visits += 1

        current_node.wins += result_from_simulation
        current_node.visits += 1

    def run_one_simulation(self):
        selected = self.selection()
        expanded_node = self.expansion(selected)
        for i in range(1000):
            res = self.simulation(expanded_node)
            self.backprop(expanded_node, res)

    def run(self, simulations):
        for i in range(simulations):
            self.run_one_simulation()
        # Find the path in the tree when each player plays optimally
        best_path = [self.root_node]
        selected = self.root_node
        while selected.children:
            best_rate = -1
            print("Player " + str(selected.state.player) + "'s turn.")
            for child in selected.children:
                # check exploitation rate (win rate)
                if child.state.player == 1:
                    win_rate = child.wins/child.visits
                else:
                    win_rate = 1 - child.wins/child.visits
                # choose node with highest win rate
                print("Found node with v =", child.visits, "w = ", child.wins, "win rate = ",
                       win_rate, "and N =", child.state.N)
                if win_rate > best_rate:
                    best_rate = win_rate
                    best_child = child
            best_path.append(best_child)
            print("> Appended N =", best_child.state.N, "to optimal path\n")
            selected = best_child
        return best_path
