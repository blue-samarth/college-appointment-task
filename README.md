
show dbs
use college_appointments
show collections
db.students.find().pretty()
db.students.deleteOne({name : "abc"})

localhost:8000/api/v1/signup_student
POST
{
    "name" : "abc",
    "email" : "abc@gmail",
    "password" : "1234"
}

result : 
{
    "status": "success",
    "message": "Student created successfully",
    "data": {
        "_id": "679384c0d6d2db4e45a496cb",
        "name": "abc",
        "email": "abc@gmail",
        "password": "$2b$12$3cFDA1CPFtY2w.cikudXr.dsgh2kObYm3HVQuvHVUuhj2xUt2DtS6",
        "enrollment_no": 1,
        "created_at": "2025-01-24T17:47:04.657000",
        "enrolled_courses": {}
    },
    "status_code": 200
}