from django_filters import FilterSet
from .models import Product

class ProductFilter(FilterSet): #Определяем фильтр

    class Meta():
        model = Product   #указываем название модели по которой фильтруем
        # fields = ('name', 'price', 'quantity', 'category')   # указываем наименования полей по которым будет работать фильтр

        fields = {
                'name': ['icontains'],
                'price': ['lt'],
                'quantity': ['gt']
                }   # указываем наименования полей по которым будет работать фильтр