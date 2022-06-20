import Queue
import copy
import itertools


class Indexes:

    def __init__(self, i, j) -> None:
        self.i = i
        self.j = j


class Node:

    def __init__(self, state, depth=0) -> None:
        self.depth = depth
        self.state = state
        for i, dimension in enumerate(self.state):
            for j, value in enumerate(dimension):
                if value == 0:
                    self.index_of_blank_tile = Indexes(i, j)


class Agent:

    def __init__(self) -> None:
        self.max_fringe_size = 0
        self.count_of_expanded_nodes = 0
        self.goal_state = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        self.flat_goal_state = list(itertools.chain(self.goal_state))
        self.total_count_of_expanded_nodes = 0

    def reset_statistics(self):
        self.max_fringe_size = 0
        self.count_of_expanded_nodes = 0

    def is_state_in_reached_state(self, state):

        if len(self.reached_states) == 0:
            return False

        for reached_state in self.reached_states:
            if self.check_elementwise(state, reached_state):
                return True

        return False

    def get_inversion_count(self, start_state):
        flatten_start_state = self.flatten_list(start_state)
        inversion_count = 0
        for i in range(len(flatten_start_state)):
            for j in range(i + 1, len(flatten_start_state)):
                if flatten_start_state[i] != 0 and flatten_start_state[j] != 0 and flatten_start_state[i] > flatten_start_state[j]:
                    inversion_count += 1

        return inversion_count

    def is_given_solvable(self, state):
        inversion_count = self.get_inversion_count(state)
        return (inversion_count % 2) == 0

    def depth_first_search(self, start_state, start_at_random_state=False):
        if start_at_random_state:
            start_state = self.get_random_state()
        self.reset_statistics()
        self.fringe = Queue.LIFOFringe()
        return self.start_search(start_state)

    def get_random_state(self):
        pass

    def depth_limited_search(self, start_state, depth_limit, start_at_random_state=False):
        if start_at_random_state:
            start_state = self.get_random_state()
        self.reset_statistics()
        self.fringe = Queue.LIFOFringe()
        return self.start_search(start_state, depth_limit)

    def breadth_first_search(self, start_state, start_at_random_state=False):
        if start_at_random_state:
            start_state = self.get_random_state()
        self.reset_statistics()
        self.fringe = Queue.FIFOFringe()
        return self.start_search(start_state, start_at_random_state)

    def start_search(self, start_state, depth_limit=0):
        self.initial_node = Node(start_state)
        self.depth_limit = depth_limit
        if self.is_given_solvable(start_state):
            self.reached_states = []
            final_state = self.expand_and_check_fringe_until_goal_state_found()
            self.total_count_of_expanded_nodes += self.count_of_expanded_nodes
            if final_state == 'Failure':
                return ('-', '-', 'Depth limit reached')
            return (final_state, self.max_fringe_size, self.count_of_expanded_nodes)
        else:
            return ('-', '-', 'Not Solvable')

    def expand_and_check_fringe_until_goal_state_found(self):
        self.fringe.push(self.initial_node)
        while self.fringe.is_not_empty():
            self.initial_node = self.fringe.pop()
            if self.expand_initial_node_and_check_for_goal_and_reached_and_limit():
                return self.goal_state

        return 'Failure'

    def iterative_depth_limit(self, start_state, start_at_random_state=False):
        limit = 1
        self.total_count_of_expanded_nodes = 0
        while True:
            final_state, max_fringe_size, count_of_expanded_nodes = self.depth_limited_search(
                start_state, limit, start_at_random_state)

            if count_of_expanded_nodes == 'Depth limit reached':
                limit += 1

            else:
                break

        return final_state, max_fringe_size, self.total_count_of_expanded_nodes

    def add_fring_if_child_not_reached_and_not_goal(self, child):
        if child is not None:
            if self.is_given_state_goal_state(child.state):
                return True

            if self.is_state_in_reached_state(child.state):
                pass
            else:
                self.reached_states.append(child.state)
                self.fringe.push(child)
                if len(self.fringe) > self.max_fringe_size:
                    self.max_fringe_size = len(self.fringe)

            return False

    def flatten_list(self, lis):
        return list(itertools.chain(*lis))

    def check_elementwise(self, initial_state, goal_state):
        flat_initial_state = self.flatten_list(initial_state)
        flat_goal_state = self.flatten_list(goal_state)
        for i in range(9):
            if flat_initial_state[i] != flat_goal_state[i]:
                return False

        return True

    def is_given_state_goal_state(self, given_state):
        return self.check_elementwise(given_state, self.goal_state)

    def swap_up_tile_and_get_child(self):
        return self.swap_tile_and_return_child(Indexes(1, 0))

    def swap_down_tile_and_get_child(self):
        return self.swap_tile_and_return_child(Indexes(-1, 0))

    def swap_right_tile_and_get_child(self):
        return self.swap_tile_and_return_child(Indexes(0, 1))

    def swap_left_tile_and_get_child(self):
        return self.swap_tile_and_return_child(Indexes(0, -1))

    def swap_tile_and_return_child(self, direction_indexes):
        none_blank_tile_indexes = self.find_none_blank_tile_indexes(
            direction_indexes)
        try:
            new_state = self.get_new_state(none_blank_tile_indexes)
            if self.is_state_in_reached_state(new_state):
                return
            return Node(new_state, self.initial_node.depth + 1)
        except:
            pass

    def find_none_blank_tile_indexes(self, direction_indexes):
        blank_tile_indexes = self.initial_node.index_of_blank_tile
        none_blank_tile_i = blank_tile_indexes.i + direction_indexes.i
        none_blank_tile_j = blank_tile_indexes.j + direction_indexes.j
        return Indexes(none_blank_tile_i, none_blank_tile_j)

    def initiliaze_new_state(self):
        initial_state = self.initial_node.state
        new_state = copy.deepcopy(initial_state)
        return new_state

    def calculate_new_state(self, new_state, none_blank_tile_indexes):
        initial_state = self.initial_node.state
        blank_tile_indexes = self.initial_node.index_of_blank_tile
        value_of_non_blank_tile = initial_state[none_blank_tile_indexes.i][none_blank_tile_indexes.j]
        new_state[none_blank_tile_indexes.i][none_blank_tile_indexes.j] = 0
        new_state[blank_tile_indexes.i][blank_tile_indexes.j] = value_of_non_blank_tile

    def get_new_state(self, none_blank_tile_indexes):
        new_state = self.initiliaze_new_state()
        self.calculate_new_state(new_state, none_blank_tile_indexes)
        return new_state

    def expand_initial_node_and_check_for_goal_and_reached_and_limit(self):
        is_goal = False
        if self.is_limit_reached():
            return is_goal

        self.count_of_expanded_nodes += 1
        childs = []
        childs.append(self.swap_up_tile_and_get_child())
        childs.append(self.swap_down_tile_and_get_child())
        childs.append(self.swap_left_tile_and_get_child())
        childs.append(self.swap_right_tile_and_get_child())

        for child in childs:
            is_goal = is_goal or self.add_fring_if_child_not_reached_and_not_goal(
                child)

        return is_goal

    def is_limit_reached(self):
        new_node_depth = self.initial_node.depth + 1
        if self.depth_limit != 0 and new_node_depth > self.depth_limit:
            return True

        else:
            return False

