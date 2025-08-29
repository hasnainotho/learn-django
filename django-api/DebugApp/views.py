from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def display_even_numbers(request):
    response = ""
    numbers = [1,2,3,4,5,6,7,8,9]
    for i in numbers:
        reminder = i % 2
        if reminder == 0:
            response += str(i) + "<br/>"
            
    return HttpResponse(response)
    