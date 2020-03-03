def welcome():
    print("      Welcome to Tic-Tac_Toe    ")
    print("      -----------------------    ")
    print("Try to get three X's or 0’s in a row!")
    while(1):
        num_players=input("     Select 1 or 2 player game:")
        num_players=int(num_players)
        if num_players==1:
            print("     1 Player game selected...")
            break
        elif num_players==2:
            print("     2 Player game selected...")
            break
        else:
            print("Choice must be 1 or 2 player...")
        print("       ---------------------")
    print("Press ENTER to start the game:")

welcome()