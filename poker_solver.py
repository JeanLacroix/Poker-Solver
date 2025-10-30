#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tkinter as tk
import random
from collections import Counter


# In[45]:


def ChooseHeroHand(): 
    root = tk.Tk()
    root.title("Hand Vs Range Equity Calculator")

    # Define card ranks and suits
    hands = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    Suits = ["s", "c", "h", "d"]
    HeroCards = []

    # Initialize the selection grid
    SelectionGrid = [[0 for _ in hands] for _ in Suits]

    # Define a function to toggle selection
    def toggleHero(row, col, button):
        # Toggle the state
        card_selected = SelectionGrid[row][col] == 1
        hand = f"{hands[col]}{Suits[row]}"  # Construct the full hand string

        if card_selected:  # Deselect the card
            SelectionGrid[row][col] = 0
            button.config(bg="gray", fg="black")
            HeroCards.remove(hand)
        elif len(HeroCards) < 2:  # Select the card if below the max limit
            SelectionGrid[row][col] = 1
            button.config(bg="green", fg="white")
            HeroCards.append(hand)


        # If the limit is reached, disable all unselected buttons
        if len(HeroCards) == 2:
            for i in range(len(Suits)):
                for j in range(len(hands)):
                    if SelectionGrid[i][j] == 0:  # Disable unselected buttons
                        buttons[i][j].config(bg="red", state="disabled")
        else:  # Re-enable buttons when limit is not reached
            for i in range(len(Suits)):
                for j in range(len(hands)):
                    if SelectionGrid[i][j] == 0:  # Enable only unselected buttons
                        buttons[i][j].config(bg="gray", state="normal")

    # Create the table of buttons (rows are suits, columns are hands)
    buttons = [[None for _ in hands] for _ in Suits]
    for i in range(len(Suits)):  # Loop through suits
        for j in range(len(hands)):  # Loop through card ranks
            btn = tk.Button(
                root,
                text=f"{hands[j]}{Suits[i]}",
                width=5,
                height=2,
                bg="gray",  # Default color
                fg="black",  # Default text color
            )
            btn.config(command=lambda r=i, c=j, b=btn: toggleHero(r, c, b))
            btn.grid(row=i, column=j, padx=1, pady=1)  # Place button in grid
            buttons[i][j] = btn

    # Add a "Done" button to finalize the selection
    def finalize():
        root.destroy()  # Close the Tkinter window

    done_button = tk.Button(root, text="Done", command=finalize, bg="blue", fg="white")
    done_button.grid(row=len(Suits), columnspan=len(hands), pady=10)

    # Run the Tkinter event loop
    root.mainloop()

    return HeroCards



# In[6]:


