from PIL import Image
import os
import inspect

def RuneWritter(word):
	letters = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
	syllables = getAllSyllables( ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"], ["a","e","i","o","u"] ) + getAllSyllables( ["a","e","i","o","u"], ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"] )
	chSyllables = ["cha","che","chi","cho","chu"]

	if len(word)>= 3:
		for index in range(0,len(word)-2):
			if word[index:index+3] in chSyllables:
				prevStr = word[:index]
				midStr = word[index:index+3]
				afterStr = word[index+3:]
				
				result = [midStr]
				if prevStr != "":
					prevResult = RuneWritter(prevStr)
					result = prevResult + result
				if afterStr != "":
					afterResult = RuneWritter(afterStr)
					result = result + afterResult

				return result

	if len(word) >= 2:
		for index in range(0,len(word)-1):
			if word[index:index+2] in syllables:
				prevStr = word[:index]
				midStr = word[index:index+2]
				afterStr = word[index+2:]
				
				result = [midStr]
				if prevStr != "":
					prevResult = RuneWritter(prevStr)
					result = prevResult + result
				if afterStr != "":
					afterResult = RuneWritter(afterStr)
					result = result + afterResult

				return result

	if len(word) == 1:
		return [word]


def RuneWriterMain(id, word):
	currentDir = os.path.dirname(os.path.abspath(__file__))
	letterDir = "/Letters/"
	absDir = os.path.join(currentDir, letterDir)
	print(absDir)

	word = word.lower()

	wordSyllables = RuneWritter(word)

	print(wordSyllables)

	for s in wordSyllables:
		test = Image.open(absDir+s.upper()+".png")




def getAllSyllables(consonants, vowels):
	syllables = []
	for x in consonants:
		for y in vowels:
			syllables.append(x+y)
	return syllables


RuneWriterMain(1,"Creation")