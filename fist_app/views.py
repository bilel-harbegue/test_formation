# import json
# from django.shortcuts import render
# from fist_app.models import Student
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt

# # Create your views here.

# @csrf_exempt
# def get_students(request):
#     if request.method == 'GET':
#         students = Student.objects.all()
#         students_list = []
#         for student in students:
#             students_list.append({
#                 'id': student.id,
#                 'first_name': student.first_name, 
#                 'last_name': student.last_name,
#                 'email': student.email,
#                 'age': student.age,
#                 'is_active': student.is_active,
#                 'created_at': student.created_at,
#             })
#         return JsonResponse({
#             'student': students_list,
#             'count': len(students_list)
#         })
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt 
# def get_student(request, pk):
#     if request.method == 'GET':
#         try:
#             student = Student.objects.get(id=pk)
#             student_data = {
#                 "id": student.id,
#                 "first_name": student.first_name, 
#                 "last_name": student.last_name,
#                 "email": student.email,
#                 "age": student.age,
#                 "is_active": student.is_active
#             }
#             return JsonResponse({
#                 "student": student_data,
#                 'success': True
#             })
#         except Student.DoesNotExist:
#             return JsonResponse({'error': 'Student not found'}, status=404)
#     return JsonResponse({'error': 'Method not Allowed'}, status=405)

# @csrf_exempt
# def create_student(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format", "success": False}, status=400)

#         required_fields = ['first_name', 'last_name', 'email', 'age']
#         for field in required_fields:
#             if field not in data:
#                 return JsonResponse({
#                     "error": f"Missing required field: {field}",
#                     "success": False
#                 }, status=400)

#         student = Student.objects.create(
#             first_name=data['first_name'], 
#             last_name=data['last_name'],
#             email=data['email'],
#             age=data['age'],
#         )

#         student_data = {
#             "id": student.id,
#             "first_name": student.first_name, 
#             "last_name": student.last_name,
#             "email": student.email,
#             "age": student.age,
#             "is_active": student.is_active
#         }

#         return JsonResponse({
#             "message": "student added successfully",
#             "data": student_data,  
#             "success": True,
#         }, status=201)
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# @csrf_exempt
# def delete_student(request, student_id):
#     if request.method == "DELETE":
#         try:
#             student = Student.objects.get(id=student_id)
#             student.delete()
#             return JsonResponse({
#                 "message": "Student deleted successfully",
#                 "success": True
#             })
#         except Student.DoesNotExist:
#             return JsonResponse({'error': 'Student not found'}, status=404)
#     return JsonResponse({"error": "Method Not Allowed"}, status=405)

# @csrf_exempt
# def update_student(request, pk):
#     if request.method == "PUT":
#         try:
#             student = Student.objects.get(id=pk)
#             data = json.loads(request.body)
            
#             if 'first_name' in data:
#                 student.first_name = data['first_name']
                
#             if 'last_name' in data:
#                 student.last_name = data['last_name']
                
#             if 'email' in data:
#                 student.email = data['email']
                
#             if 'age' in data:
#                 student.age = data['age']
                
#             if 'is_active' in data:
#                 student.is_active = data['is_active']
            
#             student.save()

#             student_data = {
#                 "id": student.id,
#                 "first_name": student.first_name,
#                 "last_name": student.last_name,
#                 "email": student.email,
#                 "age": student.age,
#                 "is_active": student.is_active
#             }
#             return JsonResponse({
#                 "message": "Student updated successfully",
#                 "student": student_data,
#                 "success": True
#             })
#         except Student.DoesNotExist:
#             return JsonResponse({'error': 'Student not found'}, status=404)
#     return JsonResponse({'error': 'Method not allowed'}, status=405)

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Student
from .serializers import StudentSerializer

@csrf_exempt
@require_http_methods(['GET'])
def get_students(request):
    '''GET:List all students'''
    students = Student.objects.all()
    serializer = StudentSerializer(students,many=True)
    return JsonResponse({
        "students":serializer.data,
        "count":len(serializer.data)
    })

@csrf_exempt
@require_http_methods(['GET'])
def get_student(request,student_id):
    '''GET:retrieve a specific student'''
    try:
         students = Student.objects.get(id=student_id)
         serializer = StudentSerializer(students)
         return JsonResponse({
            "students":serializer.data,
            "success":True
        })
    except Student.DoesNotExist:
        return JsonResponse({
            "error":"Student not found",
            "success":False
        },status=404)
   
    
@csrf_exempt
@require_http_methods(['POST'])
def create_student(request):
    '''post : creat a new student'''

    json_data = json.loads(request.body)
    serializer = StudentSerializer(data=json_data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data
        return JsonResponse({
            "message":"student created successfully",
            "student":student_data,
            "success":True
        })
    else:
        return JsonResponse({
            "error":serializer.errors,
            "success":False
        },status=400)
    

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_student(request,pk):
    '''delete : remove a student'''
    try:
        student = Student.objects.get(id=pk)
        student.delete()
        return JsonResponse({
            "message":"student deleted successfully",
            "success":True
        })
    except Student.DoesNotExist:
        return JsonResponse({
            "error":"student ot found",
            "success":False
        },status=404)
    
@csrf_exempt
@require_http_methods(['PUT','PATCH'])
def update_student(request,pk):
    '''put : update a student'''
    json_data=json.loads(request.body)
    try:
        student = Student.objects.get(id=pk)
    except Student.DoesNotExist:
        return JsonResponse({
            "error":"Student not found",
            "success":False
        },status=404)
    serializer = StudentSerializer(student,data=json_data)
    if serializer.is_valid():
        student = serializer.save()
        student_data = StudentSerializer(student).data
        return JsonResponse({
            "message":"student updated successfully",
            "student":student_data,
            "success":True
        })
    return JsonResponse({
            "error":serializer.errors,
            "success":False
        },status=400)
        