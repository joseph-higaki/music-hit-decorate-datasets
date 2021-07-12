import requests
import requests_oauthlib
from requests_oauthlib import OAuth1Session 
import xml.etree.ElementTree as ElementTree
import time

sleep_time_before_request = 2.5

class MusicStoryArtist:    
    def __init__(self):
        self.id = ""
        self.spotify_artist_id = ""    
        self.instagram_url = ""
        self.instagram_username = ""
        self.facebook_url = ""
        self.facebook_username = ""
        self.twitter_url = ""
        self.twitter_username = ""
    

class MusicStory:
    base_url = 'http://api.music-story.com/en/'
    def __init__(self, client_key, client_secret, resource_owner_key, resource_owner_secret):        
        self._session = OAuth1Session(client_key, client_secret, resource_owner_key, resource_owner_secret)        

    @staticmethod
    def _dummy_artist_by_spotify_id_response():
        #open saved music artist by spotify response
        text_file = open("response_6LuN9FCkKOj5PcnpouEgny.txt", "r")
        response_text = text_file.read()
        text_file.close()
        return response_text

    @staticmethod
    def _dummy_instagram_response():
        #open response instagram
        text_file_instagram = open("response_instagram_172321.txt", "r")
        response_instagram_text = text_file_instagram.read()
        text_file_instagram.close()
        return response_instagram_text

    def _get_music_story_response_id(self, method_url, id):    
        ## returns XML document
        url = MusicStory.base_url + method_url.format(id)
        time.sleep(sleep_time_before_request)
        response = self._session.get(url)
        return response.text 
        
    def _get_music_story_artist_by_spotify_artist_id(self, spotify_artist_id):        
        ## returns XML document
        return self._get_music_story_response_id("spotify/{}/artist", spotify_artist_id)
        #return MusicStory._dummy_artist_by_spotify_id_response()

    def get_music_story_instagram_by_id(self, id):
        ## returns XML document
        return self._get_music_story_response_id("artist/{}/instagram", id)  
        #return MusicStory._dummy_instagram_response()
        
    @staticmethod 
    def _extract_music_story_data_item(
        xml_document_text
        ):
        ## returns XML array from data item array
        root = ElementTree.fromstring(xml_document_text)   
        #print(root)
        return_value = root.findall("data/item")
        #print(return_value)
        return return_value

    @staticmethod 
    def _extract_music_story_data_item_first_node_value(
        xml_document_text,
        node_name
        ):
        ## returns first node from XML array from data item array
        node_value = ""
        try:        
            music_story_entries = MusicStory._extract_music_story_data_item(xml_document_text)
            #print(music_story_entries)
            node_value = music_story_entries[0].find(node_name).text
        except:
            node_value = ""   
        #print(node_value)
        return node_value

    @staticmethod 
    def _extract_music_story_artist_id(
        xml_document_text
        ):        
        # Extract URL value from MusicStory response XML document
        return MusicStory._extract_music_story_data_item_first_node_value(xml_document_text, "id")

    @staticmethod 
    def _extract_music_story_artist_url(
        xml_document_text
        ):
        # Extract URL value from MusicStory response XML document
        return MusicStory._extract_music_story_data_item_first_node_value(xml_document_text, "url")

    @staticmethod     
    def _extract_username_from_site_url(site_url):
        # Extract first path element after"*.com" like url. Can be used to extract instagram username
        return site_url.rsplit('.com/', 1)[-1].rstrip("/")

    def get_music_story_artist(self, spotify_artist_id):
        # Queries the Music Story Artist using Spotify artist id
        # Adds the artist instagram url and username, according to the Music-Story database
        # Returns a Music Story Artist object
        # TO-DO: extract facebook, twitter and wikimedia links
        music_story_artist = MusicStoryArtist()        
        music_story_artist.id = MusicStory._extract_music_story_artist_id(
            self._get_music_story_artist_by_spotify_artist_id(spotify_artist_id = spotify_artist_id))
        instagram_response = self.get_music_story_instagram_by_id(music_story_artist.id)
        music_story_artist.instagram_url = MusicStory._extract_music_story_artist_url(instagram_response)
        music_story_artist.instagram_username = MusicStory._extract_username_from_site_url(music_story_artist.instagram_url)
        return music_story_artist
        