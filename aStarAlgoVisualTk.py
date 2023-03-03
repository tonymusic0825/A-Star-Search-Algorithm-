"""
    Simple A* search algorithm on a 50x50 grid created using TKinter.
"""

from tkinter import *
from queue import PriorityQueue
import time
import sys

def heuristic(n1, n2):
    """Returns the Mahattan distance between two nodes.
    
    Parameter:
        n1: (x, y) coordinate position of node 1.
        n2: (x2, y2) coordinate position of node2.
    
    Return:
        (int): Manhattan distance between n1 and n2
    """
    x1, y1 = n1
    x2, y2 = n2

    return abs(x2 - x1) + abs(y2 - y1)

def create_optimal_path(most_eff_previous_node, end, start):
    """Creates and shows the most optimal path of the A* star algorithm

    Parameter:
        most_eff_previous_node: Dictionary of nodes that are the most efficient path to their corresponding key node
        end: End Node
        start: Start Node
    """

    while end in most_eff_previous_node:
        end = most_eff_previous_node[end]
        end.optimal()
        if end == end and end == start:
            end.make_start()
        end.draw()

def aStarAlgorithm(grid, start, end, neighbours, master):
    """The A* algorithm
    
    Parameter:
        grid: A NodeGrid instance
        start: Start Node
        end: End Node
        neighbours: A dictionary of neighbours using NodeGrid.find_all_neighbours() method
        master: Tk root (in this case NodeGrid())
    """
    
    count = 0
    # Create priorityqueue for A* algorithm and add the Start Node
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    most_eff_previous_node = {}

    # Remember that the total cost of a search step F(n) is...
    # The step cost + the heuristic => F(n) = G(n) + H(n)
    # Thus we will create a dictionary and include each node of the grid as a key
    # and initialize an "infinity" value to each key
    g = {}
    f = {}

    for row in grid:
        for node in row:
            g[node] = float("inf")
            f[node] = float("inf")
    
    f[start] = heuristic(start.get_pos(), end.get_pos())
    g[start] = 0
    
    # We will now include our starting node within the open set hash and start the algorithm
    open_set_hash = {start}

    while not open_set.empty():

        current_node = open_set.get()[2]
        open_set_hash = {current_node}

        if current_node == end:
            create_optimal_path(most_eff_previous_node, current_node, start)
            return True


        for neighbour in neighbours[current_node]:
            # Calculate a temp G(n) for each neighbour of current node
            temp_g_score = g[current_node] + 1

            if temp_g_score < g[neighbour]:
                # If the temp G(n) is less than the current G(n) of the current neighbour
                # Then assign this G(n) score and also calculate the F(n) and assign it
                g[neighbour] = temp_g_score
                f[neighbour] = temp_g_score + heuristic(neighbour.get_pos(), end.get_pos())
                most_eff_previous_node[neighbour] = current_node

                # Now if the current neighbour isn't in the open set hash
                # Count + 1 and add the current neighbour and it's F(n) score to the priorityqueue and hash
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    if neighbour == end or neighbour == start:
                        continue
                    else:
                        # Make neighbour a frontier and redraw
                        neighbour.frontier()
                        neighbour.draw()
        
        if current_node != start:
            # Once finished this node does not need to be used again in
            # our calculations thus we will close it off and make it explorered
            current_node.explored()
            current_node.draw()
        
    return False

class Node():
    """The Node class. Multiple instances of the Node class stacked up will create a grid."""

    # Colour constants
    FRONTIER_COLOUR = "green"
    EXPLORED_COLOUR = "red"
    OPTIMAL_PATH = "yellow"
    BARRIER_COLOUR = "black"
    START_END_COLOUR = "blue"
    EMPTY_COLOUR = "white"

    def __init__(self, master, x, y, total_rows, window_width):
        """
        Parameters:
            master: Tkinter Canvas (Grid).
            x: X-coordinate position.
            y: Y-coordinate position.
            total_rows: Total number of rows in the grid.
            window_width: Width of tkinter window.
        """
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
        """(x, y) coordinate of node."""
        return self.x, self.y
    
    def get_status(self):
        """Node status."""
        return self.status
    
    def make_start(self):
        """Make this node the starting node."""
        self.fill = Node.START_END_COLOUR
        self.status = "start"
    
    def make_end(self):
        """Make this node the end node."""
        self.fill = Node.START_END_COLOUR
        self.status = "end"
    
    def frontier(self):
        """Make this node a frontier node."""
        self.fill = Node.FRONTIER_COLOUR
        self.status = "frontier"
    
    def explored(self):
        """Make this node explored."""
        self.fill = Node.EXPLORED_COLOUR
        self.status = "explored"
    
    def optimal(self):
        """Make this node an optimal path."""
        self.fill = Node.OPTIMAL_PATH
        self.status = "optimal"
    
    def reset(self):
        """Reset this node."""
        self.fill = Node.EMPTY_COLOUR
        self.status = "empty"

    def barrier(self):
        """Make this node a barrier."""
        self.fill = Node.BARRIER_COLOUR
        self.status = "barrier"
    
    def draw(self):
        """Draw this node in the grid. Used during grid initialization and colour changes"""
        xmin = self.x * self.size
        xmax = xmin + self.size
        ymin = self.y * self.size
        ymax = ymin + self.size

        self.master.create_rectangle(xmin, ymin, xmax, ymax,
                                        fill = self.fill, outline = self.outline)
    
    # USED FOR CREATION ANIMATIONS IN TKINTER
    # def time_delay_draw(self):
    #     xmin = self.x * self.size
    #     xmax = xmin + self.size
    #     ymin = self.y * self.size
    #     ymax = ymin + self.size
    #     self.master.after(500, lambda : 
    #                     self.master.create_rectangle(xmin, ymin, xmax, ymax, 
    #                         fill = self.fill, outline = self.outline))
    