def SelectVillainRange():
    # Define the poker hand categories
    hands = [
        ["AA", "AKs", "AQs", "AJs", "ATs", "A9s", "A8s", "A7s", "A6s", "A5s", "A4s", "A3s", "A2s"],
        ["AKo", "KK", "KQs", "KJs", "KTs", "K9s", "K8s", "K7s", "K6s", "K5s", "K4s", "K3s", "K2s"],
        ["AQo", "KQo", "QQ", "QJs", "QTs", "Q9s", "Q8s", "Q7s", "Q6s", "Q5s", "Q4s", "Q3s", "Q2s"],
        ["AJo", "KJo", "QJo", "JJ", "JTs", "J9s", "J8s", "J7s", "J6s", "J5s", "J4s", "J3s", "J2s"],
        ["ATo", "KTo", "QTo", "JTo", "TT", "T9s", "T8s", "T7s", "T6s", "T5s", "T4s", "T3s", "T2s"],
        ["A9o", "K9o", "Q9o", "J9o", "T9o", "99", "98s", "97s", "96s", "95s", "94s", "93s", "92s"],
        ["A8o", "K8o", "Q8o", "J8o", "T8o", "98o", "88", "87s", "86s", "85s", "84s", "83s", "82s"],
        ["A7o", "K7o", "Q7o", "J7o", "T7o", "97o", "87o", "77", "76s", "75s", "74s", "73s", "72s"],
        ["A6o", "K6o", "Q6o", "J6o", "T6o", "96o", "86o", "76o", "66", "65s", "64s", "63s", "62s"],
        ["A5o", "K5o", "Q5o", "J5o", "T5o", "95o", "85o", "75o", "65o", "55", "54s", "53s", "52s"],
        ["A4o", "K4o", "Q4o", "J4o", "T4o", "94o", "84o", "74o", "64o", "54o", "44", "43s", "42s"],
        ["A3o", "K3o", "Q3o", "J3o", "T3o", "93o", "83o", "73o", "63o", "53o", "43o", "33", "32s"],
        ["A2o", "K2o", "Q2o", "J2o", "T2o", "92o", "82o", "72o", "62o", "52o", "42o", "32o", "22"],
    ]

    # Create the Tkinter window
    root = tk.Tk()
    root.title("Select Villain's Range")

    # Create a grid to track selected hands
    selection_grid = [[0 for _ in range(13)] for _ in range(13)]

    # List to store selected hands
    VillainRange = []

    # Define a function to toggle selection
    def toggleVillain(row, col, button):
        # Toggle the state
        selection_grid[row][col] = 1 - selection_grid[row][col]
        hand = hands[row][col]

        # Update the button color and the VillainRange list
        if selection_grid[row][col] == 1:
            button.config(bg="green", fg="white")
            VillainRange.append(hand)  # Add to VillainRange
        else:
            button.config(bg="gray", fg="black")
            VillainRange.remove(hand)  # Remove from VillainRange

    # Create the table of buttons
    for i in range(13):
        for j in range(13):
            hand = hands[i][j]
            # Normal button for other hands
            btn = tk.Button(
                root,
                text=hand,
                width=5,
                height=2,
                bg="gray",  # Default color                    fg="black",  # Default text color
                )
            btn.config(command=lambda row=i, col=j, b=btn: toggleVillain(row, col, b))
            btn.grid(row=i, column=j, padx=1, pady=1)

    # Variable to track when the user is done
    is_done = tk.BooleanVar(value=False)

    # Define a "Done" button to finalize the selection
    def finalize():
        is_done.set(True)  # Mark the selection process as complete
        root.destroy()  # Close the Tkinter window

    done_button = tk.Button(root, text="Done", command=finalize, bg="blue", fg="white")
    done_button.grid(row=14, columnspan=13, pady=10)

    # Wait for the user to click "Done"
    root.wait_variable(is_done)

    return VillainRange  # Return the selected hands



# In[8]:


def RandomVillain (RemovedCard) :
    combo = []
    PossibleCards = [f"{num}{suit}" for suit in "schd" for num in range(2, 15)]
    PossibleCards.remove (RemovedCard[0])
    PossibleCards.remove (RemovedCard[1])
    for i in range (2) : 
        RandomCard2=random.choice(PossibleCards)
        combo.append(RandomCard2)
        PossibleCards.remove (RandomCard2)
    return combo



# In[10]:


