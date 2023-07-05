from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("products/", views.products, name="products"),
    path("product/<int:product_id>", views.product, name="product"),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("ourStory/", views.ourStory, name="ourStory"),
    path("contact/", views.contact, name="contact"),
    path('intialAddToCart/', views.intialAddToCart, name="intialAddToCart")
]