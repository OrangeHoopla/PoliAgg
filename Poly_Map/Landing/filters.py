import django_filters
from example.models import *

class OrderFilter(django_filters.FilterSet):
	class Meta:
		model = bill
		fields = '__all__'