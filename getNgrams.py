#!/usr/bin/env python

import urllib,re,sys,csv,os
import urllib.parse
import urllib.request

INFO="""
Python code to retrieve data behind trajectories plotted on the Google Books Ngram Viewer: books.google.com/ngrams.
Type exactly the same string you would have type on books.google.com/ngrams, and retrieve the data in csv/tsv format.
By default, data is printed on screen and saved to file in the current directory.

Note to savvy users: 
(1) you can directly pass queries as arguments to the python script, such as "python getNgrams.py awesome"
(2) if you pass the '-quit' flag as an argument, the program will run once and quit without asking for more input, such as "python getNgrams.py awesome, sauce -quit". 	
(3) Known caveat: quotation marks are removed from the input query. 

Example usage:
  Albert Einstein, Charles Darwin
  burnt_VERB/(burnt_VERB+burned)
  Pearl Harbor, Watergate -corpus=eng_2009 -nosave 
  bells and whistles -startYear=1900 -endYear=2001 -smoothing=2
  -quit
 	
Flags:
  -corpus=CORPUS [default: eng_2019]
     this will run the query in CORPUS. Possible values are  
     recapitulated below, and here http://books.google.com/ngrams/info.  
  -startYear=YEAR [default: 1500]
     start the query in YEAR (integer). 
  -endYear=YEAR [default: 2019]
     ends the query in YEAR (integer).
  -smoothing=SMOOTHING [default: 3]
     smoothing parameter (integer). Minimum is 0. 
  -nosave
     results will not be saved to file.
  -csv
     results will be saved to a csv file (default is tsv).
  -noprint
     results will not be printed on screen.
  -help
     prints this screen.
  -quit
     quits. 

Possible corpora:
  eng_2019,eng_2012, eng_2009, eng_us_2019, eng_us_2012, eng_us_2009, eng_gb_2019, eng_gb_2012, eng_gb_2009, 
  chi_sim_2019, chi_sim_2012, chi_sim_2009, fre_2019, fre_2012, fre_2009, ger_2019, ger_2012, ger_2009,
  spa_2019, spa_2012, spa_2009, rus_2019, rus_2012, rus_2009, heb_2019, heb_2012, heb_2009, ita_2019, ita_2012,	
  eng_fiction_2019, eng_fiction_2012, eng_fiction_2009, eng_1m_2009

PLEASE do respect the terms of service of the Google Books Ngram Viewer while using this code.
This code is meant to help viewers retrieve data behind a few queries, not bang at Google's  servers with thousands of queries.
The complete dataset can be freely downloaded here: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html.

This code is not a Google product and is not endorsed by Google in any way. 

With this in mind... happy plotting!
"""

corpora={'eng_us_2012':17, 'eng_us_2009':5, 'eng_gb_2012':18, 'eng_gb_2009':6, 
	'chi_sim_2012':23, 'chi_sim_2009':11,'eng_2012':15, 'eng_2009':0,
	'eng_fiction_2012':16, 'eng_fiction_2009':4, 'eng_1m_2009':1, 'fre_2012':19, 'fre_2009':7, 
	'ger_2012':20, 'ger_2012':20, 'ger_2009':8, 'heb_2012':24, 'heb_2009':9,
	'spa_2012':21, 'spa_2009':10, 'rus_2012':25, 'rus_2009':12, 'ita_2012':22,
	'eng_2019':26, 'eng_us_2019':28, 'eng_gb_2019':29, 'eng_fiction_2019':27, 'chi_sim_2019':34,
	'fre_2019':30, 'ger_2019':31, 'heb_2019':35, 'spa_2019':32, 'rus_2019':36, 'ita_2019':33}


def extractCleanTerms(regExpression, filterTerms, fullText):

	foundSections=re.findall(regExpression, fullText.decode('utf-8'))

	for index in range(len(foundSections)):
		for filterTerm in filterTerms:
			foundSections[index] = re.sub(filterTerm, '', foundSections[index])

	return foundSections


