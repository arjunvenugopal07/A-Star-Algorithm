# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 23:14:01 2020

@author: Arjun Venugopal
"""
#%% Node instance
class node:
    def __init__(self, position, parent_node = None):
        self.position = position
        self.parent_node = parent_node
        self.g_cost = float('inf')
        self.h_cost = float('inf')
        self.f_cost = float('inf')
        self.color = COLOR["WHITE"]

    def get_neighbours(self):
        self.neighbours = []
        position_list = [(-1, -1), (-1, 0), [-1, 1], (0, -1), (0, 1), (1, -1),
                         (1, 0), (1, 1)]
        for position in position_list:
            row = self.position[0] + position[0]
            col = self.position[1] + position[1]
            if row >= 0 and row < num_rows and col >= 0 and col < num_rows :
                neighbour_node = node_list[row][col]
                if not neighbour_node.color == COLOR["GREY"]:
                    self.neighbours.append(neighbour_node)

    def update_cost(self, parent_node):
        row_diff = abs(self.position[0] - start_position[0])
        col_diff = abs(self.position[1] - start_position[1])
        if row_diff + col_diff == 2:
            g_cost = parent_node.g_cost + 14
        else:
            g_cost = parent_node.g_cost + 10

        h_cost = 10 * (abs(self.position[0] - goal_position[0])
                       + abs(self.position[1] - goal_position[1]))
        f_cost = g_cost + h_cost

        return g_cost, h_cost, f_cost

    def update_color(self, status):
        if status == "START":
            self.color = COLOR["GREEN"]
        elif status == "GOAL":
            self.color = COLOR["RED"]
        elif status == "NULL":
            self.color = COLOR["WHITE"]
        elif status == "OPEN":
            self.color = COLOR["PINK"]
        elif status == "CLOSED":
            self.color = COLOR["ORANGE"]
        elif status == "OBSTACLE":
            self.color = COLOR["GREY"]
        elif status == "PATH":
            self.color = COLOR["BLUE"]

    def draw_node(self, window):
        x = self.position[1] * node_width
        y = self.position[0] * node_width
        pg.draw.rect(window, self.color, (x, y, node_width, node_width))

#%%
def generate_nodes():
    node_list = []

    for i in range(num_rows):
        node_list.append([])
        for j in range(num_rows):
            position = (i, j)
            temp_node = node(position)
            node_list[i].append(temp_node)

    return node_list

def draw_lines(window):
    for i in range(num_rows):
        pg.draw.line(window, COLOR["GREY"], (0, i * node_width),
                     (width, i * node_width))
        for j in range(num_rows):
            pg.draw.line(window, COLOR["GREY"], (j * node_width, 0),
                         (j * node_width, width))

def draw_grid(window, node_list):
    window.fill(COLOR["WHITE"])

    for nodes in node_list:
        for temp_node in nodes:
            temp_node.draw_node(window)

    draw_lines(window)
    pg.display.update()

def get_clicked_position(xy_position):
    col, row = xy_position

    row = row // node_width
    col = col // node_width

    position = row, col

    return position

#%% Algorithm
def A_Star_Algorithm(window):
    open_list = PriorityQueue()
    open_list_hash = []
    closed_list = []
    start_node = node(start_position)
    start_node.g_cost = 0
    start_node.h_cost = 10 * (abs(start_position[0] - goal_position[0])
                              + abs(start_position[1] - goal_position[1]))
    start_node.f_cost = start_node.h_cost

    open_list.put((start_node.f_cost, start_node.h_cost, 0, start_node))
    open_list_hash.append(start_node)
    count = 1

    path_list = []
    while not open_list.empty():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        current_node = open_list.get()[3]
        open_list_hash.remove(current_node)
        closed_list.append(current_node)

        if (current_node.position != start_position
            and current_node.position != goal_position):
            current_node.update_color("CLOSED")

        if current_node.position == goal_position:
            path_list.append(goal_position)
            temp_node = current_node.parent_node
            while not temp_node.position == start_position:
                path_list.append(temp_node.position)
                temp_node.update_color("PATH")
                temp_node = temp_node.parent_node
            path_list.append(start_position)
            break

        current_node.get_neighbours()

        for neighbour_node in current_node.neighbours:
            g_cost, h_cost, f_cost = neighbour_node.update_cost(current_node)
            if neighbour_node in closed_list:
                continue

            if (g_cost < neighbour_node.g_cost
                or neighbour_node not in open_list_hash):
                neighbour_node.parent_node = current_node
                neighbour_node.g_cost = g_cost
                neighbour_node.h_cost = h_cost
                neighbour_node.f_cost = f_cost
                if not neighbour_node in open_list_hash:
                    open_list.put((neighbour_node.f_cost,
                                   neighbour_node.h_cost, count,
                                   neighbour_node))
                    open_list_hash.append(neighbour_node)
                    count += 1
                    if (neighbour_node.position != start_position
                        and neighbour_node.position != goal_position):
                        neighbour_node.update_color("OPEN")

        draw_grid(window, node_list)

    return path_list

#%% Main body
def main():
    start = None
    goal = None

    started = False

    run = True
    while run:
        draw_grid(window, node_list)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if started:
                continue

            if pg.mouse.get_pressed()[0]:
                xy_position = pg.mouse.get_pos()
                row, col = get_clicked_position(xy_position)
                temp_node = node_list[row][col]

                if not start and temp_node != goal:
                    start = temp_node
                    start.update_color("START")
                    global start_position
                    start_position = start.position

                elif not goal and temp_node != start:
                    goal = temp_node
                    goal.update_color("GOAL")
                    global goal_position
                    goal_position = goal.position

                elif temp_node != start and temp_node != goal:
                    temp_node.update_color("OBSTACLE")

            if pg.mouse.get_pressed()[2]:
                xy_position = pg.mouse.get_pos()
                row, col = get_clicked_position(xy_position)
                temp_node = node_list[row][col]
                temp_node.update_color("NULL")

                if temp_node == start:
                    start = None

                if temp_node == goal:
                    goal = None

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE and not started and start and goal:
                    for nodes in node_list:
                        for temp_node in nodes:
                            if (temp_node.color != COLOR["RED"] and
                                temp_node.color != COLOR["GREEN"] and
                                temp_node.color != COLOR["GREY"]):
                                temp_node.color = COLOR["WHITE"]
                    path = A_Star_Algorithm(window)
                    if not path:
                        print("No path exists")
                if event.key == pg.K_r and not started:
                    start = None
                    goal = None
                    for nodes in node_list:
                        for temp_node in nodes:
                            temp_node.update_color("NULL")

    pg.quit()

#%% Set parameters and call main function
import pygame as pg
from queue import PriorityQueue

width  = 500
num_rows = 25
node_width = width // num_rows

window = pg.display.set_mode((width, width))
pg.display.set_caption("A Star Path Planning")

COLOR = {"GREEN" : (150, 250, 150), "RED" : (255, 100, 100), "WHITE" : (255, 255, 255),
         "GREY" : (100, 100, 100), "BLUE" : (204, 229, 255),
         "ORANGE" : (255, 229, 204), "PINK" : (255, 204, 229),}

node_list = generate_nodes()

main()
