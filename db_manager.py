import sqlite3 as sql
from sqlite3 import Error as sqlError
def main():
    con = sql.connect('world.db')
    cur = con.cursor()

    while True:
        t = input("Type (c: Commit action (ex: INSERT), nc: Don't commit (ex: SELECT), q: quit): ")

        if t == 'c':
            commit_action(input("Command: "), cur, con)
        elif t == 'nc':
            nc_action(input("Command: "), cur)
        elif t == 'q':
            con.close()
            return


def commit_action(action: str, cur: sql.Cursor, con: sql.Connection) -> None:
    try:
        nc_action(action, cur)
        con.commit()
    except sqlError as e:
        print(e)
        

def nc_action(action: str, cur: sql.Cursor) -> None:
    try:
        cur.execute(action)
        print(cur.fetchall())
    except sqlError as e:
        print(e)
        
if __name__ == "__main__":
    main()