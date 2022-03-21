from django.urls import path
from crypto import views

urlpatterns = [
    path("", views.page_home, name="home"),
    path("import-candles", views.import_candles_request, name="import_candles"),
    path("get-candles", views.get_candles, name="get_candles"),
]
