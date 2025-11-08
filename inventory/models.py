from django.conf import settings
from django.db import models
from django.db.models import F
from django.utils import timezone

UNIT_CHOICES = [
    ("pc", "pc"),
    ("kg", "kg"),
    ("g", "g"),
    ("L", "L"),
    ("ml", "ml"),
    ("pack", "pack"),
]

class Supplier(models.Model):
    name = models.CharField(max_length=120)
    contact = models.CharField(max_length=120, blank=True)
    address = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default="pc")
    location = models.CharField(max_length=120, blank=True)   # e.g., “Stockroom A”
    reorder_level = models.PositiveIntegerField(default=0)
    # kept denormalized for speed; maintained by StockIn.save()/delete()
    stock_on_hand = models.IntegerField(default=0)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.sku})"

class StockIn(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="stockins")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    location = models.CharField(max_length=120, blank=True)   # where received
    invoice_no = models.CharField(max_length=80, blank=True)
    delivered_at = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        on_delete=models.SET_NULL, null=True, blank=True, editable=False
    )

    class Meta:
        ordering = ["-delivered_at", "-id"]

    def __str__(self):
        return f"IN {self.quantity} {self.item}"

    # keep Item.stock_on_hand in sync and reject invalid/negative changes
    def save(self, *args, **kwargs):
        if self.pk:
            prev = type(self).objects.get(pk=self.pk)
            delta = int(self.quantity) - int(prev.quantity)
        else:
            delta = int(self.quantity)

        super().save(*args, **kwargs)  # save first to have pk for delete()

        if delta != 0:
            Item.objects.filter(pk=self.item_id).update(
                stock_on_hand=F("stock_on_hand") + delta
            )

    def delete(self, *args, **kwargs):
        # reversing the added quantity
        Item.objects.filter(pk=self.item_id).update(
            stock_on_hand=F("stock_on_hand") - int(self.quantity)
        )
        return super().delete(*args, **kwargs)
