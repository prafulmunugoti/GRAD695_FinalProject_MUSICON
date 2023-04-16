#!/usr/bin/env python
# coding: utf-8

# # Software artifact using Data Structures
# 
# Name: MuSiCoN
# 
# Language: Python3
# 
# Data Structures: 
# CSV file (to store song attributes and as song library) 
# Pandas DF (to extract data from csv file) 
# list (to implement Stack DS LIFO principle , shuffle operation on playlist) 
# Circular Queue (to implement loop operation with FIFO principle using DLL) 
# Dictionary (to store the contents of playlist) 
# Stack (recently played songs list feature)
# 
# ** MuSiCoN ** Options of Menu:
# 
# 1.Add a new song to library
# 2.Delete a song from library
# 3.Show songs in library
# 4.Search songs by artist in library
# 5.Play a Song in Library
# 6.Create a playlist
# 7.Show all playlists
# 8.Add songs to the playlist
# 9.Play songs in playlist 
#   1.Normal Mode 
#   2.Shuffle Mode 
#   3.Loop Mode
# 10.Show recently played songs
# 11.Exit from application

import library
import pandas as pd
import playlist

class MusiCon():
    def __init__(self):
        #def musicon():
        df = pd.read_csv('songs.csv')
        self.playlist_object = playlist.Playlist()
        self.library_object = library.Library(df)

    # function to display menu for the users     
    def print_menu(self):
        print(30 * "-" , "MuSiCoN" , 30 * "-")
        print("0.  Menu")
        print("1.  Add a new song to library")
        print("2.  Delete a song from library")
        print("3.  Show songs in library")
        print("4.  Search by song name or artist")
        print("5.  Play a song present in Library")
        print("6.  Create a playlist")
        print("7.  Show all playlists")
        print("8.  Add songs to the playlist")
        print("9.  Play songs in playlist")
        print("10. Show recently played songs")
        print("11. Exit")
        print(67 * "-")

        loop=True      
        #while loop that goes on forever until exited 
        while loop:
            #print_menu()
            choice = int(input("\nSelect one among these Options [1-11] or 0 for menu : ",))
            if choice==0:
                print(30 * "-" , "MuSiCoN" , 30 * "-")
                print("0.  Menu")
                print("1.  Add a new song to library")
                print("2.  Delete a song from library")
                print("3.  Show songs in library")
                print("4.  Search by song name or artist")
                print("5.  Play a song present in Library")
                print("6.  Create a playlist")
                print("7.  Show all playlists")
                print("8.  Add songs to the playlist")
                print("9.  Play songs in playlist")
                print("10. Show recently played songs")
                print("11. Exit")
                print(67 * "-")
            elif choice==1:     
                print("\nyou chose to add a new song to the existing library\n\n")
                title = input("\nplease enter the song title : ")
                artist = input("please enter the song artist : ")
                length = input("\nplease enter the song length : ")
                genre = input("\nplease enter the song genre : ")
                year = int(input("\nplease enter the song year : "))
                lyrics = input("\nplease enter the song lyrics : ")
                self.library_object.add_song_attributes_into_library_list(artist,title,length,genre,year,lyrics)

            elif choice==2:
                print("you chose to delete a song from the existing library\n")
                title = input("\nplease enter the song title : ")
                check = self.library_object.check_if_title_exists_in_musicon_library(title)
                if (check):
                    self.library_object.delete_song_attributes_from_library_with_title_name(title)
                else:
                    print("title is not present in library to delete\n")

            elif choice==3:
                print("you chose to see all songs present in existing library\n")
                self.library_object.show_all_titles_present_in_musicon_library()
                
            elif choice==4:
                print("you chose option to search for songs of an Artist in library\n")
                #check for songs in library
                song_artist = input("please enter the artist name : ")
                self.num_song_artist = self.library_object.searching_for_titles_in_musicon_library_by_artist(song_artist)

            elif choice==5:
                print("you chose option to play a song in library\n")
                #check for songs in library
                song_title = input("please enter the song title : ")
                check = self.library_object.check_if_title_exists_in_musicon_library(song_title)
                if (check):
                    self.library_object.show_info_about_song_title_from_musicon_library(song_title)
                    self.playlist_object.play_individual_song_on_user_input(song_title)
                else:
                    print(song_title," doesn't exist in the library, please use option 1 to add song to the library")

            elif choice==6:
                print("you chose to create a new Playlist\n")
                playlist_name = input("please enter the name of the playlist: ")
                self.playlist_object.create_a_new_playlist(playlist_name)

            elif choice==7:
                print("Display Playlists in the Library\n")
                self.playlist_object.display_existing_playlists()

            elif choice==8:
                print("you chose to add songs to the playlist")
                print("list of playlist available in libarary are : \n")
                self.playlist_object.display_existing_playlists()
                print("select a play list to add songs and enter the playlist name\n")
                playlist_name = input("please enter the name of the playlist: ")
        #       display_song_present_in_the_library
                print("enter song name to add to the playlist ",playlist_name)
                title_name = input("please enter the name of the song: ")
                self.playlist_object.add_song_into_playlist_dictionary(playlist_name,title_name)
                while(1):
                    add_more = input("want to add more songs into playlist y/n\n")
                    if(add_more == 'n'):
                        break
                    else:
                        print("enter song name to add to the playlist ",playlist_name)
                        title_name = input("please enter the name of the song name: ")
                        self.playlist_object.add_song_into_playlist_dictionary(playlist_name,title_name)

            elif choice==9:
                print("you choose to play songs in the playlist\n")
                print("list of playlist available in libarary are : \n")
                self.playlist_object.display_existing_playlists()
                print("select a play list to play and enter the playlist name\n")
                playlist_name = input("please enter the name of the playlist: ")
                playlist_mode = int(input("please select the mode you like to choose :\n1.normal\n2.shuffle\n3.loop\n"))
                if (playlist_mode == 1):
                    self.playlist_object.play_songs_in_the_playlist(playlist_name, self.library_object)
                elif (playlist_mode == 2):
                    shuffled_playlist = self.playlist_object.shuffle_songs_in_the_playlist(playlist_name,playlist.playlist_dict[playlist_name])
                    while(1):
                        shuffle_again = input("do you wish to shuffle the playlist again -- y/n?")
                        if shuffle_again == 'y':
                            shuffled_playlist = self.playlist_object.shuffle_songs_in_the_playlist(playlist_name,shuffled_playlist)
                        elif shuffle_again == 'n':
                            break
                    self.playlist_object.play_songs_in_the_playlist(playlist_name, self.library_object)
                elif (playlist_mode == 3):
                    self.playlist_object.loop_songs_in_the_playlist(playlist_name, self.library_object)
                else:
                    self.playlist_object.play_songs_in_the_playlist(playlist_name, self.library_object)

            elif choice==10:
                print("you chose an option to see Recently played Songs from the Library\n")
                self.playlist_object.display_songs_in_recently_played_stack()
                recent_play = input("do you wish to play a song from the recently played list y/n?")            
                if (recent_play == 'y'):
                    recent_title_name = input("please enter the name of the song: ")
                    print("\nplaying the song selected from recent played stack ",recent_title_name)
                    self.library_object.show_info_about_song_title_from_musicon_library(recent_title_name)
                    self.playlist_object.play_individual_song_on_user_input(recent_title_name)
                elif (recent_play == 'n'):
                    print("No selection happened , leaving ")

            elif choice==11:
                print("Exit option selected, exiting from 'MuSiCoN' ")

                loop=False # This will make the while loop to end as value of loop is set to False
            else:
                    # Any integer inputs other than values 1-12 we print an error message
                print("Wrong option selection. Enter any key to try again..") 

    if __name__ == "__main__":
        print_menu()