class NodeGrid(Canvas):
    """The Node Grid class. A sub-class of Tk.Canvas. This class will hold the 
    Node instances (50x50) to create a grid in which to perform the A* algorithm."""
    def __init__(self, master, total_rows, window_width, *args, **kwargs):
        """
        Parameters:
            master: Tkinter root
            total_rows: Total number of rows in the grid
            window_width: Width of tkinter window
        """

        self.node_size = window_width // total_rows

        Canvas.__init__(self, master, width = self.node_size * total_rows, height = self.node_size * total_rows,
                        *args, **kwargs)
        
        self.total_rows = total_rows
        self.grid = []
        self.start_end_node_count = 0
        self.start_node = None
        self.end_node = None

        # Create nodes and stores them in a list
        for row in range(total_rows):
            temp_row = []
            for column in range(total_rows):
                temp_row.append(Node(self, row, column, total_rows, window_width))
            
            self.grid.append(temp_row)
    
        # bind all event actions
        self.bind("<Button-1>", self.mouseClick)
        self.bind_all("<space>", self.spaceKey)
        # self.bind("<Motion>", self.motion)
        self.draw()
    
    def find_all_neighbours(self):
        """
        Finds all nodes that are neighbours (Up, Down, Left, Right, Diagonals are EXCLUDED and not considered neighbours) 
        and then returns them in a dictionary format.

        Return:
            (Dict) Dictionary of nodes paired to a key node
        """
        neighbours = {}

        for row in self.grid:
            for node in row:
                temp_neighbours = []
                x, y = node.get_pos()

                # Check Up
                if y > 0 and self.grid[x][y - 1].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x][y - 1])
                # Check Down
                if y < self.total_rows - 1 and self.grid[x][y + 1].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x][y + 1])
                # Check Left
                if x > 0 and self.grid[x - 1][y].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x - 1][y])
                # Check Right 
                if x < self.total_rows - 1 and self.grid[x + 1][y].get_status() != "barrier":
                    temp_neighbours.append(self.grid[x + 1][y])
                # Assign neighbours to key Node
                neighbours[node] = temp_neighbours
        
        return neighbours
        
    def draw(self):
        """Draws all nodes into self (Tk.Canvas)."""
        for row in self.grid:
            for node in row:
                node.draw()

    def eventCoord(self, event):
        """Event handler for mouse position

        Parameters:
            event: A Tk.event
        
        Return:
            (tuple): (x, y) coordinate of the node that's the mouse is hovering over
        """
        row = event.x // self.node_size
        col = event.y // self.node_size

        return row, col

    def mouseClick(self, event):
        """Event handler for mouse clicks

        Parameters:
            event: A Tk.event
        """

        # Get node that has been clicked on
        row, col = self.eventCoord(event)
        node = self.grid[row][col]

        # If start and end nodes have not been assigned then make node start or end
        # The program will assign the selected node as a start node if no start node has been created
        # and will assign end nodes if the start node has been created but an end node hasn't been created.
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
        # If Start & End nodes have been created them clicking on nodes will make them a barrier
        # Barriers can be clicked on again to reset them to an empty Node
        elif node.get_status() == "empty":
            node.barrier()
        elif node.get_status() == "barrier":
            node.reset()
        
        node.draw()
    
    def spaceKey(self, event):
        """Event handler for the 'space' key. This will start and run the A* algorithm

        Parameters:
            event: A Tk.event
        """
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


