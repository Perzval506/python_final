from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .forms import StockInForm, ItemForm
from .models import StockIn, Item

def stockin_list(request):
    # create-on-top form
    form = StockInForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Stock-In saved.")
        return redirect("inventory:stockin_list")

    qs = StockIn.objects.select_related("item", "supplier").order_by("-delivered_at", "-id")
    page_obj = Paginator(qs, 12).get_page(request.GET.get("page"))

    return render(request, "inventory/stockin_list.html", {
        "form": form,
        "page_obj": page_obj,
        "items": Item.objects.all(),
    })

def stockin_edit(request, pk):
    si = get_object_or_404(StockIn, pk=pk)
    form = StockInForm(request.POST or None, instance=si)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Stock-In updated.")
        return redirect("inventory:stockin_list")
    return render(request, "inventory/stockin_edit.html", {"form": form, "si": si})

def stockin_delete(request, pk):
    si = get_object_or_404(StockIn, pk=pk)
    if request.method == "POST":
        si.delete()
        messages.success(request, "Stock-In deleted.")
    return redirect("inventory:stockin_list")

def item_quick_add(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Item added.")
    return redirect("inventory:stockin_list")

def stockin_report(request):
    # leave as placeholder for now so page renders
    rows = StockIn.objects.select_related("item","supplier").order_by("-delivered_at","-id")
    return render(request, "inventory/stockin_report.html", {"rows": rows, "items": Item.objects.all()})
