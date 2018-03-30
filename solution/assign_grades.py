import sys, csv, psycopg2

def make_set_grade(cursor, code, term, student_id, grade):
	return cursor.mogrify("update enrollments set grade=%s where course_code=%s and term_code=%s and student_id=%s;", (grade,code,term,student_id))

if len(sys.argv) < 2:
	print("Usage: %s <input file>",file=sys.stderr)
	sys.exit(0)
	
input_filename = sys.argv[1]

# Open your DB connection here
psql_user = 'talm' #Change this to your username
psql_db = 'talm' #Change this to your personal DB name
psql_password = 'V00795078' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()
out = []
with open(input_filename) as f:
	for row in csv.reader(f):
		if len(row) == 0:
			continue #Ignore blank rows
		if len(row) != 4:
			print("Error: Invalid input line \"%s\""%(','.join(row)), file=sys.stderr)
			#Maybe abort the active transaction and roll back at this point?
			break
		course_code,term,student_id,grade = row
		
		#Do something with the data here
		#Make sure to catch any exceptions that occur and roll back the transaction if a database error occurs.
		out.append(make_set_grade(cursor, course_code, term, student_id, grade))

try:
	for s in out:
		cursor.execute(s)
	conn.commit()
except psycopg2.ProgrammingError as err: 
	#ProgrammingError is thrown when the database error is related to the format of the query (e.g. syntax error)
	print("Caught a ProgrammingError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
except psycopg2.IntegrityError as err: 
	#IntegrityError occurs when a constraint (primary key, foreign key, check constraint or trigger constraint) is violated.
	print("Caught an IntegrityError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
except psycopg2.InternalError as err:  
	#InternalError generally represents a legitimate connection error, but may occur in conjunction with user defined functions.
	#In particular, InternalError occurs if you attempt to continue using a cursor object after the transaction has been aborted.
	#(To reset the connection, run conn.rollback() and conn.reset(), then make a new cursor)
	print("Caught an IntegrityError:",file=sys.stderr)
	print(err,file=sys.stderr)
	conn.rollback()
cursor.close()
conn.close()