import os
import sys
import re
import urllib, urllib2
import dryscrape
from BeautifulSoup import BeautifulSoup

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
        
def getlastNames(names):
    lastNames = []
    
    for name in names:
        cols = name.split(" ")
        lastNames.append(cols[-1])
    
    return lastNames        
        
def extractPeopleBehind(imdbUrl):
    imdbLink = imdbUrl + "fullcredits?ref_=tt_cl_sm#cast"
    response = urllib2.urlopen(imdbLink)
    webContent = response.read()
    
    bs = BeautifulSoup(webContent)
    tables = bs.findAll(lambda tag: tag.name=='table' and tag.has_key('class') and tag['class']=="simpleTable simpleCreditsTable") 
    writers = tables[1].findAll(lambda tag: tag.name=='a' and tag.has_key('href'))
    
    writer_list = []
    for writer in writers: 
        cols = writer.text.split(" ")
        writer_list.append(cols[-1])

    return writer_list

def findImdbUrl(movie_title, movie_writer):
    
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    
    link = "http://www.imdb.com/find?q=" + urllib.quote(movie_title) + "&s=all"
    session.visit(link)
    response = session.body()
    
    soup = BeautifulSoup(response)
    div = soup.find(lambda tag: tag.name=='div' and tag.has_key('class') and tag['class']=='findSection')
    if (div):
        div_content = "".join([unicode(x) for x in div.contents]) 
        
        title_search = re.compile('/title/tt\d+')
        search_results = re.findall(title_search, div_content)
        
        for movie_url in search_results:
            try:
                names = extractPeopleBehind("http://www.imdb.com" + movie_url + "/")
                if not set(movie_writer).isdisjoint(names):
                    return "http://www.imdb.com" + movie_url + "/"
            
                #soup_search = BeautifulSoup(resp_search)
                #people_behind = soup_search.findall(lambda tag: tag.name=='div' and tag.has_key('class') and tag['class']=='credit_summary_item')
                #for people in people_behind: print people.text
            except:
                pass
    
    return None    

def innerHTML(element):
    return element.decode_contents(formatter="html")

def listMovieScripts():
    dryscrape.start_xvfb()
    session = dryscrape.Session()
    
    imsdbLink = "http://www.imsdb.com/all scripts/"
    session.visit(imsdbLink)
    webContent = session.body()
    
    bs = BeautifulSoup(webContent)
    movies = bs.findAll(lambda tag: tag.name=='p')

    links = {}
    writers = {}
    
    for movie in movies:
        #<p><a href="/Movie Scripts/Boyhood Script.html" title="Boyhood Script">Boyhood</a> (Undated Draft)<br><i>Written by Richard Linklater</i><br></p>
        movie_title = movie.find(lambda tag: tag.name=='a').text
        if (movie_title.endswith(", The")): movie_title = "The " + movie_title.replace(", The", "")

        movie_url = "http://www.imsdb.com" + urllib.quote(movie.find(lambda tag: tag.name=='a').get("href"))
        
        movie_writer = movie.find(lambda tag: tag.name=='i').text
        movie_writer = movie_writer.replace("Written by ", "")
        movie_writer_list = getlastNames(movie_writer.split(","))

        #print movie_title, movie_url, movie_writer_list
        links[movie_title] = movie_url
        writers[movie_title] = movie_writer_list
        
    	return (links, writers)		

def listMovies():
    
    #outlist = open("sparknotes_urls_imdb.csv", "w")
    outlist = open("sparknotes_urls_imdb_imsdb.csv", "w")
    
    spark = open("sparknotes_urls.csv", "r")

    (imsdb_links, imsdb_writers) = listMovieScripts()
    
    for line in spark.readlines():
        if (line.strip() != ""):
            cols = line.strip().split(",")
            movie_title = cols[0]
            movie_writer = cols[1]
            movie_writer_list = getlastNames([cols[1]])
            spark_url = cols[2]
            
            print movie_title
            imdb_url = findImdbUrl(movie_title, movie_writer_list)
            if (not imdb_url): imdb_url = ""

            imsdb_url = ""
            if (movie_title in imsdb_links): imsdb_url = imsdb_links[movie_title]

            outlist.write(movie_title + "," + movie_writer + "," + spark_url + "," + imdb_url + "," + imsdb_url + "\n")
            
    outlist.close()
    spark.close()

def main():
    listMovies()
    
    #names = extractPeopleBehind("http://www.imdb.com/title/tt0147800/")
    #print names

if __name__ == "__main__":
    #python extractImsdb.py [output dir]
    main()

