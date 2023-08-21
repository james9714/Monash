game_record = {"size": 0, "mode": 0, "board": []}
print("""##########################
#  Create a board      #
#  Select a game mode  #
##########################""")
while True:
    if game_record["size"] == 0:
        print("Please select a board size(9,13,15)")
        size = int(input('Size: '))
        board = ['']
        game_record["size"] = size
        game_record["board"] = board
    elif game_record["mode"] == 0:
        print("Please select the game mode: \
            \n press 1 for human vs human\
            \n press 2 for human vs Cumputer")
        mode = int(input('Mode: '))
        game_record["mode"] = mode
    else:
        break