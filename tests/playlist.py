#!/usr/bin/env python
# coding: utf-8

#Class definition for a playlist with attribute as a Name and has the list of songs
#e.g: 
# name   : EdSheeran playlist
# songs  : Bad Habits , Shape of You, Perfect , Galway Girl
#
from copy import deepcopy
from Node import Node
from random import randint, shuffle

import time


class Playlist:
    def __init__(self):
        #self.name = name
        #self.songs = []
        self.playlist_dict = {}
        self.recently_played_stack = []
        self.queue_head = None
        self.queue_tail = None
        self.queue_count = 0
        
    #function to create a playlist 
    def create_a_new_playlist(self,playlist):
        # Check if key exist in dict or not
        if not playlist:
            return
        if playlist not in self.playlist_dict: 
            self.playlist_dict[playlist] = []
        else: 
            print("Playlist already exists, please use a new name again")

    #function to display existing playlists in playlist dictionary
    def display_existing_playlists(self):
        playlist_names = list(self.playlist_dict.keys())
        for playlist in playlist_names:
            print("    ",playlist,"\n")
        return len(playlist_names)
        
    #function to append the song at the end of songs list of the Playlist object
    def add_song_into_playlist_dictionary(self, playlist, title):
        # Check if key exist in dict or not
        # Check if type of value of key is list or not
        # If type is not list then make it list
        # Append the value in list
        if not playlist or not title:
            return False
        if playlist in self.playlist_dict:
            if not isinstance(self.playlist_dict[playlist], list):
                self.playlist_dict[playlist] = [self.playlist_dict[playlist]]
            self.playlist_dict[playlist].append(title)
            return True
        return False

    #function to display the songs in the playlist using a for loop
    def display_songs_in_playlist(self,playlist):
        # Iterate over all values of a dictionary 
        # and print them one by one
        # Check if key exist in dict or not
        if playlist in self.playlist_dict:
            print("Songs in the playlist are :",self.playlist_dict[playlist])
            return len(self.playlist_dict[playlist])
        else:
            print("Playlist doesn't exist in the list, please use option 6 to create a playlist")
            return False
            
    #function to randomly shuffling the list of songs in the playlist by swapping the picked element with 
    #the current element, and then picking the next random element from the remainder. The output is a random 
    #permutation of the playlist.
    def shuffle_songs_in_the_playlist(self,playlist_name,playlist):
        print("playlist before shuffle :\n",playlist)
        tmp_playlist = deepcopy(playlist)
        length = len(tmp_playlist)
        while (length):
            length = length-1
            rand_num = randint(0, length)
            tmp_playlist[length], tmp_playlist[rand_num] = \
                tmp_playlist[rand_num], tmp_playlist[length]
        if (length > 1 and tmp_playlist == playlist):
            tmp_playlist == self.shuffle_songs_in_the_playlist(playlist_name, tmp_playlist)
        print("playlist after shuffle :\n",tmp_playlist)
        self.playlist_dict[playlist_name] = tmp_playlist
        return tmp_playlist

    #function to loop the songs in the playlist 
    def loop_songs_in_the_playlist(self,playlist,library):
        #play the song, sleep for 5 seconds
        #once the song is done playing after 5 seconds before the next song starts 
        #put the song in a queue at the end
        #user Ctrl+C once they are done with the loops
        print("entered loop mode of the playlist")
        length = len(self.playlist_dict[playlist])
        for title in self.playlist_dict[playlist]:
            self.enqueue_the_song_recently_played_into_start_of_the_queue(title)
        self.display_the_elements_of_the_loop_queue()
        temp=self.queue_head
        try:
            while temp is not None:
                print("\n\nplaying ",temp.data," ")
                library.show_info_about_song_title_from_musicon_library(temp.data)
                time.sleep(5)   # Delays for 5 seconds, just to replicate the song is playing
                print("\ncompleted playing the song, pushing ",temp.data," to recently played stack")
                self.push_to_recently_played_stack(title)
            
                dequeued_title = self.dequeue_the_song_recently_played_in_playlist_to_enqueue()
                self.enqueue_the_song_recently_played_into_start_of_the_queue(dequeued_title)
                self.display_the_elements_of_the_loop_queue()
                temp=temp.next
        except KeyboardInterrupt:
            print("ending the loop mode of the playlist\n")


    #function to play the songs in the playlist
    def play_songs_in_the_playlist(self,playlist,library):
        length = len(self.playlist_dict[playlist])
        print("length of playlist : ",length)
        for title in self.playlist_dict[playlist]:
            library.show_info_about_song_title_from_musicon_library(title)
            self.play_individual_song_on_user_input(title)
            
    #function to play individual song in the 
    def play_individual_song_on_user_input(self,title):
        print("playing ",title," ")
        time.sleep(5)# Delays for 5 seconds, just to replicate the song is playing
        #place the song into a recently played stack
        print("completed playing the song, pushing ",title," to recently played stack \n")
        self.push_to_recently_played_stack(title)

    # pushes/appends an element to the recently played stack    
    def push_to_recently_played_stack(self,title): 
        return self.recently_played_stack.insert(0,title) 

    # remove/pop an element from the recently played stack
    def pop_from_recently_played_stack(self): 
        if self.is_empty():
            return None
        else:
            return self.recently_played_stack.pop() 

    ## returns the size/number of elements in a stack
    def size(self): 
        return len(self.recently_played_stack)    

    ## Boolean evaluation to check if stack if empty return true or false
    def is_empty(self):  
        return self.size() == 0
    
    # function to print the songs in recently played stack
    def display_songs_in_recently_played_stack(self):
        if self.is_empty():
            print("there are no songs that were played recently\n")
            return None
        else:
            print("Songs played Most Recent to Least recent\n")
            for recently_played_song in self.recently_played_stack:
                print(recently_played_song,"\n")
            return self.recently_played_stack

    #Queue is a collection of objects that are inserted and removed using the first in first out principle. 
    #Insertion is done at the back of the queue and elements are deleted from the front location of the queue.
    # enqueue operation used to push the titles in a playlist to run in loop mode
    def enqueue_the_song_recently_played_into_start_of_the_queue(self, data):
        if self.queue_tail is None:
            self.queue_head = Node(data)
            self.queue_tail = self.queue_head
        else :
            self.queue_tail.next = Node(data)
            self.queue_tail.next.prev = self.queue_tail
            self.queue_tail = self.queue_tail.next
        self.queue_count += 1
    
    # dequeue operation used to pop the element and 
    def dequeue_the_song_recently_played_in_playlist_to_enqueue(self):
        if self.queue_head is None:
            return None
        else:
            temp = self.queue_head.data
            self.queue_head = self.queue_head.next
            if self.queue_head is not None:
                self.queue_head.prev=None
            self.queue_count -= 1
            return temp
        
    #display the elements of the loop queue
    def display_the_elements_of_the_loop_queue(self):  
        print("queue elements are:")
        temp=self.queue_head
        while temp is not None:
            print(temp.data,end="<-")
            temp=temp.next

