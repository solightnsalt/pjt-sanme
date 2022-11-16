from django.shortcuts import render
from django.http import JsonResponse
from .models import Map
import functools, time
from django.db import connection, reset_queries
from django.conf import settings
from django.db.models import Q


def query_debugger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        reset_queries()
        number_of_start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        number_of_end_queries = len(connection.queries)
        print(f"------------------------------------------------------")
        print(f"Function : {func.__name__}")
        print(f"Number of Queries : {number_of_end_queries-number_of_start_queries}")
        print(f"Finished in : {(end - start):.2f}s")
        print(f"------------------------------------------------------")
        return result

    return wrapper


# Create your views here.
@query_debugger
def map(request):
    return render(request, "map/map.html")


@query_debugger
def map_search(request, x, y):
    parks = Map.objects.all()
    parkJson = []

    for park in parks:
        parkJson.append(
            {
                "name": park.parkNm,
                "addr": park.lnmadr,
                "lat": park.latitude,
                "long": park.longitude,
            }
        )

    data = {
        "parkJson": parkJson,
    }
    return JsonResponse(data)


def search(request):
    parkJson = []
    if request.method == "POST":
        searched = request.POST["searched"]

        if searched != "":
            park_name = Map.objects.filter(
                Q(parkNm__icontains=searched)
                | Q(rdnmadr__icontains=searched)
                | Q(lnmadr__icontains=searched)
            )

            if len(park_name) > 0:
                parkJson = []
                for park in park_name:
                    parkJson.append(
                        {
                            "name": park.parkNm,
                            "addr": park.lnmadr,
                            "parkType": park.parkSe,
                            "lat": park.latitude,
                            "long": park.longitude,
                        }
                    )
            else:
                parkJson.append("결과를 찾을 수 없습니다")

        else:
            parkJson.append("결과를 찾을 수 없습니다")

        data = {
            "parkJson": parkJson,
        }

        return JsonResponse(data)
