import os
import sys
import re
import urllib, urllib2
import dryscrape
from BeautifulSoup import BeautifulSoup
import time

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

    outlist = open("imsdb_urls_imdb.csv", "w")

    for movie in movies:
        #<p><a href="/Movie Scripts/Boyhood Script.html" title="Boyhood Script">Boyhood</a> (Undated Draft)<br><i>Written by Richard Linklater</i><br></p>
        movie_title = movie.find(lambda tag: tag.name=='a').text
        if (movie_title.endswith(", The")): movie_title = "The " + movie_title.replace(", The", "")

        print movie_title

        movie_url = "http://www.imsdb.com" + urllib.quote(movie.find(lambda tag: tag.name=='a').get("href"))
        
        movie_writer = movie.find(lambda tag: tag.name=='i').text
        movie_writer = movie_writer.replace("Written by ", "")
        movie_writer_list = getlastNames(movie_writer.split(","))

        dir_scripts = "Imsdb_scripts/"
        ensure_dir(dir_scripts)

        session.visit(movie_url)
        response = session.body()
        m = re.search(r'<a href="?\'?(/scripts/[^"\'>]*)', response)
        if m:
        	filename = m.group(1)

        	if filename.endswith(".html"):

        		outscript = open(dir_scripts + movie_title.replace(" ", "_") + ".txt", "w")            
                imsdb_url = "http://www.imsdb.com" + m.group(1)

                session.visit(imsdb_url)
                response = session.body()            
                pre = re.search(r'<pre>(.*?)</pre>', response, re.DOTALL)
            
                if pre:
                    script = pre.group(1)
                    #print re.search(r'<script>(.*?)<pre>', script, re.DOTALL)
                    rem = re.compile(r'<script>(.*?)<pre>', re.DOTALL)
                    rem2 = re.compile(r'<title>(.*?)<pre>', re.DOTALL)
                    rem3 = re.compile(r'<b>\s+\.*\d*\.*\s*</b>', re.MULTILINE)
                    script = re.sub(rem, '', script)
                    script = re.sub(rem2, '', script)
                    script = re.sub(rem3, '\n', script)
                
                    outscript.write(script.encode('utf8'))
                    outscript.close()

                    imdb_url = findImdbUrl(movie_title, movie_writer_list)
                    if (not imdb_url): imdb_url = ""

                    outlist.write(movie_title + "," + movie_writer + "," + imsdb_url + "," + imdb_url + "," + imsdb_url + "\n")

        time.sleep(60)

    outlist.close()

def main():
    listMovieScripts()
    
    #names = extractPeopleBehind("http://www.imdb.com/title/tt0147800/")
    #print names

if __name__ == "__main__":
    #python extractImsdb.py [output dir]
    main()

