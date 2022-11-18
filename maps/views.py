from django.shortcuts import render
from django.http import JsonResponse
from .models import Map
import functools, time
from django.db import connection, reset_queries
from django.conf import settings
from django.db.models import Q
from haversine import haversine


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
def map(request):
    return render(request, "maps/map.html")


@query_debugger
def map_search(request, x, y):
    parks = Map.objects.all()
    parkJson = []

    latitude_range = (float(x) - 0.025 , float(x) + 0.025)
    longitude_range = (float(y) - 0.0375, float(y) + 0.0375)

    user_distance = int(haversine((float(x), float(y)), (float(parks[1].latitude), float(parks[1].longitude))) * 1000)


    for park in parks:
        if park.latitude != '' and park.longitude != '':
            if latitude_range[0] <= float(park.latitude) <= latitude_range[1] and longitude_range[0] <= float(park.longitude) <= longitude_range[1]:
                
                
                user_distance = haversine((float(x), float(y)), (float(park.latitude), float(park.longitude))) * 1000
                
                if user_distance <= 1000:
                    user_distance = str(int(user_distance)) + 'm'
                else:
                    user_distance = user_distance / 1000
                    user_distance = str(format(user_distance, ".2f")) + 'km'
                
                parkJson.append(
                    {
                        "id" : park.id,
                        "name": park.parkNm,
                        "addr": park.lnmadr,
                        "lat": park.latitude,
                        "long": park.longitude,
                        "userDistance": user_distance,
                    }
                )

    data = {
        "parkJson": parkJson,
    }
    return JsonResponse(data)


def search(request):
    park_list = []
    if request.method == "POST":
        searched = request.POST['searched']

        if searched != "":
            park_name = Map.objects.filter(
                Q(parkNm__icontains=searched)
                | Q(rdnmadr__icontains=searched)
                | Q(lnmadr__icontains=searched)
            )

            if len(park_name) > 0:
                for park in park_name:
                    park_list.append(
                        {
                            "name": park.parkNm,
                            "addr": park.lnmadr,
                            "parkType": park.parkSe,
                            "lat": park.latitude,
                            "long": park.longitude,
                        }
                    )

    data = {
        "parkJson": park_list,
    }

    return JsonResponse(data)