from django.http import JsonResponse


def index(req):
    return JsonResponse('hello world', safe=False)