class ProfileJoseph:
  def __init__(self, name, username, followers):
      self.name = name
      self.username = username
      self.followers = followers

profiles = [
    ProfileJoseph("Imagine Dragons", "imaginedragons", 5027239),
    ProfileJoseph("Imagine.dragons.esp", "imagine.dragons.esp", 2919),
    ProfileJoseph("magine Dragons BR", "imaginedragons2m", 175)]
    
# profiles = [
#     {name: "Imagine Dragons",
#     username: "imaginedragons",
#     followers: 5027239},
#     {name: "Imagine.dragons.esp",
#     username: "imagine.dragons.esp",
#     followers: 2919},
#     {name: "magine Dragons BR",
#     username: "imaginedragons2m",
#     followers: 175}
# ]

#for p in profiles: 
#    print(p.name + " " + p.username + " " + str(p.followers)) 

#Imagine Dragons imaginedragons 5027239
#Imagine.dragons.esp imagine.dragons.esp 2919
#imagine Dragons BR imaginedragons2m 175

import decorate_artist_list

# this is used for testing purposes
# If max_artist_csv_iteration = 0, 
#       then we will iterate the entire artist csv input
# If max_artist_csv_iteration > 0, 
#       then we will iterate the first max_artist_csv_iteration from the artist csv input
max_artist_csv_iteration = 0

artists_csv = decorate_artist_list.read_csv_artist_list("spotify_artists.csv")

iterating_list = artists_csv.values
if max_artist_csv_iteration:
    iterating_list = artists_csv.head(max_artist_csv_iteration).values
for artist in iterating_list:
    print(artist[1])