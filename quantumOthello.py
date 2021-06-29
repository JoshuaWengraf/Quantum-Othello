# -*- coding: utf-8 -*-
"""
Square grid of counters each initialy hidden 
When you flip a counter it automatically flips another counter on the board.
The aim of the game is to form the largest cluster of counters on the board.
The game is ended when all counters are flipped

"""

import pygame
import numpy as np
import random
import math 
from scipy.ndimage import measurements

#Colours
white = (255,255,255)
grey = (220,220,220)
red = (255,0,0)
pink = (255, 192, 203)
blue = (0,0,255)
black = (0,0,0)

def drawGrid(GameDisplay, grid):
    for i in range(numberOfColumns):
        for j in range(numberOfRows):
            if grid[i,j] == 0:          
                pygame.draw.rect(GameDisplay, grey, (i*(boxwidth)+boxborderthickness, j*(boxwidth)+boxborderthickness, boxwidth-boxborderthickness,boxwidth- boxborderthickness))
            if grid[i,j] == 1:  
                pygame.draw.rect(GameDisplay, red, (i*(boxwidth)+boxborderthickness,j*(boxwidth)+boxborderthickness,boxwidth-boxborderthickness,boxwidth-boxborderthickness))
            if grid[i,j] == 2:   
                pygame.draw.rect(GameDisplay, blue, (i*(boxwidth)+boxborderthickness,j*(boxwidth)+boxborderthickness,boxwidth-boxborderthickness,boxwidth-boxborderthickness))
    
    x, y = pygame.mouse.get_pos()
    i_mouse = math.floor(x/boxwidth) 
    j_mouse = math.floor(y/boxwidth)
    

def highlightMousePosition(i_mouse,j_mouse, GameDisplay):
    if i_mouse in range(numberOfColumns) and j_mouse in range(numberOfRows): #If mouse inside grid
        if grid[i_mouse,j_mouse] == 0: 
            i_redBoxes, j_redBoxes = np.where(matrixOfPairs == matrixOfPairs[i_mouse,j_mouse]) 

            for ctr in range(2):
                pygame.draw.rect(GameDisplay, (255,0,0), (i_redBoxes[ctr]*(boxwidth)+boxborderthickness,j_redBoxes[ctr]*(boxwidth)+boxborderthickness,boxwidth-boxborderthickness,boxwidth-boxborderthickness))
            
    pygame.display.flip()

    
def scoreGridPoint(i_player,j_player, colour):

    if colour == red:
        grid[i_player,j_player] = 1
    if colour == blue:
        grid[i_player,j_player] = 2
  
    
        
def maxClusterSize(GameDisplay, player_number):

    pixels = [[0 for i in range(numberOfColumns)] for j in range(numberOfRows)]
    
    for i in range(numberOfColumns):
        for j in range(numberOfRows):
            if grid[i,j] == player_number:
                pixels[i][j] = 1
                
    [labelledpixels, number_of_clusters] = measurements.label(pixels, [[1,1,1], [1,1,1], [1,1,1]]) #Label all the clusters
    
    cluster_areas = []
    for n in range(1,number_of_clusters+1):
        cluster_areas.append(measurements.sum(pixels, labelledpixels,n))
        
    largest_cluster = max(cluster_areas)
    
    return largest_cluster
    
def endGame(GameDisplay):
    print('End of Game')
    
    print('Player 1 has:', maxClusterSize(GameDisplay,1))
    print('Player 2 has:', maxClusterSize(GameDisplay,2))
            
    pygame.quit()
            
    quit()


numberOfColumns = 4
numberOfRows = 4

grid = np.zeros([numberOfColumns,numberOfRows])

listOfPairs = []
for ctr in range(int(grid.size/2)):
    listOfPairs.append(ctr)
    listOfPairs.append(ctr)

np.random.shuffle(listOfPairs)

matrixOfPairs = np.reshape(listOfPairs, (numberOfColumns, numberOfRows))

boxwidth = 20 
boxborderthickness = 5 

print(matrixOfPairs)

running = True
while running:
    pygame.init() 
    
    screen_width = numberOfColumns * boxwidth + boxborderthickness 
    screen_height = numberOfRows * boxwidth + boxborderthickness

    GameDisplay = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Quantum Othello") 
    GameDisplay.fill(black)
                        
    playing = True 
    while playing:
        x, y = pygame.mouse.get_pos()
        i_mouse = math.floor(x/boxwidth) #get grid coordinate
        j_mouse = math.floor(y/boxwidth)
            
        if i_mouse in range(numberOfColumns) and j_mouse in range(numberOfRows): #If mouse within grid
            n,m = np.where(matrixOfPairs == matrixOfPairs[i_mouse,j_mouse])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                MouseKeys = pygame.mouse.get_pressed()
                if MouseKeys[0]: #If the left mouse button is clicked          
                    
                    if grid[i_mouse,j_mouse] == 0: 

                        scoreGridPoint(i_mouse,j_mouse, red) 
                                               
                        i_values, j_values = np.where(matrixOfPairs == matrixOfPairs[i_mouse,j_mouse])

                        print(i_values)
                        
                        scoreGridPoint(i_values,j_values, red) 
                                              
                        if 0 not in grid:
                            endGame(GameDisplay)

                        # Computers Turn
                        pygame.time.delay(1000)

                        [i_values_cpu, j_values_cpu] = np.where(grid == 0)

                        randomIndex = random.randint(0,len(i_values_cpu)-1)

                        i_cpu = i_values_cpu[randomIndex]
                        j_cpu = j_values_cpu[randomIndex]

                        scoreGridPoint(i_cpu, j_cpu, blue) 
                        
                        i_values_cpu, j_values_cpu = np.where(matrixOfPairs == matrixOfPairs[i_cpu,j_cpu])
                        
                        scoreGridPoint(i_values_cpu, j_values_cpu, blue) 

                        print(grid)
        
        drawGrid(GameDisplay, grid)
        highlightMousePosition(i_mouse,j_mouse, GameDisplay)

        if 0 not in grid: 
            endGame(GameDisplay)
            