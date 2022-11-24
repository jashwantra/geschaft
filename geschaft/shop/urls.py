from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='shophome'),
    path('about/', views.about,name='aboutus'),
    path('contact/', views.Contact,name='contactus'),
    path('special/', views.special,name='trackingstatus'),
    path('search/', views.search,name='search'),
    path('productview/<int:myid>', views.prodview,name='productview'),
    path('checkout/', views.checkout,name='checkout')
]