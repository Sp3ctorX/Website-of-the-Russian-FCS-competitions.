# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect('sait2_new.db')
cursor = conn.cursor()

# Check if columns exist
cursor.execute("PRAGMA table_info(expert_applications)")
columns = [col[1] for col in cursor.fetchall()]
print('Current columns:', columns)

if 'achievement' not in columns:
    cursor.execute('ALTER TABLE expert_applications ADD COLUMN achievement TEXT')
    print('Added achievement column')

if 'description' not in columns:
    cursor.execute('ALTER TABLE expert_applications ADD COLUMN description TEXT')
    print('Added description column')

conn.commit()
conn.close()
print('Database updated!')