def ChosenRunout(): 
    root = tk.Tk()
    root.title("Runout")

    # Define card ranks and suits
    hands = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    Suits = ["s", "c", "h", "d"]
    Flop = []
    Turn = ""
    River = ""
    FullRunout = []

    # Display labels for feedback
    Question = tk.Label(root, text="Choose between 3 and 5 cards please", font=("Helvetica bold", 16))
    FlopReturn = tk.Label(root, text="Selected Flop: None", font=("Helvetica", 12))
    TurnReturn = tk.Label(root, text="Selected Turn: None", font=("Helvetica", 12))
    RiverReturn = tk.Label(root, text="Selected River: None", font=("Helvetica", 12))
    Question.grid(row=0, column=0, columnspan=13, pady=10)
    FlopReturn.grid(row=5, column=0, columnspan=13, pady=5)
    TurnReturn.grid(row=6, column=0, columnspan=13, pady=5)
    RiverReturn.grid(row=7, column=0, columnspan=13, pady=5)

    # Define toggle logic for Flop, Turn, and River
    def toggleRunout(row, col, button):
        nonlocal Turn, River  # Allow modifying Turn and River within the function
        hand = f"{hands[col]}{Suits[row]}"  # Construct the full hand string

        # Toggle Flop
        if len(Flop) < 3 or hand in Flop:
            if hand in Flop:
                Flop.remove(hand)
                button.config(bg="gray", fg="black")
            else:
                Flop.append(hand)
                button.config(bg="green", fg="white")
            FlopReturn["text"] = f"Selected Flop: {Flop if Flop else 'None'}"

        # Toggle Turn
        elif len(Flop) == 3 and (not Turn or hand == Turn):
            if hand == Turn:
                Turn = ""
                button.config(bg="gray", fg="black")
            else:
                Turn = hand
                button.config(bg="green", fg="white")
            TurnReturn["text"] = f"Selected Turn: {Turn if Turn else 'None'}"

        # Toggle River
        elif len(Flop) == 3 and Turn and (not River or hand == River):
            if hand == River:
                River = "" 
                button.config(bg="gray", fg="black")
            else:
                River = hand
                button.config(bg="green", fg="white")
            RiverReturn["text"] = f"Selected River: {River if River else 'None'}"

        # Update button states based on selections
        update_button_states()

    # Disable/Enable buttons dynamically based on selections
    def update_button_states():
        for i in range(len(Suits)):
            for j in range(len(hands)):
                hand_to_check = f"{hands[j]}{Suits[i]}"
                if hand_to_check not in Flop + ([Turn] if Turn else []) + ([River] if River else []):
                    if len(Flop) == 3 and Turn and River:  # Full runout selected
                        buttons[i][j].config(bg="red", state="disabled")
                    else:
                        buttons[i][j].config(bg="gray", state="normal")
                else:
                    buttons[i][j].config(state="normal")  # Selected cards remain clickable

    # Create the table of buttons (rows are suits, columns are hands)
    buttons = [[None for _ in hands] for _ in Suits]
    for i in range(len(Suits)):  # Loop through suits
        for j in range(len(hands)):  # Loop through card ranks
            btn = tk.Button(
                root,
                text=f"{hands[j]}{Suits[i]}",
                width=5,
                height=2,
                bg="gray",
                fg="black",
            )
            btn.config(command=lambda r=i, c=j, b=btn: toggleRunout(r, c, b))
            btn.grid(row=i+1, column=j, padx=1, pady=1)
            buttons[i][j] = btn

    # Finalize button to close the window and validate runout
    def finalize():
        nonlocal FullRunout
        if len(Flop) < 3:
            FullRunout = "Incoherent Runout: Please select at least 3 flop cards."
        elif not Turn:
            FullRunout = Flop
        elif not River:
            FullRunout = Flop + [Turn]
        else:
            FullRunout = Flop + [Turn, River]
        root.destroy()  # Close the Tkinter window

    done_button = tk.Button(root, text="Done", command=finalize, bg="blue", fg="white")
    done_button.grid(row=8, columnspan=13, pady=10)

    # Run the Tkinter event loop
    root.mainloop()
    return FullRunout 



# In[78]:


def RandomRunoutCompleter (IncompleteRunout, Hero): 
    FinalRunout=[item for item in IncompleteRunout]

    NumberOfMissingCards = 5 - len(IncompleteRunout) 
    PossibleCards = [f"{num}{suit}" for suit in "schd" for num in range(2, 15)]

    UsedCards = Hero 

    RemainingCards = [item for item in PossibleCards if item not in UsedCards]

    for i in range(NumberOfMissingCards): 
        card = random.choice(RemainingCards)
        FinalRunout.append(card)
        RemainingCards.remove(card)  

    return FinalRunout





# In[14]:


def RandomRunout (Hero, Villain):
    Runout = [] 
    PossibleCards = [f"{num}{suit}" for suit in "schd" for num in range(2, 15)]
    RemovedCards = Hero + Villain

    RemainingCards = [item for item in PossibleCards if item not in RemovedCards]

    for i in range(5): 
        card = random.choice(RemainingCards)
        Runout.append(card)
        RemainingCards.remove(card)  

    return Runout


# In[16]:


def RandomRunoutVsRange (Hero):
    Runout = [] 
    PossibleCards = [f"{num}{suit}" for suit in "schd" for num in range(2, 15)]

    RemovedCards = Hero 

    RemainingCards = [item for item in PossibleCards if item not in RemovedCards]

    for i in range(5): 
        card = random.choice(RemainingCards)
        Runout.append(card)
        RemainingCards.remove(card)  

    return Runout



# In[18]:


def RankToNumber(rank):
    if rank == "A":
        return "14"
    elif rank == "K":
        return "13"
    elif rank == "Q":
        return "12"
    elif rank == "J":
        return "11"
    elif rank == "T":
        return "10"
    else:
        return rank


