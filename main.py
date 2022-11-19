import string
import pyautogui
import time
import sys
from PIL import ImageGrab

def wordChecks(word):
  for index in green:
    if currentWord[index] != word[index]:
      return False
    else:
      word = word[:index] + "_" + word[index + 1:]
  
  for index in yellow:
    if currentWord[index] not in word or currentWord[index] == word[index]:
      return False
    
  for letter in unusedLetters:
    if letter in word:
      return False
      
  return True

def getWordFrequency(word):
  freq = 0
  for letter in word:
    freq += letterFrequency[letter] / word.count(letter)
    
  return freq

def updateUnusedLetters():
  newLetters = [currentWord[letterIndex] for letterIndex, _ in enumerate(currentWord) if letterIndex not in green + yellow]
  
  for letter in newLetters:
    if letter not in unusedLetters:
      unusedLetters.append(letter)
      
  return unusedLetters

with open("words.txt", "r") as f:
  availableWords = f.read().splitlines()

attempts = 0
wordleRect = (628, 285, 975, 705)
unusedLetters = []
letterFrequency = dict.fromkeys(string.ascii_lowercase, 0)

greenCol = (121, 184, 81)
yellowCol = (243, 194, 55)

for letter in letterFrequency:
  freq = 0
  for word in availableWords:
    freq += word.count(letter)
  
  letterFrequency[letter] = freq

availableWords.sort(key=getWordFrequency, reverse=True)
currentWord = availableWords[0]

time.sleep(5)

pyautogui.write(currentWord, interval=0.25)
pyautogui.press("enter")

availableWords.remove(currentWord)

while attempts < 7:
  time.sleep(2)
  img = ImageGrab.grab().crop(wordleRect)
  width, height = img.size
  letterWidth = width / 5
  rowHeight = height / 6
  
  green = []
  yellow = []
  
  for index in range(5):
    rgb = img.getpixel((letterWidth * index + letterWidth / 10, rowHeight * attempts + rowHeight / 10))
    
    if rgb == greenCol:
      green.append(index)
    elif rgb == yellowCol:
      yellow.append(index)
  
  unusedLetters = updateUnusedLetters()

  passedWords = [word for word in availableWords if wordChecks(word)]
  
  passedWords.sort(key=getWordFrequency, reverse=True)
  
  try:
    currentWord = passedWords[0]
  except:
    pyautogui.alert("You won!")
    sys.exit()
  
  pyautogui.write(currentWord, interval=0.25)
  pyautogui.press("enter")
  
  availableWords.remove(currentWord)
  
  attempts += 1
  
pyautogui.alert("You lost!")