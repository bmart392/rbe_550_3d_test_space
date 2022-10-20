#!/usr/bin/env python

from Environment import World, Robot
import matplotlib.pyplot as plt
import math as m


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        # g: length of the shortest path from start to current (so far)
        # h: weight of graph edge

        self.g = 0 # edge weight
        self.h = 0 # goal heuristic
        self.f = 0 # total weight

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def calc_f(self):
        # recalculate total weight
        self.f = self.g + self.h

    @staticmethod
    def p2p_dist(s, s_):
        # calculates point to point euclidian distance between two locations in the map
        if len(s) == 2 and len(s_) == 2: # 2D
            d = m.sqrt((s_[0] - s[0]) ** 2 + (s_[1] - s[1]) ** 2)
        elif len(s) == 3 and len(s_) == 3: # 3D
            d = m.sqrt((s_[0] - s[0]) ** 2 + (s_[1] - s[1]) ** 2 + (s_[2] - s[2]) ** 2)
        else:
            print('warn: bad lengths')
            d = None
        return abs(d)


class AStar:

    def __init__(self, world, robot):
        self.world = world
        self.robot = robot

    def plan(self, start, goal):
        start_node = Node(None, start) # set start node with no parent
        start_node.g = start_node.h = 0 # set start weights to zero
        start_node.calc_f()
        axis = plt.gca()
        self.world.plot_cell(axis,start_node, 'r', 5) # plot start cell

        end_node = Node(None, goal) # set goal node with no parent
        end_node.g = end_node.h = 0 # set end weights to zero
        end_node.calc_f()
        self.world.plot_cell(axis,end_node, 'g', 5) # plot end cell

        open_list = [] # list of cells that can be visited
        closed_set = set() # set of cells that can no longer be visited

        open_list.append(start_node) # add start node to cells to look at, we will start here

        plt_cnt = 0 # counter so we don't update the graph too much
        while len(open_list) > 0: # run until the possible nodes is empty
            curr_node = open_list[0] # set first possible node as current
            curr_ind = 0

            # if there is another open item with a lower cost, use that instead of the current node
            for index, item in enumerate(open_list):
                if item.f < curr_node.f:
                    curr_node = item
                    curr_ind = index

            open_list.pop(curr_ind) # pop newly selected node off the list

            # check for goal condition reached and recreate path
            if curr_node == end_node:
                res_path = []
                curr_ = curr_node
                while curr_ is not None: # start cell is only in chain to have no parent
                    res_path.append(curr_.position) # take the current cells parent position
                    curr_ = curr_.parent
                return res_path[::-1] # output reversed path

            children = []
            for new_pos in self.robot.motion_options(curr_node.position): # get all possible neighbors and cycle through
                # only add to children to list if they are valid
                if self.world.is_valid_cell(new_pos):
                    new_node = Node(curr_node, new_pos) # create new node for child
                    children.append(new_node)

            for child in children:
                if child in closed_set:
                    continue # if child closed, go back to next child
                child.g = curr_node.g + Node.p2p_dist(curr_node.position,child.position) # update edge weight with distacne to child and add to existing node weight
                child.h = Node.p2p_dist(child.position, end_node.position) # calculate heuristic to goal
                child.calc_f() # calculate total weight

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g: # if the child is in the open list and the edge weight is more than another possible node
                        continue # go back to loop to next child

                open_list.append(child) # add child to open list
                closed_set.add(child) # add child to closed list

                # if child.position != start_node.position and child.position != end_node.position:
                #     self.world.plot_cell(axis, child, 'c', 1)

            if plt_cnt == 100: # only plot every 100
                plt.pause(0.0001)
                plt_cnt = 0
            plt_cnt += 1


if __name__ == '__main__':
    # *3D Example*
    # start_p = (5, 5, 0)
    # end_p = (45, 45, 0)
    #
    # room = World('Earth', [50, 50, 1], 'room_map.png')
    # sphere = Robot('Sphere', 1)
    #
    # fig = plt.figure()
    # ax = plt.axes(projection='3d')
    # ax.view_init(elev=90.0, azim=-90.0)
    # room.plot_occupancy_grid(fig, ax)

    # *2D Example*
    start_p = (5, 5)
    end_p = (14, 45)

    room = World('Earth', [50, 50], 'room_map.png')
    sphere = Robot('Sphere', 1)

    fig, ax = plt.subplots()
    room.plot_occupancy_grid(ax)

    plan = AStar(room, sphere)
    path = plan.plan(start_p, end_p)
    print(path)

    room.plot_path(ax,path)

    plt.show()
