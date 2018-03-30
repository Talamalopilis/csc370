import psycopg2, sys

def print_row(term, course_code, course_name, instructor_name, total_enrollment, maximum_capacity):
	print("%6s %10s %-35s %-25s %s/%s"%(str(term), str(course_code), str(course_name), str(instructor_name), str(total_enrollment), str(maximum_capacity)) )


psql_user = 'talm' #Change this to your username
psql_db = 'talm' #Change this to your personal DB name
psql_password = 'V00795078' #Put your password (as a string) here
psql_server = 'studdb2.csc.uvic.ca'
psql_port = 5432

conn = psycopg2.connect(dbname=psql_db,user=psql_user,password=psql_password,host=psql_server,port=psql_port)
cursor = conn.cursor()

cursor.execute("""select a.term_code, a.course_code, a.course_name, a.instructor, 
						case when b.course_code is null then 0 else count(*) end as enrollment, 
						a.max_capacity
					from course_offerings as a 
					left outer join
					enrollments as b
					on a.term_code=b.term_code and a.course_code = b.course_code
					group by (a.term_code, a.course_code, b.course_code)
					order by a.term_code, a.course_code;
			   """)

while True:
	row = cursor.fetchone()
	if row is None:
		break
	print_row(*row)

cursor.close()
conn.close()