# In[20]:


def ConvertHandWhenLetters(PossibleCombo):
    equivalent = []
    for card in PossibleCombo:
        # Split rank and suit
        rank, suit = card[:-1], card[-1]
        # Convert rank using rank_to_number and append the full card
        equivalent.append(RankToNumber(rank) + suit)
    return equivalent


# In[22]:


def UsualHandToComputingHandsInRange(Hand):
    SuitedOrOffSuit = Hand[-1]  # Get the last character to determine suited/off-suited
    card1 = Hand[0]
    card2 = Hand[1]
    possiblesuits = ["s", "c", "h", "d"]
    ComputingRange = []

    equivalent1 = RankToNumber(card1)
    equivalent2 = RankToNumber(card2)

    # Generate suited combinations
    if SuitedOrOffSuit == "s":
        for suit in possiblesuits:
            ComputingRange.append([equivalent1 + suit, equivalent2 + suit])

    # Generate off-suited combinations
    elif SuitedOrOffSuit == "o":
        for suit1 in possiblesuits:
            for suit2 in possiblesuits:
                if suit1 != suit2:  # Ensure different suits
                    ComputingRange.append([equivalent1 + suit1, equivalent2 + suit2])

    # Handle pocket pairs (e.g., "AA")
    elif SuitedOrOffSuit != "o" and SuitedOrOffSuit != "s":
        for i in range(len(possiblesuits)):
            for j in range(i + 1, len(possiblesuits)):  # Avoid same suit combinations
                ComputingRange.append([equivalent1 + possiblesuits[i], equivalent1 + possiblesuits[j]])
    return ComputingRange


# In[24]:


def HandCategory (Combo, CommunityCards) :

    #defining the cards used 
    UsableCards = CommunityCards + Combo
    Hand=0
    numbers = [int(card[:-1]) for card in UsableCards]
    suits = [card[-1] for card in UsableCards]

    #finding most common suits and numbers
    CountSameSuit = Counter(suits).most_common(1)
    MostCommonSuit = CountSameSuit[0][0]
    CounterSameNumber = Counter(numbers)

    #for flush
    SuitedNumbers = [numbers[i] for i in range(len(numbers)) if suits[i] == MostCommonSuit]
    SuitedNumbers.sort(reverse=True)  # Sort numbers to check for consecutive sequences

    if CountSameSuit[0][1]>=5:
        if CountSameSuit[0][1]==5:
            FirstDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(4)]
            if Counter(FirstDifferenceSuited)[1]+1 == 5 : 
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers
                return Hand, NumbersUsed
        elif CountSameSuit[0][1] == 6 :
            FirstDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(4)]
            SecondDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(1,5)]
            if Counter(FirstDifferenceSuited)[1]+1 == 5 :
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers[:5]
                return Hand, NumbersUsed
            elif Counter(SecondDifferenceSuited)[1]+1 == 5 :
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers[1:6]
                return Hand, NumbersUsed
        elif CountSameSuit[0][1] == 7 :
            FirstDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(4)]
            SecondDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(1,5)]
            ThirdDifferenceSuited = [SuitedNumbers[i]-SuitedNumbers[i+1] for i in range(2,6)]
            if Counter(FirstDifferenceSuited)[1]+1 == 5 :
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers[:5]
                return Hand, NumbersUsed
            elif Counter(SecondDifferenceSuited)[1]+1 == 5 :
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers[1:6] 
                return Hand, NumbersUsed
            elif Counter(ThirdDifferenceSuited)[1]+1 == 5 :
                Hand = ["Straight Flush", 1]
                NumbersUsed = SuitedNumbers[2:7]  
                return Hand, NumbersUsed

    if 4 in CounterSameNumber.values() :
        Hand = ["Four of a kind",2]
        CriticalCard = CounterSameNumber.most_common(1)[0][0]
        numbers=[item for item in numbers if item!=CriticalCard]
        NumbersUsed= [CriticalCard, numbers[0]]
        return Hand, NumbersUsed

    if 3 in CounterSameNumber.values() and 2 in CounterSameNumber.values() : 
        Hand = ["Full", 3]
        NumbersUsed = [CounterSameNumber.most_common(1)[0][0],CounterSameNumber.most_common(2)[1][0]]
        return Hand, NumbersUsed

    if CountSameSuit[0][1]>=5 and Hand != ["Straight Flush", 1] and Hand!=["Full", 3] : 
        Hand = ["Flush",4]
        NumbersUsed=SuitedNumbers[:5] ##question here : this finds if there is a flush (problem with the straight flush"
        return Hand, NumbersUsed
    #elif CountSameSuit[0][1]>=5 and Hand == "": 
        #Hand = ["Flush",4]
        #NumbersUsed=SuitedNumbers[:5] ##question here : this finds if there is a flush (problem with the straight flush)"
    numbers.sort(reverse=True)#say why this is useful
    UniqueNumbers = sorted(set(numbers), reverse=True)
    for i in range(len(UniqueNumbers) - 4):  # At least 5 cards are needed for a straight
        if UniqueNumbers[i] - UniqueNumbers[i + 4] == 4:        
            Hand = ["Straight", 5]
            NumbersUsed = numbers[:5]
            return Hand, NumbersUsed


    if 3 in CounterSameNumber.values() :
        Hand = ["Three of a kind",6]
        CriticalCard = CounterSameNumber.most_common(1)[0][0]
        numbers=[item for item in numbers if item!=CriticalCard]
        NumbersUsed= [CriticalCard, numbers[:2]]
        return Hand, NumbersUsed

    if 2 in CounterSameNumber.values() : 
        if 2 in Counter(CounterSameNumber.values()).values() :
            Hand = ["2 Pair",7]
            CriticalCard = CounterSameNumber.most_common(2)[0][0]
            CriticalCard2= CounterSameNumber.most_common(2)[1][0]
            numbers=[item for item in numbers if item!=CriticalCard and item!=CriticalCard2]
            NumbersUsed= [CriticalCard,CriticalCard2, numbers[0]]
            return Hand, NumbersUsed
        else : 
            Hand = ["Pair",8]
            CriticalCard = CounterSameNumber.most_common(2)[0][0]
            numbers=[item for item in numbers if item!=CriticalCard]
            NumbersUsed= [CriticalCard, numbers[:2]]
            return Hand, NumbersUsed

    if Hand==0 : 
        Hand = ["High Card",9]
        NumbersUsed=numbers

    return Hand, NumbersUsed

