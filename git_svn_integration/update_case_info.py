import config
import sqlite3
from datetime import datetime


def main():
    start = datetime.now()
    # loop each record in case_info table get file_name
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    sql = '''SELECT FILE_NAME FROM SVN_FILES_INFO'''
    c.execute(sql)
    rows = c.fetchall()

    # search file name in svn_log_entry table and get the original author and create date update to case_info table
    for row in rows:
        print('file: %s in processing...' % row[0])
        sql_get_info = '''SELECT AUTHOR, DATE, REVISION FROM SVN_LOG_ENTRY WHERE ENTRY_ID =
                 (SELECT ENTRY_ID FROM SVN_FILES_INFO WHERE FILE_NAME = ?)
                 ORDER BY REVISION ASC LIMIT 1'''
        c.execute(sql_get_info, (row[0],))
        info = c.fetchone()
        print('fetched log entry[author=%s, date=%s, revision=%s]' % (info[0], info[1], info[2]))
        
        sql_update_info = '''UPDATE CASE_INFO SET AUTHOR=?, CREATE_DATE=? WHERE FILE_NAME=?'''
        c.execute(sql_update_info, (info[0], info[1], row[0]))

    conn.commit()
    conn.close()

    end = datetime.now()
    print("Time Cost: %s" % (end-start).total_seconds())
    
if __name__ == '__main__':
    main()
