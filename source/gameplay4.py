import heapq
import extract
from pygame import event, QUIT, display
import render

# Heuristic function (h(x): estimated distance from processing location to goal)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(matrix, node): # node = tuple (x,y) => node[0] = x, node[1] = y
    neighbors = []
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Phải trái trên dưới
        if 0 <= node[0] + i < len(matrix) and 0 <= node[1] + j < len(matrix[0]) and (matrix[node[0] + i][node[1] + j])  != 1 : # check index of node is out of range and not a wall
                                                                                                                                                                                                #here or (matrix[node[0] + i][node[1] + j] ==0)
            if 0 <= node[0] + i < len(matrix) and 0 <= node[1] + j < len(matrix[0]) and matrix[node[0] + i][node[1] + j] in (0,1,2,999) : # treat monster like wall
               
                neighbors.append((node[0] + i, node[1] + j))
     
    return neighbors # tuple (x,y)

def get_neighbors_monster(matrix, node): # this function like above but not process monster
    neighbors = []
    for i, j in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Phải trái trên dưới
        if 0 <= node[0] + i < len(matrix) and 0 <= node[1] + j < len(matrix[0]) and matrix[node[0] + i][node[1] + j] != 1 : # check index of node is out of range and not a wall
                neighbors.append((node[0] + i, node[1] + j))
    return neighbors

# A* algorithm with existence of ghost in no mind.
def astar_monster(matrix, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    while open_set:
        current = heapq.heappop(open_set)[1] 
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for neighbor in get_neighbors_monster(matrix, current):
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score = temp_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    return None

def astar_multi_goal(matrix, start, goals):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {start: None}
    g_score = {start: 0}
    while open_set:
        current = heapq.heappop(open_set)[1]
        if current in goals:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for neighbor in get_neighbors(matrix, current):
            
            temp_g = g_score[current] + 1
            if neighbor not in g_score or temp_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g
                f_score = temp_g + min(heuristic(neighbor, goal) for goal in goals)
                heapq.heappush(open_set, (f_score, neighbor))
    return None

# Find nearest available food


def find_path_to_food(matrix, pacman_position):
    foods_position = []
    if is_more_food(matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 2:
                    foods_position.append((i,j))

        return astar_multi_goal(matrix, pacman_position, foods_position)
    else:
        return False
        

def is_more_food(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 2:
                return True
    return False

# Update Pacman's position based on the path found by A*
def update_pacman_position(matrix, pacman_position):
    if is_more_food(matrix):
        path_to_food = find_path_to_food(matrix, pacman_position )
        foods_position = []
        monster_positions = []
        
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if matrix[i][j] == 2 :
                    foods_position.append((i,j))
                if matrix[i][j] // 3 > 0 and matrix[i][j] not in (888,999,0):
                    monster_positions.append((i,j))
        
        if path_to_food:
            next_position = path_to_food[1]  # Lấy vị trí thứ hai trong danh sách đường đi
            if matrix[next_position[0]][next_position[1]] % 3 == 0 and matrix[next_position[0]][next_position[1]] not in (888,999,0):  # Kiểm tra nếu Pacman chạm vào quái vật
                # Kết thúc trò chơi ở đây
                print("Game Over")
                return (-1,-1)
            else:
                matrix[pacman_position[0]][pacman_position[1]] = 999  # Đánh dấu lại vị trí mà Pacman đã đi qua
                if (next_position[0], next_position[1]) in foods_position:
                    
                    foods_position = foods_position.remove((next_position[0], next_position[1]))
                    render.score_value+=20
                    
                matrix[next_position[0]][next_position[1]] = 888  # Di chuyển Pacman đến vị trí tiếp theo
                return next_position
        else:

            path_to_monster = astar_monster(matrix, pacman_position, foods_position[0]) # still the shortest way to food but pacman might collide with monster
            next_position = path_to_monster[1] if path_to_monster else pacman_position

            matrix[pacman_position[0]][pacman_position[1]] = 999  # Đánh dấu lại vị trí mà Pacman đã đi qua
            if (next_position[0], next_position[1]) in monster_positions:
                print("Game Over")
                return False
            matrix[next_position[0]][next_position[1]] = 888  # Di chuyển Pacman đến vị trí tiếp theo
            
            return next_position
    else:
        return (-1,-1)

def update_monster_position(matrix, monster_postion):

    food_position = None

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 888:
                food_position = (i, j)
                break
    
    path_to_monster = astar_monster(matrix, monster_postion, food_position)
    
    next_position = path_to_monster[1] if path_to_monster else monster_postion

    # Delete the current postion of ghost
    matrix[monster_postion[0]][monster_postion[1]] -= 3
    # Update the next postion
    matrix[next_position[0]][next_position[1]] += 3
    if (next_position[0], next_position[1]) == food_position:
        print("Game Over")
        return (-1,-1)
    return next_position


def update_monsters_postion (matrix):
    monsters_position = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] not in (888,999,0) and matrix[i][j] // 3 > 0:
                if matrix[i][j] > 999:
                    repeat = (matrix[i][j] - 999) // 3
                else:
                    repeat = matrix[i][j] // 3
                
                for k in range(repeat):
                    monsters_position.append((i,j))
 
    for monster_position in monsters_position:
        update_monster_position(matrix, monster_position)

def play(timer, screen):
    fps = 10
    run = True      
    matrix = extract.extractMatrix('map{}.txt'.format(4))
    player_location = extract.extractLocation('map{}.txt'.format(4))      
    counter = 0
    render.score_value = 100           
    player_x = player_location[0] 
    player_y = player_location[1]

    matrix[player_x][player_y] = 888

    while run:
        timer.tick(fps)
        if counter < 19:
            counter+=1
        else:
            counter = 0
        screen.fill('black')
        
        
        update_monsters_postion(matrix)
        (player_x,player_y) = update_pacman_position(matrix, (player_x, player_y))
        if (player_x,player_y) == (-1,-1):
            run = False
        render.score_value -= 1
         
        
        render.render(matrix)
        render.render_score(300,700, render.score_value)

        for eventElement in event.get():
            if eventElement.type == QUIT:
                run = False
        display.flip()