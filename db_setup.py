import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

conn = sqlite3.connect(os.getenv("DB_PATH"))

conn.execute("""
CREATE TABLE "member" (
"member_id"	INTEGER,
"intro_link"	TEXT,
"pronouns"	TEXT NOT NULL DEFAULT 'None',
"rp_opted_in"	INTEGER NOT NULL DEFAULT 0,
PRIMARY KEY("member_id")
);
""")

conn.execute("""
CREATE TABLE "roleplayer" (
"member_id"	INTEGER,
"balance"	REAL DEFAULT 0,
PRIMARY KEY("member_id")
);
""")

conn.close()
