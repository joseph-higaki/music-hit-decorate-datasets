import instaloader
import time

# #of seconds to wait before instagram requests 
sleep_time_before_request = 8
# # of records to iterate to find max follower count at instagram search results
max_top_search_results = 1

class InstagramArtist:
    # This is just a POJO to exchange the relevant instagram artist information around our functions
    # or should I say POPO (Plain Old Python Object)
    def __init__(self, data = "", name = "", username = "", followers = -1):
        self.data = data
        self.name = name
        self.username = username
        self.followers = followers

    def get_url(self):        
        return "https://www.instagram.com/" + self.username if self.username else ""

class Instagram:
    # This will be the instaloaer wrapper to hide some of its complexity and include some business rules 
    def __init__(self, user, password):
        # Keeps user session alive through this object lifecycle
        self.loader = instaloader.Instaloader()        
        time.sleep(sleep_time_before_request)
        self.loader.login(user, password)

    def get_artist(self, instgram_handler):
        return_value_artist = InstagramArtist()
        try:
            if instgram_handler:
                time.sleep(sleep_time_before_request)
                profile = instaloader.Profile.from_username(self.loader.context, instgram_handler)                
                return_value_artist.data = profile._node
                return_value_artist.followers = profile.followers
        except:
            #silent error, I'm deeply sorry I'm on a rush
            pass
        return return_value_artist


    def get_artist_search(self, search_string):
        # returns Instagram profile iterator  
        top_search_results = instaloader.TopSearchResults(self.loader.context, search_string)      
        return top_search_results.get_profiles()


    def get_artist_by_name(self, artist_name):
        # returns 2 results
        # 0:  the artist having most followers from the array
        # 1:  the list of search results from name criteria
        return_value_artist = InstagramArtist()
        return_value_artist_name_search_results = []
        try:
            if artist_name:
                time.sleep(sleep_time_before_request)
                profiles = self.get_artist_search(artist_name)
                top_result_count = 1
                for profile in profiles:
                    time.sleep(sleep_time_before_request)
                    iteratingArtist = InstagramArtist(profile._node, profile.full_name, profile.username, profile.followers)
                    return_value_artist_name_search_results.append(iteratingArtist)
                    if (iteratingArtist.followers > return_value_artist.followers):
                        return_value_artist = iteratingArtist
                    # This iterator will call N times (search results) the ig website and eventually locks my account out
                    # I'm hoping first results are the more relevant ones, just iterating TOP K results 
                    top_result_count += 1
                    if top_result_count > max_top_search_results:
                        break
        except:
            #silent error, I'm deeply sorry I'm on a rush
            pass
        return [return_value_artist, return_value_artist_name_search_results]

      
