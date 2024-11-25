import os

ships = [ [(0,1)], [(0,4)], [(3,0)], [(6,5)], [(2,5), (3,5)], [(6,0), (6,1)], [(2,3),(3,3),(4,3)]  ]

all_ship_coordinates = []
for ship in ships:
    for coordinate in ship:
        all_ship_coordinates.append(coordinate)
print(all_ship_coordinates)

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
