from locale import currency
from django.db import models
from authentication.models import User
from app.models import BaseModel
# from django.template.defaultfilters import slugify

# STATUS = ((0, "Draft"), (1, "Publish"), (2, "Delete"))
# TIMEFRAME = (('1m', "1 minute"), ("1h", "1 hour"), (2, "Delete"))


class Currency(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    slug = models.SlugField(max_length=20, blank=False, null=False, unique=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Currency"

    def __str__(self):
        return self.name


class Exchange(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Exchange"

    def __str__(self):
        return self.name


class Strategy(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    parameters = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Strategy"

    def __str__(self):
        return self.name

class Pair(BaseModel):
    from_exchange = models.ForeignKey(Exchange, blank=False, null=True, on_delete=models.DO_NOTHING)
    currency = models.ForeignKey(Currency, blank=False, null=False, on_delete=models.DO_NOTHING, related_name='currency')
    to_currency = models.ForeignKey(Currency, blank=False, null=False, on_delete=models.DO_NOTHING, related_name='to_currency')
    last_imported = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pair"
        unique_together = ('from_exchange', 'currency', 'to_currency',)

    def __str__(self):
        return f"{self.currency.slug}/{self.to_currency.slug} ({self.from_exchange})"


class Order(BaseModel):
    exchange = models.ForeignKey(Exchange, blank=True, null=True, on_delete=models.DO_NOTHING)
    pair = models.ForeignKey(Pair, blank=True, null=True, on_delete=models.DO_NOTHING)
    strategy = models.ForeignKey(Strategy, blank=True, null=True, on_delete=models.DO_NOTHING)
    backtest = models.BooleanField()
    is_active = models.BooleanField()
    

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"

    def __str__(self):
        return f"{self.pair.currency.slug}/{self.pair.to_currency.slug} ({self.pair.exchange})"



class Historic(BaseModel):
    from_exchange = models.ForeignKey(Exchange, blank=True, null=True, on_delete=models.SET_NULL, editable=False)
    pair = models.ForeignKey(Pair, blank=True, null=True, on_delete=models.SET_NULL, editable=False)
    # timeframe = models.CharField(choices=TIMEFRAME, default=0)
    timeframe = models.CharField(max_length=20, blank=False, null=False)
    open_datetime = models.DateTimeField(blank=True, null=True, editable=False)
    close_datetime = models.DateTimeField(blank=True, null=True, editable=False)
    open_amount = models.FloatField()
    close_amount = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Historic"

    def __str__(self):
        return f"{self.pair.currency.slug}/{self.pair.to_currency.slug} ({self.from_exchange})"




# class Page(BaseModel):
#     title = models.CharField(max_length=255, blank=False, null=False, unique=True)
#     slug = models.SlugField(max_length=255, blank=True, null=False, unique=True)
#     author = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, editable=False)
#     content = models.JSONField(blank=True, null=True)
#     status = models.IntegerField(choices=STATUS, default=0)

#     class Meta:
#         ordering = ["-created_at"]
#         verbose_name = "Page"

#     def __str__(self):
#         return self.title

#     def save(self, *args, **kwargs):
#         if not self.slug:
#             self.slug = slugify(self.title)

#         super().save(*args, **kwargs)
