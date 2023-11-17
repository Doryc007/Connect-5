# python 3.9.6 64-bit

from boardAnalysis import *

def AvailablePiecePlacement(playerCoordinateID: int, nearby_allArrays: list, nearby_allArraysCoordinates: list, nearby_connection_streak: list, nearby_connection_streak_coordinate: list) -> list:

    availableArrays = {}
    availableArraysID = {}
    availableArraysIssueID = {}
    # Check the arrays that the Player can actually connect 5 pieces
    # Meaning the connection-streak and the enarby empty slots adds up to 5

    allArrays = nearby_allArrays[playerCoordinateID]
    ArrayCoordinates = {}
    for arrayDictID in range(len(nearby_allArraysCoordinates[playerCoordinateID])):
        ArrayCoordinates[str(allArrays[arrayDictID])] = nearby_allArraysCoordinates[playerCoordinateID][arrayDictID]
    connectionStreakValueDict = nearby_connection_streak[playerCoordinateID]
    connectionStreakCoordinateDict = nearby_connection_streak_coordinate[playerCoordinateID]

    # arraySSID: Array Surronding Scan ID
    for arraySSID in range(len(allArrays)):
        # Check both side of the array with "startingPoint" and "endingPoint"
        currentArray = allArrays[arraySSID]
        startingPoint, endingPoint = connectionStreakCoordinateDict[arraySSID]
        startingPointInd = ArrayCoordinates[str(currentArray)].index(startingPoint)
        endingPointInd = ArrayCoordinates[str(currentArray)].index(endingPoint)

        playerRemainingPieceToWin = 5 - connectionStreakValueDict[arraySSID] # Determine remaining pieces for player to win
        
        print("currentArray:",currentArray)
        print("startingPoint:",startingPoint, "startingPointInd:", startingPointInd)
        print("endingPoint:",endingPoint, "endingPointInd:",endingPointInd)
        print("playerRemainingPieceToWin:",playerRemainingPieceToWin)

        # Check in front of the startingPoint of Player's Connection-Streak
        startScanIssueID = [startScanID for startScanID in range(startingPointInd, -1, -1) if currentArray[startScanID] == 'X']
        endScanIssueID = [endScanID for endScanID in range(endingPointInd, len(currentArray), 1) if currentArray[endScanID] == 'X']

        # startScanIssueID, endScanIssueID cannot be empty, must be represented with a certain value
        startScanIssueID = [0] if startScanIssueID == [] else startScanIssueID 
        endScanIssueID = [len(currentArray) - 1] if endScanIssueID == [] else endScanIssueID 

        print("startScanIssueID:",startScanIssueID, "endScanIssueID:",endScanIssueID)

        """###### Objective: Check if the array contains enough empty space to build up to 5 or more ######"""
        if len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1:
            # There are Bot pieces both in front and behind the Player's connection-streak
            print("len(startScanIssueID) >= 1 and len(endScanIssueID) >= 1")

            if endScanIssueID[0] - startScanIssueID[0] > 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = (endScanIssueID[0] - startScanIssueID[0]) - 1
            else:
                print("currentArray1:",currentArray, " is not available")

        elif len(startScanIssueID) == 0 and len(endScanIssueID) > 0: 
            # The Bot pieces are on the right side of the Player's connection-streak
            # The Player could only expand on it's left
            print("len(startScanIssueID) == 0")

            if (endScanIssueID[0] - 1) >= 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = (endScanIssueID[0] - 1)
            else:
                print("currentArray2:",currentArray, " is not available")

        elif len(startScanIssueID) > 0 and len(endScanIssueID) == 0:
            # The Bot pieces are on the left side of the Player's connection-streak
            # The Player could only expand on it's right
            print("len(endScanIssueID) == 0")

            if 10 - startScanIssueID[0] > 5:
                availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
                availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
                availableArrays[str(currentArray)] = 10 - startScanIssueID[0]
            else:
                print("currentArray3:",currentArray, " is not available")
        
        elif len(startScanIssueID) == 0 and len(endScanIssueID) == 0:
            print("# There are completely no Bot pieces at all on the current choosen array")
            availableArraysIssueID[arraySSID] = [startScanIssueID, endScanIssueID]
            availableArraysID[arraySSID] = [startingPointInd-1, endingPointInd+1]
            availableArrays[str(currentArray)] = len(currentArray)

        print("-"*50)

    print("availableArrays:",availableArrays)
    print("availableArraysID:",availableArraysID) # Connection-Streak-Length = (endingIndex - startingIndex) / 2
    print("availableArraysIssueID:",availableArraysIssueID)

def FindingIntersections(adjacentPointArrays: list, playerPointArrays: list) -> list:

    # This function should find the intersection point between two arrays 
    pass

def RetrieveEligibleLists(Game_Board: list, playerCoordinate: list):
    player_nearby_coordinates, nearby_allArrays, nearby_allArraysCoordinates, nearby_connection_streak, nearby_connection_streak_coordinate\
          = Optimal_neighbour(Game_Board, playerCoordinate)

    """ ---------- Prioritize Player Max Connection-Streak Array ---------- """

    # Prioritize sorting based on connection-streak length
    playerCoordinateID = player_nearby_coordinates.index(playerCoordinate)

    # Section for Player Data 
    maxVal = max(nearby_connection_streak[playerCoordinateID].values())

    """ This is focused on the arrays associating with the player coordinate """
    # primarySelection: Array ID that leads to the array with highest connection-streak
    #                       maximum is four element and minimum is one
    #                       minimum is always one because the bot is programmed to place a piece
    #                       randomly on the adjacent points of playerCoordinate
    primarySelectionID = [key for key, val in nearby_connection_streak[playerCoordinateID].items() if val == maxVal] 
    primaryArrays = [nearby_allArraysCoordinates[playerCoordinateID][i] for i in primarySelectionID] 
    primaryArraysStreakCoordinates = [nearby_connection_streak_coordinate[playerCoordinateID][i] for i in primarySelectionID] # This array consists the starting&ending point of the streak
    playerConnectionPoints = [nearby_connection_streak_coordinate[playerCoordinateID][key] for key in primarySelectionID]

    for coordinateID in range(len(player_nearby_coordinates)):
        if coordinateID == playerCoordinateID:
            pass 
        else:
            current_coordinate = player_nearby_coordinates[coordinateID]
            current_arrays = nearby_allArrays[coordinateID]
            current_arrays_coordinates = nearby_allArraysCoordinates[coordinateID] 
            current_connection_streak = nearby_connection_streak[coordinateID] 

            print(coordinateID)
            print(current_coordinate)
            print(current_arrays)
            print(current_arrays_coordinates)
            print(current_connection_streak)
            print("-" * 50)
    

    # AvailablePiecePlacement(playerCoordinateID, nearby_allArrays, nearby_allArraysCoordinates, nearby_connection_streak, nearby_connection_streak_coordinate)

Game_Board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' '], 
                  [' ', ' ', ' ', ' ', 'X', ' ', 'X', 'O', ' ', ' ', 'X'], # [3,7]
                  [' ', ' ', ' ', ' ', 'X', 'O', 'O', 'O', ' ', ' ', ' '], 
                  [' ', ' ', ' ', 'X', 'O', 'O', 'O', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
                  [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
playerCoordinate=[3,7]
     

RetrieveEligibleLists(Game_Board, playerCoordinate)
