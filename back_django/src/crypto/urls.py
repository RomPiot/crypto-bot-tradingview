from django.urls import path
from crypto import views

urlpatterns = [
    path("", views.page_home, name="home"),
    path("import-historical", views.import_historical_request, name="import_historical"),
    path("get-candles", views.get_candles, name="get_candles"),
]
