#BlackJack by Dav Vrat Chadha


import random

#Function to generate a random card from the decks
def randomCardGen():
    #list of card suits
    suitList = ["\u2663", "\u2666", "\u2665", "\u2660"]
    #list of card in a suit.
    #Notice that a space has been added in almost all items in this list to make the card
    #numbers 2-charactered for easier printing.
    numList = ["A ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "10", "J ", "Q ", "K "] 
    #list of card values, corresponding to cards in numList
    cardValue = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    #randomly generating card
    suit = random.choice(suitList)
    index = random.randint(0,12)
    number = numList[index]
    value = cardValue[index]
    #adding values into the card for AsciiArt
    card = (""" _________ 
|         |
| %s      |
|         |
|    %s    |
|         |
|       %s|
|_________|""" % (number, suit, number))
    return card, value

#Function to distribute cards to begin the game
def initialCardDistributer():
    #Generating four cards using randomCardGen()
    (card1,value1) = randomCardGen()
    (card2,value2) = randomCardGen()
    (card3,value3) = randomCardGen()
    (card4,value4) = randomCardGen()
    #In following lists, format is: [Number of Aces, Net value of cards without considering Aces]
    playerHand = [0, 0] #List of player's cards
    dealerHand = [0, 0] #List of dealer's cards
    hiddenCard = [0, 0] #List for dealer's hidden card
    #If-Else statements for getting net value of cards without considering value of aces
    if value1 == 11:
        playerHand[0] += 1
    else:
        playerHand[1] += value1
    if value2 == 11:
        dealerHand[0] += 1
    else:
        dealerHand[1] += value2
    if value3 == 11:
        playerHand[0] += 1
    else:
        playerHand[1] += value3
    if value4 == 11:
        hiddenCard[0] += 1
    else:
        hiddenCard[1] += value4
    #AsciiArt for dealer's hidden card
    faceDownCard = """ _________ 
|         |
| \u2605\ufeff    \u2605 |
|   DVC\u2122  |
|    \u2660    |
|  GAMES  |
| \u2605\ufeff    \u2605 |
|_________|"""
    #appending cards in the lists
    playerHand.append(card1)
    dealerHand.append(card2)
    playerHand.append(card3)
    dealerHand.append(faceDownCard)
    hiddenCard.append(card4)
    return playerHand,  dealerHand, hiddenCard

#Function to calculate actual value of cards in hand
def calcHandValue(dealerHand, playerHand):
    while playerHand[0] > 0: #number of Aces in Hand
        if playerHand[1] == 10:
            playerHand[1] += 11 #new value of hand
            playerHand[0] -= 1 #new number of Aces in Hand
            
        if playerHand[1] >= 11: #value of hand
            playerHand[1] += 1 #new value of hand
            playerHand[0] -= 1 #new number of Aces in Hand
        else:
            sum = playerHand[1]
            playerHand[1] = "?"
            printCards(dealerHand, playerHand)
            ask = eval(input("""You have an Ace and its value needs to be decided.
Would you like it to have value = 1 or 11?
Please enter the value you want:"""))
            if ask == 1:
                playerHand[1] = sum + 1
                playerHand[0] -= 1
            elif ask == 11:
                playerHand[1] = sum + 11
                playerHand[0] -= 1
            else: print("Invalid Input")
        
    while dealerHand[0] > 0: #number of Aces in Hand
        if dealerHand[1] >= 11: #value of hand
            dealerHand[1] += 1 #new value of hand
            dealerHand[0] -= 1 #new number of Aces in Hand
        else:
            dealerHand[1] += 11
            dealerHand[0] -= 1
    return dealerHand, playerHand
    
#Function for printing cards onto the shell
def printCards(dealerHand, playerHand):
    a = dealerHand.copy()
    b = playerHand.copy()
    valA = a[1]
    valB = b[1]
    print("Dealer's Hand")
    while a[2]:
        for i in range(2,len(a)):
            card = a[i]
            print(card[:11] + " ", sep = " ", end = "")
            a[i] = card[12:]
        print("")
    if valA == 11 and a[0] == 1:
        print("Value = 1/11\n\n") 
    else:
        print("Value = " + str(valA) + "\n\n")
        
    print("Player1's Hand")
    while b[2]:
        for i in range(2,len(b)):
            card = b[i]
            print(card[:11] + " ", sep = " ", end = "")
            b[i] = card[12:]
        print("")
    if valB == 11 and b[0] == 1:
        print("Value = 1/11\n\n") 
    else:
        print("Value = " + str(valB) + "\n\n")
    return

#Function to calculate score and check for victory
def score(playerHand, dealerHand, hiddenCard):
    print("\n")

    if (dealerHand[1] == 10 or dealerHand[1] == 11) and dealerHand[3] != hiddenCard: #Checking for Dealer's BlackJack
        total = dealerHand[1] + hiddenCard[1]
        if total == 21:
            #opening face down card
            print("Dealer opens the Face Down Card.")
            dealerHand[3] = hiddenCard[2]
            dealerHand[0] += hiddenCard[0]
            if hiddenCard[1] != 11:
                dealerHand[1] += hiddenCard[1]
            dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
            printCards(dealerHand, playerHand)
            if dealerHand[1] == 21 and playerHand == 21: #Tie with both getting 21
                print("Its a tie as both, the player and the dealer, have got 21.")
                victoryStatus = "Tie"
            else:
                dealerHand, playerHand, victoryStatus = score(playerHand, dealerHand, hiddenCard)
            
    if playerHand[1] == 21 and dealerHand[3] != hiddenCard: #Checking for BlackJack
        #opening face down card
        print("Dealer opens the Face Down Card.")
        dealerHand[3] = hiddenCard[2]
        dealerHand[0] += hiddenCard[0]
        if hiddenCard[1] != 11:
            dealerHand[1] += hiddenCard[1]
        dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
        printCards(dealerHand, playerHand)
        
        if dealerHand[1] == 21 and playerHand == 21: #Tie with both getting 21
            print("Its a tie as both, the player and the dealer, have got 21.")
            victoryStatus = "Tie"
        else: #Only player gets 21
            print("Congrats!! You have got 21 and won the match.")
            victoryStatus = "Player1"
    
    
    
    elif dealerHand[1] == 21: #Dealer gets 21
        print("Dealer got 21 and has won the match.")
        victoryStatus = "Dealer"
    elif playerHand[1] > 21 and dealerHand[3] != hiddenCard[2]: #Player busted
        #opening face down card
        print("Dealer opens the Face Down Card.")
        dealerHand[3] = hiddenCard[2]
        dealerHand[0] += hiddenCard[0]
        if hiddenCard[1] != 11:
            dealerHand[1] += hiddenCard[1]
        dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
        printCards(dealerHand, playerHand)
        print("You have been Busted and Dealer has won the match.")
        victoryStatus = "Dealer"     
    elif dealerHand[1] > 21 and playerHand[1] < 22: #Dealer busted
        print("Congrats!! Dealer has been Busted and you have won the match.")
        victoryStatus = "Player1"
    elif dealerHand[3] == hiddenCard[2]: #If dealer's hidden card has been opened after Player1's move STAY
        if playerHand[1] == dealerHand[1]: #Normal tie without BlackJack
            print("Its a tie as both, the player and the dealer, have got " + str(playerHand[1]) +".")
            victoryStatus = "Tie"
        elif playerHand[1] > dealerHand[1]: #Player's card have higher value than dealer's cards
            print("Congrats!! You have won the match.")
            victoryStatus = "Player1"
        else: #Dealer's card have higher value than player's cards
            print("Dealer has won the match.")
            victoryStatus = "Dealer" 
    else: #To continue the match
        victoryStatus = "NA"
    return dealerHand, playerHand, victoryStatus
            
#Function for doing various processes that have to happen simultaneously     
def processes(dealerHand, playerHand, hiddenCard):
    moneyChange = 100
    dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
    printCards(dealerHand, playerHand)
    dealerHand, playerHand, victoryStatus = score(playerHand, dealerHand, hiddenCard)
    if victoryStatus == "Tie":
        moneyChange = 1 #Get all money back
    elif victoryStatus == "Player1":
        moneyChange = 2 #Get double money back
    elif victoryStatus == "Dealer":
        moneyChange = 0 #Get no money back
    elif victoryStatus == "NA":
        moneyChange = 100 #Secret code to continue the game
    return dealerHand, playerHand, moneyChange

#Function for main game
def blackJack():
    playerHand, dealerHand, hiddenCard = initialCardDistributer()
    dealerHand, playerHand, moneyChange = processes(dealerHand, playerHand, hiddenCard)
    if moneyChange == 100: #To continue the game with Player1's turn
        #Asking user for their move
        flagJr = eval(input("""\nWould you like to Hit or Stay?
Choose from the following options(index):
(1) Hit
(2) Stay\n"""))
        if flagJr == 2:
            move = "Stay"
        else:
            move = "Hit"
    while moneyChange == 100:
        #if player's move is to HIT
        while move == "Hit":
            cardPicked, value = randomCardGen()
            playerHand.append(cardPicked)
            if value == 11:
                playerHand[0] += 1
            else:
                playerHand[1] += value
            dealerHand, playerHand, moneyChange = processes(dealerHand, playerHand, hiddenCard)
            if moneyChange != 100:
                break
            if playerHand[1] < 22: #Asking user for their next move
                flagJr = eval(input("""\nWould you like to Hit or Stay?
Choose from the following options(index):
(1) Hit
(2) Stay\n"""))
                if flagJr == 2:
                    move = "Stay"
            else: move = "Stay"
        if move == "Stay": #if player's move is to STAY
            #opening face down card
            print("Dealer opens the Face Down Card.")
            dealerHand[3] = hiddenCard[2]
            dealerHand[0] += hiddenCard[0]
            if hiddenCard[1] != 11:
                dealerHand[1] += hiddenCard[1]
            dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
            if dealerHand[1] < 17:
                printCards(dealerHand, playerHand)
                
            #Allowing dealer's card to be opened till their value is < 17
            while dealerHand[1] < 17:
                print("Dealer picks another card from the deck.")
                cardPicked, value = randomCardGen()
                dealerHand.append(cardPicked)
                if value == 11:
                    dealerHand[0] += 1
                else:
                    dealerHand[1] += value
                dealerHand, playerHand = calcHandValue(dealerHand, playerHand)
                if dealerHand[1] < 17:
                    printCards(dealerHand, playerHand)
            dealerHand, playerHand, moneyChange = processes(dealerHand, playerHand, hiddenCard)
    return moneyChange

#Function to play game
def game():
    print("Welcome to BlackJack, an interesting game by DVC Games Enterprise.")
    flag = 1 #Used to play the game
    cash = 500 #$500 to begin with as bankroll
    round = 1 #Match number
    while flag == 1:
        #Asking for user input
        print("Current Cash Balance = $" + str(cash))
        print("Match " + str(round))
        bet = eval(input("How much money would you like to bet in this match?"))
        if bet > cash or bet < 1:
            print("Invalid Input")
            return
        moneyChange = blackJack()
        cash = cash + bet*(moneyChange - 1) #Calculating new cash balance/bankroll
        print("\nNew Cash Balance = $" + str(cash))
        if cash == 0: #if user loses all money coz he is a bad player
            #Asking for user input
            wish = eval(input("""You have lost all your money.
Would you like to reset BankRoll to $500?
Choose from the following options(index):
(1) Yes
(2) No\n"""))
            if wish == 1: #Reseting bankroll to play again
                print("***************************************************************************")
                game()
            else:
                print("\nThank you for playing a BlackJack, a project of DVC Game Enterprise.")
                print("***************************************************************************")
                return
        #Asking for user input
        flag = eval(input("""Would you like to play another match?
Choose from the following options(index):
(1) Yes
(2) Cash Out
(3) Reset BankRoll\n"""))
        if flag == 2: #ending game by calculating profit/loss
            if cash >= 500:
                print("You have cashed out with profit of $" + str((cash - 500)))
            else:
                print("You have cashed out with loss of $" + str((500 - cash)))
            print("\nThank you for playing a BlackJack, a project of DVC Game Enterprise.")
            print("***************************************************************************")
            return
        elif flag == 3: #Reseting bankroll to play again
            print("***************************************************************************")
            game()
        else:
            round += 1
            print("***************************************************************************")
    return
#This is the real place where the game actually starts(or sarcastically ends because of end of code)
game()
