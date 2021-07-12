import pandas 
from datetime import datetime
import music_story
import instagram
import config

#we're iterating 1K + datasets and sometimes the api blocks us out or the network connection fails
# saving to disk, every K iteration, allows us to pause/resume. At least manually
# this is used at the instagram BY NAME search, as instagram blocks us out
# and we're doing several requests per artist at our list
save_on_every_n_iter = 6

# this is used for testing purposes
# If max_artist_csv_iteration = 0, 
#       then we will iterate the entire artist csv input
# If max_artist_csv_iteration > 0, 
#       then we will iterate the first max_artist_csv_iteration from the artist csv input
max_artist_csv_iteration = 5

music_story_enriched_artist_columns = [
    "index",
    "spotify_artist_id", 
    "list_original_name", 
    "music_story_id",
    "instagram_url",
    "instagram_username",
    "facebook_url",
    "facebook_username",
    "twitter_url",
    "twitter_username"]

instagram_enriched_artist_columns = [
    "index",
    "spotify_artist_id", 
    "list_original_name", 
    "music_story_id",
    "instagram_url",
    "instagram_username",
    "facebook_url",
    "facebook_username",
    "twitter_url",
    "twitter_username",
    "instagram_followers",
    "instagram_data"]

instagram_search_results_by_name_columns = [
  "name_search",
  "instagram_name",
  "instagram_username",
  "instagram_url",
  "followers"
]


def read_csv_artist_list(filename_csv):      
  return pandas.read_csv(filename_csv, quotechar="\"")

def write_artist_csv_enriched(filename_prefix, enriched_artist_array, columns): 
    timestamped_filename_csv = "{0}{1}.csv".format(filename_prefix, datetime.now().strftime("%Y-%m-%d_%H%M%S%f"))
    enriched = pandas.DataFrame(enriched_artist_array, columns = columns)
    enriched.to_csv(timestamped_filename_csv)    
    return timestamped_filename_csv

def write_music_story_enriched_artist( 
    enriched_artist_array):          
    return write_artist_csv_enriched("music_story_enriched_artist", enriched_artist_array, music_story_enriched_artist_columns)

def write_instagram_enriched_artist( 
    enriched_artist_array):          
    return write_artist_csv_enriched("instagram_enriched_artist", enriched_artist_array, instagram_enriched_artist_columns)

def write_instagram_search_results_by_name( 
    enriched_artist_array):          
    return write_artist_csv_enriched("instagram_search_results_by_name", enriched_artist_array, instagram_search_results_by_name_columns)

# iterates an artist list, and gets music story entity, using the spotify artist id
def decorate_music_story_artist(filename = "spotify_artists.csv"):
  return_value_csv_file = ""
  spotify_artists_csv = read_csv_artist_list(filename)
  iterating_list = spotify_artists_csv.values
  if max_artist_csv_iteration:
    iterating_list = spotify_artists_csv.head(max_artist_csv_iteration).values

  enriched_artists = []
  index = 0
  music_story_loader = music_story.MusicStory( config.get_config("music_story_consumer_key"), #consumer key
                                  client_secret = config.get_config("music_story_consumer_secret"), #consumer secret
                                  resource_owner_key =  config.get_config("music_story_access_token"), #access token
                                  resource_owner_secret = config.get_config("music_story_token_secret")) #token secret
  try:      
      for artist in iterating_list:        
          index += 1
          spotify_artist_id = artist[0]        
          list_original_name = artist[1]
          music_story_artist = music_story_loader.get_music_story_artist(spotify_artist_id = spotify_artist_id)
          music_story_id = music_story_artist.id
          instagram_url = music_story_artist.instagram_url #"http://www.instagram.com/thegr8khalid"
          instagram_username = music_story_artist.instagram_username #  extract_instagram_username_from_url(instagram_url)
          facebook_url = ""
          facebook_username = ""
          twitter_url = ""
          twitter_username = ""          
          enriched_artists.append([index, spotify_artist_id, list_original_name, music_story_id, instagram_url, instagram_username, facebook_url, facebook_username, twitter_url, twitter_username])
          print("music_story_enrichment{0}".format(index))
  finally:
    return_value_csv_file = write_music_story_enriched_artist(enriched_artists)
  return return_value_csv_file


# It grabs a CSV and iterates the list invoking instagram based on instagram username
def decorate_instagram_followers_artist_based_on_username(artist_csv):
  return_value_csv_file = ""
  artists_csv = read_csv_artist_list(artist_csv)
  iterating_list = artists_csv.values
  if max_artist_csv_iteration:
    iterating_list = artists_csv.head(max_artist_csv_iteration).values

  enriched_artists = []
  index = 0
  instagram_user = config.get_config("instagram_user")
  instagram_password = config.get_config("instagram_password")
  instagram_client = instagram.Instagram(instagram_user, instagram_password)
  try:    
    for artist in iterating_list:
      index0 = artist[0]
      index1 = artist[1]
      spotify_artist_id = artist[2]
      list_original_name = artist[3]
      music_story_id = artist[4]
      instagram_url =  artist[5]
      instagram_username =  artist[6]
      facebook_url =  artist[7]
      facebook_username =  artist[8]
      twitter_url =  artist[9]
      twitter_username =  artist[10]
      instagram_artist = instagram_client.get_artist(instagram_username)    
      instagram_followers = instagram_artist.followers
      instagram_data = instagram_artist.data
      #print(instagram_artist.data)
      enriched_artists.append([index1, spotify_artist_id, list_original_name, music_story_id, instagram_url, instagram_username, facebook_url, facebook_username, twitter_url, twitter_username, instagram_followers, instagram_data])
      print("decorate_instagram_followers_artist_based_on_music_story_{0}".format(index1))
  finally:
    return_value_csv_file = write_instagram_enriched_artist(enriched_artists)
  return return_value_csv_file

