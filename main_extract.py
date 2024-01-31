import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import json
from datetime import datetime
from io import StringIO                      
import pandas as pd


def main():
  client_credentials_manager = SpotifyClientCredentials(client_id='***', client_secret='***')


  sp = spotipy.Spotify(client_credentials_manager= client_credentials_manager)
  playlist_link = 'https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF'
  playlist_URI= playlist_link.split('/')[-1]
  data = sp.playlist_tracks(playlist_URI)
  song_list = []
  for row in data['items']:
      song_id = row['track']['id']
      song_name = row['track']['name']
      song_duration = row['track']['duration_ms']
      song_url = row['track']['external_urls']['spotify']
      song_popularity = row['track']['popularity']
      song_added = row['added_at']
      album_id = row['track']['album']['id']
      artist_id = row['track']['album']['artists'][0]['id']
      song_element = {'song_id':song_id,'song_name':song_name,'duration_ms':song_duration,'url':song_url,
                      'popularity':song_popularity,'song_added':song_added,'album_id':album_id,
                      'artist_id':artist_id}
      song_list.append(song_element)

  album_list = []
  for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']
        album_element = {'album_id':album_id,'name':album_name,'release_date':album_release_date,
                            'total_tracks':album_total_tracks,'url':album_url}
        album_list.append(album_element)

  artists_list=[]
  for row in data['items']:
        for key,value in row.items():
            if key=='track':
                for artist in value['artists']:
                    artists_dict={'artist_id':artist['id'], 'artist_name':artist['name'], 'external_url': artist['href']}
                    artists_list.append(artists_dict)


  album_df= pd.DataFrame.from_dict(album_list)
  album_df = album_df.drop_duplicates(subset=['album_id'])
  album_df['release_date'] = pd.to_datetime(album_df['release_date'])

  artist_df= pd.DataFrame.from_dict(artists_list)
  artist_df = artist_df.drop_duplicates(subset=['artist_id'])

  song_df = pd.DataFrame.from_dict(song_list)
  song_df['song_added']= pd.to_datetime(song_df['song_added'])


  song_key = 'transformed_data/songs_data/song_transformed_'+str(datetime.now())+'.csv'
  song_buffer = StringIO()                      # Creating StringIO() object
  song_df.to_csv(song_buffer, index=False)                 # passing strinio object to csv func. It will convert entire DF to String like object
  song_content = song_buffer.getvalue()
  #song_df.to_csv('/content/sample_data/song.csv', index=False)



if __name__ =="__main__":
    main()




