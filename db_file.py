from sqlite3 import connect

"""
Jira database
Name of the table: issues
Columns: id (AUTOINCREMENT); key.
Query: CREATE TABLE issues (id INTEGER PRIMARY KEY AUTOINCREMENT, key VARCHAR(32));

Questions:

How to get all data from table ? 
Query: SELECT * FROM issues;

How to get last updated from table ?
Query: SELECT key FROM issues ORDER BY id DESC LIMIT 1;
"""

conn = connect(database="jira_database.sqlite")
cur = conn.cursor()

# cur.execute(f"INSERT INTO issues (key) VALUES ();")
# cur.execute("DELETE FROM issues;")
# cur.execute("SELECT key FROM issues;")
# conn.commit()
if __name__ == '__main__':
    print([x[0] for x in cur.fetchall()])