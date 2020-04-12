This is a modification of an assignment completed for the Python for Everybody
Specialization taught by Dr. Chuck.

Lines 8-67 are the SQL/JSON code required to read the JSON file containing
class information and organize in a SQL file. The SQL code 
creates three tables; Member, Course, and User.

Lines 42-49 are specifically for reading the JSON file, the code then
the code continues to create the three tables.

Lines 72-75 were created to pull the necessary Course and Member information,
the tables are then merged so that we can identify all students in the
same Course.

The enrollment function counts all individuals in the each class and then
subtracts 1 from the total to account for the instructor in class

From the Course series and the list comprehension created from calling
the enrollment function on the Course series, the length of the two lists
are compared to verify their compatability for plotting.

Course is then converted to a list of strings, used as an assertion to make
clearer for the program, not necessary.

The data is plotted