## Removed auto-execution: example call was running on import


# In[26]:


def WinOrLose (Hero, Villain, communityCards) :
    HeroCategory = HandCategory (Hero,communityCards)
    VillainCategory = HandCategory (Villain,communityCards)
    result=""
    if HeroCategory[0][1]<VillainCategory[0][1]:
        result="win"
    elif HeroCategory[0][1]>VillainCategory[0][1]:
        result="lose"
    else :
        for i in range(len(HeroCategory[1])):
            if HeroCategory[1][i]>VillainCategory[1][i] : 
                result = "win" 
                break
            if HeroCategory[1][i]<VillainCategory[1][i] : 
                result = "lose"
                break

        if result =="":
            result = "draw"


    return result

## Removed auto-execution: example call was running on import






# In[28]:


def SetOfQuestions():
    root = tk.Tk()
    root.title("Two Questions")

    # Variables to hold responses
    response1 = tk.StringVar(value="")  # Holds the response for question 1
    response2 = tk.StringVar(value="")  # Holds the response for question 2
    is_done = tk.BooleanVar(value=False)  # Tracks whether the user clicked "Done"

    # Define function to handle button clicks
    def set_response(question_num, value, selected_button, other_button):
        if question_num == 1:
            # If already selected, deselect it
            if response1.get() == value:
                response1.set("")  # Clear the response
                selected_button.config(bg="green", fg="white", state="normal")
                other_button.config(state="normal")  # Re-enable the other button
            else:
                response1.set(value)
                selected_button.config(bg="blue", fg="white", state="disabled")
                other_button.config(bg="gray", fg="black", state="normal")
        elif question_num == 2:
            # If already selected, deselect it
            if response2.get() == value:
                response2.set("")  # Clear the response
                selected_button.config(bg="green", fg="white", state="normal")
                other_button.config(state="normal")  # Re-enable the other button
            else:
                response2.set(value)
                selected_button.config(bg="blue", fg="white", state="disabled")
                other_button.config(bg="gray", fg="black", state="normal")

    # Define the finalize function for the "Done" button
    def finalize():
        is_done.set(True)  # Mark the selection process as complete
        root.destroy()  # Close the Tkinter window

    # Question 1
    question1_label = tk.Label(
        root,
        text="Do you want to simulate your hand against all the other possible hands or do you wish to narrow it down to the possible range of hands your opponent might have?",
        font=("Helvetica", 10),
        wraplength=600
    )
    question1_label.pack(pady=10)

    # Buttons for Question 1
    yes_button1 = tk.Button(root, text="All the possible hands", bg="green", fg="white")
    no_button1 = tk.Button(root, text="The possible range", bg="red", fg="white")

    yes_button1.config(command=lambda: set_response(1, "RandomVillain", yes_button1, no_button1))
    no_button1.config(command=lambda: set_response(1, "VillainRange", no_button1, yes_button1))

    yes_button1.pack(pady=5)
    no_button1.pack(pady=5)

    # Question 2
    question2_label = tk.Label(
        root,
        text="Do you want to simulate your hand for all possible Runouts or do you wish to narrow it down to a certain runout?",
        font=("Helvetica", 10),
        wraplength=600
    )
    question2_label.pack(pady=20)

    # Buttons for Question 2
    yes_button2 = tk.Button(root, text="All Possible Runouts", bg="green", fg="white")
    no_button2 = tk.Button(root, text="Determined Runout", bg="red", fg="white")

    yes_button2.config(command=lambda: set_response(2, "RandomRunout", yes_button2, no_button2))
    no_button2.config(command=lambda: set_response(2, "ChosenRunout", no_button2, yes_button2))

    yes_button2.pack(pady=5)
    no_button2.pack(pady=5)

    # Add the "Done" button
    done_button = tk.Button(root, text="Done", command=finalize, bg="blue", fg="white")
    done_button.pack(pady=20)

    # Wait for the user to click "Done"
    root.wait_variable(is_done)

    Responses = response1.get(), response2.get()

    # Return responses for both questions
    return Responses





