from library import Library
import pandas as pd
import unittest

class LibraryTest(unittest.TestCase):
    def setUp(self):
        df = pd.read_csv('songs.csv')
        self.library = Library(df)

    # test check_if_title_exists_in_musicon_library()
    def test_check_if_title_exists_in_musicon_library_empty_input(self):
        input = ""
        expected_output = False
        output = self.library.check_if_title_exists_in_musicon_library(input)
        self.assertEqual(output, expected_output)

    def test_check_if_title_exists_in_musicon_library_exist(self):
        input = "Shape Of You"
        expected_output = True
        output = self.library.check_if_title_exists_in_musicon_library(input)
        self.assertEqual(output, expected_output)

    def test_check_if_title_exists_in_musicon_library_not_exist(self):
        input = "something does not exist"
        expected_output = False
        output = self.library.check_if_title_exists_in_musicon_library(input)
        self.assertEqual(output, expected_output)

    # test add_song_attributes_into_library_list()
    def test_add_song_attributes_into_library_list_new_song(self):
        input_artist = "artist"
        input_title = "title"
        input_length = "length"
        input_genre = "genre"
        input_year = "year"
        input_lyrics = "Some lyrics"
        expected_length = len(self.library.df)+1
        self.library.add_song_attributes_into_library_list(
            input_artist, input_title, input_length, input_genre, input_year, input_lyrics)
        self.assertEqual(len(self.library.df), expected_length)
    
    def test_add_song_attributes_into_library_list_limited_info(self):
        input_artist = "artist"
        input_title = ""
        input_length = ""
        input_genre = ""
        input_year = ""
        input_lyrics = ""
        expected_length = len(self.library.df)+1
        self.library.add_song_attributes_into_library_list(
            input_artist, input_title, input_length, input_genre, input_year, input_lyrics)
        self.assertEqual(len(self.library.df), expected_length)
    
    def test_add_song_attributes_into_library_list_empty(self):
        input_artist = ""
        input_title = ""
        input_length = ""
        input_genre = ""
        input_year = ""
        input_lyrics = ""
        expected_length = len(self.library.df)
        self.library.add_song_attributes_into_library_list(
            input_artist, input_title, input_length, input_genre, input_year, input_lyrics)
        self.assertEqual(len(self.library.df), expected_length)

    def test_add_song_attributes_into_library_list_all_None(self):
        input_artist = None
        input_title = None
        input_length = None
        input_genre = None
        input_year = None
        input_lyrics = None
        expected_length = len(self.library.df)
        self.library.add_song_attributes_into_library_list(
            input_artist, input_title, input_length, input_genre, input_year, input_lyrics)
        self.assertEqual(len(self.library.df), expected_length)

    # test delete_song_attributes_from_library_with_title_name()
    def test_delete_song_attributes_from_library_with_title_name_None(self):
        input = None
        expected_length = len(self.library.df)
        self.library.delete_song_attributes_from_library_with_title_name(input)
        self.assertEqual(len(self.library.df), expected_length)

    def test_delete_song_attributes_from_library_with_title_name_empty(self):
        input = ""
        expected_length = len(self.library.df)
        self.library.delete_song_attributes_from_library_with_title_name(input)
        self.assertEqual(len(self.library.df), expected_length)

    def test_delete_song_attributes_from_library_with_title_not_exist(self):
        input = "something does not exist"
        expected_length = len(self.library.df)
        self.library.delete_song_attributes_from_library_with_title_name(input)
        self.assertEqual(len(self.library.df), expected_length)

    def test_delete_song_attributes_from_library_with_title_success(self):
        input = "Shape Of You"
        expected_length = len(self.library.df)-1
        self.library.delete_song_attributes_from_library_with_title_name(input)
        self.assertEqual(len(self.library.df), expected_length)

    # test searching_for_titles_in_musicon_library_by_artist()
    def test_searching_for_titles_in_musicon_library_by_artist_None(self):
        input = None
        expected_output = 0
        output = self.library.searching_for_titles_in_musicon_library_by_artist(input)
        self.assertEqual(output, expected_output)

    def test_searching_for_titles_in_musicon_library_by_artist_empty(self):
        input = ""
        expected_output = 0
        output = self.library.searching_for_titles_in_musicon_library_by_artist(input)
        self.assertEqual(output, expected_output)

    def test_searching_for_titles_in_musicon_library_by_artist_not_exist(self):
        input = "something does not exist"
        expected_output = 0
        output = self.library.searching_for_titles_in_musicon_library_by_artist(input)
        self.assertEqual(output, expected_output)

    def test_searching_for_titles_in_musicon_library_by_artist_success(self):
        input = "Ed Sheeran"
        expected_output = 47
        output = self.library.searching_for_titles_in_musicon_library_by_artist(input)
        self.assertEqual(output, expected_output)

    # test show_all_titles_present_in_musicon_library()
    def test_show_all_titles_present_in_musicon_library(self):
        input = None
        expected_output = 47
        output = self.library.show_all_titles_present_in_musicon_library()
        self.assertEqual(output, expected_output)

    # show_info_about_song_title_from_musicon_library()
    def test_show_info_about_song_title_from_musicon_library_None(self):
        input = None
        expected_output = 0
        output = self.library.show_info_about_song_title_from_musicon_library(input)
        self.assertEqual(output, expected_output)

    def test_show_info_about_song_title_from_musicon_library_empty(self):
        input = ""
        expected_output = 0
        output = self.library.show_info_about_song_title_from_musicon_library(input)
        self.assertEqual(output, expected_output)
    
    def test_show_info_about_song_title_from_musicon_library_not_exist(self):
        input = "something does not exist"
        expected_output = 0
        output = self.library.show_info_about_song_title_from_musicon_library(input)
        self.assertEqual(output, expected_output)

    def test_show_info_about_song_title_from_musicon_library_success(self):
        input = "Shape Of You"
        expected_output = 1
        output = self.library.show_info_about_song_title_from_musicon_library(input)
        self.assertEqual(output, expected_output)
    
    def test_show_info_about_song_title_from_musicon_library_duplicates(self):
        input = "Shape Of You"
        self.library.add_song_attributes_into_library_list(None, input, None, None, None, None)
        expected_output = 2
        output = self.library.show_info_about_song_title_from_musicon_library(input)
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()