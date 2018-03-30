import psycopg2, sys

def print_header(student_id, student_name):
	print("Transcript for %s (%s)"%(str(student_id), str(student_name)) )
	
def print_row(course_term, course_code, course_name, grade):
	if grade is not None:
		print("%6s %10s %-35s   GRADE: %s"%(str(course_term), str(course_code), str(course_name), str(grade)) )
	else:
		print("%6s %10s %-35s   (NO GRADE ASSIGNED)"%(str(course_term), str(course_code), str(course_name)) )

if len(sys.argv) < 2:
	print('Usage: %s <student id>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
student_id = sys.argv[1]


psql_user = 'talm' #Change this to your username
psql_db = 'talm' #Change this to your personal DB name
psql_password = 'V00795078' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""select student_id, name from students where student_id=%s;
				""", (student_id,))

row = cursor.fetchone()
if row is not None:
	print_header(*row)
else:
	print("Student not found.", file=sys.stderr)

cursor.execute("""select term_code, course_code, course_name, grade
				  from enrollments natural join course_offerings
				  where student_id=%s
				  order by term_code, course_code;
				""", (student_id,))

while True:
	row = cursor.fetchone()
	if row is None:
		break
	print_row(*row)

cursor.close()
conn.close()