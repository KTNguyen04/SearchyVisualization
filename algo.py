from networkx import eulerian_circuit
from settings import EXPAND_COLOR, FINISHED_COLOR, GOAL_COLOR, PATH_COLOR, REACHED_COLOR, SELECTED_COLOR, START_COLOR, UNBLOCKED_COLOR, Settings
from collections import deque
from queue import PriorityQueue
import pygame


class Algo:
    def __init__(self):
        self.start = None
        self.goals = []
        self.matrix = []

    def init_tracer(self):
        self.trace = [[]]

    def bfs(self, drawer):

        queue = deque()
        queue.append(self.start)
        while queue:
            c_cell = queue.popleft()
            self.select(c_cell)
            self.drawy(drawer)

            if self.check_goals(c_cell, drawer):
                self.drawy(drawer)

            for cell in self.get_neighboor(c_cell):
                if self.is_free(cell):
                    self.expand(cell)
                    queue.append(cell)
                    cell.father = c_cell

            self.reached(c_cell)
            self.drawy(drawer)

    def dfs(self, drawer):

        stack = []
        stack.append(self.start)
        while stack:
            c_cell = stack.pop()
            self.select(c_cell)
            self.drawy(drawer)

            if self.check_goals(c_cell, drawer):
                self.drawy(drawer)

            for cell in self.get_neighboor(c_cell):
                if self.is_free(cell):
                    self.expand(cell)
                    stack.append(cell)
                    cell.father = c_cell

            self.reached(c_cell)
            self.drawy(drawer)

    def a_star(self, drawer):
        pq = PriorityQueue()
        self.start.eval = 0
        pq.put((self.start))
        while not pq.empty():
            c_cell = pq.get()
            self.select(c_cell)
            self.drawy(drawer)

            if self.check_goals(c_cell, drawer):
                self.drawy(drawer)
                return

            for cell in self.get_neighboor(c_cell):
                if self.is_free(cell):
                    if (not self.is_expanded(cell)):
                        self.expand(cell)
                        cell.distance = c_cell.distance + 1
                        cell.father = c_cell
                    elif cell.distance > c_cell.distance+1:
                        cell.distance = c_cell.distance + 1
                        cell.father = c_cell
                    # stack.append(cell)
                    cell.eval = self.eval_function(cell)
                    pq.put((cell))

            self.reached(c_cell)
            self.drawy(drawer)

    def heuristic(self, cell):
        return self.euclidean_dis(cell)

    def mannhattan_dis(self, cell):
        if self.goals:
            return abs(cell.row - self.goals[0].row) + abs(cell.col - self.goals[0].col)
        return 0

    def euclidean_dis(self, cell):
        if self.goals:
            return ((cell.row - self.goals[0].row)**2 + (cell.col - self.goals[0].col)**2)**.5
        return 0

    def path_cost(self, cell):
        return cell.distance

    def eval_function(self, cell):
        return self.path_cost(cell) + self.heuristic(cell)

    def is_expanded(self, cell):
        return cell.color == EXPAND_COLOR

    def is_reached(self, cell):
        return cell.color == REACHED_COLOR

    def get_neighboor(self, cell):
        res = []
        pos_x, pos_y = cell.pos
        idx_diff = [(1, 0), (0, 1),  (-1, 0), (0, -1)]
        for i, j in idx_diff:
            c_cell = self.matrix[pos_x+i][pos_y+j]
            res.append(c_cell)

        return res

    def is_free(self, cell):
        return cell.color == UNBLOCKED_COLOR or cell.color == GOAL_COLOR or cell.color == FINISHED_COLOR

    def expand(self, cell):
        cell.color = EXPAND_COLOR

    def reached(self, cell):
        cell.color = REACHED_COLOR

    def select(self, cell):
        cell.color = SELECTED_COLOR

    def check_goals(self, cell, drawer):

        for goal in self.goals:
            if cell == goal:
                if not goal.is_finished():
                    goal.finished()
                    self.make_path(goal, drawer)
                    return True

        return False

    def pathing(self, cell):
        cell.color = PATH_COLOR

    def make_path(self, goal, drawer):
        trace = goal.father
        while trace.father != None:
            self.pathing(trace)
            self.drawy(drawer)

            trace = trace.father

    def run(self, drawer):
        # self.bfs(drawer)
        self.a_star(drawer)

    def update(self):
        self.start.color = START_COLOR
        for goal in self.goals:
            goal.color = GOAL_COLOR

    def drawy(self, drawer):
        drawer()
        self.update()
        pygame.display.flip()
