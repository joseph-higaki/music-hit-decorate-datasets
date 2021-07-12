# Instagram / Music Story - Decorate Datasets

This is a Python console program that fetches data from [Instagram](https://www.instagram.com/) and [Music Story](https://www.music-story.com/).

This program's purpose is to add artists' social media information into the datasets that we will use to predict a [Spotify](https://www.spotify.com/) song popularity, primarily based on its [audio features](https://developer.spotify.com/documentation/web-api/reference/#endpoint-get-audio-features).

Using Machine Learning Models to predict a song's popularity, is a [group](#team) project from the Data Science and Advanced Analytics course from the Big Data &amp; Analytics Masters @ [EAE](https://www.eae.es/) class of 2021.

## Usage
Console has three main purposes
for examples on how to use them, see console.out

### Search Music Story Entity & Instagram URL by Spotify Artist ID
``` python
 MODE_SEARCH_IG_PROFILE_BY_NAME 
```

### Get Instagram profile and followers using instagram username as input
``` python
 MODE_SEARCH_IG_FOLLLOWERS_BY_IG_USERNAME 
```
Previous Step #1 resulted in: music_story_enriched_artist_<timestamp>.csv
At first, the design we wanted was one, where we link one step to another
Thus, the functions return the filename. We could link them thru command line pipes
In between steps we need to exclude found records and allow the next step to complete the missing ones

### Search Instagram profile and followers using artist name as input
``` python
MODE_SEARCH_IG_FOLLLOWERS_BY_ARTIST_NAME 
```
Previous Step #2 resulted in: instagram_enriched_artist_<timestamp>.csv
This was also thought to pipe/link it to the final name search.
In between steps we need to exclude found records and allow the next step to complete the missing ones
THis way we are more efficient, only doing name based searches on not fount artists.
But, we realized that even after music story had returned the artist entity
this one, may be a fan account, not the real one
that is why, we have manual intervention between one step to another
decorate_instagram_followers_artist_based_on_name_search "instagram_enriched_artist"
  MS: stands for Music Story Search
  IS: stands for INstagram Name Search
We had to run several manual searches and join them together because:
       * Instagram requests lock out limit
       * Found artists at ig, were not considered if follow count was < 2k. We didn't automate this logic

### Prepare test dataset using Spotify playlist as input
``` python
MODE_PRODUCE_TEST_DATASET_BY_PLAYLIST
```
Taking as input a spotify playlist id, this option will iterate through the list
* add spotify audio features
* add instagram followers 
* save playlist items at a csv

## Team
(music-hit-decorate-datasets/music-hit-analyze-data/music-hit-train-predict)
* [Henrique Avila](https://www.linkedin.com/in/henrique-avila-101170a0/) 
* [Joseph Higaki](https://www.linkedin.com/in/josephhigaki/) ([GitHub](https://github.com/joseph-higaki/))
* [Raquel Ganuza](https://www.linkedin.com/in/raquel-ganuza-catal%C3%A1n/)
* [Romain Baleynaud](https://www.linkedin.com/in/romain-baleynaud/) ([GitHub](https://github.com/RomainBal)) 
* [Ziyad Ashukri](https://www.linkedin.com/in/ziyadashukri/)

# Professor
* **[Marta Tolós](https://www.linkedin.com/in/martatolos/)**
 
**Professor Assistants**
* [Pere Miquel Brull Borràs](https://www.linkedin.com/in/pmbrull/)
* [Alberto Villa](https://www.linkedin.com/in/avillam/)


## To-Do list 
The: "I didn't do cause we needed to submit this ASAP"
[] Have two different consoles, to separate concerns: Instagram / Music Story
[] Package them like a hero
[] A better (or one at least) pause/halt/fail - resume mechanism. Useful when APIs timeout on too many requests.
[] Explore other services the music story database provided. Such as artists' tweets, lyrics 

