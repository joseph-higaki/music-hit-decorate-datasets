import pandas 
from datetime import datetime
import music_story
import instagram
import config

instagram_user = config.get_config("instagram_user")
instagram_password = config.get_config("instagram_password")
instagram_client = instagram.Instagram(instagram_user, instagram_password)
profiles = instagram_client.get_artist_search("Imagine Dragons")
for p in profiles:

    print(p.full_name + " " + p.username + " " + str(p.followers))
    

#print(count(profiles))
#print(profiles)
#print(profiles[0]._node)


