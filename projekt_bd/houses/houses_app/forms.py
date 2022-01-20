from tokenize import group
from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

class AnnoucementForm(forms.Form):
    address = forms.CharField(label='Adress', max_length=255)
    city = forms.CharField(label='City', max_length=255)
    floor = forms.FloatField(label='Floor')
    price = forms.FloatField(label='Price')
    rooms = forms.FloatField(label='Rooms')
    sq = forms.FloatField(label='sq')
    year = forms.FloatField(label='Year')

Cities_choices = (
    ("1", "Warsaw"),
    ("2", "Poznan"),
    ("3", "Krakow")
)

divide_choice = (
    ("1", "average price"),
    ("2", "average price per sq"),
    ("3", "average price for room"),
    ("4", "number of apartaments available"),
)

class ChoiceCityForm(forms.Form):
    chosen_city_1 = forms.MultipleChoiceField(choices = Cities_choices, label='choose first city')
    minimum_1 = forms.FloatField(label='starting price')
    maksimum_1 = forms.FloatField(label='ending price')
    rooms_1 = forms.FloatField(label='number of rooms')
    min_sq_1 = forms.FloatField(label='minimum sq')
    max_sq_1 = forms.FloatField(label='maks sq')
    chosen_city_2 = forms.MultipleChoiceField(choices = Cities_choices, label = 'choose second city ')
    minimum_2 = forms.FloatField(label='starting price')
    maksimum_2 = forms.FloatField(label='ending price')
    rooms_2 = forms.FloatField(label='number of rooms')
    min_sq_2 = forms.FloatField(label='minimum sq')
    max_sq_2 = forms.FloatField(label='maks sq')
    chosen_type = forms.MultipleChoiceField(choices = divide_choice, label = 'choose parameter to compare')
    

sort_by_element = (
    ('1', "price"),
    ('2', "floors"),
    ('3', "sq")
)

class choiceApartamentForm(forms.Form):
    chosen_type = forms.MultipleChoiceField(label="sort by", choices = sort_by_element)
    minimum = forms.FloatField(label='starting price')
    maksimum = forms.FloatField(label='ending price')
    rooms = forms.FloatField(label='number of rooms')
    min_sq = forms.FloatField(label='minimum sq')
    max_sq = forms.FloatField(label='maks sq')

group_by_element = (
    ('1', "average price"),
    ('2', "number of apartaments"),
    ('3', "average price peq sq")
)

class groupByApartmentForm(forms.Form):
    grouping_element = forms.MultipleChoiceField(label='show the metric:', choices=group_by_element)


class advancedQueryForm(forms.Form):
    id = forms.CharField(label='id of apartment', max_length=255)
    range_of_sq = forms.FloatField(label='range of sq')

