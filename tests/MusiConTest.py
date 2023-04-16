from unittest.mock import patch
from MusiCon import MusiCon
from library import Library
import pandas as pd
import unittest

from playlist import Playlist

class MusiConTest(unittest.TestCase):
    def setUp(self):
        self.musiCon = MusiCon()

    action_list_1 = [
        # Add a new song
        '1',
        # New song - title, artist, length, genre, year, lyrics
        'New Song', 'artist', 'length', 'genre', '2020', 'lyrics',
        # Delete a song
        '2',
        # Delete 'Shape Of You'
        'Shape Of You',
        # Show all songs
        '3',
        # Search songs by artist
        '4',
        # Search songs - artist
        'Ed Sheeran',
        # Play a song
        '5',
        # Play New Song
        'New Song',
        # Create a new playlist
        '6',
        # Create playlist - 'New Playlist'
        'New Playlist',
        # Display existing playlist
        '7',
        # Add songs into playlist
        '8',
        # Add songs into 'New Playlist'
        'New Playlist',
        # Add 'New Song' into 'New Playlist'
        'New Song',
        # Add more songs
        'y',
        # Add 'Castle On The Hill' into 'New Playlist'
        'Castle On The Hill',
        # Finish adding songs
        'n',
        # Play songs in the playlist
        '9',
        # Play songs in 'New Playlist'
        'New Playlist',
        # Normal mode
        '1',
        # Show rently played songs
        '10',
        # Play a song in recently played list
        'y',
        # Play 'New Song'
        'New Song',
        # Not an option
        '12',
        # Exit
        '11',
        ]

    # test the system - Add a song
    @patch('builtins.input', side_effect = action_list_1)
    def test_musiCon_addASong(self, mock_inputs):
        # Before action, verify contents
        original_num_songs = len(self.musiCon.library_object.df)
        self.assertEqual(original_num_songs, 49)
        original_num_playlist = len(self.musiCon.playlist_object.playlist_dict)
        self.assertEqual(original_num_playlist, 0)
        self.assertTrue(self.musiCon.library_object.df['title'].str.contains('Shape Of You').any())
        self.assertFalse(self.musiCon.library_object.df['title'].str.contains('New Song').any())
        self.assertEqual(len(self.musiCon.playlist_object.recently_played_stack), 0)
        self.assertIsNone(self.musiCon.playlist_object.queue_head)
        self.assertIsNone(self.musiCon.playlist_object.queue_tail)
        self.assertEqual(self.musiCon.playlist_object.queue_count, 0)

        # Take mock actions
        self.musiCon.print_menu()

        # After actions, verify results
        self.assertEqual(len(self.musiCon.library_object.df), 49)
        self.assertTrue(self.musiCon.library_object.df['title'].str.contains('New Song').any())
        self.assertFalse(self.musiCon.library_object.df['title'].str.contains('Shape Of You').any())
        self.assertEqual(self.musiCon.num_song_artist, 46)
        self.assertEqual(len(self.musiCon.playlist_object.playlist_dict), 1)
        self.assertEqual(len(self.musiCon.playlist_object.playlist_dict['New Playlist']), 2)
        self.assertEqual(len(self.musiCon.playlist_object.recently_played_stack), 4)

if __name__ == '__main__':
    unittest.main()