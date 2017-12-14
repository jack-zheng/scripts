import svn.local
import sqlite3
import config
from os.path import join
from os import walk
import svn.remote
from datetime import datetime

def main():
    # do some enhance, fetch log and record in loop will cost a lot of time. try batch fetch 
    r = svn.remote.RemoteClient(config.svn_addr, username=config.svn_username, password=config.svn_pwd)
    
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    sql = '''select entry_id, file_path from svn_files_info'''
    c.execute(sql)
    rows = c.fetchall()
    
    start = datetime.now()
    for row in rows:
        logs = r.log_default(rel_filepath=row[1])
        for log in logs:
            sql = '''INSERT INTO SVN_LOG_ENTRY VALUES (?, ?, ?, ?, ?)'''
            comment = log.msg
            values = (row[0], log.date.timestamp(), "NA" if comment is None else comment.encode("utf-8"), log.revision, log.author)
            c.execute(sql, values)
            print('insert record id: %s' % row[0])

    conn.commit()
    conn.close()      

    end = datetime.now()
    print('Time Cost: %s' % (end-start)total_seconds)


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

