import pygame
import math
from queue import PriorityQueue

from pygame.constants import MOUSEMOTION

WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algo")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width # for drawing in pygame
        self.y = col*width 
        self.colour = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.weight = 1
        


    def get_pos(self):
        return self.row, self.col

    def is_closed(self): #Is the node in the closed set (been looked at already)
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_obstacle(self):
        return self.colour == BLACK

    def is_rough(self):
        return self.colour == BLUE

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == TURQUOISE

    def reset(self):
        self.colour = WHITE
        self.weight = 1

    def make_closed(self): # Set node colours
        self.colour = RED

    def make_closed_rough(self):
        self.colour = ORANGE
    
    def make_open(self):
        self.colour = GREEN

    def make_obstacle(self):
        self.colour = BLACK

    def make_rough(self):
        self.colour = BLUE
        self.weight = 10 

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE
    
    def draw(self,win):
        pygame.draw.rect(win, self.colour,(self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])


    def __lt__(self,other): # Less Than
        return False

def reconstruct_path(prev_node,current,draw):
    while current in prev_node:
        current = prev_node[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #heat sort algo get min element from queue
    open_set.put((0, count, start)) #add start node into open set
    prev_node = {} # dictionary for prev node - keeps track of where current node came from
    g_score = {node: float("inf") for row in grid for node in row} # current shortest distance from start node to current node
    g_score[start] = 0  
    f_score = {node: float("inf") for row in grid for node in row} # predicted distance from current node to end node (manhattan length)
    f_score[start] = h(start.get_pos(), end.get_pos()) # initial heuristic from start to end node

    open_set_hash = {start} #check what is in PriorityQueue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() # this algo takes over quit below

        current = open_set.get()[2] # get node object from PriorityQueue
        open_set_hash.remove(current) # remove current node from open set

        if current == end: # if at end, algo done
            reconstruct_path(prev_node, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors: # otherwise look at current node neighbors
            temp_g_score = g_score[current] + neighbor.weight # add weight of node

            if temp_g_score < g_score[neighbor]: # if temp g_score is better than current g_score, update
                prev_node[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash: # Add node to open set
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start and current.weight == 1:
            current.make_closed()
        elif current != start and current.weight > 1:
            current.make_closed_rough()
    
    return False

def h(p1,p2): # H function (heuristic) using Manhattan Length
    x1,y1 = p1
    x2,y2 = p1
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    gap = width // rows #interger division 
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,gap,rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap),(width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0),(j * gap, width))

def draw(win, grid,rows, width): #main draw function
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid_lines(win, rows,width)
    pygame.display.update()
        
# get mouse position for click

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row,col

# Main function
def main(win,width):
    ROWS = 30
    grid = make_grid(ROWS,width)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(win,grid,ROWS,WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue # stops user from changing once started (apart from quit)

            if pygame.mouse.get_pressed()[0]: #left key press
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]: #right press
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            elif pygame.mouse.get_pressed()[1]: #mid press
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if node != end and node != start:
                    node.make_rough()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS,width)
    pygame.quit()

main(WIN,WIDTH)