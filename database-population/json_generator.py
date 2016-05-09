from firebase import firebase
from datetime import datetime
import string
import os

def strpbrk(haystack, needleCharacters) :
	index = len(haystack) +1
	for c in needleCharacters :
		calc = haystack.find(c)
		if calc != -1 and calc < index : index = calc
	return index

def whitespace_to_one_space(entry) :
	calcS = entry

	for whitespace in string.whitespace :
		calcS = calcS.replace(whitespace, ' ')
	for whitespace in "\r\n" :
		calcS = calcS.replace(whitespace, ' ')
	while '  ' in calcS :
		calcS = calcS.replace('  ', ' ')
	calcS = calcS.strip()
	return calcS

def parseDataDoc(filename) :
	detailsDoc = open(filename)
	detailsDocString = detailsDoc.read()
	paragraphs = detailsDocString.split('[')
	jsonObject = {}
	cardsUnderConstruction 	= {}
	supportedCardTypes 	= {'CompanyDetailedCard', 'CompanyBriefCard', 'EntrepreneurCard'}
	entryCounts		= {}
	associatedHash = {	'EntrepreneurHeading'	: 'EntrepreneurCard',
				'InvestorHeading'	: 'InvestorCard',
				'CompanyDetailedHeading': 'CompanyDetailedCard',
				'CompanyDetailedBody'	: 'CompanyDetailedCard',
				'CompanyDetailedLogo'	: 'CompanyDetailedCard',
				'CompanyBriefHeading'	: 'CompanyBriefCard',
				'CompanyBriefBody'	: 'CompanyBriefCard',
				'CompanyBriefLogo'	: 'CompanyBriefCard',
			 }
	for cardtype in supportedCardTypes :
		entryCounts[cardtype] = 0

	for paragraph in paragraphs[1:len(paragraphs)] :
#parse the [bracketed statement]. this contains all the styling fields this paragraph should be placed under in the database
		calc = paragraph.find(']')
		if calc == -1 :
			raise ValueError("mismatched close bracket!")
		fieldTypes	= paragraph[0: calc]
		fieldTypes	= fieldTypes.strip()


		paragraph 	= paragraph[calc +1: len(paragraph)]
		paragraph 	= paragraph.strip()
		calc 		= fieldTypes.find('|')
		if calc == -1 :
			raise ValueError("entry " + fieldTypes + " requires at least one specified field type (specified with |)")
		fieldsHere = []
		while calc != -1 :
			calcS 	= fieldTypes[0:calc]
			calcS = calcS.strip()
			fieldsHere.append(calcS)
			fieldTypes = fieldTypes[calc + 1: len(fieldTypes)]
			calc 	= fieldTypes.find('|')
		title = fieldTypes
		if len(title) == 0 :
			title =  "<+Untitled+>"
		for fieldType in fieldsHere :
			if fieldType in supportedCardTypes :
				if fieldType in cardsUnderConstruction :
					if not (fieldType + "s") in jsonObject :
						jsonObject[fieldType + "s"] = {}
					jsonObject[fieldType + "s"][entryCounts[fieldType]] = {}
#					jsonObject[fieldType + "s"][entryCounts[fieldType]][fieldType] 	= cardsUnderConstruction[fieldType]
					jsonObject[fieldType + "s"][entryCounts[fieldType]] 		= cardsUnderConstruction[fieldType]
					
					entryCounts[fieldType] += 1
				cardsUnderConstruction[fieldType] = {}
				cardsUnderConstruction[fieldType]['Title'] = title
#add the paragraph data to one of the cards under construction
			else :
				if not fieldType in associatedHash  :
					raise ValueError("entry " + title + " is not recognized.")
				if not associatedHash[fieldType] in cardsUnderConstruction :
					raise ValueError("entry " + title + " requires a preceeding " + associatedHash[fieldType])
				if not fieldType in cardsUnderConstruction[associatedHash[fieldType]] :
					cardsUnderConstruction[associatedHash[fieldType]][fieldType] = {}
				cardsUnderConstruction[associatedHash[fieldType]][fieldType][title] = paragraph
	for lastCards in supportedCardTypes :
		if lastCards in cardsUnderConstruction :
			if not (lastCards + "s") in jsonObject :
				jsonObject[lastCards + "s"] = {}
			jsonObject[lastCards + "s"][entryCounts[lastCards]] = {}
			jsonObject[lastCards + "s"][entryCounts[lastCards]] = cardsUnderConstruction[lastCards]
	return jsonObject	
	
#https://github.com/ozgur/python-firebase
firebase = firebase.FirebaseApplication('https://seattle-angels.firebaseio.com', None);
do_write = True

firebasePath = '/'
for dataDocFile in os.listdir('.') :
	if dataDocFile[dataDocFile.rfind('.'):] != '.txt' :
		continue
	parsed = parseDataDoc(dataDocFile)
	parsed['cardsetOrder'] = [ 	'FrontCoverCards',
					'OverviewCards',
					'AgendaCards',
					'WelcomeMessageCards',
					'KeynoteSpeakerCards',
					'InvestorsCards',
					'CompanyBriefCards',
					'FiresideChatCards',
					'WinnerSelectionCards'
					'OurSponsorsCards',
					'AngelGroupsCards',
					'SeattleAngelCards'
				]
	if do_write :
		try :
			databaseReply = firebase.put(firebasePath, 'SAC_9_1', parsed);
		except :
			print("---------------------------")
			print(parsed)
			print("---------------------------")
			raise ValueError("upload barfed on " + 	"\n\t" + firebasePath)
	else :
		print(parsed)
