
import numpy as np
import pandas as pd
import json
import sqlite3
from matplotlib import pyplot as plt

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

# Table Setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    user_id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    course_id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = 'roster_data.json'

"""Data stored as [ "name", "title", role ],
[ "Mea", "si110", 0 ]
name = Mea, Course = si110, role = 0 (student)
if role = 1, role is teacher"""

str_data = open(fname).read()
json_data = json.loads(str_data)

for entry in json_data:

    name = entry[0];
    title = entry[1];
    role = entry[2]

    #print(name, title, role)

    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT user_id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT course_id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )
    
    conn.commit()

"""Create Dataframe to plot enrollment per course number, JOIN on Course_ID to
show class title"""


member_df = pd.read_sql_query('SELECT user_id, course_id, role FROM Member', conn)
course_df = pd.read_sql_query('SELECT course_id, title from Course', conn)
merged_df = pd.merge(member_df[['user_id','role','course_id']], course_df[['course_id','title']], 
                how='inner', on='course_id')


"""Check dataframe to clean if necessary"""
print('\n Merged dataframe info:')
print(merged_df.head())
print(merged_df.shape)
print('Null values: ' + str(sum(merged_df.isnull().sum() != 0)) + '\n')
print('Number of Teachers: ' + str(np.sum(merged_df['role'])))


def enrollment(course_index):
    """count enrollment of each class"""
    count = 0
    for id_number in merged_df['title']:
        if id_number == course_index:
            count += 1
    return count - 1  # account for teacher in each class


# Call enrollment function into list for easy plotting
course = merged_df['title']
course = pd.Series(course).unique()
enrollment_numbers = [enrollment(i) for i in course]

# Check course enrollment numbers against course
if len(enrollment_numbers) == len(course):
    print(True)
else:
    print(False)

# Convert integers to strings to allow for clear plotting of data
course = list(map(str, course))

# make plot
plt.figure(figsize = (10, 7))
plt.tight_layout()
plt.bar(course, enrollment_numbers)
plt.ylabel('Students Enrolled')
plt.title('Enrollment by Course Number')
plt.xlabel('Course Title')

plt.show()
