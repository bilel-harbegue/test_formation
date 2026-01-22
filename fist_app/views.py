import json
from django.shortcuts import render
from fist_app.models import Student
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def get_students(request):
    if request.method == 'GET':
        students = Student.objects.all()
        students_list = []
        for student in students:
            students_list.append({
                'id': student.id,
                'first_name': student.first_name, 
                'last_name': student.last_name,
                'email': student.email,
                'age': student.age,
                'is_active': student.is_active,
                'created_at': student.created_at,
            })
        return JsonResponse({
            'student': students_list,
            'count': len(students_list)
        })
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt 
def get_student(request, pk):
    if request.method == 'GET':
        try:
            student = Student.objects.get(id=pk)
            student_data = {
                "id": student.id,
                "first_name": student.first_name, 
                "last_name": student.last_name,
                "email": student.email,
                "age": student.age,
                "is_active": student.is_active
            }
            return JsonResponse({
                "student": student_data,
                'success': True
            })
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Method not Allowed'}, status=405)

@csrf_exempt
def create_student(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format", "success": False}, status=400)

        required_fields = ['first_name', 'last_name', 'email', 'age']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    "error": f"Missing required field: {field}",
                    "success": False
                }, status=400)

        student = Student.objects.create(
            first_name=data['first_name'], 
            last_name=data['last_name'],
            email=data['email'],
            age=data['age'],
        )

        student_data = {
            "id": student.id,
            "first_name": student.first_name, 
            "last_name": student.last_name,
            "email": student.email,
            "age": student.age,
            "is_active": student.is_active
        }

        return JsonResponse({
            "message": "student added successfully",
            "data": student_data,  
            "success": True,
        }, status=201)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_student(request, student_id):
    if request.method == "DELETE":
        try:
            student = Student.objects.get(id=student_id)
            student.delete()
            return JsonResponse({
                "message": "Student deleted successfully",
                "success": True
            })
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({"error": "Method Not Allowed"}, status=405)

@csrf_exempt
def update_student(request, pk):
    if request.method == "PUT":
        try:
            student = Student.objects.get(id=pk)
            data = json.loads(request.body)
            
            if 'first_name' in data:
                student.first_name = data['first_name']
                
            if 'last_name' in data:
                student.last_name = data['last_name']
                
            if 'email' in data:
                student.email = data['email']
                
            if 'age' in data:
                student.age = data['age']
                
            if 'is_active' in data:
                student.is_active = data['is_active']
            
            student.save()

            student_data = {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "email": student.email,
                "age": student.age,
                "is_active": student.is_active
            }
            return JsonResponse({
                "message": "Student updated successfully",
                "student": student_data,
                "success": True
            })
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)