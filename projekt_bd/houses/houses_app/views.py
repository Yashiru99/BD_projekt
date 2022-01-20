from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
from .forms import *
from itertools import chain
from django.db.models import Count, Avg

# to moze do zmiany bo na pewno da się mądrzej
# ale załómy ze ogarniczam się do tych 3 duzych miast
cities = {
    "warsaw":"Warszawa",
    "cracow":"Kraków",
    "poznan":"Poznań"
}

def index(request):
    return render(request, 'index.html')

def result(request):
    if request.method == "POST":
        city_name= request.POST['result'].lower().strip()
    try:
        name_to_search = cities[city_name]
        return render(request, city_name + ".html")
    except:
        return HttpResponse("nie ma takiego miasta")

def comparing(request):
    cities_vec = ['warsaw', 'poznan', 'cracow']
    if request.method == 'POST':
        form = ChoiceCityForm(request.POST)
        if form.is_valid():
            city1 = cities[cities_vec[int(form.cleaned_data['chosen_city_1'][0]) - 1]]
            city2 = cities[cities_vec[int(form.cleaned_data['chosen_city_2'][0]) - 1]]
            result1 = Apartment.objects.filter(city=city1)
            result2 = Apartment.objects.filter(city=city2)
            result1 = result1.filter(price__gte=form.cleaned_data['minimum_1']).filter(price__lte=form.cleaned_data['maksimum_1'])
            result1 = result1.filter(rooms=form.cleaned_data['rooms_1'])
            result1 = result1.filter(sq__gte=form.cleaned_data['min_sq_1']).filter(sq__lte=form.cleaned_data['max_sq_1'])
            result2 = result2.filter(price__gte=form.cleaned_data['minimum_2']).filter(price__lte=form.cleaned_data['maksimum_2'])
            result2 = result2.filter(rooms=form.cleaned_data['rooms_2'])
            result2 = result2.filter(sq__gte=form.cleaned_data['min_sq_2']).filter(sq__lte=form.cleaned_data['max_sq_2'])
            if not result1 or not result2:
                return HttpResponse("empty query")

            if form.cleaned_data['chosen_type'][0] == '1':
                avg1 = result1.aggregate(Avg('price'))['price__avg']
                avg2 = result2.aggregate(Avg('price'))['price__avg']
            elif form.cleaned_data['chosen_type'][0] == '2':
                avg1 = result1.aggregate(Avg('price'))['price__avg'] / result1.aggregate(Avg('sq'))['sq__avg']
                avg2 = result2.aggregate(Avg('price'))['price__avg'] / result2.aggregate(Avg('sq'))['sq__avg']
            elif form.cleaned_data['chosen_type'][0] == '3':
                avg1 = result1.aggregate(Avg('price'))['price__avg'] / form.cleaned_data['rooms_1']
                avg2 = result2.aggregate(Avg('price'))['price__avg'] / form.cleaned_data['rooms_2']
            else:
                avg1 = result1.count()
                avg2 = result2.count()
            return HttpResponse(str(avg1) + " vs " + str(avg2))
    else:
        form = ChoiceCityForm()

    return render(request, 'comparing.html', {'form': form})

def annoucement(request):
    return render(request, 'annoucement.html')
    
def warsaw(request):
    text = "Warsaw -officially the Capital City of Warsaw, is the capital and largest city of Poland. The metropolis stands on the River Vistula in east-central Poland and its population is officially estimated at 1.8 million residents within a greater metropolitan area of 3.1 million residents, which makes Warsaw the 7th most-populous capital city in the European Union. The city area measures 517 km2 (200 sq mi) and comprises 18 boroughs, while the metropolitan area covers 6,100 km2 (2,355 sq mi). Warsaw is an alpha- global city, a major cultural, political and economic hub, and the country's seat of government. Its historical Old Town was designated a UNESCO World Heritage Site."
    result_temp = Apartment.objects.filter(city='Warszawa')[:100]
    result = Apartment.objects.filter(city='Warszawa')
    if request.method == 'POST' and 'form1' in request.POST:
        form = choiceApartamentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['chosen_type']
            if data[0] == "1":
                result = result.order_by('price')
            elif data[0] == "2":
                result = result.order_by('floor')
            elif data[0] == "3":
                result = result.order_by('sq')
            min = form.cleaned_data['minimum']
            maks = form.cleaned_data['maksimum']
            result = result.filter(price__gte=min).filter(price__lte=maks)
            result = result.filter(rooms = form.cleaned_data['rooms'])
            result = result.filter(sq__gte=form.cleaned_data['min_sq']).filter(sq__lte=form.cleaned_data['max_sq'])
            return render(request, 'city_list.html', {'apartments': result})
    elif request.method == 'POST' and 'form2' in request.POST:
        form = groupByApartmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['grouping_element']
            if data[0] == "1":
                result = result.aggregate(Avg('price'))['price__avg']
            elif data[0] == "2":
                result = result.count()
            elif data[0] == "3":
                result = result.aggregate(Avg('price'))['price__avg'] / result.aggregate(Avg('sq'))['sq__avg']
            return HttpResponse(result)
    elif request.method == 'POST' and 'form3' in request.POST:
        form = advancedQueryForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            sq_range = form.cleaned_data['range_of_sq']
            apart = result.filter(id=id).first()
            result = result.filter(rooms = apart.rooms)
            result = result.filter(sq__gte=apart.sq-sq_range).filter(sq__lte=apart.sq+sq_range)
            res = result.count()
            return HttpResponse(str(res))
    else:
        form1 = choiceApartamentForm()
        form2 = groupByApartmentForm()
        form3 = advancedQueryForm()
    return render(request, 'city.html', { 'text' : text,
                                            'apartments': result_temp,
                                            'form1' : form1,
                                            'form2' : form2,
                                            'form3' : form3})

