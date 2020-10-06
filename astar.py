import pygame
import math
from queue import PriorityQueue

from pygame.constants import MOUSEMOTION

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algo")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
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

    def get_pos(self):
        return self.row, self.col

    def is_closed(self): #Is the node in the closed set (been looked at already)
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_obstacle(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == TURQUOISE

    def reset(self):
        self.colour = WHITE

    def make_closed(self): # Set node colours
        self.colour = RED
    
    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_start(self):
        self.colour = ORANGE

    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE
    
    def draw(self,win):
        pygame.draw.rect(win, self.colour,(self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        pass

    def __lt__(self,other): # Less Than
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
    ROWS = 50
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
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: #right press
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

    pygame.quit()

main(WIN,WIDTH)