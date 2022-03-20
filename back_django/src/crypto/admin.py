from django.contrib import admin
from crypto.models import Currency, Exchange, Historic, Order, Pair, Strategy
from django.db import models


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "updated_at")
#     list_editable = ("status",)
    pass

@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    pass

@admin.register(Historic)
class HistoricAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Pair)
class PairAdmin(admin.ModelAdmin):
    pass

@admin.register(Strategy)
class StrategyAdmin(admin.ModelAdmin):
    pass





#     form = PageForm

#     list_display = ("title", "author", "updated_at", "status")
#     list_editable = ("status",)

    # add_form = CustomAddFooForm  # It is not a native django field. I created this field and use it in get_form method.

    # def get_form(self, request, obj=None, **kwargs):
    #     """
    #     Use special form during foo creation
    #     """
    #     defaults = {}
    #     if obj is None:
    #         defaults["form"] = self.add_form
    #     defaults.update(kwargs)
    #     return super().get_form(request, obj, **defaults)


# @admin.register(Page)
# class PageAdmin(admin.ModelAdmin):
#     form = CustomFooForm
#     add_form = CustomAddFooForm  # It is not a native django field. I created this field and use it in get_form method.

#     def get_form(self, request, obj=None, **kwargs):
#         """
#         Use special form during foo creation
#         """
#         defaults = {}
#         if obj is None:
#             defaults["form"] = self.add_form
#         defaults.update(kwargs)
#         return super().get_form(request, obj, **defaults)