def cracow(request):
    text = "Cracow is the second-largest and one of the oldest cities in Poland. Situated on the Vistula River in Lesser Poland Voivodeship, the city dates back to the seventh century. Kraków was the official capital of Poland until 1596 and has traditionally been one of the leading centres of Polish academic, economic, cultural and artistic life. Cited as one of Europe's most beautiful cities, its Old Town was declared the first UNESCO World Heritage Site in the world."
    result_temp = Apartment.objects.filter(city='Kraków')[:100]
    result = Apartment.objects.filter(city='Kraków')
    if request.method == 'POST' and 'form1' in request.POST:
        form = choiceApartamentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['chosen_type']
            if data[0] == "1":
                result = result.order_by('price')
            elif data[0] == "2":
                result = result.order_by('floor')
            elif data[0] == "3":
                result = result.order_by('sq')
            min = form.cleaned_data['minimum']
            maks = form.cleaned_data['maksimum']
            result = result.filter(price__gte=min).filter(price__lte=maks)
            result = result.filter(rooms = form.cleaned_data['rooms'])
            result = result.filter(sq__gte=form.cleaned_data['min_sq']).filter(sq__lte=form.cleaned_data['max_sq'])
            return render(request, 'city_list.html', {'apartments': result})
    elif request.method == 'POST' and 'form2' in request.POST:
        form = groupByApartmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['grouping_element']
            if data[0] == "1":
                result = result.aggregate(Avg('price'))['price__avg']
            elif data[0] == "2":
                result = result.count()
            elif data[0] == "3":
                result = result.aggregate(Avg('price'))['price__avg'] / result.aggregate(Avg('sq'))['sq__avg']
            return HttpResponse(result)
    elif request.method == 'POST' and 'form3' in request.POST:
        form = advancedQueryForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            sq_range = form.cleaned_data['range_of_sq']
            apart = result.filter(id=id).first()
            result = result.filter(rooms = apart.rooms)
            result = result.filter(sq__gte=apart.sq-sq_range).filter(sq__lte=apart.sq+sq_range)
            res = result.count()
            return HttpResponse(str(res))
    else:
        form1 = choiceApartamentForm()
        form2 = groupByApartmentForm()
        form3 = advancedQueryForm()
    return render(request, 'city.html', { 'text': text,
                                            'apartments': result_temp,
                                            'form1' : form1,
                                            'form2' : form2,
                                            'form3' : form3})

def poznan(request):
    text = "Poznan is a city on the River Warta in west-central Poland, within the Greater Poland region. The city is an important cultural and business centre, and one of Poland's most populous regions with many regional customs such as Saint John's Fair (Jarmark Świętojański), traditional Saint Martin's croissants and a local dialect. Among its most important heritage sites are the Renaissance Old Town, Town Hall and Gothic Cathedral."
    result_temp = Apartment.objects.filter(city='Poznań')[:100]
    result = Apartment.objects.filter(city='Poznań')
    if request.method == 'POST' and 'form1' in request.POST:
        form = choiceApartamentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['chosen_type']
            if data[0] == "1":
                result = result.order_by('price')
            elif data[0] == "2":
                result = result.order_by('floor')
            elif data[0] == "3":
                result = result.order_by('sq')
            min = form.cleaned_data['minimum']
            maks = form.cleaned_data['maksimum']
            result = result.filter(price__gte=min).filter(price__lte=maks)
            result = result.filter(rooms = form.cleaned_data['rooms'])
            result = result.filter(sq__gte=form.cleaned_data['min_sq']).filter(sq__lte=form.cleaned_data['max_sq'])
            return render(request, 'city_list.html', {'apartments': result})
    elif request.method == 'POST' and 'form2' in request.POST:
        form = groupByApartmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['grouping_element']
            if data[0] == "1":
                result = result.aggregate(Avg('price'))['price__avg']
            elif data[0] == "2":
                result = result.count()
            elif data[0] == "3":
                result = result.aggregate(Avg('price'))['price__avg'] / result.aggregate(Avg('sq'))['sq__avg']
            return HttpResponse(result)
    elif request.method == 'POST' and 'form3' in request.POST:
        form = advancedQueryForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            sq_range = form.cleaned_data['range_of_sq']
            apart = result.filter(id=id).first()
            result = result.filter(rooms = apart.rooms)
            result = result.filter(sq__gte=apart.sq-sq_range).filter(sq__lte=apart.sq+sq_range)
            res = result.count()
            return HttpResponse(str(res))
    else:
        form1 = choiceApartamentForm()
        form2 = groupByApartmentForm()
        form3 = advancedQueryForm()
    return render(request, 'city.html', { 'text' : text,
                                            'apartments': result_temp,
                                            'form1' : form1,
                                            'form2' : form2,
                                            'form3' : form3})

def success(request):
    return HttpResponse(request, 'annoucement.html')

def add_an_annoucement(request):
    return HttpResponseRedirect('/admin')
