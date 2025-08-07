import sqlite3
import time
import os

DB_WITH_CONSTRAINT = 'with_constraint.db'
DB_NO_CONSTRAINT = 'no_constraint.db'
TABLE_NAME = 'test_table'
NUM_ROWS = 1000000

def setup_db(db_name, with_constraint):
    if os.path.exists(db_name):
        os.remove(db_name)
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    if with_constraint:
        cur.execute(f'''
            CREATE TABLE {TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                value INTEGER,
                name TEXT,
                status TEXT,
                email TEXT,
                created_at TEXT,
                CHECK (value >= 0 AND value <= 100),
                CHECK (length(name) > 0 AND length(name) <= 50),
                CHECK (status IN ('active', 'inactive', 'pending')),
                CHECK (email LIKE '%_@__%.__%'),
                CHECK (created_at LIKE '____-__-__T__:__:__%')
            )
        ''')
    else:
        cur.execute(f'''
            CREATE TABLE {TABLE_NAME} (
                id INTEGER PRIMARY KEY,
                value INTEGER,
                name TEXT,
                status TEXT,
                email TEXT,
                created_at TEXT
            )
        ''')
    conn.commit()
    conn.close()

def time_inserts(db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    start = time.time()
    statuses = ['active', 'inactive', 'pending']
    for i in range(NUM_ROWS):
        value = i % 101
        name = f'Name_{i}'
        status = statuses[i % len(statuses)]
        email = f'user{i}@example.com'
        # ISO 8601 format: YYYY-MM-DDTHH:MM:SS
        created_at = f"2025-08-{(i % 28) + 1:02d}T{(i % 24):02d}:{(i % 60):02d}:{(i % 60):02d}"
        cur.execute(
            f'INSERT INTO {TABLE_NAME} (value, name, status, email, created_at) VALUES (?, ?, ?, ?, ?)',
            (value, name, status, email, created_at)
        )
    conn.commit()
    end = time.time()
    conn.close()
    return end - start

def main():
    print('Setting up databases...')
    setup_db(DB_WITH_CONSTRAINT, True)
    setup_db(DB_NO_CONSTRAINT, False)

    print('Timing inserts WITH constraint...')
    time_with = time_inserts(DB_WITH_CONSTRAINT)
    print(f'Insert time with constraint: {time_with:.2f} seconds')

    print('Timing inserts WITHOUT constraint...')
    time_without = time_inserts(DB_NO_CONSTRAINT)
    print(f'Insert time without constraint: {time_without:.2f} seconds')

    print(f'\nSummary ({NUM_ROWS:,} Rows):')
    print(f'With constraint: {time_with:.2f} s')
    print(f'Without constraint: {time_without:.2f} s')
    print(f'Difference: {time_with - time_without:.2f} s')

    print('\nPer 100 Rows:')
    print(f'With constraint: {((time_with*1000)/NUM_ROWS*100):.2f} ms')
    print(f'Without constraint: {((time_without*1000)/NUM_ROWS*100):.2f} ms')
    print(f'Difference: {(((time_with - time_without)*1000)/NUM_ROWS*100):.2f} ms')


if __name__ == '__main__':
    main()
