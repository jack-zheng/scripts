import config
import sqlite3
import os
from os import walk
from os.path import join
from datetime import datetime

def main():
	start = datetime.now()

	name_path_dict = {}
	# create a dict store name: path relationship
	for dir, subdir, files in walk(config.git_repo + '/src'):
		for file in files:
			name_path_dict[file] = join(dir, file)

	# query file name from db
	conn = sqlite3.connect(config.db_path)
	c = conn.cursor()
	sql = '''SELECT FILE_NAME FROM CASE_INFO'''
	c.execute(sql)
	rows = c.fetchall()
	
	# update file path to case info table
	for row in rows:
		name = row[0]
		path = name_path_dict[name].replace(config.git_repo, '.')
		print('%s, %s' % (name, path))
		update_sql = '''UPDATE CASE_INFO SET FILE_PATH = ? WHERE FILE_NAME = ?'''
		print('sql executing...')
		c.execute(update_sql, (path, name))

	conn.commit()
	conn.close()
	print('Finish Update !')
	
	end = datetime.now()
	print('Time Cost: %s' % (end - start).total_seconds())

if __name__ == '__main__':
	main()
