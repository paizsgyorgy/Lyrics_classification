# Lyrics classification
**A customised command-line interface with a lyrics downloader and a Naive Bayes lyrics classification module that is capable of telling the user which artist the user input most likely belongs to.**
<br></br>
## Usage (WARNING: this program has not been extensively tested):

1. Git clone this repository to your computer to get started

```git clone https://github.com/paizsgyorgy/Lyrics_classification.git```

2. Install all required Python packages

```pip install -r requirements.txt```

3. Launch the LyricsSearch.py in your bash command line to search for lyrics

```python LyricsSearch.py```


*The program uses a simple .csv file as its database and only downloads lyrics if not already available*

4. Launch the LyricsClassifier.py if you want your input to be classified according

```python LyricsClassifier.py```


## Methodology
* BeautifulSoup used for scraping lyrics from lyrics.com
* Spacy used for classifying custom user input into an artist category
