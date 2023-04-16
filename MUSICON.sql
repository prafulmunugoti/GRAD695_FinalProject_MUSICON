{\rtf1\ansi\ansicpg1252\cocoartf2709
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;\f1\froman\fcharset0 TimesNewRomanPSMT;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\csgray\c0;}
\margl1440\margr1440\vieww28600\viewh15060\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
\'97 Database creation \'97 \
\
DROP DATABASE IF EXISTS MUSICON;\
CREATE DATABASE IF NOT EXISTS MUSICON;\
\
USE MUSICON;\
\
\'97 DROP STATEMENTS to delete any existing tables\
\
DROP TABLE IF EXISTSMUSICON.artists;\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 DROP TABLE IF EXISTS MUSICON.albums;\
DROP TABLE IF EXISTS MUSICON.users;\
DROP TABLE IF EXISTS MUSICON.playlists;\
DROP TABLE IF EXISTS MUSICON.songs;\
DROP TABLE IF EXISTS MUSICON.interactions;\
DROP TABLE IF EXISTS MUSICON.playlist_song;\
DROP TABLE IF EXISTS MUSICON.recently_played_stack;\
\
\'97 CREATE STATEMENTS to create tables\
\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 CREATE TABLE IF NOT EXISTS MUSICON.artists ( \
artist_id int AUTO_INCREMENT, \
artist_name varchar(255), \
artist_image BLOB, \
created_dt timestamp, \
updated_dt timestamp, \
primary key(artist_id) );\
\
GRANT SELECT ON artists TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.albums ( \
album_id int, \
artist_id int, \
album_name varchar(255), \
album_cover BLOB, \
created_dt timestamp, \
updated_dt timestamp, \
primary key(album_id), \
FOREIGN KEY (artist_id) REFERENCES artists(artist_id) on delete cascade \
);\
\
GRANT SELECT ON albums TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.users ( \
user_id int, \
user_name varchar(255), \
user_email varchar(255), \
user_password varchar(255), \
is_admin varchar(10), \
preferences text, \
created_dt timestamp, \
updated_dt timestamp, \
primary key(user_id) \
);\
\
GRANT SELECT, UPDATE, INSERT ON users TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.playlists ( \
playlist_id int, \
user_id int, \
playlist_name varchar(255), \
songs_count int, \
created_dt timestamp, \
updated_dt timestamp, \
primary key(playlist_id), \
FOREIGN KEY (user_id) REFERENCES users(user_id) on delete cascade \
);\
\
GRANT SELECT, INSERT, UPDATE ON playlists TO public\
\
\
CREATE TABLE IF NOT EXISTS MUSICON.songs ( \
song_id int AUTO_INCREMENT, \
album_id int, \
artist_id int, \
title varchar(255), \
length float, \
track varchar(255), \
year int, \
genre varchar(10), \
location text, \
lyrics text, \
created_dt timestamp, \
updated_dt timestamp, \
primary key(song_id), \
FOREIGN KEY (artist_id) REFERENCES artists(artist_id) on delete cascade, \
FOREIGN KEY (album_id) REFERENCES albums(album_id) on delete cascade\
);\
\
GRANT SELECT ON songs TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.interactions ( \
interaction_id int, \
user_id int, \
song_id int, \
liked boolean, \
play_count int, \
mode_played varchar(255), \
created_dt timestamp, \
updated_dt timestamp, \
session_id int, \
PRIMARY KEY (interaction_id), \
FOREIGN KEY (user_id) REFERENCES users(user_id) on delete cascade, \
FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade \
);\
\
GRANT SELECT, UPDATE, INSERT ON interactions TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.playlist_song ( \
playlist_song_id int, \
playlist_id int, \
song_id int, \
PRIMARY KEY (playlist_song_id), \
FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) on delete cascade, \
FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade \
); \
\
GRANT SELECT, UPDATE, INSERT ON playlist_song TO public;\
\
CREATE TABLE IF NOT EXISTS MUSICON.recently_played_stack ( \
recently_played_stack_id int NOT NULL AUTO_INCREMENT, \
song_id int, \
playlist_id int, \
user_id varchar(20),\
PRIMARY KEY (recently_played_stack_id), \
FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) on delete cascade, \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 FOREIGN KEY (user_id) REFERENCES users(user_id) on delete cascade, \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 FOREIGN KEY (song_id) REFERENCES songs(song_id) on delete cascade ); \
\
GRANT SELECT, UPDATE, INSERT ON recently_played_stack TO public;\
\
\'97 INSERT statements into the users table\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf2 \CocoaLigature0 INSERT INTO MUSICON.users VALUES(\'911\'92,\'92user1\'92,\'92user1@gmail.com\'92,\'92user1\'92,\'92 no\'92,\'92NULL\'92,\'922023-04-03 11:56:46\'92,\'922023-04-03 11:56:46\'92);\
INSERT INTO MUSICON.users VALUES((\'912', 'user2','user2@gmail.com', 'user2',' no', 'NULL','2023-04-03 11:57:08','2023-04-03 11:57:08\'92);\
INSERT INTO MUSICON.users VALUES('3','user3','user3@gmail.com','user3',' no','NULL','2023-04-03 11:57:23','2023-04-03 11:57:23\'92);\
INSERT INTO MUSICON.users VALUES((\'911111','generic','generic@gmail.com','generic','no','NULL','2023-04-03 22:36:57','2023-04-03 22:36:57\'92);\
INSERT INTO MUSICON.users VALUES(\'919999','praful','praful2807@gmail.com','praful','yes','NULL','2023-03-31 21:56:26','2023-03-31 21:56:26\'92);\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \CocoaLigature1 \
\'97 INSERT statements into artists table\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf2 \CocoaLigature0 INSERT INTO MUSICON.artists VALUES(\'911\'92,\'92Ed Sheeran\'92,\'920x4E554C4C\'92,\'922023-03-31 23:28:24\'92,\'922023-03-31 23:28:24\'92);\
INSERT INTO MUSICON.artists VALUES('2','Eminem','0x4E554C4C','2023-03-31 23:28:47','2023-03-31 23:28:47\'92);\
INSERT INTO MUSICON.artists VALUES(\'913\'92,\'92Shakira','0x4E554C4C','2023-03-31 23:29:03','2023-03-31 23:29:03\'92);\
INSERT INTO MUSICON.artists VALUES('4','Jennifer Lopez','0x4E554C4C','2023-03-31 23:29:30','2023-03-31 23:29:30\'92);\
INSERT INTO MUSICON.artists VALUES('5','Justin Bieber','0x4E554C4C','2023-03-31 23:29:55','2023-03-31 23:29:55\'92);\
INSERT INTO MUSICON.artists VALUES('6','Jonas brothers','0x4E554C4C','2023-03-31 23:30:28','2023-03-31 23:30:28\'92);\
INSERT INTO MUSICON.artists VALUES('7','Imagine Dragons','0x4E554C4C','2023-04-01 15:10:37','2023-04-01 15:10:37\'92);\
\
\'97- INSERT statements into albums table \
\
INSERT INTO MUSICON.albums VALUES(\'911\'92,\'921\'92,\'92collaborations','NULL','2023-03-31 23:34:58 ','2023-03-31 23:34:58\'92);\
INSERT INTO MUSICON.albums VALUES('2','1','divide','NULL','2023-03-31 23:36:30','2023-03-31 23:36:30');\
INSERT INTO MUSICON.albums VALUES('3','1','tour edition','NULL','2023-03-31 23:37:29','2023-03-31 23:37:29');\
INSERT INTO MUSICON.albums VALUES('4','2','recovery','NULL','2023-03-31 23:53:35','2023-03-31 23:53:35');\
INSERT INTO MUSICON.albums VALUES('5','2','encore','NULL','2023-03-31 23:54:02','2023-03-31 23:54:02');\
INSERT INTO MUSICON.albums VALUES('6','7','evolve','NULL','2023-04-01 15:13:12','2023-04-01 15:13:12');\
\
\'97- INSERT statements into playlists table\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f1\fs26 \cf0 \CocoaLigature1 \
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs24 \cf2 \CocoaLigature0 INSERT INTO MUSICON.playlists VALUES(\'920\'92,\'921\'92,\'92generic','1','2023-04-03 22:37:45','2023-04-03 22:37:45\'92);\
INSERT INTO MUSICON.playlists VALUES('1','1','user1_playlist1','3','2023-04-03 13:02:14','2023-04-03 16:25:02\'92);\
INSERT INTO MUSICON.playlists VALUES('2','1','user1_playlist2','0','2023-04-03 13:23:52','2023-04-03 13:23:52\'92);\
INSERT INTO MUSICON.playlists VALUES('3','2','user2_playlist1','0','2023-04-03 13:24:18','2023-04-03 13:24:18\'92);\
INSERT INTO MUSICON.playlists VALUES('4','3','user3_playlist1','0','2023-04-03 13:24:48','2023-04-03 13:24:48\'92);\
INSERT INTO MUSICON.playlists VALUES('99','1','rerun','1','2023-04-04 00:17:41','2023-04-04 00:17:41\'92);
\f1\fs26 \cf0 \CocoaLigature1 \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
\'97-  INSERT statements into songs table\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf2 \CocoaLigature0 INSERT INTO MUSICON.songs VALUES('1','1','1','beautiful people','3.18','NULL','2019\'92,\'92pop',' <project_path>/songs/beautiful people.mp3',' ','2023-03-31 23:44:19 ','2023-03-31 23:44:19\'92);\
INSERT INTO MUSICON.songs VALUES('2','1','1','i dont care','3.4','NULL','2019','pop',' <project_path>/songs/i dont care.mp3',' ','2023-03-31 23:45:32','2023-03-31 23:45:32\'91);\
INSERT INTO MUSICON.songs VALUES('3','1','1','1000 nights','3.31',' NULL','2019','pop',' <project_path>/songs/1000 nights.mp3',' ','2023-03-31 23:46:17','2023-03-31 23:46:17\'91);\
INSERT INTO MUSICON.songs VALUES('4','2','1','perfect','4.25',' NULL','2017','pop',' <project_path>/songs/perfect.mp3',' ','2023-03-31 23:47:59 ','2023-03-31 23:47:59\'91);\
INSERT INTO MUSICON.songs VALUES('5','2','1','shape of you','3.51',' NULL','2017','pop',' <project_path>/songs/ShapeOfYou.mp3',' ','2023-03-31 23:48:41 ','2023-03-31 23:48:41\'91);\
INSERT INTO MUSICON.songs VALUES('6','2','1','galway girl','3.51',' NULL','2017','pop',' <project_path>/songs/Galway Girl.mp3',' ','2023-03-31 23:49:13 ','2023-03-31 23:49:13\'91);\
INSERT INTO MUSICON.songs VALUES(\'927\'92,\'923','1','shivers','3.27',' NULL',' 2021','pop',' <project_path>/songs/shivers.mp3',' ','2023-03-31 23:50:26 ','2023-03-31 23:50:26\'91);\
INSERT INTO MUSICON.songs VALUES('8','3','1','bad habits','3.52',' NULL','2021','pop',' <project_path>/songs/bad habits.mp3',' ','2023-03-31 23:50:54 ','2023-03-31 23:50:54\'91);\
INSERT INTO MUSICON.songs VALUES('9','4','2','not afraid','4.09',' NULL','2010',' rap',' <project_path>/songs/not afraid.mp3',' ','2023-03-31 23:55:58 ','2023-03-31 23:55:58\'91);\
INSERT INTO MUSICON.songs VALUES('10\'92,\'924\'92,\'922','love the way you lie','4.24',' NULL','2010',' rap',' <project_path>/songs/love the way you lie.mp3',' ','2023-03-31 23:56:38 ','2023-03-31 23:56:38\'92);\
INSERT INTO MUSICON.songs VALUES('11','6','7','Believer','3.14',' NULL','2017','pop rock',' <project_path>/songs/Believer.mp3',' ',' 2023-04-01 15:09:46 ','2023-04-01 15:09:46\'92);\cf0 \CocoaLigature1 \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \
\'97- INSERT statements into playlist_song table\
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf2 \CocoaLigature0 INSERT INTO MUSICON.playlist_song VALUES(\'911\'92,\'921\'92,\'921\'92);\
INSERT INTO MUSICON.playlist_song VALUES(\'912\'92,\'921\'92,\'924\'92);\
INSERT INTO MUSICON.playlist_song VALUES(\'913\'92,\'921\'92,\'928\'92);\
INSERT INTO MUSICON.playlist_song VALUES(\'914\'92,\'921\'92,\'925\'92);\cf0 \CocoaLigature1 \
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \
\'97- INSERT statements into recently_played_stack table \
\
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0
\cf2 \CocoaLigature0 INSERT INTO MUSICON.recently_played_stack VALUES(\'911\'92,\'921\'92,\'920\'92,\'921111\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES(\'913\'92,\'924\'92,\'920\'92,\'921\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('4','4','0','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('5','1','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('6','4','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('7','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('8','8','99','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('9','4','0','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('10','2','0','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('11','2','99','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('12','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('13','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('14','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('15','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('16','1','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('17','8','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('18','4','1','1\'92);\
INSERT INTO MUSICON.recently_played_stack VALUES('19','8','1','1\'92);\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 \CocoaLigature1 \
\
\
\
\
\
\
\
\
\
}