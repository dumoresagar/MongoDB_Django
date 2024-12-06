from django.shortcuts import render
from .models import person_collection
from django.http import HttpResponse
import logging
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("<h1>App is Running</h1>")



def get_all_person(request):
    persons= person_collection.find()
    return HttpResponse(persons)


@csrf_exempt
def add_person(request):
    if request.method == 'POST':
        try:
            # Print the raw body for debugging
            logging.info(f"Request Body: {request.body}")

            # Parse JSON data from the request
            data = json.loads(request.body.decode('utf-8'))

            # Check if the data is a list
            if not isinstance(data, list):
                return JsonResponse({'error': 'Data must be an array of objects'}, status=400)

            # Validate each object in the list
            for person in data:
                if 'first_name' not in person or 'last_name' not in person:
                    return JsonResponse({'error': 'Missing required fields in one or more objects'}, status=400)

            # Insert multiple records into MongoDB
            person_collection.insert_many(data)

            return JsonResponse({'message': f'{len(data)} persons added successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid HTTP method'}, status=405)