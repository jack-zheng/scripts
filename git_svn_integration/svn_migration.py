import svn.local
import sqlite3
import config
from os.path import join
from os import walk

def main():
    insert_record_to_info()

def build_svn_info_sql(file_name, file_path):
    return "INSERT INTO SVN_FILES_INFO (FILE_NAME, FILE_PATH) VALUES ('{}', '{}')".format(file_name, file_path)

def insert_record_to_info():
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    
    for dir, subdir, files in walk(config.svn_src):
            for file in files:
                c.execute(build_svn_info_sql(file, join(dir, file).replace(config.svn_prefix, '.').replace('\\', '/')))
   
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()

