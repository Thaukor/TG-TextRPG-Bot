import datetime
import time
import sqlite3 as sql
from sqlite3 import Error as sqlError
import os
from typing import Tuple

def main():
    con = sql.connect('world.db')
    cur = con.cursor()

    while True:
        t = input("Type (c: Commit action (ex: INSERT), nc: Don't commit (ex: SELECT), init: Recreate a base DB q: quit): ")

        if t == 'c':
            commit_action(input("SQLite Command: "), cur, con)
        elif t == 'nc':
            cmd = input("SQLite Command: ")
            nc_action(cmd, cur)
        elif t == "init":
            con.close()
            if input("Are you sure you want to reset and reinitialize the database? A backup will be created. (y/n)").lower() == 'y':
                con, cur = init()
                print("Done! Restart bot to use the new database.")
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
        
def init() -> Tuple[sql.Connection, sql.Cursor]:
    print("Creating backup")
    if os.path.exists("world.db"):
        os.rename("world.db", f"world {time.time()}.db")
    con = sql.connect('world.db')
    cur = con.cursor()

    print("Creating tables")
    tables = """
    CREATE TABLE 'classes'
    (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    );

    CREATE TABLE 'starter_stats'
    (
        class_id INTEGER,
        hp INTEGER,
        base_damage INTEGER,
        base_armour INTEGER,
        resources INTEGER,
        resource_regen INTEGER,

        FOREIGN KEY(class_id) REFERENCES classes(id)
    );

    CREATE TABLE 'skills'
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER,
        level_req INTEGER,
        base_damage INTEGER,
        cooldown INTEGER,
        resource_cost INTEGER,
        name TEXT,
        description TEXT,
        FOREIGN KEY(class_id) REFERENCES classes(id)
    );
    
    CREATE TABLE 'pjs' 
    (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        class_id INTEGER,
        user_id INTEGER,

        FOREIGN KEY(class_id) REFERENCES classes(id) 
    );
    
    CREATE TABLE 'pjs_stats' (
        pj_id INTEGER,
        level INTEGER,
        exp INTEGER,
        hp INTEGER,
        base_damage INTEGER,
        base_armour INTEGER,
        resources INTEGER,
        resource_regen INTEGER,

        FOREIGN KEY(pj_id) REFERENCES pjs(id)
    );
    """

    data = """INSERT INTO 'classes' VALUES 
    (
        1,
        'Warrior',
        'A melee, tanky class that uses rage as resource. They attacks get stronger the longer the fights drags on, their AoE damage is high as their resistances to damage. They struggle against strong, single targets, but their resilience and taunts make them excelent meat shields while other classes deal with their targets.'
    );

    INSERT INTO 'classes' VALUES 
    (
        2,
        'Mage',
        'A ranged class with a very high damage potential. They have excelente single target bursts, excelent crowd control and they are able to empower their allies. They HP and resistances are low, so they are not good at soloing'
    );

    INSERT INTO 'classes' VALUES 
    (
        3,
        'Archer',
        'A ranged class with a medium damage potential, which combines a good AoE damage and single target burst. They don''t shine in any area, neither they fall short on any. They are good at soloing and as a constant damage source for their teams. They, alongside their team, can find more pickups at the of each battle.'
    );

    INSERT INTO 'starter_stats' VALUES
    (
        1,
        20,
        3,
        1,
        10,
        3
    );

    INSERT INTO 'skills' VALUES
    (
        1,
        1,
        0,
        1,
        0,
        -2,
        'Attack',
        'Warriors basic attack. Generates rage.'
    );
    """

    try:
        cur.executescript(tables)
        print("Adding data")
        cur.executescript(data)
    except sqlError as e:
        print(e)

    return con, cur

if __name__ == "__main__":
    main()