# In[82]:


def EquityCalculator (NumberOfIterations):
    winCount = 0
    DrawCount = 0 
    LostCount = 0 
    NumberOfloops = 0
    CategoryOffinalHand = []
    WonWith = []
    LostTo = []
    HeroInUsual = ChooseHeroHand()
    if len(HeroInUsual)!= 2 : return "Incoherent Hero Cards, please select 2 cards for Hero"
    Hero = ConvertHandWhenLetters(HeroInUsual)
    Answers = SetOfQuestions()

    if Answers[1] == "ChosenRunout" : 
        MaybeIncompleteRunoutInUsual = ChosenRunout()
        if MaybeIncompleteRunoutInUsual == "Incoherent Runout: Please select at least 3 flop cards.":
            return MaybeIncompleteRunoutInUsual
        MaybeIncompleteRunoutInComputing = ConvertHandWhenLetters (MaybeIncompleteRunoutInUsual)
    else : MaybeIncompleteRunoutInComputing = []

    if Answers[0] == "VillainRange" : 
        OpponentRangeInUsual = SelectVillainRange()
        if OpponentRangeInUsual == [] : return "Incoherent Range, please select at least 1 combinaison"
        OpponentRangeInComputing = [UsualHandToComputingHandsInRange(UsualNotation) for UsualNotation in OpponentRangeInUsual]
        FlattenedRange = [hand for sublist in OpponentRangeInComputing for hand in sublist]

    if len(MaybeIncompleteRunoutInComputing) == 5 and Answers[0] == "VillainRange" : 
        Runout = MaybeIncompleteRunoutInComputing
        for i in range(len(FlattenedRange)): 
            Villain = FlattenedRange[i]
            HeroHand = HandCategory(Hero, Runout)
            CategoryOffinalHand.append(HeroHand)
            VillainHand = HandCategory(Villain, Runout)
            State = WinOrLose(Hero, Villain, Runout)
            NumberOfloops += 1

            if State == "win":
                winCount += 1
                WonWith.append(HeroHand)
            elif State == "draw":
                DrawCount += 1
            else:
                LostTo.append(VillainHand)

    else : 
        for _ in range(NumberOfIterations):
            if Answers[0] == "RandomVillain" : 
                FlattenedRange = ["Only 1 hand"]
            for i in range(len(FlattenedRange)): 
                if Answers[0] == "VillainRange" : Villain = FlattenedRange[i]
                else : Villain = RandomVillain (Hero)
                if Answers[1] == "RandomRunout":
                    Runout = RandomRunout(Villain, Hero)
                elif len(MaybeIncompleteRunoutInComputing)<5 : 
                    Runout = RandomRunoutCompleter (MaybeIncompleteRunoutInComputing, Hero)
                else : Runout = MaybeIncompleteRunoutInComputing

        


                HeroHand = HandCategory(Hero, Runout)
                CategoryOffinalHand.append(HeroHand)
                VillainHand = HandCategory(Villain, Runout)
                State = WinOrLose(Hero, Villain, Runout)
                NumberOfloops += 1

                if State == "win":
                    winCount += 1
                    WonWith.append(HeroHand)
                elif State == "draw":
                    DrawCount += 1
                else:
                    LostCount += 1
                    LostTo.append(VillainHand)

    winRatio = winCount / (NumberOfloops)
    DrawRatio =  DrawCount / (NumberOfloops)
    equity = winRatio + 0.5*DrawRatio

    handTypes = ["High Card", "Pair", "2 Pair", "Three of a kind","Straight", "Flush", "Full", "Four of a kind", "Straight Flush"]
    WinHandCount = {hand: 0 for hand in handTypes}  
    LostToHandCount = {hand: 0 for hand in handTypes}  # Initialize frequencies to 0
    MadeHandCount = {hand: 0 for hand in handTypes}


    for hand in WonWith:
        handName = hand[0][0]
        WinHandCount[handName] += 1


    if winCount > 0:
        WinHandFrequency = {hand: count / winCount for hand, count in WinHandCount.items()}
    else : WinHandFrequency = {hand: 0 for hand in handTypes}


    for hand in LostTo:
        handName = hand[0][0]
        LostToHandCount[handName] += 1


    if LostCount > 0:
        LostToHandFrequency = {hand: count / len(LostTo) for hand, count in LostToHandCount.items()}
    else : LostToHandFrequency = {hand: 0 for hand in handTypes}

    for hand in CategoryOffinalHand: 
        handName = hand[0][0]
        MadeHandCount[handName] += 1

    if CategoryOffinalHand: 
        MadeHandFrequency = {hand: count / len(CategoryOffinalHand) for hand, count in MadeHandCount.items()}

    MadeHandDetails = [
        f"Hero Made a - {hand} - in {MadeHandFrequency[hand]:.2%} of the times."
        for hand in handTypes
    ]


    WinDetails = [
        f"Hero Won with - {hand} - in {WinHandFrequency[hand]:.2%} of the times when he won."
        for hand in handTypes
    ]
    LossDetails = [
        f"Hero Lost to - {hand} - in {LostToHandFrequency[hand]:.2%} of the times when he lost."
        for hand in handTypes
    ]

    return (
        f"For the specific Hand {HeroInUsual}, Hero has {equity:.2%} equity with a "
        f"{winRatio:.2%} Win Ratio, and {DrawRatio:.2%} of Draws "
        f"against {"a random Villain" if Answers[0] == "RandomVillain" else f"the range {OpponentRangeInUsual}"}"
        f" on {"a random Runout" if Answers[1] == "RandomRunout" else f" {MaybeIncompleteRunoutInUsual}."}",
        *MadeHandDetails,

        *WinDetails,

        *LossDetails,
    )

## Removed auto-execution: example call was running on import


# In[ ]:





# In[ ]:





# In[ ]:





# Timing/plotting analysis moved to a separate module to avoid side effects on import.

if __name__ == "__main__":
    """
    When this script is executed directly it will prompt the user for the number of
    iterations and then launch the equity calculator. The equity calculator
    opens a series of small Tkinter windows to gather input on the hero hand,
    villain range and any community cards, then estimates the hero's equity
    versus the selected range over a number of random simulations.

    A default of 1 000 iterations is used if no valid integer is provided.
    """
    try:
        iterations = int(input("Enter number of iterations for equity calculation (e.g. 1000): "))
    except (ValueError, EOFError):
        iterations = 1000
    result = EquityCalculator(iterations)


# In[ ]:




