#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from copy import deepcopy
from random import randint
import time
import psycopg2
import pymysql
import mysql.connector
import re
import time
import datetime
from tkinter import *
from PIL import ImageTk,Image
import pymysql
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
from colorama import Fore, Back, Style

#initialize mixer 
mixer.init()

# Create a connection object
# IP address of the MySQL database server
Host = "localhost" 
# User name of the database server
User = "root"       
# Password for the database user
Password = "password"           
# Database for the project
Database = "MUSICON"

conn = pymysql.connect(host=Host, user=User, password=Password, database=Database)
# Create a cursor object
cur = conn.cursor()

try:
    # creating database 
    cur.execute("CREATE DATABASE IF NOT EXISTS MUSICON") 
    cur.execute("USE MUSICON") 
    # SQL query string for all the tables based on dependency
    sql_cmd = " create table if not exists MUSICON.artists (       artist_id int AUTO_INCREMENT,       artist_name varchar(255),       artist_image BLOB,       created_dt timestamp,       updated_dt timestamp,       primary key(artist_id) )"
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    
    cur.execute("GRANT SELECT ON artists TO public")
    cur.execute(sql_cmd)

    sql_cmd = "create table if not exists MUSICON.albums (       album_id int,       artist_id int,       album_name varchar(255),       album_cover BLOB,       created_dt timestamp,       updated_dt timestamp,       primary key(album_id),       FOREIGN KEY (artist_id) REFERENCES artists(artist_id) on delete cascade )" 
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    
    cur.execute("GRANT SELECT ON albums TO public")
    cur.execute(sql_cmd)

    sql_cmd = "create table if not exists MUSICON.users (       user_id int,       user_name varchar(255),       user_email varchar(255),       user_password varchar(255),       is_admin varchar(10),       preferences text,       created_dt timestamp,       updated_dt timestamp,       primary key(user_id) )"
    # Execute the sqlQuery
    cur.execute(sql_cmd)

    cur.execute("GRANT SELECT,UPDATE,INSERT ON users TO public")
    cur.execute(sql_cmd)
    
    sql_cmd = "create table if not exists MUSICON.playlists (       playlist_id int,       user_id int,       playlist_name varchar(255),       songs_count int,       created_dt timestamp,       updated_dt timestamp,       primary key(playlist_id),       FOREIGN KEY (user_id) REFERENCES users(user_id) on delete cascade )"
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    
    cur.execute("GRANT SELECT,INSERT,UPDATE ON playlists TO public")
    cur.execute(sql_cmd)

    sql_cmd = "create table if not exists MUSICON.songs (       song_id int AUTO_INCREMENT,       album_id int,       artist_id int,       title varchar(255),       length float,       track varchar(255),       year int,       genre varchar(10),       location text,       lyrics text,       created_dt timestamp,       updated_dt timestamp,       primary key(song_id),       FOREIGN KEY (artist_id) REFERENCES artists(artist_id) on delete cascade,       FOREIGN KEY (album_id) REFERENCES albums(album_id) on delete cascade)"
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    
    cur.execute("GRANT SELECT ON songs TO public")
    cur.execute(sql_cmd)
    
    sql_cmd = "create table if not exists MUSICON.interactions (       interaction_id int,       user_id int,       song_id int,       liked boolean,       play_count int,       mode_played varchar(255),       created_dt timestamp,       updated_dt timestamp,       session_id int,       PRIMARY KEY (interaction_id),       FOREIGN KEY (user_id) REFERENCES users(user_id) on delete cascade,       FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade )"
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    
    cur.execute("GRANT SELECT,UPDATE,INSERT ON interactions TO public")
    cur.execute(sql_cmd)

    sql_cmd = "create table if not exists MUSICON.playlist_song (       playlist_song_id int,       playlist_id int,       song_id int,       PRIMARY KEY (playlist_song_id),       FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) on delete cascade,       FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade )" 
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    conn.commit()

    cur.execute("GRANT SELECT,UPDATE,INSERT ON playlist_song TO public")
    cur.execute(sql_cmd)
    
    sql_cmd = "create table if not exists MUSICON.recently_played_stack (       recently_played_stack_id int NOT NULL AUTO_INCREMENT,       song_id int,       playlist_id int,       PRIMARY KEY (recently_played_stack_id),       FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) on delete cascade,       FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade )" 
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    conn.commit()

    cur.execute("GRANT SELECT,UPDATE,INSERT ON recently_played_stack TO public")
    cur.execute(sql_cmd)
    
    # SQL query string
    sql_cmd = "show tables"   
    # Execute the sqlQuery
    cur.execute(sql_cmd)
    #Fetch all the rows
    rows = cur.fetchall()
    for row in rows:
        print(row[0])    
    #conn.close()
