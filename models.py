import sqlite3

def log_query(case_type, case_number, filing_year, response):
    try:
        with sqlite3.connect('db.sqlite3', timeout=10) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    case_type TEXT,
                    case_number TEXT,
                    filing_year TEXT,
                    response TEXT
                )
            ''')
            c.execute('''
                INSERT INTO logs (case_type, case_number, filing_year, response)
                VALUES (?, ?, ?, ?)
            ''', (case_type, case_number, filing_year, response))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(f"[ERROR] Database is locked: {e}")
