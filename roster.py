
import numpy as np
import pandas as pd
import json
import sqlite3
from matplotlib import pyplot as plt

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

#Table Setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);

CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
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
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id, role) VALUES ( ?, ?, ? )''',
        ( user_id, course_id, role ) )

    conn.commit()

"""Create Dataframe to plot enrollment per course number"""

member_df = pd.read_sql_query('SELECT user_id, course_id, role FROM Member', conn)

"""Check dataframe to clean if necessary"""
print('Member dataframe info:')
print(member_df.head())
print(member_df.shape)
print('Null values: ' + str(sum(member_df.isnull().sum() != 0)) + '\n')

course = member_df['course_id']
course = pd.Series(course).unique()

def enrollment(course_index):
    """count enrollment of each class"""
    count = 0
    for course in member_df['course_id']:
        if course == course_index:
            count += 1
    return count

#Call enrollment function into list for easy plotting
enrollment_numbers = [enrollment(course[0]), enrollment(course[1]), enrollment(course[2]), 
                     enrollment(course[3]), enrollment(course[4]), enrollment(course[5]),
                     enrollment(course[6]), enrollment(course[7]), enrollment(course[8]),
                     enrollment(course[9])]

#Check course enrollment numbers against course
if len(enrollment_numbers) == len(course):
    print(True)
else:
    print(False)

#Convert integers to strings to allow for clear plotting of data
course = list(map(str,course))

#make plot
plt.figure(figsize = (10,7))
plt.tight_layout()
plt.bar(course, enrollment_numbers)
plt.xlabel('Students Enrolled')
plt.title('Enrollment by Course Number')
plt.ylabel('Course No.')

plt.show()
