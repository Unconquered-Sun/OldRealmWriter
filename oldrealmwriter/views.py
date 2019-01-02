from django.views.generic import View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from .models import old_realm_runes

from PIL import Image
from pathlib import Path
import math
import base64
from io import BytesIO 
import json

# Create your views here.
class Main(View):

	def get(self, request):
		print("TEST_GET")
		csrf_token =  get_token(self.request)
		return render(request, "oldrealmwriter/home.html", {"csrf":csrf_token})
	@csrf_exempt
	def post(self, request):
		print("TEST_POST")
		uncleanInput = request.POST["runeInput"]
		cleanInput = ""
		
		#1st clean the phrase of any non alphabetic character
		for letter in uncleanInput:
			if letter == " " or letter.isalpha():
				cleanInput = cleanInput + letter
		print(cleanInput)
		
		#2nd seperate each word by splitting on spaces
		cleanedWords = cleanInput.split(" ")
		print(cleanedWords)

		#3rd remove any empty words
		finalWords = []
		for word in cleanedWords:
			if word != "":
				finalWords.append(word) 

		#4th process each word and store it
		runes = []
		for word in finalWords:
			#test if word is in database
			results = old_realm_runes.objects.filter(word=word)
			if results != []:
				rune = RuneWriterMain(word)
				new_rune = old_realm_runes(word=word, image=rune.tobytes())

				buffer = BytesIO()
				rune.save(buffer,format="PNG")
				runeimage = buffer.getvalue()
				runeHex = str(base64.b64encode(runeimage))[2:-1]
				# print(runeHex,"\n")
				runes.append(runeHex)
				
			else:
				rune = PIL.Image.frombytes('RGBA', (204,306), results[0].image, decoder_name='raw')
				
				buffer = BytesIO()
				rune.save(buffer,format="PNG")
				runeimage = buffer.getvalue()
				runeHex = str(base64.b64encode(runeimage))[2:-1]
				# print(runeHex,"\n")
				runes.append(runeHex)

		output = json.dumps({"images":runes})
		# print(output)
		return JsonResponse(output,safe=False)
		# return render(request, "oldrealmwriter/home.html")






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
		#If no characters fit the syllable combos the next charcter is added to the result
		result = [word[0]]
		afterStr = word[1:]
		if afterStr != "":
			result = result + RuneWritter(afterStr)
		return result

	if len(word) == 1:
		return [word]


def RuneWriterMain(word):
	currentDir = Path().absolute().joinpath("Letters")
	revSyllables = getAllSyllables( ["a","e","i","o","u"], ["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z"] )
	# Size is in x,y format
	runeSizes = {
					1:[{"size":[204,306],"position":[0,0]}],
					2:[{"size":[204,153],"position":[0,0]}, {"size":[204,153],"position":[0,153]}],
					3:[{"size":[102,102],"position":[0,0]}, {"size":[102,102],"position":[102,0]}, {"size":[204,204],"position":[0,102]}],
					4:[{"size":[102,102],"position":[0,0]}, {"size":[102,102],"position":[0,102]}, {"size":[102,102],"position":[102,0]}, {"size":[102,102],"position":[102,102]}],
					5:[{"size":[136,102],"position":[0,0]}, {"size":[68 ,204],"position":[0,102]}, {"size":[68 ,204],"position":[68,102]}, {"size":[68 ,153],"position":[136,0]}, {"size":[68 ,153],"position":[136,153]}]
	}

	#start processing
	word = word.lower()

	wordSyllables = RuneWritter(word)

	# get all relevant letters
	runes = []
	for s in wordSyllables:
		if s in revSyllables:
			s=s[::-1]
			tempImage = Image.open(currentDir.joinpath(s.upper()+".png"))
			tempImage.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.FLIP_TOP_BOTTOM)
			runes.append(tempImage)
		else:
			tempImage = Image.open(currentDir.joinpath(s.upper()+".png"))
			runes.append(tempImage)

	#Make new image
	result = Image.new('RGBA', (204,306), (0,0,0,0))
	#If letters fit in a template use a prexisting template
	if len(runes) <= 5:
		for index in range(0,len(runes)):
			tempImage = runes[index].copy()
			position = runeSizes[len(runes)][index]["position"]
			size = runeSizes[len(runes)][index]["size"]
			tempImage = tempImage.resize(size)
			result.paste(tempImage, position)
		return result
	else:
		rows = math.ceil( len(runes)/2 )
		odd = False
		if len(runes)%2 == 1:
			odd = True
		height = math.floor( 306/rows )
		width = 102

		#left rows
		current_row = 1
		index = 0
		x = 0
		y = 0
		while current_row <= rows:
			tempImage = runes[index].copy()
			position = (x,y)
			size = (width, height)
			tempImage = tempImage.resize(size)
			result.paste(tempImage, position)
			y=y+height

			current_row+=1
			index+=1

			if current_row == rows and odd == True:
				break

		
		x=102
		y=0
		current_row=1

		while current_row <= rows:
			tempImage = runes[index].copy()
			position = (x,y)
			size = (width, height)
			tempImage = tempImage.resize(size)
			result.paste(tempImage, position)
			y=y+height

			current_row+=1
			index+=1

			if current_row == rows and odd == True:
				tempImage = runes[index].copy()
				position = (0,y)
				size = (204, height)
				tempImage = tempImage.resize(size)
				result.paste(tempImage, position)
				current_row+=1
		return result
				
def getAllSyllables(consonants, vowels):
	syllables = []
	for x in consonants:
		for y in vowels:
			syllables.append(x+y)
	return syllables