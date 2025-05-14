from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('organic-products/', views.organic_products_view, name='organic_products'),
    path('organic-manures/', views.organic_manures_view, name='organic_manures'),
    path('buy/<str:product_type>/<str:product_name>/', views.buynow_view, name='buynow'),
    path('sell-product/', views.sell_product_view, name='sell_product'),  # Add this line
    path('sell/', views.sell, name='sell'),  # Add this line
    path('organic-manures/', views.organic_manures_view, name='organic_manures'),
    path('organic-products/', views.organic_products_view, name='organic_products'),
]

