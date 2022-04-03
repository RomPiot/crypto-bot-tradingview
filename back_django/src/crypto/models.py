from django.db import models
from app.models import BaseModel

# from authentication.models import User

# from django.template.defaultfilters import slugify

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
    slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    limit = models.CharField(max_length=255, blank=False, null=False)

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


class Symbol(BaseModel):
    from_exchange = models.ForeignKey(Exchange, blank=False, null=True, on_delete=models.DO_NOTHING)
    from_currency = models.ForeignKey(
        Currency, blank=False, null=False, on_delete=models.DO_NOTHING, related_name="from_currency"
    )
    to_currency = models.ForeignKey(
        Currency, blank=False, null=False, on_delete=models.DO_NOTHING, related_name="to_currency"
    )
    last_imported_minute = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_five_minutes = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_fiveteen_minutes = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_hour = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_four_hours = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_twelve_hours = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_day = models.DateTimeField(blank=True, null=True, editable=True)
    last_imported_week = models.DateTimeField(blank=True, null=True, editable=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Symbol"
        unique_together = (
            "from_exchange",
            "from_currency",
            "to_currency",
        )

    def __str__(self):
        return f"{self.from_currency.slug}/{self.to_currency.slug} ({self.from_exchange})"


class Order(BaseModel):
    exchange = models.ForeignKey(Exchange, blank=True, null=True, on_delete=models.DO_NOTHING)
    symbol = models.ForeignKey(Symbol, blank=True, null=True, on_delete=models.DO_NOTHING)
    strategy = models.ForeignKey(Strategy, blank=True, null=True, on_delete=models.DO_NOTHING)
    backtest = models.BooleanField()
    is_active = models.BooleanField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"

    def __str__(self):
        return f"{self.symbol.from_currency.slug}/{self.symbol.to_currency.slug} ({self.symbol.exchange})"


class Historical(BaseModel):
    from_exchange = models.ForeignKey(Exchange, blank=True, null=True, on_delete=models.SET_NULL, editable=False)
    symbol = models.ForeignKey(Symbol, blank=True, null=True, on_delete=models.SET_NULL, editable=False)
    timeframe = models.CharField(max_length=20, blank=False, null=False)
    datetime = models.DateTimeField(blank=True, null=True, editable=False)
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    volume = models.FloatField()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Historical"

        unique_together = (
            "from_exchange",
            "symbol",
            "timeframe",
            "datetime",
        )

    def __str__(self):
        return f"{self.symbol.from_currency.slug}/{self.symbol.to_currency.slug} ({self.from_exchange})"
