# IMS Stock-In Subsystem (Inventory Management System)

**Course:** SIA / Software Engineering  
**Subsystem Implemented:** Boyds Pizza House Inventory Management System
**Original System:** *Inventory Management System (IMS)*

---

## 👥 Group

- **Group Name:** Lonita
- **Members:** Estanislao · Igtanloc · Ilanga · Mearns · Pimentel · Rivera

---

##  What this subsystem does (Use Cases & Flow)

**Primary Use Case: Record Stock-In**  
Staff records new deliveries into the stockroom; the system updates stock levels automatically.

- **Actors:** Staff (Stockroom), Owner/Manager  
- **Preconditions:** Delivery/Invoice exists  
- **Trigger:** Staff inputs delivery details  
- **Main Flow:**
  1) Enter **Item, Supplier, Quantity, Unit Cost, Location, Invoice No., Date, Notes**
  2) Submit form → system **creates a StockIn record**
  3) System **recalculates `Item.stock_on_hand`** (atomic update)
- **Postconditions:** Stockroom inventory increased; levels reconciled  
- **Exceptions:** Invalid/negative quantity or missing required fields → form rejects

**Related (future) Use Cases:** Transfer to Shelf, Record Stock-Out, Stock Count.

---

## Features (rubric-aligned)

- **CRUD on one page**
  - **List page** `/stockin/`: shows records (paginated)
  - **Create form** on top of the list
  - **Edit page** `/stockin/<id>/edit/` (not on navbar)
  - **Delete** link (POST + CSRF)
- **Printable report** `/stockin/report/`  
  - Filter by date range and item; totals; print stylesheet
- **Auto stock reconciliation**  
  - Save/Edit/Delete a Stock-In adjusts `Item.stock_on_hand`
- **Simple Bootstrap UI** with functional navbar
- **Admin panel** to maintain Items & Suppliers

---

##  Data Model (Entities)

- **Supplier**: `name`, `contact`, `address`  
- **Item**: `sku`, `name`, `unit`, `location`, `reorder_level`, `stock_on_hand`  
- **StockIn**: `item`, `supplier`, `quantity`, `unit_cost`, `location`, `invoice_no`, `delivered_at`, `notes`, `created_by`, timestamps

> Business rule: `StockIn.save()` / `delete()` adjust `Item.stock_on_hand` with atomic `F()` updates.

---

##  URLs

- `/stockin/` — List + **Create**  
- `/stockin/<id>/edit/` — **Edit** (separate page)  
- `/stockin/<id>/delete/` — **Delete** (POST)  
- `/stockin/report/` — **Report & Print**  
- `/admin/` — Django Admin

---

## 🛠️ Tech Stack

- Django 4.2 (Python 3.12)  
- SQLite (dev)  
- Templates with Bootstrap 5 (CDN)

---

##  How to run locally

```bash
# 1) clone
git clone https://github.com/Perzval506/python_final.git
cd python_final

# 2) venv
python3 -m venv .venv
source .venv/bin/activate

# 3) install
pip install -r requirements.txt

# 4) database + admin
python manage.py migrate
python manage.py createsuperuser

# 5) run
python manage.py runserver
# open http://127.0.0.1:8000/stockin/
