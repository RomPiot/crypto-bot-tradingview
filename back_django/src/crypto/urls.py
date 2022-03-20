from django.urls import path
from crypto import views

urlpatterns = [
    path("", views.page_home, name="home"),
    # path("reparation/", views.page_reparation, name="reparation"),
    # path("contact/", views.page_contact, name="contact"),
]