except:
    print('Database Connection Failed!')


# #### Library Class and functions 

# In[2]:


#reading the information in CSV file into a dataframe object 
df = pd.read_csv('songs.csv')

#Song with attributes title, artist, album, year, lyrics
# e.g:
# title  : Bad Habits
# artist : EdSheeran
# year   : 2021
# length : 3:04
# lyrics : Every time you come around, you know I can't say no
#          Every time the sun goes down, I let you take control
#          I can feel the paradise before my world implodes
#          And tonight had something wonderful .... goes on
#
#Class definition to store music library which has the above information 
class Library:
    def __init__(self):
        self.dummy = None
        self.user_name = ""
        
    def fetch_artist_id_from_artists_table_by_artist_name(self,artist):
        #extract artist_id from artists table using artist_name
        sql_cmd = "select artist_id from MUSICON.artists where artist_name = '"+artist+"'"
        try:
            cur.execute(sql_cmd)

        except pymysql.Error as e:
            print("could not fetch artist_id from artists table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            artist_id = i[0]
        return artist_id
    
    def fetch_album_id_from_albums_table_by_album_name_artist_id(self,artist_id,album_name):
        #extract artist_id from artists table using artist_name
        #sql_cmd = "select album_id from MUSICON.albums where album_name = '"+album_name+"' and artist_id = '"+artist_id+"'"  
        sql_cmd = "SELECT album_id FROM MUSICON.albums WHERE album_name = %s and artist_id = %s"
        values = (album_name,artist_id)
        try:
            cur.execute(sql_cmd,values)

        except pymysql.Error as e:
            print("could not fetch album_id from albums table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            album_id = i[0]
        return album_id      
    
    def add_song_attributes_into_library_list(self,artist,title,length,genre,year,lyrics,album_name):
        print(" adding ",title," song into library using Data frame")
        df.loc[len(df.index)] = [artist,title,length,genre,year,lyrics]
        print("completed adding the song to Data frame object")
        
        location= "/Users/praful/Documents/Harrisburg University Courses/Research Methodology/Final Project/songs"
        
        artist_id = self.fetch_artist_id_from_artists_table_by_artist_name(artist);
        album_id = self.fetch_album_id_from_albums_table_by_album_name_artist_id(artist_id,album_name);
        
        sql_cmd = "select MAX(song_id) from MUSICON.songs"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not fetch song_id from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            song_id = i[0]
        song_id = song_id+1
        
        # Prepare the SQL query
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # Preparing SQL query to INSERT a record into the database.
        sql_cmd = f"insert into MUSICON.songs (song_id,album_id,artist_id,title,length,track,year,genre,location,lyrics,created_dt,updated_dt) values ('{song_id}','{album_id}','{artist_id}','{title}','{length}',NULL,'{year}','{genre}','{location}','{lyrics}','{timestamp}','{timestamp}')"
        try:
            cur.execute(sql_cmd)
            conn.commit()
            print("successfully added the songs into Songs DB\n")
        except pymysql.Error as e:
            print("could not insert data into songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))    
    
    def delete_song_attributes_from_library_with_title_name(self,title):
        print(" deleting ",title," song from libary using Data frame\n")
        df.drop(df.loc[df['title']==title].index, inplace=True)
        print("completed deleting the song from Data frame object")
        sql_cmd = "delete from MUSICON.songs where title = '"+title+"'"
        try:
            cur.execute(sql_cmd)
            conn.commit()
            print("successfully deleted the songs from Songs DB\n")
        except pymysql.Error as e:
            print("could not delete data from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))    
    
    def searching_for_titles_in_musicon_library_by_artist(self,artist):
        #extract the unique artist list 
        artist_list = df["artist"].unique().tolist()
        #extract the titles based on artist name
        musicon_artists_df = df.loc[df['artist'] == artist]
        musicon_artist_list = musicon_artists_df["title"].tolist()
        print("\n\nSongs of ",artist," in library/DB are : \n")
        total_songs = len(musicon_artist_list)
        if total_songs == 0:
            print("there are no songs with artist ",artist," in library\n")
        else:
            for artist_song in musicon_artist_list:
                print("    ",artist_song)
        #count number of records 
        sql_cmd = "select COUNT(s.title) from MUSICON.songs as s, MUSICON.artists as ar where ar.artist_id = s.artist_id and ar.artist_name = '"+artist+"'"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not count from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            total_song_count = i[0]
        if total_song_count == 0:
            print("there are no songs with artist ",artist," in DB\n")
        else:
            sql_cmd = "select s.title from MUSICON.songs as s, MUSICON.artists as ar where ar.artist_id = s.artist_id and ar.artist_name = '"+artist+"'"
            try:
                cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
                records = cur.fetchall()
            ## Showing the data
                for record in records:
                    print(record)
            except pymysql.Error as e:
                print("could not fetch titles from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))

        
    def check_if_title_exists_in_musicon_library(self,title):
        #check if the song name exists in the library and returns true or false
        title_exists = df['title'].eq(title).any()
        sql_cmd = "select count(*) from MUSICON.songs where title = '"+title+"'"
        try:
            cur.execute(sql_cmd)

        except pymysql.Error as e:
            print("could not count from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            count = i[0]
        return title_exists,count
        
    def show_all_titles_present_in_musicon_library(self):
        #extract the unique song titles list 
        #song_titles_list = df["title"].unique().tolist()
        #for song_title in song_titles_list:
            #print("  ",song_title," \n")
        #    print("")
        print ("\n Available songs in the DB are : \n")
        print ("\n Artist/Singer         Song Name")
        print ("\n --------------------------------")
        sql_cmd = "select ar.artist_name,s.title from MUSICON.songs as s, MUSICON.artists as ar where ar.artist_id = s.artist_id"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            ## Showing the data
            for record in records:
                print(record[0],"  ",record[1], "\n")
        except pymysql.Error as e:
            print("could not fetch titles from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
    
    def show_info_about_song_title_from_musicon_library(self,title):
        #extract the information about the song 
        print ("Attributes of the Song : ",title,"\n\n")
        sql_cmd = "select s.title,ar.artist_name,s.genre,s.length,s.year,al.album_name,s.lyrics from MUSICON.songs as s, MUSICON.artists as ar,MUSICON.albums as al         where al.album_id = s.album_id and ar.artist_id = s.artist_id and s.title = '"+title+"'"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            ## Showing the data
            for record in records:
            # print requested song attributes for the title
                print("    Title :",record[0],"\n")
                print("    Artist :",record[1],"\n")
                print("    Length :",record[3],"\n")
                print("    Genre :",record[2],"\n")
                print("    Year :",record[4],"\n")
                print("    Album :",record[5],"\n")
                print("    Lyrics :\n",record[6],"\n")
        except pymysql.Error as e:
            print("could not fetch titles from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))

                    
            
class Node(object): ## Create node class with data and next and previous pointers vars
    def __init__(self, data=None, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev
        


# #### Playlist Class Functions  

# In[3]:


#Class definition for a playlist with attribute as a Name and has the list of songs
#e.g: 
# name   : EdSheeran playlist
# songs  : Bad Habits , Shape of You, Perfect , Galway Girl
#
class Playlist:
    
    def __init__(self):
        #self.name = name
        #self.songs = []
        self.user_name = ""
        self.playlist_dict = {}
        self.playlist_songs_list = []
        self.recently_played_stack = []
        self.queue_head = None
        self.queue_tail = None
        self.queue_count = 0

#function to check if user exists in users table
    def check_if_user_exists_in_users_table(self,user_name):
        print ("checking for existance of user in DB \n")
        user_id = ''
        sql_cmd = "select user_id from MUSICON.users where user_name = '"+user_name+"'"         
        try:
            cur.execute(sql_cmd)
            for i in cur:
                user_id = i[0]
        except pymysql.Error as e:
            print("could not find userid from users table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        if (user_id == ''):
            print ("check your user name again, there is no entry of user in DB\n")
        else:
            print ("found the entry of ",user_name," in users DB\n")
        return user_id

#function to check if user is an admin or not
    def check_if_user_is_admin_in_users_table(self,user_name):
        print ("checking admin access of user in DB \n")
        sql_cmd = "select is_admin from MUSICON.users where user_name = '"+user_name+"'"         
        try:
            cur.execute(sql_cmd)
            for i in cur:
                is_admin = i[0]
        except pymysql.Error as e:
            print("getting admin access from users table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        if (is_admin == 'yes'):
            print ("you have admin access in DB\n")
            return 1
        else:
            print ("you have no admin access in DB\n")
            return 0
        
#function to check if playlist exists in DB 
    def check_if_playlist_exists_in_playlists_table(self,playlist,user_name):
        user_id = self.check_if_user_exists_in_users_table(user_name)
        sql_cmd = f"select count(*) from MUSICON.playlists where user_id = '{user_id}' and playlist_name = '{playlist}'"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not count from playlists table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        
        for i in cur:
            count = i[0]
            
        if (count > 0):
            print (playlist,"playlist already exists in playlists DB\n")
            return 0
        else:
            print (playlist,"playlist doesn't exists in playlists DB\n")
            return 1
        
#function to create a playlist 
    def create_a_new_playlist(self,playlist,user_name):

# Check if key exist in dict or not
        if playlist not in self.playlist_dict: 
            self.playlist_dict[playlist] = []
        else: 
            print("Playlist already exists, please use a new name again")
        check_flag = self.check_if_playlist_exists_in_playlists_table(playlist,user_name)
        user_id = self.check_if_user_exists_in_users_table(user_name)
        # initialization values
        playlist_id = 1
        songs_count = 0
#fetch playlist_id to increment        
        sql_cmd = "select MAX(playlist_id) from MUSICON.playlists"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not fetch playlist_id from playlists table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            playlist_id = i[0]
        playlist_id = playlist_id+1

# time calculation
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        # Preparing SQL query to INSERT a record into the database.
        if (check_flag):
            sql_cmd = f"insert into MUSICON.playlists (playlist_id,user_id,playlist_name,songs_count,created_dt,updated_dt) values ('{playlist_id}','{user_id}','{playlist}','{songs_count}','{timestamp}','{timestamp}')"
            try:
                cur.execute(sql_cmd)
                conn.commit()
                print("successfully created the playlist",playlist," for the user ",user_name," into playlists DB\n")
            except pymysql.Error as e:
                print("could not insert data into playlists table, error pymysql %d: %s" %(e.args[0], e.args[1]))        
        else: 
            print ("playlist exists, select other options like 8 or 9 in the menu")

#function to get the songs in the playlist
    def get_songs_list_added_in_the_playlist_db(self,playlist_name):
        sql_cmd = "select s.title from playlist_song as ps, songs as s, playlists as pl where ps.playlist_id = pl.playlist_id and pl.playlist_name = '"+playlist_name+"' and s.song_id = ps.song_id order by ps.playlist_song_id"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            ## Showing the data
            for record in records:
                title = record[0]
                print ("title:",title)
                self.playlist_songs_list.append(title)
        except pymysql.Error as e:
            print("could not fetch titles from playlist_song_id table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        return self.playlist_songs_list
            
#function to display existing playlists in playlist dictionary
    def display_existing_playlists(self):
        
        playlist_names = list(self.playlist_dict.keys())
        for playlist in playlist_names:
            #print("    ",playlist,"\n")
            print(" ")
## sql query for fetching the playlist names 
        sql_cmd = "select u.user_name,pl.playlist_name from MUSICON.playlists as pl , MUSICON.users as u where pl.user_id = u.user_id"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            playlists = cur.fetchall()
            ## Showing the data
            print ("Available playlists in DB are: \n")
            for playlist in playlists:
                print(playlist[0]," -- ",playlist[1],"\n")
        except pymysql.Error as e:
            print("could not fetch playlist names from playlists table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        
#function to append the song at the end of songs list of the Playlist object
    def add_song_into_playlist_dictionary(self, playlist,title):
# Check if key exist in dict or not
# Check if type of value of key is list or not
# If type is not list then make it list
# Append the value in list
        if playlist in self.playlist_dict:
            if not isinstance(self.playlist_dict[playlist], list):
                self.playlist_dict[playlist] = [self.playlist_dict[playlist]]
            self.playlist_dict[playlist].append(title)
        playlist_song_id = 1;
        #fetch playlist_id to increment        
        sql_cmd = "select MAX(playlist_song_id) from MUSICON.playlist_song"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not fetch playlist_song_id from playlist_song table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            playlist_song_id = i[0]
        playlist_song_id = playlist_song_id+1
        
#extract song_id from songs table using song_name
        sql_cmd = "select song_id from MUSICON.songs where title = '"+title+"'"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not fetch song_id from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            song_id = i[0]
#extract playlist_id from playlists table using playlist_name
        sql_cmd = "select playlist_id from MUSICON.playlists where playlist_name = '"+playlist+"'"
        try:
            cur.execute(sql_cmd)
        except pymysql.Error as e:
            print("could not fetch song_id from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        for i in cur:
            playlist_id = i[0]
#tie the songs into playlists         
        sql_cmd = f"insert into MUSICON.playlist_song (playlist_song_id,playlist_id,song_id) values ('{playlist_song_id}','{playlist_id}','{song_id}')"
        print("SQL_CMD:",sql_cmd)
        try:
            cur.execute(sql_cmd)
            conn.commit()
            print("successfully added the songs into playlist_songs DB\n")
        except pymysql.Error as e:
            print("could not insert data into playlist_song table, error pymysql %d: %s" %(e.args[0], e.args[1]))         

#function to display the songs in the playlist using a for loop
    def display_songs_in_playlist(self,playlist):
# Iterate over all values of a dictionary 
# and print them one by one
# Check if key exist in dict or not
        if playlist in self.playlist_dict:
            for key, value in self.playlist_dict.items():
                if key == playlist:
                    print("Songs in the playlist are :",self.playlist_dict[playlist])
        else:
            print("Playlist doesn't exist in the list, please use option 6 to create a playlist")
        
        
            
#function to randomly shuffling the list of songs in the playlist by swapping the picked element with 
#the current element, and then picking the next random element from the remainder. The output is a random 
#permutation of the playlist.
    def shuffle_songs_in_the_playlist(self,playlist_name,playlist):
##sql query to extract playlist for the playlist name provided
        if (len(playlist) == 0) :
            playlist = self.get_songs_list_added_in_the_playlist_db(playlist_name)           
        print("playlist before shuffle :",playlist)
        tmp_playlist = deepcopy(playlist)
        length = len(tmp_playlist)
        while (length):
            length = length-1
            rand_num = randint(0, length)
            tmp_playlist[length], tmp_playlist[rand_num] = tmp_playlist[rand_num], tmp_playlist[length]
        print("playlist after shuffle :",tmp_playlist)
        self.playlist_songs_list = tmp_playlist
        return tmp_playlist

#function to loop the songs in the playlist 
    def loop_songs_in_the_playlist(self,playlist_name,playlist):
        #play the song, sleep for 5 seconds
        #once the song is done playing after 5 seconds before the next song starts 
        #put the song in a queue at the end
        #user Ctrl+C once they are done with the loops
        print("entered loop mode of the playlist")
        ##sql query to extract playlist for the playlist name provided
        if (len(playlist) == 0) :
            playlist = self.get_songs_list_added_in_the_playlist_db(playlist_name) 
            
        length = len(playlist)
        for title in playlist:
            self.enqueue_the_song_recently_played_into_start_of_the_queue(title)
        self.display_the_elements_of_the_loop_queue()
        temp=self.queue_head
        try:
            while temp is not None:
                print("\n\nplaying ",temp.data," ")
                Library.show_info_about_song_title_from_musicon_library(self,temp.data)
                #time.sleep(5)   # Delays for 5 seconds, just to replicate the song is playing
                self.play_individual_song_on_user_input(title)
                print("\ncompleted playing the song, pushing ",temp.data," to recently played stack")
                self.push_to_recently_played_stack(title,playlist_name)
            
                dequeued_title = self.dequeue_the_song_recently_played_in_playlist_to_enqueue()
                self.enqueue_the_song_recently_played_into_start_of_the_queue(dequeued_title)
                self.display_the_elements_of_the_loop_queue()
                temp=temp.next
        except KeyboardInterrupt:
            print("ending the loop mode of the playlist\n")

#function to play the songs in the playlist
    def play_songs_in_the_playlist(self,playlist_name,playlist_songs_list):
        if (len(playlist_songs_list) == 0):
            playlist_songs_list = self.get_songs_list_added_in_the_playlist_db(playlist_name)

## store the titles into a dictionary used to play normal mode.loop mode or shuffle mode           
        length = len(self.playlist_songs_list)
        print("length of playlist : ",length)
        for title in self.playlist_songs_list:
            Library.show_info_about_song_title_from_musicon_library(self,title)
            self.play_individual_song_on_user_input(title,playlist_name)
            while mixer.music.get_busy():
                pygame.time.wait(5)  # ms
                print ("Playing...")
        # infinite loop
            
#function to play individual song in the 
    def play_individual_song_on_user_input(self,title,playlist_name):
        print("playing ",title," ")
##fetch location of the song
        sql_cmd = "select location from MUSICON.songs where title = '"+title+"'"
        location = "/Users/praful/Documents/Harrisburg University Courses/Research Methodology/Final Project/songs/sample.mp3" 
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            records = cur.fetchall()
            ## Showing the data
            for record in records:
                location = record[0]  
        except pymysql.Error as e:
            print("could not fetch titles from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
        
        #location = "/Users/praful/Documents/Harrisburg University Courses/Research Methodology/Final Project/songs/sample.mp3"
        #print("playing "+title)
        #print("location: ",location)
        mixer.music.load(location)
        mixer.music.play()
        while True:
            print("Press 'p' to pause, 'r' to resume")
            print("Press 'e' to exit the program")
            query = input("  ")
            if query == 'p':
            # Pausing the music
                mixer.music.pause()     
            elif query == 'r':       
            # Resuming the music
                mixer.music.unpause()
            elif query == 'e':
            # Stop the mixer
                mixer.music.stop()
                break
        #time.sleep(5)# Delays for 5 seconds, just to replicate the song is playing
        #place the song into a recently played stack
        print("completed playing the song, pushing ",title," to recently played stack DB \n")
        self.push_to_recently_played_stack(title,playlist_name)
                    
# pushes/appends an element to the recently played stack    
    def push_to_recently_played_stack(self,title,playlist_name): 
#fetch song_id
        sql_cmd = "select song_id from MUSICON.songs where title = '"+title+"'"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            songs = cur.fetchall()
            ## Showing the data
            for song in songs:
                song_id = song[0] 
        except pymysql.Error as e:
            print("could not fetch song_id from songs table, error pymysql %d: %s" %(e.args[0], e.args[1]))
#fetch playlist id
        sql_cmd = "select playlist_id from MUSICON.playlists where playlist_name = '"+playlist_name+"'"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            playlists = cur.fetchall()
            ## Showing the data
            for playlist in playlists:
                playlist_id = playlist[0] 
        except pymysql.Error as e:
            print("could not fetch playlist_id from playlists table, error pymysql %d: %s" %(e.args[0], e.args[1]))
#fetch user id
        sql_cmd = "select user_id from MUSICON.users where user_name = '"+self.user_name+"'"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            users = cur.fetchall()
            ## Showing the data
            for user in users:
                user_id = user[0] 
        except pymysql.Error as e:
            print("could not fetch user_id from users table, error pymysql %d: %s" %(e.args[0], e.args[1]))
#insert statement into recently played stack 
        sql_cmd = f" insert into recently_played_stack values(NULL,{song_id},{playlist_id},{user_id});"
        try:
            cur.execute(sql_cmd) 
            conn.commit()
        except pymysql.Error as e:
            print("could not insert into recently_played_stack table, error pymysql %d: %s" %(e.args[0], e.args[1]))

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
        #fetch recently played stack songs
        #sql_cmd = "select s.title,u.user_name,pl.playlist_name from recently_played_stack as rps , songs as s, users as u where u.user_id = rps.user_id and rps.song_id = s.song_id and  u.user_name = '"+self.user_name+"' order by recently_played_stack_id DESC" 
        sql_cmd = "select s.title,u.user_name,pl.playlist_name from playlists as pl,recently_played_stack as rps , songs as s, users as u where u.user_id = rps.user_id and rps.song_id = s.song_id and rps.playlist_id = pl.playlist_id and u.user_name = '"+self.user_name+"' order by recently_played_stack_id DESC"
        try:
            cur.execute(sql_cmd)
            ## fetching all records from the 'cursor' object
            recent_list = cur.fetchall()
            ## Showing the data
            if (len(recent_list) == 0):
                print("there are no songs that were played recently by the user \"",self.user_name,"\" \n")
            else:
                print("Songs played Most Recent to Least recent\n\n\n")
                print ("user_name    song_name     playlist_name\n")
                print ("------------------------------------------\n")
                for rl in recent_list:
                    print (rl[1],"   ",rl[0],"        ",rl[2])
        except pymysql.Error as e:
            print("could not fetch user_id from users table, error pymysql %d: %s" %(e.args[0], e.args[1]))


#Queue is a collection of objects that are inserted and removed using the first in first out principle. 
#Insertion is done at the back of the queue and elements are deleted from the front location of the queue.
# enqueue operation used to push the titles in a playlist to run in loop mode
    def enqueue_the_song_recently_played_into_start_of_the_queue(self, data):
        if self.queue_tail is None:
            self.queue_head = Node(data)
            self.queue_tail = self.queue_head
        else:
            self.queue_tail.next = Node(data)
            self.queue_tail.next.prev = self.queue_tail
            self.queue_tail = self.queue_tail.next
    
# dequeue operation used to pop the element and 
    def dequeue_the_song_recently_played_in_playlist_to_enqueue(self):
        if self.queue_head is None:
            return None
        else:
            temp = self.queue_head.data
            self.queue_head = self.queue_head.next
            self.queue_head.prev=None
            return temp
        
#display the elements of the loop queue
    def display_the_elements_of_the_loop_queue(self):  
        print("queue elements are:")
        temp=self.queue_head
        while temp is not None:
            print(temp.data,end="<-")
            temp=temp.next


# #### Functionality to Display MENU for ADMINS/USERS

# In[4]:


# function to display menu for the users     
def print_menu():    
    print(30 * "-" , "MUSICON" , 30 * "-")
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

#def musicon():
    playlist = Playlist()
    library = Library()
    
    library.user_name = input("\nplease enter your user name: ")
    playlist.user_name = library.user_name
    user_id = playlist.check_if_user_exists_in_users_table(library.user_name)
    if (user_id == "") :
        print ("\n")
    else:
        admin_flag = playlist.check_if_user_is_admin_in_users_table(library.user_name)
    if (admin_flag):
        print ("you will have access to admin menu to add new/delete/browse/user preferences and all opearations \n")
    else :
        print ("you will have to access to user menu to create playlist,play songs and various search/display operations\n")
    
    loop=True      
    #while loop that goes on forever until exited 
    while loop:
        #print_menu()
        choice = int(input("\nSelect one among these Options [1-11] or 0 for menu : ",))
        if choice==0:
            print(30 * "-" , "MUSICON" , 30 * "-")
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
        if choice==1:
            if (admin_flag):
                print("\nyou chose to add a new song to the existing library\n\n")
                title = input("\nplease enter the song title : ")
                artist = input("please enter the song artist : ")
                length = input("\nplease enter the song length : ")
                genre = input("\nplease enter the song genre : ")
                year = int(input("\nplease enter the song year : "))
                lyrics = input("\nplease enter the song lyrics : ")
                album_name = input("\nplease enter the song album name: ")
                library.add_song_attributes_into_library_list(artist,title,length,genre,year,lyrics,album_name)
            else:
                print(Fore.RED + "you don't have access to add songs to library, contact admins\n")
                
        elif choice==2:
            if (admin_flag):
                print("you chose to delete a song from the existing library\n")
                title = input("\nplease enter the song title : ")
                check,count = library.check_if_title_exists_in_musicon_library(title)
                if (check or count):
                    library.delete_song_attributes_from_library_with_title_name(title)
                else:
                    print("title is not present in library to delete\n")
            else:
                print(Fore.RED + "you don't have access to delete songs from library, contact admins\n")

        elif choice==3:
            print("you chose to see all songs present in existing library\n")
            library.show_all_titles_present_in_musicon_library()
            
        elif choice==4:
            print("you chose option to search for songs of an Artist in library\n")
            #check for songs in library
            song_artist = input("please enter the artist name : ")
            library.searching_for_titles_in_musicon_library_by_artist(song_artist)

        elif choice==5:
            print("you chose option to play a song in library\n")
            #check for songs in library
            song_title = input("please enter the song title : ")
            check,count = library.check_if_title_exists_in_musicon_library(song_title)
            if (check,count):
                library.show_info_about_song_title_from_musicon_library(song_title)
                playlist.play_individual_song_on_user_input(song_title,"generic")
            else:
                print(title," doesn't exist in the library, please use option 1 to add song to the library")

        elif choice==6:
            print("you chose to create a new Playlist\n")
            playlist_name = input("please enter the name of the playlist: ")
            user_name = input("please enter the user_name to tie the playlist: ")
            playlist.create_a_new_playlist(playlist_name,user_name)

        elif choice==7:
            print("Display Playlists in the Library\n")
            playlist.display_existing_playlists()

        elif choice==8:
            print("you chose to add songs to the playlist \n")
            #print("list of playlist available in libarary are : \n")
            playlist.display_existing_playlists()
            #show all the available titles for users reference        
            library.show_all_titles_present_in_musicon_library()
            print("select a play list to add songs and enter the playlist name\n")
            playlist_name = input("please enter the name of the playlist: ")
            #display_song_present_in_the_library
            print("enter song name to add to the playlist ",playlist_name)
            title_name = input("please enter the name of the song: ")
            playlist.add_song_into_playlist_dictionary(playlist_name,title_name)
            while(1):
                add_more = input("want to add more songs into playlist y/n\n")
                if(add_more == 'n'):
                    break;
                else:
                    print("enter song name to add to the playlist ",playlist_name)
                    title_name = input("please enter the name of the song name: ")
                    playlist.add_song_into_playlist_dictionary(playlist_name,title_name)

        elif choice==9:
            print("you choose to play songs in the playlist\n")
            print("list of playlist available in libarary are : \n")
            playlist.display_existing_playlists()
            print("select a play list to play and enter the playlist name\n")
            playlist_name = input("please enter the name of the playlist: ")
            playlist_mode = int(input("please select the mode you like to choose :\n1.normal\n2.shuffle\n3.loop\n"))
            if (playlist_mode == 1):
                playlist.play_songs_in_the_playlist(playlist_name,playlist.playlist_songs_list)
            elif (playlist_mode == 2):
                shuffled_playlist = playlist.shuffle_songs_in_the_playlist(playlist_name,playlist.playlist_songs_list)
                while(1):
                    shuffle_again = input("do you wish to shuffle the playlist again -- y/n?")
                    if shuffle_again == 'y':
                        shuffled_playlist = playlist.shuffle_songs_in_the_playlist(playlist_name,shuffled_playlist)
                    elif shuffle_again == 'n':
                        break;
                playlist.play_songs_in_the_playlist(playlist_name,playlist.playlist_songs_list)
            elif (playlist_mode == 3):
                playlist.loop_songs_in_the_playlist(playlist_name,playlist.playlist_songs_list)
            else:
                playlist.play_songs_in_the_playlist(playlist_name,playlist.playlist_songs_list)

        elif choice==10:
            print("you chose an option to see Recently played Songs from the Library\n")
            playlist.display_songs_in_recently_played_stack()
            recent_play = input("do you wish to play a song from the recently played list y/n?")            
            if (recent_play == 'y'):
                recent_title_name = input("please enter the name of the song: ")
                print("\nplaying the song selected from recent played stack ",recent_title_name)
                library.show_info_about_song_title_from_musicon_library(recent_title_name)
                playlist.play_individual_song_on_user_input(recent_title_name,"rerun")
            elif (recent_play == 'n'):
                print("No selection happened , leaving ")

        elif choice==11:
            print("Exit option selected, exiting from 'MUSICON' ")

            loop=False # This will make the while loop to end as value of loop is set to False
        else:
                # Any integer inputs other than values 1-12 we print an error message
            print("Wrong option selection. Enter any key to try again..") 


# In[ ]:


print_menu()


# In[ ]:




