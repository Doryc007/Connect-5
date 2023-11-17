# python 3.9.6 64-bit


def Find_Coordinates_Of_Arrays(PlayerCoordinate: list, ArrayType: str) -> list:
    # Array = [' ', ' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', 'X', ' ']
    # PlayerCoordinate = [4, 5]
    # ArrayType = Horizontal, Vertical, Diagonal

    # Goal: Determine all the coordinates of the array based on the "PlayerCoordinate" and "ArrayType"
    # Steps: Given the "PlayerCoordinate", it is possible to find the nearby coordinates based on the
    #       "ArrayType" pattern. The coordinates can be extrapolated and will be remsembled in a new array
    #       The array that will be returned would look somewhat like this:
    #       coordinateArray = [[2,0], [2,1], [2,2], [2,3], ...] 
    rowVal, colVal = PlayerCoordinate
    rowVal, colVal = int(rowVal), int(colVal)
    if ArrayType == "Horizontal":
        # Given the "ArrayType" of "Horizontal"
        # The coordinates could simply be found with the "row" value provided within the "PlayerCoordinate"
        coordinateArray = [[rowVal, colVal] for colVal in [i for i in range(0, 11)]]
    elif ArrayType == "Vertical":
        coordinateArray = [[rowVal, colVal] for rowVal in [i for i in range(0, 11)]]
    elif ArrayType == "PositiveDiagonal":
        rightUpCord = []
        leftDownCord = []

        # Right Up
        rightUpRange = min(abs(colVal - 10), 10 - rowVal)
        for _ in range(rightUpRange):
            # Moving in up-right direction
            rowVal -= 1
            colVal += 1
            if rowVal < 0:
                continue
            rightUpCord.append([rowVal, colVal])

        # Left Down
        leftDownRange = min(10 - rowVal, colVal)
        for _ in range(leftDownRange):
            rowVal += 1
            colVal -= 1
            if rowVal < 0:
                continue
            leftDownCord.append([rowVal, colVal])

        # Convert the two lists to sets
        rightUpSet = set(tuple(x) for x in rightUpCord)
        rightDownSet = set(tuple(x) for x in leftDownCord)

        # Combine the two sets and convert back to a list
        combined_set = rightDownSet.union(rightUpSet)
        coordinateArray = sorted([list(x) for x in combined_set], key=lambda x: x[0])
    elif ArrayType == "NegativeDiagonal":
        leftUpCord = []
        rightDownCord = []

        # Left Up
        leftUpRange = min(rowVal, colVal)
        for _ in range(leftUpRange):
            rowVal -= 1
            colVal -= 1
            if rowVal < 0:
                continue
            leftUpCord.append([rowVal, colVal])

        # Right Down
        rightDownRange = min(10 - rowVal, 10 - colVal)
        for _ in range(rightDownRange):
            rowVal += 1
            colVal += 1
            if rowVal < 0:
                continue
            rightDownCord.append([rowVal, colVal])

        # Convert the two lists to sets
        leftUpCord = set(tuple(x) for x in leftUpCord)
        rightDownCord = set(tuple(x) for x in rightDownCord)

        # Combine the two sets and convert back to a list
        combined_set = leftUpCord.union(rightDownCord)
        coordinateArray = sorted([list(x) for x in combined_set], key=lambda x: x[0])
    return coordinateArray

# ---------------------------------------------------------------------------------------
def Find_allArrays(Game_Board: list, playerCoordinate: list) -> list:
    arrayTypes = ["Horizontal", "Vertical", "PositiveDiagonal", "NegativeDiagonal"]
    # allArrays consists all the arrays that passes through "playerCoordinate"
    # Horizontal, Vertical, Positive/Negative Diagonal
    ArrayIDCoordinates = {} # ID: Coordinates -> Used to match up with the correct array
    for arrayScanID in range(len(arrayTypes)):
        current_array = arrayTypes[arrayScanID]
        ArrayIDCoordinates[arrayScanID] = Find_Coordinates_Of_Arrays(playerCoordinate, current_array)
    
    ArrayIDLines = {} # Similar layout structure as "allArrays"
    for arrayScanID in range(len(ArrayIDCoordinates)):
        # arrayScanID represent each line index present inside the previous dictionary: 4 in total
        ArrayIDLines[arrayScanID] = []
        for coordinates in ArrayIDCoordinates[arrayScanID]:
            # looping through all the coordinates under one type of line
            row = coordinates[0]
            col = coordinates[1] 
            current_character = Game_Board[row][col] # Add the in-board character, so could be 'X', 'O', ' '.
            ArrayIDLines[arrayScanID].append(current_character) 

    return [array for array in ArrayIDLines.values()], ArrayIDCoordinates

