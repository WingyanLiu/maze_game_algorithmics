#using depth first search (DFS) to generate walls for the maze game.
import numpy
from random import randint
from maze_game_classes import Wall

def maze_wall_generator(path_width, path_height, map_x_dim, map_y_dim):
    rows = map_y_dim//path_height
    square_height = map_y_dim//rows
    wall_height = int((map_y_dim%path_height)/rows)
    columns = map_x_dim//path_width
    square_width = map_x_dim//rows
    wall_width = int((map_x_dim%path_width)/columns)
    
    
    #preventing walls from being too thin
    if wall_height <=5:
        rows -= 1
        wall_height = wall_height + path_height//(rows-1)
    if wall_width <=5:
        columns -= 1
        wall_width = wall_width + path_width//(columns-1)
    
    
    walls=list()
    walls_horizontal = list()
    walls_vertical = list()
    print('wall_width:',wall_width)
    print('wall_height:',wall_height)
    print('square_width:',square_width)
    print('square_height',square_height)

    for r in range(rows-1):
        h = list()
        for c in range(columns):
            x_pos = square_width*(c+1)+wall_width*c
            y_pos = square_height*(r+1)+wall_height*r
            width = square_width
            height = wall_height
            h.append(Wall(x_pos,y_pos,width,height))
        walls_horizontal.append(h)

    for r in range(rows):
        v = list()
        for c in range(columns-1):
            x_pos = square_width*(c+1)+wall_width*(c+1)
            y_pos = square_height*r+wall_height*r
            width = wall_width
            height = square_height
            v.append(Wall(x_pos,y_pos,width,height))
        walls_vertical.append(v)
    
    walls.append(walls_horizontal)
    walls.append(walls_vertical)

    maze_matrix = numpy.zeros([rows,columns])
    print(walls)
    #DPS data structure
    all_vertex = dict()
    for i in range(rows):
        for j in range(columns):
            property = dict()
            property['visited']=False
            connected_squares = list()
            if i-1>=0:
                connected_squares.append(f'r{i-1}c{j}')
            if i+1!=rows:
                connected_squares.append(f'r{i+1}c{j}')
            if j-1>=0:
                connected_squares.append(f'r{i}c{j-1}')
            if j+1!=columns:
                connected_squares.append(f'r{i}c{j+1}')
            property['connected_squares']=connected_squares
            all_vertex[f'r{i}c{j}']=property
    print(all_vertex)

    #Chosing a starting point (must lay on one of the walls)
    fixed_axises = ['x','y']
    chosen_starting_axis = fixed_axises[randint(0,1)]
    if chosen_starting_axis == 'x':
        all_x_axis = [0,rows-1]
        which_axis = randint(0,1)
        chosen_starting_x = all_x_axis[which_axis]
        chosen_starting_y = randint(0,columns-1)
        chosen_starting_square = f'r{chosen_starting_x}c{chosen_starting_y}'
    if chosen_starting_axis == 'y':
        all_y_axis = [0,columns-1]
        which_axis = randint(0,1)
        chosen_starting_x = all_y_axis[which_axis]
        chosen_starting_y = randint(0,rows-1)
        chosen_starting_square = f'r{chosen_starting_x}c{chosen_starting_y}'
    
    print(chosen_starting_square)

    
    def go_until_deadend(chosen_starting_square):
        reached_dead_end = False
        visited_squares = list()
        while reached_dead_end != True:
            all_vertex[chosen_starting_square]['visited']=True
            visited_squares.append(chosen_starting_square)
            options_to_visit = all_vertex[chosen_starting_square]['connected_squares']
            if len(options_to_visit)>0:
                chosen_starting_square = options_to_visit[randint(0,len(options_to_visit)-1)]
                while all_vertex[chosen_starting_square]['visited']== True and len(options_to_visit) > 0:
                    options_to_visit.remove(chosen_starting_square)
                    if len(options_to_visit)>0:
                        chosen_starting_square = options_to_visit[randint(0,len(options_to_visit)-1)]
            if len(options_to_visit) == 0:
                reached_dead_end = True
        if len(visited_squares)>1:
            return visited_squares
        else:
            return []

    def backtracking(visited_squares):
        visited_squares_copy = visited_squares.copy()
        while len(visited_squares_copy) > 0:
            chosen_starting_square = visited_squares_copy[-1]
            options_to_visit = all_vertex[chosen_starting_square]['connected_squares']
            while len(options_to_visit)>0:
                visited_squares_new = go_until_deadend(chosen_starting_square)
                visited_squares=visited_squares+visited_squares_new
            visited_squares_copy.pop()
        return visited_squares

    visited_squares_old = go_until_deadend(chosen_starting_square)
    visited_squares_new = backtracking(visited_squares_old)

    while len(visited_squares_new)-len(visited_squares_old)>0:
        visited_squares_old = visited_squares_new
        visited_squares_new = backtracking(visited_squares_old)

    print(visited_squares_new)
    for coord in all_vertex:
        if all_vertex[coord]['visited']==False:
            print('False')
    


    for i in range(len(visited_squares_new)-1):
        current_square = visited_squares_new[i]
        current_coord = current_square[1:].split('c')
        next_square = visited_squares_new[i+1]
        next_coord = next_square[1:].split('c')
        print('Current_coord:',current_coord,'Next_coord:',next_coord)
        if next_coord[0]==current_coord[0]:
            if current_coord[1]<next_coord[1]:
                walls[1][int(current_coord[0])][int(current_coord[1])] = 0
            else:
                walls[1][int(next_coord[0])][int(next_coord[1])] = 0
        
        if next_coord[1]==current_coord[1]:
            if current_coord[0]<next_coord[0]:
                walls[0][int(current_coord[0])][int(current_coord[1])] = 0
            else:
                walls[0][int(next_coord[0])][int(current_coord[1])] = 0

    print(walls)
    return walls
