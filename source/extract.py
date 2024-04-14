
import numpy as np

WIDTH = 700 # width of console
HEIGHT = 750 # height of console


def extractMatrix(nameFile): # return numpy matrix
    last_line = None
    with open(f'input/{nameFile}', 'r') as file:
        for line in file:
            last_line = line
    file.close()
    
    file = open(f'input/{nameFile}', 'r')
    first_line = file.readline().strip().split(' ')
    row = int(first_line[0]) # number of row
    col = int(first_line[1]) # number of col
    matrix = np.zeros((row, col), dtype= int)
    
    i = 0
    for line in file:
        if line != last_line:
            line_vals = line.rstrip().split(',')
            for j in range(col):
                matrix[i][j] = int(line_vals[j])
                  
        i += 1 
    file.close()
    return matrix

def extractLocation(nameFile): # return tuple
    last_line = None
    with open(f'input/{nameFile}', 'r') as file:
        for line in file:
            last_line = line
    last_line_vals = last_line.split(' ')
    x = int(last_line_vals[0])
    y = int(last_line_vals[1])
    location = (x,y)
    return location


    

 
    

