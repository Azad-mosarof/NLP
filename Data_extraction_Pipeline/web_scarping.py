import requests
import bs4
import pandas as pd
from pandas import Series, DataFrame
from ipywidgets import FloatProgress
from time import sleep
from IPython.display import display
import re
import pickle

url = 'http://www.imdb.com/chart/top?ref_=nv_mv_250_6'

result = requests.get(url)
c = result.content
soup = bs4.BeautifulSoup(c, 'lxml')

summary = soup.find('div', {'class':'article'})

movieName = []
cast = []
description = []
rating = []
ratingOutOf = []
year = []
genre = []
director = []


rgx = re.compile('[%s]' % '()')
f = FloatProgress(min=0, max=250)
display(f)
for row,i in zip(summary.find('table').
    findAll('tr'), range(len(summary.find('table').findAll('tr')))):
        for sitem in row.findAll('span', {'class':'secondaryInfo'}):
            s = sitem.find(text=True)
            year.append(rgx.sub("",s))

        for ritem in row.findAll('td', {'class':'ratingColumn imdbRating'}):
            for iget in ritem.findAll('strong'):
                rating.append(iget.find(text=True))
                ratingOutOf.append(iget.get('title').split(' ',4)[3])

        for ritem in row.findAll('td', {'class':'titleColumn'}):
            for href in ritem.findAll('a', href=True):
                movieName.append(href.find(text=True))
                cast.append(href.get('title'))
                rurl = 'https://www.rottentomatoes.com/m/'+ href.find(text=True)
                try:
                    rresult = requests.get(rurl)
                except requests.exceptions.ConnectionError:
                    status_code = "Connection refused"
                rc = rresult.content
                rsoup = bs4.BeautifulSoup(rc, 'lxml')
                try:
                    m_info = rsoup.find('div', {'class':'panel-body content_body'})
                    genre.append(m_info.find('div', {'class':'meta-value genre'}).find(text=True))
                    director.append(m_info.find('a', {'data-qa':'movie-info-director'}).find(text=True))
                    description.append(m_info.find('div', {'class':'movie_synopsis clamp clamp-6 js-clamp'}).find(text=True))
                except:
                    genre.append("")
                    description.append("")
                    director.append("")
        if(i == 10):
            break


# with open('movieb.txt', '+a') as fileHandler:
#     for i in range(len(movieName)):
#         fileHandler.write("Movie name: %s\n" % movieName[i])
#         fileHandler.write("Description: %s\n" % description[i])
#         fileHandler.write("Genre: %s\n" % genre[i])
#         fileHandler.write("Cast: %s\n" % cast[i])
#         fileHandler.write("Director: %s\n" % director[i])
#         fileHandler.write("Year: %s\n" % year[i])
#         fileHandler.write("Rating: %s\n" % rating[i])
#         fileHandler.write("Rating Out Of: %s\n" % ratingOutOf[i])
#         fileHandler.write("\n")

movieName = Series(movieName)
cast = Series(cast)
description = Series(description)
genre = Series(genre)
director = Series(director)
year = Series(year)
rating = Series(rating)
ratingOutOf = Series(ratingOutOf)

imdb_df = pd.concat([movieName,cast,description,genre,director,year,rating,ratingOutOf], axis=1)
imdb_df.columns = ['movie_name', 'cast', 'description', 'genre', 'director', 'year', 'rating', 'rating_out_of']
imdb_df['rank'] = imdb_df.index + 1 
imdb_df.to_csv('imdbReport.csv')

