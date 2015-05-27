# NgramScript

Created by JB Michel for the Harvard Cultural Observatory, Oct 19 2012 www.culturomics.org, @culturomics, @jb_michel.

Modified by M Shamim for the Rice Cultural Observatory, May 27, 2015 www.culturomics.org, @theaidenlab.


This is a basic python code to retrieve data behind trajectories plotted on the Google Books Ngram Viewer: books.google.com/ngrams. Just type exactly the same string you would have type on books.google.com/ngrams, and retrieve the data in tsv format. By default, data is printed on screen and saved to file in the current directory.

Note to savvy users: 
1. you can directly pass queries as arguments to the python script, such as "python getNgrams.py awesome" or "getNgrams.exe great". 
2. if you pass the '-quit' flag as an argument, the program will run once and quit without asking for more input, such as "python getNgrams.py awesome, sauce -quit". 	
3. Known caveat: quotation marks are removed from the input query. 

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

PLEASE do respect the terms of service of the Google Books Ngram Viewer while using this code.
This code is meant to help viewers retrieve data behind a few queries, not bang at Google's  servers with thousands of queries.
The complete dataset can be freely downloaded here: http://storage.googleapis.com/books/ngrams/books/datasetsv2.html.
This code is not a Google product and is not endorsed by Google in any way. 

With this in mind... happy plotting!
