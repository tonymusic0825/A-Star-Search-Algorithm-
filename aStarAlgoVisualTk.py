from tkinter import *
from queue import PriorityQueue
import time
import sys


def heuristic(n1, n2):
    x1, y1 = n1
    x2, y2 = n2

    return abs(x2 - x1) + abs(y2 - y1)

def create_optimal_path(most_eff_previous_node, end, start):

    while end in most_eff_previous_node:
        end = most_eff_previous_node[end]
        end.optimal()
        if end == end and end == start:
            end.make_start()
        end.draw()

def aStarAlgorithm(grid, start, end, neighbours, master):
    
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    most_eff_previous_node = {}
    g = {}
    f = {}

    for row in grid:
        for node in row:
            g[node] = float("inf")
            f[node] = float("inf")
    
    f[start] = heuristic(start.get_pos(), end.get_pos())
    g[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        time.sleep(0.025)
        current_node = open_set.get()[2]
        open_set_hash = {current_node}

        if current_node == end:
            create_optimal_path(most_eff_previous_node, current_node, start)
            return True

        for neighbour in neighbours[current_node]:
            temp_g_score = g[current_node] + 1

            if temp_g_score < g[neighbour]:
                g[neighbour] = temp_g_score
                f[neighbour] = temp_g_score + heuristic(neighbour.get_pos(), end.get_pos())
                most_eff_previous_node[neighbour] = current_node

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    if neighbour == end or neighbour == start:
                        continue
                    else:
                        neighbour.frontier()
                        neighbour.draw()
        
        if current_node != start:
            current_node.explored()
            current_node.draw()
        
    return False

class Node():

    FRONTIER_COLOUR = "green"
    EXPLORED_COLOUR = "red"
    OPTIMAL_PATH = "yellow"
    BARRIER_COLOUR = "black"
    START_END_COLOUR = "blue"
    EMPTY_COLOUR = "white"


    def __init__(self, master, x, y, total_rows, window_width):
        self.master = master
        self.size = window_width // total_rows
        self.x = x
        self.y = y
        self.row = x // self.size
        self.col = y // self.size
        self.fill = Node.EMPTY_COLOUR
        self.outline = "black"
        self.status = "empty"

    def get_pos(self):
        return self.x, self.y
    
    def get_status(self):
        return self.status
    
    def make_start(self):
        self.fill = Node.START_END_COLOUR
        self.status = "start"
    
    def make_end(self):
        self.fill = Node.START_END_COLOUR
        self.status = "end"
    
    def frontier(self):
        self.fill = Node.FRONTIER_COLOUR
        self.status = "frontier"
    
    def explored(self):
        self.fill = Node.EXPLORED_COLOUR
        self.status = "explored"
    
    def optimal(self):
        self.fill = Node.OPTIMAL_PATH
        self.status = "optimal"
    
    def reset(self):
        self.fill = Node.EMPTY_COLOUR
        self.status = "empty"

    def barrier(self):
        self.fill = Node.BARRIER_COLOUR
        self.status = "barrier"
    
    def draw(self):
        
        xmin = self.x * self.size
        xmax = xmin + self.size
        ymin = self.y * self.size
        ymax = ymin + self.size

        # if self.status == "frontier" or self.status == "explored":
        #     self.master.after(500, lambda : 
        #                 self.master.create_rectangle(xmin, ymin, xmax, ymax, 
        #                     fill = self.fill, outline = self.outline))
        # else:
        self.master.create_rectangle(xmin, ymin, xmax, ymax,
                                        fill = self.fill, outline = self.outline)
    
    def time_delay_draw(self):
        xmin = self.x * self.size
        xmax = xmin + self.size
        ymin = self.y * self.size
        ymax = ymin + self.size
        self.master.after(500, lambda : 
                        self.master.create_rectangle(xmin, ymin, xmax, ymax, 
                            fill = self.fill, outline = self.outline))
    

class NodeGrid(Canvas):
    def __init__(self, master, total_rows, window_width, *args, **kwargs):

        self.node_size = window_width // total_rows

        Canvas.__init__(self, master, width = self.node_size * total_rows, height = self.node_size * total_rows,
                        *args, **kwargs)
        
        self.total_rows = total_rows
        self.grid = []
        self.start_end_node_count = 0
        self.start_node = None
        self.end_node = None

        for row in range(total_rows):
            temp_row = []
            for column in range(total_rows):
                temp_row.append(Node(self, row, column, total_rows, window_width))
            
            self.grid.append(temp_row)
    
        #bind all event actions
        self.bind("<Button-1>", self.mouseClick)
        self.bind_all("<space>", self.spaceKey)
        # self.bind("<Motion>", self.motion)
        self.draw()
    
    def find_all_neighbours(self):
        neighbours = {}

        for row in self.grid:
            for node in row:
                temp_neighbours = []
                x, y = node.get_pos()

                if y > 0 and self.grid[x][y - 1].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x][y - 1])
                
                if y < self.total_rows - 1 and self.grid[x][y + 1].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x][y + 1])
                
                if x > 0 and self.grid[x - 1][y].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x - 1][y])
                
                if x < self.total_rows - 1 and self.grid[x + 1][y].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x + 1][y])
                
                neighbours[node] = temp_neighbours
        
        return neighbours
        


    # def motion(self, event):
    #     x, y = event.x, event.y
    #     print(x, y)

    def draw(self):
        for row in self.grid:
            for node in row:
                node.draw()

    def eventCoord(self, event):
        row = event.x // self.node_size
        col = event.y // self.node_size

        return row, col

    def mouseClick(self, event):
        row, col = self.eventCoord(event)
        node = self.grid[row][col]

        if node.get_status() == "start":
            node.reset()
            self.start_node = None
            self.start_end_node_count -= 1
        elif node.get_status() == "end":
            node.reset()
            self.end_node = None
            self.start_end_node_count -= 1
        elif self.start_end_node_count < 2 and not self.start_node:
            if node != self.end_node:
                node.make_start()
                self.start_node = node
                self.start_end_node_count += 1
        elif self.start_end_node_count < 2 and not self.end_node:
            if node != self.start_node:
                node.make_end()
                self.end_node = node
                self.start_end_node_count += 1
        elif node.get_status() == "empty":
            node.barrier()
        elif node.get_status() == "barrier":
            node.reset()
        
        node.draw()
    
    def spaceKey(self, event):
        aStarAlgorithm(self.grid, self.start_node, self.end_node, self.find_all_neighbours(), self.master)

def main():
    WINDOW_WIDTH = 1000
    TOTAL_ROWS = 50
    root = Tk()
    root.geometry('1000x1000')
    grid = NodeGrid(root, TOTAL_ROWS, WINDOW_WIDTH)
    grid.pack()

    root.mainloop()

if __name__ == "__main__":
    main()