# ---------------------------------------------------------------------------------------
def Connection_Streak(allArrays: list, ArrayIDCoordinates: list) -> list:
    """ ###### Connection-Streak Verification ###### """
    # How many Player's pieces on a line does not matter, how many are connected matters more
    connectionStreakValueDict = {}
    connectionStreakCoordinateDict = {}

    for arrayCSVID in range(len(allArrays)): # CSV: Connection-Streak Verification

        currentArray = allArrays[arrayCSVID]
        currentArrayCoordinates = ArrayIDCoordinates[arrayCSVID]
        maximumLength = 0 
        startingPoint = None 
        endingPoint = None
        for charScanID in range(len(currentArray)):
            if currentArray[charScanID] == 'O': # If it's Player's piece
                phaseLength = 0
                for playerScanID in range(charScanID, len(currentArray)):
                    if currentArray[playerScanID] == 'O':
                        phaseLength += 1
                    elif currentArray[playerScanID] == 'X' or currentArray[playerScanID] == ' ':
                        if phaseLength > maximumLength: 
                            maximumLength = phaseLength
                            startingPoint = currentArrayCoordinates[charScanID]
                            endingPoint = currentArrayCoordinates[playerScanID-1]
                        break
        
        connectionStreakValueDict[arrayCSVID] = maximumLength
        connectionStreakCoordinateDict[arrayCSVID] = [startingPoint, endingPoint]
    return connectionStreakValueDict, connectionStreakCoordinateDict

# ---------------------------------------------------------------------------------------
def Optimal_neighbour(Game_Board: list, playerCoordinate: list) -> list:
    """ ###### Find Overlap Coordinate(s) in All Linear Line ###### """
    """
    It is impossible to have overlapping coordinates because there will not be other than the current piece
    So by dilating the bot's view by 1, all 8 surronding spot will be searched for it's linear coordinates
    Then check for overlapping coordinates with it's original 4 linear lines
    """
    center_x = playerCoordinate[0]
    center_y = playerCoordinate[1]
    radius = 1

    player_nearby_coordinates2 = []
    for x in range(center_x - radius, center_x + radius+1):
        for y in range(center_y - radius, center_y + radius+1):
            player_nearby_coordinates2.append([x,y])

    player_nearby_coordinates = player_nearby_coordinates2[::]
    # Check for points that are Player's pieces
    for coordinateID in range(len(player_nearby_coordinates2)):
        coordinate = player_nearby_coordinates2[coordinateID]
        row = coordinate[0]
        col = coordinate[1]
        if Game_Board[row][col] == 'X':
            player_nearby_coordinates.remove(coordinate)
    
    # Loop through all 9 coordinates(Including current player coordinate)
    # Input all the data into the 2 dictionaries above
    nearby_allArrays = {} # (0: [[' ', ' ', ' ', 'X', 'O', 'O', ' ', ' ', ' ', ' ', ' '], [], ...], 1: ...)
    nearby_allArraysCoordinates = {} # {nearby_index: {0: [[3, 7], [3, 7]], 1: [[3, 7], [4, 7]], 2: [[3, 7], [5, 5]], 3: [[3, 7], [3, 7]]}}
    nearby_connection_streak = {}
    nearby_connection_streak_coordinate = {}

    for coordinateID in range(len(player_nearby_coordinates)):
        coordinate = player_nearby_coordinates[coordinateID]
        allArrays, ArrayIDCoordinates = Find_allArrays(Game_Board, coordinate)
        nearby_allArrays[coordinateID] = allArrays
        nearby_allArraysCoordinates[coordinateID] = ArrayIDCoordinates

        # Loop through all 9 coordinate again to find their connection_streak by passing them through "Connection_Streak"
        connectionStreakValueDict, connectionStreakCoordinateDict = Connection_Streak(allArrays, ArrayIDCoordinates)
        nearby_connection_streak[coordinateID] = connectionStreakValueDict
        nearby_connection_streak_coordinate[coordinateID] = connectionStreakCoordinateDict

    return [player_nearby_coordinates, nearby_allArrays, nearby_allArraysCoordinates, nearby_connection_streak, nearby_connection_streak_coordinate]

