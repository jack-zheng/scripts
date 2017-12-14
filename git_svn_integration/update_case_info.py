import config
import sqlite3


def main():
    # loop each record in case_info table get file_name
    conn = sqlite3.connect(config.db_path)
    c = conn.cursor()
    sql = '''SELECT FILE_NAME FROM CASE_INFO'''
    c.execute(sql)
    rows = c.fetchall()

    # search file name in svn_log_entry table and get the original author and create date update to case_info table
    
    
if __name__ == '__main__':
    main()
