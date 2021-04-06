import numpy as np
import math
import sys

######################### Global Variables #########################
#my seed
np.random.seed(1063199)

#card details
CARD_LETTERS = ["A", "B", "C", "D"]
CARD_DIGIT_LENGTH = 16
LOWEST_PRICE = 20
HIGHEST_PRICE = 100

#hash table details
TOTAL_CARD_VISITS = 20
#(before I use it the program changes it to the nearest prime number)
INITIAL_CAPACITY = 5
MAX_LOAD_FACTOR = 0.6

######################### Functions #########################

def createCard():
    #create a random number with the specified length
    cardDigits = [str(np.random.randint(0, 9)) for i in range(CARD_DIGIT_LENGTH)]
    
    #find the spots you will replace with letters
    spotsToReplace = np.random.choice(CARD_DIGIT_LENGTH - 1, len(CARD_LETTERS), replace=False)

    #replace these spots with letters
    for i in range(len(CARD_LETTERS)):
        cardDigits[spotsToReplace[i]] = CARD_LETTERS[i]

    #when you are finished convert the list to a string
    cardDigits = "".join(cardDigits)

    #pick a random value between 20 and 100 for the price they paid
    value = np.random.randint(LOWEST_PRICE, HIGHEST_PRICE)

    #pick a random day (1-7 for Monday-Sunday)
    day = np.random.randint(0, 6)

    return cardDigits, value, day


def isPrime(number):
    #we only need to check until the square root of the number
    for i in range (2, math.ceil(math.sqrt(number))+1):
        if number % i == 0:
            return False
    return True


def findClosestPrime(number):
    while isPrime(number) == False:
        number += 1    
    return number

def hash(key):
    #this where we store the result pf the hash
    result = 0

    #convert string to list
    keyList = []
    keyList[:0] = key

    for i in range(len(keyList)):

        #if its a number then we multiply with the appropriate power of 10
        if keyList[i].isnumeric():
            result += int(keyList[i])*10**i
        #if its a letter convert it to a number first
        else:
            if keyList[i] == "A":
                val = 11
            elif keyList[i] == "B":
                val = 12
            elif keyList[i] == "C":
                val = 13
            else:
                val = 14

            result += val*10**i

    return result

class Card:
    def __init__(self, key, value, day):
        self.key = key
        self.val = value
        self.days = [day]

def putInHashTable(card, hashTable):
    #get the hash result
    result = hash(card.key) % len(hashTable)

    #check if that spot is free
    if type(hashTable[result]) != Card:
        #if it is free it also means that we haven't used that card
        hashTable[result] = card

    else:
        while True:
            #loop until you find an empty spot to put the card
            if type(hashTable[result]) != Card:
                hashTable[result] = card 
                break
            #or loop until you have the same card in that spot 
            #(in that case you need to update it)
            elif hashTable[result].key == card.key:
                hashTable[result].val += card.val
                hashTable[result].days.extend(card.days)
                break

            #this is to move spots
            result = (result+1) % len(hashTable)

    return hashTable


def redefineHashTable(hashTable):
    #create a new hash table with double the size
    newHashTable = [None] * findClosestPrime(2*len(hashTable))

    #copy all the elements to the new hash table
    #(they will have a different position)
    for i in range (len(hashTable)):
        if type(hashTable[i]) == Card:
            newHashTable = putInHashTable(hashTable[i], newHashTable)

    return newHashTable
    

def exceedLoadFactror(hashTable):
    #get the number of cards in the list
    cardCount = sum(isinstance(i, Card) for i in hashTable)

    #if the percentage of Cards exceeds the limit return True
    if cardCount / len(hashTable) > MAX_LOAD_FACTOR:
        return True
    return False
    

######################### Main #########################
#create an empty the hash table    
hashTable = [None] * findClosestPrime(INITIAL_CAPACITY)
print("The initial size of the hash table is: {}" .format(len(hashTable)))

#fill the table with cards
for i in range (TOTAL_CARD_VISITS):
    #get all the values for a card
    id, val, day = createCard()
    #create the card
    card = Card(id, val, day)
    #put the card in the table
    hashTable = putInHashTable(card, hashTable)

    #if the table is too filled then create a bigger one
    #and move everything to it
    if exceedLoadFactror(hashTable):        
        hashTable = redefineHashTable(hashTable)
        print("The new size of the hash table is: {}" .format(len(hashTable)))

print(hashTable)


#variables to answer the questions
#set the min payment value to the max of the system so that we definately find a smaller number in a card
minPaymentsCard = Card('', sys.maxsize, [])
#in the card with the max visits we put an empty list to change it once we find another card
maxVisitsCard = Card('', 0, None)
#create a dictionary with the visits of each day
dayVisits = 7 * [0]
#total number of conflicts
conflictsNum = 0

for i in range(len(hashTable)):
    #first check if we have a card
    if type(hashTable[i]) == Card:

        #to get the card with the least amount payed
        if hashTable[i].val < minPaymentsCard.val:
            minPaymentsCard = hashTable[i]

        #to get the card with the most visits
        if len(hashTable[i].days) >= len(maxVisitsCard.days) or maxVisitsCard.days == [None]:
            maxVisitsCard = hashTable[i]

        #update the visits for each day
        for j in range(len(hashTable[i].days)):
            dayVisits[hashTable[i].days[j]] += 1

        #if the hash of the card doesn't match its position in the list it means that we had a conflict
        if hash(hashTable[i].key)%len(hashTable) != i:
            conflictsNum += 1


print("The card with the least amount payed is {} with {} payed " .format(minPaymentsCard.key, minPaymentsCard.val))
print("The card with the most visits is {} with {} visit(s) " .format(maxVisitsCard.key, len(maxVisitsCard.days)))
print("The day with the most visits is {} with {} visit(s) " .format(dayVisits.index(max(dayVisits)), max(dayVisits)))
print("The total number of conflicts is {}" .format(conflictsNum))
