import psycopg2, sys

def print_header(course_code, course_name, term, instructor_name):
	print("Class list for %s (%s)"%(str(course_code), str(course_name)) )
	print("  Term %s"%(str(term), ) )
	print("  Instructor: %s"%(str(instructor_name), ) )
	
def print_row(student_id, student_name, grade):
	if grade is not None:
		print("%10s %-25s   GRADE: %s"%(str(student_id), str(student_name), str(grade)) )
	else:
		print("%10s %-25s"%(str(student_id), str(student_name),) )

def print_footer(total_enrolled, max_capacity):
	print("%s/%s students enrolled"%(str(total_enrolled),str(max_capacity)) )


if len(sys.argv) < 3:
	print('Usage: %s <course code> <term>'%sys.argv[0], file=sys.stderr)
	sys.exit(0)
	
course_code, term = sys.argv[1:3]

psql_user = 'talm' #Change this to your username
psql_db = 'talm' #Change this to your personal DB name
psql_password = 'V00795078' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""select course_code, course_name, term_code, instructor
				  from course_offerings where course_code=%s and term_code=%s;
				""", (course_code, term))


print_header(*cursor.fetchone())

cursor.execute("""select student_id, name, grade
				  from enrollments natural join students
				  where course_code=%s and term_code=%s
				  order by student_id;
				""", (course_code, term))

while True:
	row = cursor.fetchone()
	if row is None:
		break
	print_row(*row)

cursor.execute("""select case when b.course_code is null then 0 else count(*) end as enrollment, 
						a.max_capacity
					from course_offerings as a 
					left outer join
					enrollments as b
					on a.term_code=b.term_code and a.course_code = b.course_code
					where a.course_code=%s and a.term_code=%s
					group by (a.term_code, a.course_code, b.course_code);
				""", (course_code, term))
#Print the last line (enrollment/max_capacity)
print_footer(*cursor.fetchone())

cursor.close()
conn.close()