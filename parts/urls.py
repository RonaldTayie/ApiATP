from django.urls import path
from django.views.generic import TemplateView

from .views import *

urlpatterns = [
    path('',TemplateView.as_view(template_name='views/index.html')),
    path('part',PartListView.as_view(),name="parts"),
    path('contact-us',TemplateView.as_view(template_name='views/contact-us.html')),
    path('cart',TemplateView.as_view(template_name='views/cart.html')),
    path('part/<str:id>',get_part,name="part"),
    path('bulk-create-parts',upload_parts)
]