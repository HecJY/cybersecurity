def game(num):
    str = list()
    for i in range(0,9):
        str.append(" ")


    game = list()
    row = list()
    # init the game period
    for i in range(0,3):
        for j in range(0,3):
            row.append(" ")
        game.append(row)


    player = {"X", "O"}
    which = 0
    for i in range(0, 9):
        which = which % 2
        str = "Player " + str(which + 1) + " select a grid location: "
        pos = eval(str)
        row = pos[0] - "a"
        col = int(pos[1])
        game[row][col] = player[which]
        print_game(game)


def print_game(game):
    row = ["A", "B", "C"]
    print("    1   2   3 \n")
    print("   ----------- \n")
    for i in range(0,3):
        for j in range(0,3):
            print(row[i])
            print(" |")
            print(" ")
            print(game[i][j])
            print(" ")
            print("|")
        print("\n")

    print("   ----------- \n")

def check(grid):
    #check the row first
    for i in range(0,3):
        if(grid[i][0] == grid[i][1] and grid[i][1] == grid[i][2]):
            return grid[i][0]


    #check col
    for i in range(0,3):
        if (grid[0][i] == grid[1][i] and grid[1][i] == grid[2][i]):
            return grid[0][i]

    #check diag
    if(grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]):
        return grid[0][0]

    if(grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]):
        return grid[0][2]

    return False

def print_game(game):
    col_num = {1, 2, 3}
    row_letter = {"A", "B", "C"}
    print("     1   2   3 \n")
    print("    ----------- ")
    for i in range(0, 3):
        for j in range(0, 3):


