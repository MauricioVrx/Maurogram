"""Maurogram views"""

#Django
from django.http import HttpResponse
from django.http import JsonResponse
# import json

#Utilities
from datetime import datetime

def hello_world(request):
    """Return a greeting"""
    now = format(str(datetime.now().strftime('%b %d, %Y - %H:%M')))
    # now = format(datetime.now())
    return HttpResponse(f'Oh, hi! the current server time is {now}')


def sort_integers(request):
    """ Return a JSON response with sorted integers"""
    numbers = map(int,request.GET['numbers'].split(","))
    # numbers = [int(i) for i in numbers]
    data = {
        'status' : 'ok',
        'numbers':sorted(numbers),
        'message': 'Integers sorted successfully.'
    }
    return JsonResponse(
        data,
        json_dumps_params={'indent': 4}
    )


def say_hi(request, name, age):
    """Return a greeting."""
    if age < 12:
        message = f"Sorry {name}, but you are not allowed here. 😒"
    else:
        message = f"Welcome {name} to Maurogram 🧡"

    return HttpResponse(message)
