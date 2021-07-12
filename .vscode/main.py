import sys
import decorate_artist_list
import produce_test_dataset


#Modes accepted 
MODE_SEARCH_IG_PROFILE_BY_ARTIST_NAME_MUSIC_STORY = "MODE_SEARCH_IG_PROFILE_BY_ARTIST_NAME_MUSIC_STORY"
MODE_SEARCH_IG_FOLLLOWERS_BY_IG_USERNAME = "MODE_SEARCH_IG_FOLLLOWERS_BY_IG_USERNAME"
MODE_SEARCH_IG_FOLLLOWERS_BY_ARTIST_NAME = "MODE_SEARCH_IG_FOLLLOWERS_BY_ARTIST_NAME"
MODE_PRODUCE_TEST_DATASET_BY_PLAYLIST = "MODE_PRODUCE_TEST_DATASET_BY_PLAYLIST"

def main():
    message = ""
    arguments = sys.argv[1:]
    print(arguments)
    if len(arguments) < 2:
        message = "mode and input file needed"
        print(message)
        return message

    mode = arguments[0]
    input_filename = arguments[1]

    if mode == MODE_SEARCH_IG_PROFILE_BY_ARTIST_NAME_MUSIC_STORY:
        print(f"calle funtion : {mode} with param file {input_filename}")
        #input_filename = "spotify_artists.csv"
        return decorate_artist_list.decorate_music_story_artist(input_filename)
    elif mode == MODE_SEARCH_IG_FOLLLOWERS_BY_IG_USERNAME:
        print(f"calle funtion : {mode} with param file {input_filename}")
        #input_filename = "music_story_enriched_artist.csv"
        return decorate_artist_list.decorate_instagram_followers_artist_based_on_username(input_filename)
    elif mode == MODE_SEARCH_IG_FOLLLOWERS_BY_ARTIST_NAME:
        print(f"calle funtion : {mode} with param file {input_filename}")
        #input_filename = "UNION MSI01-IS01-IS02 - Not Found - Duplicates Removed.csv"
        return decorate_artist_list.decorate_instagram_followers_artist_based_on_name_search(input_filename)
    elif mode == MODE_PRODUCE_TEST_DATASET_BY_PLAYLIST:
        print(f"calle funtion : {mode} with param file {input_filename}")
        #spotify_playlist_id = "2be8Q4uvGVnH3didCoySP6"
        spotify_playlist_id = input_filename
        return produce_test_dataset.produce_test_dataset_by_spotify_playlist(spotify_playlist_id)
    else:
        message = f"invalid mode: {mode}"
        print(message)
        return message

if __name__ == "__main__":
    sys.exit(main())