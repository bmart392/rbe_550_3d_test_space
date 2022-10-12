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

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)

    def calc_f(self):
        self.f = self.g + self.h

    @staticmethod
    def p2p_dist(s, s_):
        # calculates point to point distance between two locations in the map
        if len(s) == 2 and len(s_) == 2:
            d = m.sqrt((s_[0] - s[0]) ** 2 + (s_[1] - s[1]) ** 2)
        elif len(s) == 3 and len(s_) == 3:
            d = m.sqrt((s_[0] - s[0]) ** 2 + (s_[1] - s[1]) ** 2 + (s_[2] - s[2]) ** 2)
        else:
            print('warn: bad lengths')
            d = None
        return abs(d)


class AStar:

    def __init__(self, world, robot):
        self.world = world
        self.robot = robot

    def recreate_path_to_goal(self):
        pass

    def plan(self, start, goal):
        start_node = Node(None, start)
        start_node.g = start_node.h = 0
        start_node.calc_f()
        axis = plt.gca()
        self.world.plot_cell(axis,start_node, 'r', 5)

        end_node = Node(None, goal)
        end_node.g = end_node.h = 0
        end_node.calc_f()
        self.world.plot_cell(axis,end_node, 'g', 5)

        open_list = []
        closed_set = set()

        open_list.append(start_node)

        plt_cnt = 0
        while len(open_list) > 0:
            curr_node = open_list[0]
            curr_ind = 0
            for index, item in enumerate(open_list):
                if item.f < curr_node.f:
                    curr_node = item
                    curr_ind = index

            open_list.pop(curr_ind)

            if curr_node == end_node:
                res_path = []
                curr_ = curr_node
                while curr_ is not None:
                    res_path.append(curr_.position)
                    curr_ = curr_.parent
                return res_path[::-1] # reversed path

            children = []
            for new_pos in self.robot.motion_options(curr_node.position):
                if self.world.is_valid_cell(new_pos):
                    new_node = Node(curr_node, new_pos)
                    children.append(new_node)

            for child in children:
                if child in closed_set:
                    continue
                child.g = curr_node.g + Node.p2p_dist(curr_node.position,child.position)
                child.h = Node.p2p_dist(child.position, end_node.position)
                child.calc_f()

                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                open_list.append(child)
                closed_set.add(child)
                # if child.position != start_node.position and child.position != end_node.position:
                #     self.world.plot_cell(axis, child, 'c', 1)
            if plt_cnt == 100:
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
    room.plot_occupancy_grid(fig, ax)

    plan = AStar(room, sphere)
    path = plan.plan(start_p, end_p)
    print(path)

    room.plot_path(ax,path)

    plt.show()
