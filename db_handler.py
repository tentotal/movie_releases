#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

def create_table():
	conn = sqlite3.connect('etolol.db')
	c = conn.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS Users(user_id INT PRIMARY KEY, stage TEXT, movies_list TEXT)")
	conn.commit()
	c.close()
	conn.close()

def add_user(user_id):
	try:
		conn = sqlite3.connect('etolol.db')
		c = conn.cursor()
		c.execute("INSERT INTO Users (user_id) VALUES (?)", (user_id,))
		print('User id was added')
		conn.commit()
		c.close()
		conn.close()
	except Exception as e: 
		print('User id was not added.', e)

def set_stage(stage, user_id):
	try:
		conn = sqlite3.connect('etolol.db')
		c = conn.cursor()
		c.execute("UPDATE Users SET stage=? WHERE user_id=?", (stage, user_id))
		print('Stage was changed: ' + stage)
		conn.commit()
		c.close()
		conn.close()
	except Exception as e:
		print('Stage was changed.', e)

def get_stage(user_id):
	try:
		conn = sqlite3.connect('etolol.db')
		c = conn.cursor()
		c.execute('SELECT stage FROM Users WHERE user_id=?', (user_id,))
		data = c.fetchone()[0]
		print('Stage was selected: ' + data)
		conn.commit()
		c.close()
		conn.close()
		return data
	except Exception as e:
		print('Stage was not selected.', e)


def update_movie_list(movies_list, user_id):
	try:
		conn = sqlite3.connect('etolol.db')
		c = conn.cursor()
		c.execute("UPDATE Users SET movies_list=? WHERE user_id=?", (movies_list, user_id))
		print('Movie list was updated')			
		conn.commit()
		c.close()
		conn.close()
	except Exception as e:
		print('Movie list was not updated.', e)

def get_movie_list(user_id):
	try:
		conn = sqlite3.connect('etolol.db')
		c = conn.cursor()
		c.execute('SELECT movies_list FROM Users WHERE user_id=?', (user_id,))
		print('Movie list was selected')
		data = c.fetchone()[0]
		conn.commit()
		c.close()
		conn.close()
		return data
	except Exception as e: 
		print('Movie list was not selected.', e)	
	

if __name__ == '__main__':
	create_table()
	add_user(2)
	update_movie_list('test2', 2)