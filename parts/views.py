import base64
import json

from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ApiATP.helpers import process_parts_data
from .forms.part_filter_form import PartFilterForm
from .serializers import *


class PartListView(ListView):
    model = Part
    template_name = 'parts.html'
    context_object_name = 'parts'
    form_class = PartFilterForm
    paginate_by = 10  # Number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['form'] = form
        context['parts'] = self.get_serialized_data()
        return context

    def get_form(self):
        return PartFilterForm(self.request.GET or None)

    def get_queryset(self):
        queryset = super().get_queryset()
        form = self.get_form()
        if form.is_valid():
            part_name = form.cleaned_data.get('part_name')
            category = form.cleaned_data.get('category')

            if part_name:
                queryset = queryset.filter(part__icontains=part_name)
            if category:
                descendants = Category.objects.filter(pk=category.pk) | Category.objects.filter(parent=category)
                descendant_ids = descendants.values_list('id', flat=True)
                queryset = queryset.filter(category_id__in=descendant_ids)

        return queryset

    def get_serialized_data(self):
        """ Serialize the paginated queryset. """
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page = paginator.get_page(page_number)
        serializer = PartSerializer(page.object_list, many=True)
        return serializer.data


@api_view(['POST'])
@permission_classes([AllowAny])
def post(request):
    data = request.data
    if 'usefile' in data:
        with open("C:\\Users\\Maidport\\Documents\\Projects\\python\\ATP\\outlook.json",'r') as file:
            json_data = json.load(file)
            result = process_parts_data(json_data)
        return Response(result)
    else:
        result = process_parts_data(data)
        return Response(result)


def get_part(request, id):
    part = Part.objects.get(part=id)
    if not part:
        raise Http404
    serializer = PartSerializer(part)
    return render(request, 'views/part.html', context={'part': serializer.data})
