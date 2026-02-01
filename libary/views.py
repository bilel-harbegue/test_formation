from datetime import date, datetime
import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Sum
from .serializers import bookSerialzer
from django.views.decorators.csrf import csrf_exempt
from .models import Book
# Create your views here.

@csrf_exempt
@require_http_methods(['GET'])
def get_all_books(request):
    books=Book.objects.all()
    print({"book type":books})
    serialzer_for_book=bookSerialzer(books,many=True)
    total_price=books.aggregate(total=Sum('price'))['total'] or 0
    return JsonResponse({
        "books":serialzer_for_book.data,
        "count":len(serialzer_for_book.data),
        "total price":total_price
    })



@csrf_exempt
@require_http_methods(['GET'])
def get_book(request, pk):
    """ GET: get a single book """
    try:
        book = Book.objects.get(id=pk)
        limite_date = date(2019,12,31)
        if book.published_date>limite_date:
            serializer_for_book = bookSerialzer(book)
            return JsonResponse({
                "book": serializer_for_book.data,
                "success": True
            })
        else:
            return JsonResponse({
                "error":"book puplished befor 31/12/2019",
                "success":False
            })
    except Book.DoesNotExist:
        return JsonResponse({
            "error": "book not found",
            "success": False
        })


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_book(request,pk):
    '''delete : remove a book'''
    try:
        book = Book.objects.get(id=pk)
        book.delete()
        return JsonResponse({
            "message":"book deleted successfully",
            "success":True
        })
    except Book.DoesNotExist:
        return JsonResponse({
            "error":"book ot found",
            "success":False
        },status=404)
    


# 


# @csrf_exempt
# @require_http_methods(['POST'])
# def create_book(request):
#     '''post : creat a new student'''

#     json_data = json.loads(request.body)
#     promo_date=date(2019,12,31)
#     data_book=json_data['published_date']
#     price_book=json_data['price']

#     serializer = bookSerialzer(data=json_data)
#     if serializer.is_valid():
#         book = serializer.save()
#         book_data = bookSerialzer(book).data
#         return JsonResponse({
#             "message":"book created successfully",
#             "book":book_data,
#             "success":True
#         })
#     else:
#         return JsonResponse({
#             "error":serializer.errors,
#             "success":False
#         },status=400)
    

@csrf_exempt
@require_http_methods(["POST"])
def create_book(request):
    """POST: create book"""

    try:
        json_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON",
            "success": False
        }, status=400)

    print("json_data:", json_data)

    promo_date = date(2019, 12, 31)

    date_book = datetime.strptime(json_data["published_date"],"%Y-%m-%d").date()


    price_book = float(json_data["price"])

    if date_book < promo_date:
        price_book = round(price_book - ((price_book / 100) * 25), 2)

    json_data["price"] = price_book

    serializer = bookSerialzer(data=json_data)

    if serializer.is_valid():
        book = serializer.save()
        book_data = bookSerialzer(book).data

        return JsonResponse({
            "message": "book created successfully",
            "book": book_data,
            "success": True
        }, status=201)

    else:
        return JsonResponse({
            "error": serializer.errors,
            "success": False
        }, status=400)
    






@csrf_exempt
# @require_http_methods(['PUT','PATCH'])
# def update_book(request,pk):
#     '''put : update a student'''
#     json_data=json.loads(request.body)
#     try:
#         book = Book.objects.get(id=pk)
#     except Book.DoesNotExist:
#         return JsonResponse({
#             "error":"Student not found",
#             "success":False
#         },status=404)
#     serializer = bookSerialzer(book,data=json_data)
#     if serializer.is_valid():
#         book = serializer.save()
#         book_data = bookSerialzer(book).data
#         return JsonResponse({
#             "message":"book updated successfully",
#             "student":book_data,
#             "success":True
#         })
#     return JsonResponse({
#             "error":serializer.errors,
#             "success":False
#         },status=400)





@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_one_book(request):
    json_data = json.loads(request.body)

    try:
        book = Book.objects.get(id=json_data["id"])
    except Book.DoesNotExist:
        return JsonResponse({
            "error": "book not found"
        }, status=404)

    del json_data["id"]

    serializer = bookSerialzer(
        book,
        data=json_data,
        partial=True 
    )

    if serializer.is_valid():
        book = serializer.save()
        book_data = bookSerialzer(book).data

        return JsonResponse({
            "message": "book updated successfully",
            "book": book_data
        }, status=200)

    return JsonResponse({
        "error": serializer.errors
    }, status=400)