import sys, pygame
import numpy as np
import time


# Grid params
grid_size = 8
freq_live = 0.35

# Live params
lone_death_th = 1
overcrowding_death_th = 4

# Display params
cell_pixel_size = 50

# Colors
COLOR_BACKGROUND = (30, 30, 30)
COLOR_ACTIVE_CELL = (240, 240, 240)
COLOR_LINE = (150, 150, 150)


def init_grid(grid_size, freq_live):
    grid = np.random.random((grid_size, grid_size))
    grid[grid>np.quantile(grid, 1-freq_live)] = 1
    grid[grid!=1] = 0
    return grid


def update_grid(grid):
    grid_new = np.zeros(grid.shape)
    grid_new[1:] += grid[:-1]
    grid_new[:-1] += grid[1:]
    grid_new[:, 1:] += grid[:,:-1]
    grid_new[:, :-1] += grid[:,1:]    
    grid_new[(grid_new>=overcrowding_death_th)|(grid_new<=lone_death_th)] = 0
    grid_new[grid_new!=0] = 1
    return grid_new


def draw_grid(surface, grid):
    # background
    surface.fill(COLOR_BACKGROUND)
    
    # verticals lines
    for i in range(1, grid_size):
        pygame.draw.line(surface, COLOR_LINE, (i*cell_pixel_size, 0), (i*cell_pixel_size, grid_size*cell_pixel_size))
    
    # horizontal lines
    for i in range(1, grid_size):
        pygame.draw.line(surface, COLOR_LINE, (0, i*cell_pixel_size), (grid_size*cell_pixel_size, i*cell_pixel_size))

    # cells
    for x, y in zip(*np.where(grid==1)):
        pygame.draw.rect(surface, COLOR_ACTIVE_CELL, (x*cell_pixel_size, y*cell_pixel_size, cell_pixel_size, cell_pixel_size))
    
    
def main():
    pygame.init()
    surface = pygame.display.set_mode((grid_size*cell_pixel_size, grid_size*cell_pixel_size))
    pygame.display.set_caption("Game of Life")
    grid = init_grid(grid_size, freq_live)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        draw_grid(surface, grid)
        grid = update_grid(grid)
        
        pygame.display.update()
        time.sleep(0.25)
if __name__=='__main__':
    main()