def getNgrams(query, corpus, startYear, endYear, smoothing):
	urlquery = urllib.parse.quote_plus(query, safe='"')
	corpusNumber=corpora[corpus]
	url = 'http://books.google.com/ngrams/graph?content=%s&year_start=%d&year_end=%d&corpus=%d&smoothing=%d'%(urlquery,startYear,endYear,corpusNumber,smoothing)
	response = urllib.request.urlopen( url ).read()
	
	timeseries = extractCleanTerms("\"timeseries\": \[.*?\]",["\"timeseries\": \[","\]"],response)
	termsSearched = extractCleanTerms("\{\"ngram\": \".*?\"",["\{\"ngram\": \"","\""],response)
	
	termsToTimeseries = {}
	for index in range(len(termsSearched)):
		termsToTimeseries[termsSearched[index]] = [float(time) for time in timeseries[index].split(",")]

	return url, urlquery, termsToTimeseries


def reOrganizeDataByYear(data, startYear, endYear):

	terms = data.keys()
	sortedData = {}

	for i in range(endYear-startYear+1):
		values = []
		for term in terms:
			values.append(data[term][i])
		sortedData[startYear+i] = values

	return terms, sortedData


def saveData(fname, data, url, outputAsTSV, startYear, endYear):
	# write to csv first (can't directly write using tab delimeters with csvwriter)
	# then convert to tsv and delete the csv file

	terms, resortedData = reOrganizeDataByYear(data, startYear, endYear)
	
	outputFile = open(fname+".csv", 'w',newline='')
	writer = csv.writer(outputFile)
	writer.writerow([url])
	writer.writerow(["year"]+list(terms))

	for year in range(startYear,endYear+1):
		writer.writerow([year] + resortedData[year])


	#for key, value in data.items():
	#	writer.writerow([key] + value)
	outputFile.close()

	if(outputAsTSV):
		csv.writer(file(fname+".tsv", 'w+'), delimiter="\t").writerows(csv.reader(open(fname+".csv")))
		os.remove(fname+".csv")
	


def runQuery(argumentString):
	arguments = argumentString.split()
	query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
	params = [arg for arg in arguments if arg.startswith('-')]
	printHelp, toSave, toTSV, toPrint,corpus,startYear,endYear,smoothing=False, True, True, True, 'eng_2019',1500,2019,3
	
	# parsing the query parameters
	for param in params:
		if '-nosave' in param:
			toSave=False
		elif '-csv' in param:
			toTSV=False
		elif '-noprint' in param:
			toPrint=False
		elif '-corpus' in param:
			corpus=param.split('=')[1].strip()
		elif '-startYear' in param:
			startYear=int(param.split('=')[1])
		elif '-endYear' in param:
			endYear=int(param.split('=')[1])
		elif '-smoothing' in param:
			smoothing=int(param.split('=')[1])	
		elif '-help' in param:
			printHelp=True
		elif '-quit' in param:
			pass
		else:
			print ('Did not recognize the following argument:', param)
	
	if printHelp:
		print (INFO)
	else:			
		url, urlquery,data = getNgrams(query, corpus, startYear, endYear, smoothing)
		if toPrint:
			print (url)
			print (data)
		if toSave:
			filename='%s：%d-%d（%s）'%(urlquery.replace('%2C',' '),startYear,endYear,corpus)
			saveData(filename,data,url,toTSV, startYear, endYear)
			print ('Data saved to %s'%filename)

if __name__ == '__main__':
	argumentString = ' '.join(sys.argv[1:])
	if '-quit' in argumentString.split():
		runQuery(argumentString)
		
	if argumentString=='':
		argumentString = input("Please enter an ngram query (or -help, or -quit):")
	while '-quit' not in argumentString.split():
		#try:
		runQuery(argumentString)
		#except:
		#	print 'An error occurred.'
		argumentString = input("Please enter an ngram query (or -help, or -quit):")
