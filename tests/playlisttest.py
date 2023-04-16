#!/usr/bin/env python
# coding: utf-8
from library import Library
from playlist import Playlist

import pandas as pd
import unittest

class PlaylistTest(unittest.TestCase):
    def setUp(self):
        df = pd.read_csv('songs.csv')
        self.library = Library(df)
        self.playlist = Playlist()

    # Test create_a_new_playlist()
    def test_create_a_new_playlist_none_input(self):
        input = None
        expected_output = len(self.playlist.playlist_dict.keys())
        self.playlist.create_a_new_playlist(input)
        self.assertEqual(len(self.playlist.playlist_dict.keys()), expected_output)

    def test_create_a_new_playlist_empty_input(self):
        input = ""
        expected_output = len(self.playlist.playlist_dict.keys())
        self.playlist.create_a_new_playlist(input)
        self.assertEqual(len(self.playlist.playlist_dict.keys()), expected_output)

    def test_create_a_new_playlist_valid_input(self):
        input = "playlist1"
        expected_output =len(self.playlist.playlist_dict.keys())+1
        self.playlist.create_a_new_playlist(input)
        self.assertEqual(len(self.playlist.playlist_dict.keys()), expected_output)
        
    def test_create_a_new_playlist_existing_name_input(self):
        input = "playlist1"
        expected_output = len(self.playlist.playlist_dict.keys())+1
        self.playlist.create_a_new_playlist(input)
        self.playlist.create_a_new_playlist(input)
        self.assertEqual(len(self.playlist.playlist_dict.keys()), expected_output)

    def test_create_a_new_playlist_multiple_input(self):
        input1 = "playlist1"
        input2 = "playlist2"
        expected_output = len(self.playlist.playlist_dict.keys())+2
        self.playlist.create_a_new_playlist(input1)
        self.playlist.create_a_new_playlist(input2)
        self.assertEqual(len(self.playlist.playlist_dict.keys()), expected_output)

    # Test display_existing_playlists()
    def test_display_existing_playlists_input(self):
        input = None
        expected_output = len(self.playlist.playlist_dict.keys())
        output = self.playlist.display_existing_playlists()
        self.assertEqual(output, expected_output) 
    
    # Test add_song_into_playlist_dictionary()
    def test_add_song_into_playlist_dictionary_None_input(self):
        playlist_name_input = None
        title_name_input = None
        expected_output = False
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 

    def test_add_song_into_playlist_dictionary_empty_input(self):
        playlist_name_input = ""
        title_name_input = ""
        expected_output = False
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 
        
    def test_add_song_into_playlist_dictionary_valid_playlist_empty_title(self):
        playlist_name_input = "playlist1"
        title_name_input = ""
        expected_output = False
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 
    
    def test_add_song_into_playlist_dictionary_empty_playlist_valid_title(self):
        playlist_name_input = ""
        title_name_input = "Waka Waka"
        expected_output = False
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 
    
    def test_add_song_into_playlist_dictionary_valid_playlist_valid_title(self):
        playlist_name_input = "playlist1"
        title_name_input = "Waka Waka"
        expected_output = True
        self.playlist.create_a_new_playlist(playlist_name_input)
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 
        
    def test_add_song_into_playlist_dictionary_invalid_playlist_valid_title(self):
        playlist_name_input = "playlist100"
        title_name_input = "Waka Waka"
        expected_output = False
        output = self.playlist.add_song_into_playlist_dictionary(playlist_name_input, title_name_input)
        self.assertEqual(output, expected_output) 

    # Test display_songs_in_playlist()
    def test_display_songs_in_playlist_None(self):
        input = None
        expected_output = False
        output = self.playlist.display_songs_in_playlist(input)
        self.assertEqual(output, expected_output)
    
    def test_display_songs_in_playlist_empty(self):
        input = ""
        expected_output = False
        output = self.playlist.display_songs_in_playlist(input)
        self.assertEqual(output, expected_output)
    
    def test_display_songs_in_playlist_not_exist(self):
        input = "something does not exist"
        expected_output = False
        output = self.playlist.display_songs_in_playlist(input)
        self.assertEqual(output, expected_output)

    def test_display_songs_in_playlist_empty_playlist(self):
        input = "Playlist1"
        expected_output = 0
        self.playlist.create_a_new_playlist(input)
        output = self.playlist.display_songs_in_playlist(input)
        self.assertEqual(output, expected_output)
    
    def test_display_songs_in_playlist_success(self):
        input = "Playlist1"
        expected_output = 2
        self.playlist.create_a_new_playlist(input)
        self.playlist.add_song_into_playlist_dictionary(input, "title1")
        self.playlist.add_song_into_playlist_dictionary(input, "title2")
        output = self.playlist.display_songs_in_playlist(input)
        self.assertEqual(output, expected_output)

    # Test shuffle_songs_in_the_playlist()
    def test_shuffle_songs_in_the_playlist_empty(self):
        input = "Playlist1"
        self.playlist.create_a_new_playlist(input)
        original_list = self.playlist.playlist_dict[input]
        output = self.playlist.shuffle_songs_in_the_playlist(input, original_list)
        # Empty list should remain the same after shuffle
        self.assertEqual(output, original_list)

    def test_shuffle_songs_in_the_playlist_one_song(self):
        input = "Playlist1"
        self.playlist.create_a_new_playlist(input)
        self.playlist.add_song_into_playlist_dictionary(input, "title1")
        original_list = self.playlist.playlist_dict[input]
        output = self.playlist.shuffle_songs_in_the_playlist(input, original_list)
        # List with one element should remain the same after shuffle
        self.assertEqual(output, original_list)
        self.assertCountEqual(output, original_list)

    def test_shuffle_songs_in_the_playlist_multiple_songs(self):
        input = "Playlist1"
        self.playlist.create_a_new_playlist(input)
        self.playlist.add_song_into_playlist_dictionary(input, "title1")
        self.playlist.add_song_into_playlist_dictionary(input, "title2")
        self.playlist.add_song_into_playlist_dictionary(input, "title3")
        self.playlist.add_song_into_playlist_dictionary(input, "title4")
        self.playlist.add_song_into_playlist_dictionary(input, "title5")
        original_list = self.playlist.playlist_dict[input]
        output = self.playlist.shuffle_songs_in_the_playlist(input, original_list)
        self.assertNotEqual(output, original_list)
        self.assertCountEqual(output, original_list)

    # Test push_to_recently_played_stack
    def test_push_to_recently_played_stack_empty(self):
        input = "Waka Waka"
        expected_output = input
        self.playlist.push_to_recently_played_stack(input)
        self.assertEqual(len(self.playlist.recently_played_stack), 1)
        self.assertEqual(self.playlist.recently_played_stack[0], expected_output)

    def test_push_to_recently_played_stack_non_empty(self):
        input = "Waka Waka"
        expected_output = input
        self.playlist.recently_played_stack.append("Stale Song")
        self.playlist.push_to_recently_played_stack(input)
        self.assertEqual(len(self.playlist.recently_played_stack), 2)
        self.assertEqual(self.playlist.recently_played_stack[0], expected_output)
        self.assertEqual(self.playlist.recently_played_stack[1], "Stale Song")

    # Test display_songs_in_recently_played_stack
    def test_display_songs_in_recently_played_stack_empty(self):
        self.assertIsNone(self.playlist.display_songs_in_recently_played_stack())

    def test_display_songs_in_recently_played_stack_nonempty(self):
        self.playlist.recently_played_stack.append("Stale Song")
        expected_output = self.playlist.recently_played_stack
        self.assertEqual(self.playlist.display_songs_in_recently_played_stack(), expected_output)

    # Test enqueue_the_song_recently_played_into_start_of_the_queue
    def test_enqueue_the_song_recently_played_into_start_of_the_queue_empty(self):
        input_data = "title1"
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue(input_data)
        self.assertEqual(self.playlist.queue_count, 1)
        self.assertEqual(self.playlist.queue_head, self.playlist.queue_tail)
        self.assertEqual(self.playlist.queue_head.data, input_data)

    def test_enqueue_the_song_recently_played_into_start_of_the_queue_one_node(self):
        input_data = "title2"
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue("title1")
        expected_head = self.playlist.queue_head
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue(input_data)
        self.assertEqual(self.playlist.queue_count, 2)
        self.assertEqual(self.playlist.queue_head, expected_head)
        self.assertEqual(self.playlist.queue_tail.data, input_data)
    
    def test_enqueue_the_song_recently_played_into_start_of_the_queue_more_nodes(self):
        input_data = "title3"
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue("title1")
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue("title2")
        expected_head = self.playlist.queue_head
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue(input_data)
        self.assertEqual(self.playlist.queue_count, 3)
        self.assertEqual(self.playlist.queue_head, expected_head)
        self.assertEqual(self.playlist.queue_head.next.data, "title2")
        self.assertEqual(self.playlist.queue_tail.data, input_data)

    # Test dequeue_the_song_recently_played_in_playlist_to_enqueue
    def test_dequeue_the_song_recently_played_in_playlist_to_enqueue_empty(self):
        self.assertIsNone(self.playlist.dequeue_the_song_recently_played_in_playlist_to_enqueue())

    def test_dequeue_the_song_recently_played_in_playlist_to_enqueue_one_song(self):
        expected_output = "title1"
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue(expected_output)
        output = self.playlist.dequeue_the_song_recently_played_in_playlist_to_enqueue()
        self.assertEqual(self.playlist.queue_count, 0)
        self.assertEqual(output, expected_output)

    def test_dequeue_the_song_recently_played_in_playlist_to_enqueue_more_songs(self):
        expected_output = "title1"
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue(expected_output)
        self.playlist.enqueue_the_song_recently_played_into_start_of_the_queue("title2")
        tail = self.playlist.queue_tail
        output = self.playlist.dequeue_the_song_recently_played_in_playlist_to_enqueue()
        self.assertEqual(self.playlist.queue_count, 1)
        self.assertEqual(output, expected_output)
        self.assertEqual(self.playlist.queue_tail, tail)

    # Test play_individual_song_on_user_input
    def test_play_individual_song_on_user_input_normal(self):
        input_title = "Shape of You"
        expected_length = len(self.playlist.recently_played_stack)+1
        self.playlist.play_individual_song_on_user_input(input_title)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_length)
 
    def test_play_individual_song_on_user_input_empty_input(self):
        input_title = ""
        expected_length = len(self.playlist.recently_played_stack)+1
        self.playlist.play_individual_song_on_user_input(input_title)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_length)

    def test_play_individual_song_on_user_input_song_not_in_library(self):
        input_title = "Song that does not exist in the library"
        expected_length = len(self.playlist.recently_played_stack)+1
        self.playlist.play_individual_song_on_user_input(input_title)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_length)

    # test play_songs_in_the_playlist
    def test_play_songs_in_the_playlist(self):
        expected_output = "One"
        self.playlist.playlist_dict = {'t1': ["One"]}
        output = self.playlist.play_songs_in_the_playlist('t1', self.library)
        self.assertEqual(self.playlist.recently_played_stack[0], expected_output)

    def test_play_songs_in_the_playlist_empty(self):
        expected_output = 0
        self.playlist.playlist_dict = {'t1': []}
        output = self.playlist.play_songs_in_the_playlist('t1', self.library)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_output)

    # test loop_songs_in_the_playlist
    def test_loop_songs_in_the_playlist(self):
        expected_output = 2
        self.playlist.playlist_dict = {'t1': ["Sing", "One"]}
        self.playlist.loop_songs_in_the_playlist('t1', self.library)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_output)
    
    def test_loop_songs_in_the_playlist_empty(self):
        expected_output = 0
        self.playlist.playlist_dict = {'t1': []}
        self.playlist.loop_songs_in_the_playlist('t1', self.library)
        self.assertEqual(len(self.playlist.recently_played_stack), expected_output)
        
if __name__ == '__main__':
    unittest.main()
