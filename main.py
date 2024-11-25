################################################################################
import random

ships = []
freezone = set()

def create_freezone():
    global freezone
    freezone = set()
    for i in range(7):
        for j in range(7):
            freezone.add((i, j))

def random_direction():
    direction = random.randint(0, 1)
    return direction

def del_from_freezone(coordinates):
    for coordinate in coordinates:
        freezone.discard(coordinate)
        x, y = coordinate[0], coordinate[1]
        freezone.discard((x + 1, y))
        freezone.discard((x - 1, y))
        freezone.discard((x, y + 1))
        freezone.discard((x, y - 1))
        freezone.discard((x + 1, y + 1))
        freezone.discard((x - 1, y - 1))
        freezone.discard((x + 1, y - 1))
        freezone.discard((x - 1, y + 1))

def big_ship():
    global freezone
    global ships
    if random_direction() == 1:
        first_cell = (random.randint(0, 6), random.randint(0, 4))
        second_cell = (first_cell[0], first_cell[1] + 1)
        third_cell = (first_cell[0], first_cell[1] + 2)
        ships.append([first_cell, second_cell, third_cell])
        del_from_freezone([first_cell, second_cell, third_cell])
    else:
        first_cell = (random.randint(0, 4), random.randint(0, 6))
        second_cell = (first_cell[0] + 1, first_cell[1])
        third_cell = (first_cell[0] + 2, first_cell[1])
        ships.append([first_cell, second_cell, third_cell])
        del_from_freezone([first_cell, second_cell, third_cell])

def medium_ship():
    global ships
    global freezone
    if random_direction() == 1:
        first_cell = random.choice(list(freezone))
        if 0 <= first_cell[0] <= 6 and 0 <= first_cell[1] <= 5:
            second_cell = (first_cell[0], first_cell[1] + 1)
            if second_cell in freezone:
                ships.append([first_cell, second_cell])
                del_from_freezone([first_cell, second_cell])
            else:
                medium_ship()
                return 0
        else:
            medium_ship()
            return 0

    else:
        first_cell = random.choice(list(freezone))
        if 0 <= first_cell[0] <= 5 and 0 <= first_cell[1] <= 6:
            second_cell = (first_cell[0] + 1, first_cell[1])
            if second_cell in freezone:
                ships.append([first_cell, second_cell])
                del_from_freezone([first_cell, second_cell])
            else:
                medium_ship()
                return 0
        else:
            medium_ship()
            return 0


def one_ship():
    global ships
    global freezone
    first_cell = random.choice(list(freezone))
    ships.append([first_cell])
    del_from_freezone([first_cell])


def last_one_ship():
    global ships
    global freezone
    if len(freezone) == 0:
        ships = []
        create_freezone()
        big_ship()
        medium_ship()
        medium_ship()
        one_ship()
        one_ship()
        one_ship()
        last_one_ship()
    else:
        first_cell = random.choice(list(freezone))
        ships.append([first_cell])
        del_from_freezone([first_cell])

def field_generation():
    global ships
    ships = []
    create_freezone()
    big_ship()
    medium_ship()
    medium_ship()
    one_ship()
    one_ship()
    one_ship()
    last_one_ship()
    ship_coordinate = ships
    return ship_coordinate
################################################################################

import os
ships = field_generation()

all_ship_coordinates = []
for ship in ships:
    for coordinate in ship:
        all_ship_coordinates.append(coordinate)
print(ships)

player_coordinates = []
sunk_counter = 0

name = input('Enter your name: ')
field = [['*' for i in range(7)] for j in range(7)]

def clear():
    os.system('cls' if os.name=='nt' else 'clear')
clear()

def print_field():
    global field
    for i in field:
        print(' '.join(i))

def ship_is_sunk(row, column):
    global ships
    global player_coordinates
    for ship in ships:
        if (row,column) in ship:
            found_ship = ship

    for coordinate in found_ship:
        if coordinate not in player_coordinates:
            return False
    return True

def marked_sunk(row, column):
    global field
    global ships
    global player_coordinate
    for ship in ships:
        if (row,column) in ship:
            found_ship = ship

    for coordinate in found_ship:
        row, column = coordinate
        field[row][column] = 'X'

def sea_battle():
    global sunk_counter
    global field
    global player_coordinates

    while sunk_counter != 7:
        clear()
        print_field()
        x, y = input().split(',')
        row, column = int(x),int(y)
        player_coordinates.append((row,column))
        if (row, column) in all_ship_coordinates:
            field[row][column] = 'H'
            if ship_is_sunk(row,column) == True:
                marked_sunk(row,column)
                sunk_counter+=1
        else:
            field[row][column] = 'M'

def write_data(name,shots):
    with open("leaderboard.txt", 'a') as file:
        file.write(str(name) + ';' + str(shots) + '\n')
        file.close()

def print_leaderboard():
    with open("leaderboard.txt") as file:
        player_list = []

        for line in file:
            data = line.rstrip()
            name, shots = data.split(';')
            player_list.append((int(shots), name))

        player_list = sorted(player_list)
        print('BEST PLAYERS:')
        for player in player_list:
            print(player[1], '-', player[0])
        file.close()

sea_battle()
clear()
print_field()
shots = len(player_coordinates)
print('The number of shots are', shots)

choice = input('Do you wanna restart the game? (Yes/No): ')
while choice == 'Yes':
    player_coordinates = []
    field = [['*' for i in range(7)] for j in range(7)]
    ships = field_generation()
    shots = 0
    sunk_counter = 0
    sea_battle()
    choice = input('Do you wanna restart the game? (Yes/No): ')
else:
    write_data(name, shots)
    print_leaderboard()
