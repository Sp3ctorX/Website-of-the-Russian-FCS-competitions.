# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('sait2_new.db')
cursor = conn.cursor()

# Add yandex_link to competition_tasks
cursor.execute("PRAGMA table_info(competition_tasks)")
columns = [col[1] for col in cursor.fetchall()]
print('Current task columns:', columns)

if 'yandex_link' not in columns:
    cursor.execute('ALTER TABLE competition_tasks ADD COLUMN yandex_link TEXT NOT NULL DEFAULT ""')
    print('Added yandex_link column to tasks')

# Add regulation_link to competitions
cursor.execute("PRAGMA table_info(competitions)")
columns = [col[1] for col in cursor.fetchall()]
print('Current competition columns:', columns)

if 'regulation_link' not in columns:
    cursor.execute('ALTER TABLE competitions ADD COLUMN regulation_link TEXT')
    print('Added regulation_link column to competitions')

conn.commit()
conn.close()
print('Database updated!')
