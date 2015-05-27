import urllib,re,sys

INFO="""
JB Michel for the Harvard Cultural Observatory, Oct 19 2012 www.culturomics.org, @culturomics, @jb_michel. License: None, please distribute, modify and improve as you see fit. 

This is a basic python code to retrieve data behind trajectories plotted on the Google Books Ngram Viewer: books.google.com/ngrams.

Just type exactly the same string you would have type on books.google.com/ngrams, and retrieve the data in tsv format. By default, data is printed on screen and saved to file in the current directory.

Note to savvy users: 
(1) you can directly pass queries as arguments to the python script, such as "python getNgrams.py awesome" or "getNgrams.exe great". 
(2) if you pass the '-quit' flag as an argument, the program will run once and quit without asking for more input, such as "python getNgrams.py awesome, sauce -quit". 	
(3) Known caveat: quotation marks are removed from the input query. 

Example usage:
  Albert Einstein, Charles Darwin
  burnt_VERB/(burnt_VERB+burned)
  Pearl Harbor, Watergate -corpus=eng_2009 -nosave 
  bells and whistles -startYear=1900 -endYear=2001 -smoothing=2
  -quit
 	
Flags:
  -corpus=CORPUS [default: eng_2012]
     this will run the query in CORPUS. Possible values are  
     recapitulated below, and here http://books.google.com/ngrams/info.  
  -startYear=YEAR [default: 1800]
     start the query in YEAR (integer). 
  -endYear=YEAR [default: 2000]
     ends the query in YEAR (integer).
  -smoothing=SMOOTHING [default: 3]
     smoothing parameter (integer). Minimum is 0. 
  -nosave
     results will not be saved to file.
  -noprint
     results will not be printed on screen.
  -help
     prints this screen.
  -quit
     quits. 

Possible corpora:
  eng_2012, eng_2009, eng_us_2012, eng_us_2009, eng_gb_2012, eng_gb_2009, 
  chi_sim_2012, chi_sim_2009, fre_2012, fre_2009, ger_2012, ger_2009,
  spa_2012, spa_2009, rus_2012, rus_2009, heb_2012, heb_2009, ita_2012,	
  eng_fiction_2012, eng_fiction_2009, eng_1m_2009

PLEASE do respect the terms of service of the Google Books Ngram Viewer while using this code. This code is meant to help viewers retrieve data behind a few queries, not bang at Google's  servers with thousands of queries. The complete dataset can be freely downloaded here: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html. This code is not a Google product and is not endorsed by Google in any way. 

With this in mind... happy plotting!
"""

corpora={'eng_us_2012':17, 'eng_us_2009':5, 'eng_gb_2012':18, 'eng_gb_2009':6, 
	'chi_sim_2012':23, 'chi_sim_2009':11,'eng_2012':15, 'eng_2009':0,
	'eng_fiction_2012':16, 'eng_fiction_2009':4, 'eng_1m_2009':1, 'fre_2012':19, 'fre_2009':7, 
	'ger_2012':20, 'ger_2009':8, 'heb_2012':24, 'heb_2009':9, 
	'spa_2012':21, 'spa_2009':10, 'rus_2012':25, 'rus_2009':12, 'ita_2012':22}

def getNgrams(query, corpus, startYear, endYear, smoothing):
	urlquery = urllib.quote_plus(query, safe='"')
	corpusNumber=corpora[corpus]
	url = 'http://books.google.com/ngrams/graph?content=%s&year_start=%d&year_end=%d&corpus=%d&smoothing=%d&share='%(urlquery,startYear,endYear,corpusNumber,smoothing)
	response = urllib.urlopen( url ).read()
	
	res=re.findall("data.addColumn(.*?);", response)
	terms=[r[:-1].split(',')[1].replace("'","").strip() for r in res]
		
	res = re.findall("data.addRows(.*?);", response.replace('\n',''))
	data = [[float(c) for c in r[1:-1].split(',')] for r in re.findall("\[.*?\]", res[0][1:].strip()[1:-1:])]
	
	return url, urlquery, [terms]+data

def saveData(fname, data, url):
	fo = open(fname, 'w')
	fo.write(url+'\n')
	for d in data:
		try:
			fo.write('%d,'%int(d[0])+','.join([str(s) for s in d[1:]])+'\n')
		except:
			fo.write(','.join([str(s) for s in d])+'\n')
	fo.close()

def runQuery(argumentString):
	arguments = argumentString.split()
	query = ' '.join([arg for arg in arguments if not arg.startswith('-')])
	params = [arg for arg in arguments if arg.startswith('-')]
	printHelp, toSave, toPrint,corpus,startYear,endYear,smoothing=False, True,True, 'eng_2012',1800,2000,3
	
	# parsing the query parameters
	for param in params:
		if '-nosave' in param:
			toSave=False
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
			print 'Did not recognize the following argument:', param
	
	if printHelp:
		print INFO
	else:			
		url, urlquery,data = getNgrams(query, corpus, startYear, endYear, smoothing)
		if toPrint:
			print url
			for d in data:
				try:
					print '%d,'%int(d[0])+','.join([str(s) for s in d[1:]])
				except:
					print ','.join([str(s) for s in d])
		if toSave:
			filename='%s-%s-%d-%d-%d.tsv'%(urlquery,corpus,startYear,endYear,smoothing)
			saveData(filename,data,url)
			print 'Data saved to %s'%filename

if __name__ == '__main__':
	argumentString = ' '.join(sys.argv[1:])
	if '-quit' in argumentString.split():
		runQuery(argumentString)
		
	if argumentString=='':
		argumentString = raw_input("Please enter an ngram query (or -help, or -quit):")
	while '-quit' not in argumentString.split():
		try:
			runQuery(argumentString)
		except:
			print 'An error occurred.'
		argumentString = raw_input("Please enter an ngram query (or -help, or -quit):")		