# It grabs a CSV and iterates the list invoking instagram based on artist name,
# it will record artist with most followers on the list
# also, will record a list of values from instagram search results for each artist name
def decorate_instagram_followers_artist_based_on_name_search(artist_csv):
  return_value_csv_file = ""
  artists_csv = read_csv_artist_list(artist_csv)
  iterating_list = artists_csv.values
  if max_artist_csv_iteration:
    iterating_list = artists_csv.head(max_artist_csv_iteration).values

  enriched_artists = []
  # initialize the object that will have name search criteria + InstagramArrtist object attributes
  instagram_artist_name_matches = []
  
  index = 0
  instagram_user = config.get_config("instagram_user")
  instagram_password = config.get_config("instagram_password")
  instagram_client = instagram.Instagram(instagram_user, instagram_password)
  try:    
    for artist in iterating_list:
      index += 1
      index0 = artist[0]
      index1 = artist[1]
      spotify_artist_id = artist[2]
      list_original_name = artist[3]
      music_story_id = artist[4]
      instagram_url =  artist[5]
      instagram_username =  artist[6]
      facebook_url =  artist[7]
      facebook_username =  artist[8]
      twitter_url =  artist[9]
      twitter_username =  artist[10]

      instagram_artist_search_result = instagram_client.get_artist_by_name(list_original_name)
      # all instagram profiles that matched the name search              
      for instagram_artist_name_match in instagram_artist_search_result[1]:
          # needs to match column order from: instagram_search_results_by_name_columns        
          instagram_artist_name_matches.append([list_original_name, 
              instagram_artist_name_match.name, 
              instagram_artist_name_match.username, 
              instagram_artist_name_match.get_url(), 
              instagram_artist_name_match.followers])

      #record proposed result, the one with most followers
      instagram_artist = instagram_artist_search_result[0]
      instagram_username = instagram_artist.username
      instagram_url = instagram_artist.get_url()
      instagram_followers = instagram_artist.followers
      instagram_data = instagram_artist.data
      #print(instagram_artist.data)
      enriched_artists.append([index1, spotify_artist_id, list_original_name, music_story_id, instagram_url, instagram_username, facebook_url, facebook_username, twitter_url, twitter_username, instagram_followers, instagram_data])
      print("decorate_instagram_followers_artist_based_on_name_search {0} - {1} - {2} - {3}".format(index, index1, instagram_username, instagram_followers))

      if (index % save_on_every_n_iter == 0):      
        return_value_csv_file = write_instagram_enriched_artist(enriched_artists)
        write_instagram_search_results_by_name(instagram_artist_name_matches)              
        print("decorate_instagram_followers_artist_based_on_name_search - preventive save - iter:{0} - row:{1}  | filename {2}".format(index, index1, return_value_csv_file))
  finally:
    return_value_csv_file = write_instagram_enriched_artist(enriched_artists)
    write_instagram_search_results_by_name(instagram_artist_name_matches)      
  return return_value_csv_file


#MODE_SEARCH_IG_PROFILE_BY_NAME 1
#decorate_music_story_artist("spotify_artists.csv")

#MODE_SEARCH_IG_FOLLLOWERS_BY_IG_USERNAME 2
# Previous Step #1 resulted in: music_story_enriched_artist_<timestamp>.csv
# At first, the design we wanted was one, where we link one step to another
# Thus, the functions return the filename. We could link them thru command line pipes
# In between steps we need to exclude found records and allow the next step to complete the missing ones
#decorate_instagram_followers_artist_based_on_username("music_story_enriched_artist.csv")

#MODE_SEARCH_IG_FOLLLOWERS_BY_ARTIST_NAME 3
# Previous Step #2 resulted in: instagram_enriched_artist_<timestamp>.csv
# This was also thought to pipe/link it to the final name search.
# In between steps we need to exclude found records and allow the next step to complete the missing ones
# THis way we are more efficient, only doing name based searches on not fount artists.
# But, we realized that even after music story had returned the artist entity
# this one, may be a fan account, not the real one
# that is why, we have manual intervention between one step to another
# decorate_instagram_followers_artist_based_on_name_search "instagram_enriched_artist"
# MS: stands for Music Story Search
# IS: stands for INstagram Name Search
# We had to run several manual searches and join them together because:
#       * Instagram requests lock out limit
#       * Found artists at ig, were not considered if follow count was < 2k. We didn't automate this logic
#decorate_instagram_followers_artist_based_on_name_search("UNION MSI01-IS01-IS02 - Not Found - Duplicates Removed.csv")



