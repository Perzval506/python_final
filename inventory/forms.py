from django import forms
from .models import StockIn, Item, Supplier

class StockInForm(forms.ModelForm):
    class Meta:
        model = StockIn
        fields = ["item", "supplier", "quantity", "unit_cost", "location",
                  "invoice_no", "delivered_at", "notes"]
        widgets = {
            "delivered_at": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 2, "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            if not isinstance(f.widget, forms.Textarea):
                f.widget.attrs.setdefault("class", "form-control")

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["sku", "name", "unit", "location", "reorder_level"]
        widgets = {f: forms.TextInput(attrs={"class": "form-control"}) for f in ["sku","name","location"]}
