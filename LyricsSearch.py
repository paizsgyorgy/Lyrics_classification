### Load necessary packages for the program to run
import requests
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
import numpy as np
import re
import os
from tqdm import tqdm

### Create user defined function for scraping lyrics
def get_lyrics(urls):
    """
    This function takes a urls from an artist on Lyrics.com and outputs a dataframe including all its songs lyrics
    """
 
    ## Download all the lyrics for all the songs listed from the artist
    lyrics = []

    ## For loop including a tqdm progress bar (super cool!)
    for i in tqdm(urls):
        url = 'https://www.lyrics.com' + i
        try:
            html = requests.get(url)
            page = soup(html.text, 'html.parser')
            try:
                refined_text = page.find_all(attrs={'class':'lyric-body'})
                lyrics.append(refined_text[0].text)
            except:
                lyrics.append(np.NaN)
        except:
            pass
        time.sleep(1)

    ## Create a dataframe out of the three lists

    df = pd.DataFrame({'URL':['https://www.lyrics.com' + i for i in urls],'Title':titles, 'Lyrics': lyrics})

    return df


### Initiate user search and prompt user for input
user_search = input('What do you want to search for?')

### Strip user input and replace user input whitespaces with '%20' that is used as space on Lyrics.com
user_search = user_search.strip()
user_search = re.sub('( ){1,}', '%20', user_search)
user_search = user_search.lower()

### Create link to be used for going to search results site on Lyrics.com
searchlink = 'https://www.lyrics.com/lyrics/' + user_search

### Parse the website with beautifulsoup
html = requests.get(searchlink)
searchpage = soup(html.text, 'html.parser')

a = searchpage.find_all('a')

artist_urls = []
artist_names = []

for i in a:
    if 'artist/' in i.get('href'):
        artist_urls.append('https://www.lyrics.com/' + i.get('href'))
        artist_names.append(i.get('title'))

## Create options dataframe (there are duplicates and we want to select only the first nine occurances)
artist_opts = pd.DataFrame({'URL':artist_urls[0:18:2],'Name':artist_names[0:18:2]})

## Print out each element in my artist_names list for the user to choose from
print()
print('The following artists were found on Lyrics.com for your search:')
for i, name in enumerate(artist_opts['Name']):
    print(str(i+1) + ') ' + str(name))

print()

## Prompt user for input and confirm the input of the user is among the listed options
while True:
    try:
        user_selection = input('Please type the number of the artist you want to load lyrics from: ')
        if int(user_selection) in list((artist_opts.index.values + 1)):
            break
        else:
            raise ValueError
    except ValueError:
        print("Not a valid option! Please try again ...")
        
### Print an empty line and then the user selected artist name
print()
print(f'Great, I will search lyrics for {artist_opts.iloc[int(user_selection)-1, 1]}')

### Save selected artist url in artist_url variable
artist_url = artist_opts.iloc[int(user_selection)-1, 0]

## Download artist website under url
html = requests.get(artist_url)

## Parse the HTML site with BeautifulSoup
urls_page = soup(html.text, 'html.parser')

## Extract all tags with 'a' from the parsed through html file
a = urls_page.find_all('a')

## Get all the URLs and titles for the artists' songs on Lyrics.com
urls = []
titles = []
for i in a:
    if '/lyric/' in i.get('href'):
        urls.append(i.get('href'))
        titles.append(i.get_text())

### Estimate time it will take to load all lyrics and confirm with user
est = len(urls) * 3
est_min = est // 60
est_sec = est % 60
print()
print(f'It will take approximately {est_min} minutes {est_sec} seconds to load all {len(urls)} songs from this artist.')
print()

while True:
    try:
        confirm = input('Do you want to continue? (Y/N)')
        if confirm in ['Y','N']:
            break
        else:
            raise ValueError
    except ValueError:
        print("Not a valid option! Please try again with Y or N...")

if confirm == 'N':
    print('Okay then, quitting the program...')
    quit()

else:  
    ### Run the user defined function that scrapes the website for lyrics and puts it into a dataframe
    ### A tqdm progress bar is included in the defined function above
    lyrics = get_lyrics(urls)

    ### Print message
    print()
    print('All lyrics loaded into dataframe.')

    ### Strip down the artist name to be used for filename
    string = artist_opts.iloc[int(user_selection)-1, 1]
    artist_shortened = ''.join(e for e in string if e.isalnum())

    ### Write out dataframe to a csv output file
    filename = f'{artist_shortened}_lyrics.csv'
    lyrics.to_csv(filename)

    dirpath = os.getcwd()
    filepath = dirpath + '/' + filename

    ### Print message
    print()
    print(f'CSV file created with all lyrics for artist {string}.')
    print(f'The file is saved in the following location:  {filepath}')
    print()