def pr_results(type, final_state, max_fringe_size, count_of_expanded_nodes):
    print('Algorithm type:')
    print(type)
    print('Max fringe size: ')
    print(max_fringe_size)
    print('Count of expanded nodes: ')
    print(count_of_expanded_nodes)
    for row in final_state:
        print(row)


def save_results_to_file(type, final_state, max_fringe_size, count_of_expanded_nodes):
    with open('results.txt', 'a') as file:
        file.write(type + '\n')
        if count_of_expanded_nodes != 'Not Solvable':
            file.write('Count of expanded nodes: ')
            file.write(str(count_of_expanded_nodes))
            file.write('\nMax fringe size: ')
            file.write(str(max_fringe_size))
            file.write('\n')
            for row in final_state:
                file.write('[')
                for num in row:
                    file.write(str(num))
                    file.write(',')
                file.write(']\n')
        else:
            file.write('Not solvable\n')

            

def save_input_to_file(start_state):
    with open('results.txt', 'a') as file:
        file.write('Start State:\n')
        for row in start_state:
            file.write('[')
            for num in row:
                file.write(str(num))
                file.write(',')
            file.write(']\n')


def pr_input(start_state):
    print('Start state:')
    for row in start_state:
        print(row)





start_state = [[3, 1, 2], [4, 5, 8], [6, 0, 7]]
agent = Agent()
pr_input(start_state)
pr_results('Breadth First', *agent.breadth_first_search(start_state))
pr_results('Depth Limited', *agent.depth_limited_search(start_state, depth_limit=10))
pr_results('Iterative Depth Limit', *agent.iterative_depth_limit(start_state))
pr_results('Depth First', *agent.depth_first_search(start_state))