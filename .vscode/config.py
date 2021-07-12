# When we're as cool as JLo, we will get this from a secret's file
# for now, we'll probably just .gitignore this
def get_config(key):
    __config_settings = {
        "instagram_user": "josephs.not.my.username",
        "instagram_password": "notmypasswEither",

        "spotify_client_id": "<spotify_client_id>",
        "spotify_client_secret": "<spotify_client_secret>",

        "music_story_consumer_key": "<music_story_consumer_key>",
        "music_story_consumer_secret": "<music_story_consumer_secret>",
        "music_story_access_token": "<music_story_access_token>",
        "music_story_token_secret": "<music_story_token_secret>"
    }
    return __config_settings[key]
