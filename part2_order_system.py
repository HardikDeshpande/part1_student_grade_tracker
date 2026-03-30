# ============================================================
# Restaurant Menu & Order Management System
# ============================================================

import copy  # needed for deep copy in task 3


# ---------- provided data (untouched) ----------

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}


# ============================================================
# TASK 1 — Explore the Menu
# ============================================================

print("\n\n========== TASK 1: Menu Explorer ==========\n")

# collect unique categories in a fixed display order
# (dict insertion order is preserved in Python 3.7+, but categories repeat,
#  so we build a list of unique ones as we see them)
categories = []
for item_info in menu.values():
    cat = item_info["category"]
    if cat not in categories:
        categories.append(cat)

# print grouped menu
for cat in categories:
    print(f"===== {cat} =====")
    for item_name, item_info in menu.items():
        if item_info["category"] == cat:
            # pick the label based on the boolean
            availability = "[Available]" if item_info["available"] else "[Unavailable]"
            print(f"  {item_name:<18} ₹{item_info['price']:.2f}   {availability}")
    print()  # blank line between categories

# --- dictionary stats ---

total_items = len(menu)  # .keys() is implied

# count available ones by going through all items
available_count = 0
for info in menu.values():
    if info["available"]:
        available_count += 1

# find the most expensive item manually (not using max() with key= — more readable for beginners)
expensive_item = None
expensive_price = -1
for name, info in menu.items():
    if info["price"] > expensive_price:
        expensive_price = info["price"]
        expensive_item = name

print(f"Total items on menu  : {total_items}")
print(f"Available items      : {available_count}")
print(f"Most expensive item  : {expensive_item} (₹{expensive_price:.2f})")

# items under ₹150
print("Items priced under ₹150:")
for name, info in menu.items():
    if info["price"] < 150:
        print(f"  {name:<18} ₹{info['price']:.2f}")


# ============================================================
# TASK 2 — Cart Operations
# ============================================================

print("\n\n========== TASK 2: Cart Operations ==========\n")

cart = []

# --- helper functions for cart logic ---

def add_to_cart(cart, item_name, quantity):
    # first check the item exists at all
    if item_name not in menu:
        print(f"  ✗ '{item_name}' is not on the menu.")
        return

    # then check availability
    if not menu[item_name]["available"]:
        print(f"  ✗ '{item_name}' is currently unavailable.")
        return

    # check if it's already sitting in the cart
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            print(f"  ✓ Updated '{item_name}' quantity to {entry['quantity']}")
            return

    # not found in cart, so add fresh entry
    cart.append({
        "item": item_name,
        "quantity": quantity,
        "price": menu[item_name]["price"]
    })
    print(f"  ✓ Added '{item_name}' × {quantity} to cart")


def remove_from_cart(cart, item_name):
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            cart.pop(i)
            print(f"  ✓ Removed '{item_name}' from cart")
            return
    # only reaches here if item wasn't found
    print(f"  ✗ '{item_name}' is not in the cart.")


def update_quantity(cart, item_name, new_qty):
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = new_qty
            print(f"  ✓ '{item_name}' quantity updated to {new_qty}")
            return
    print(f"  ✗ '{item_name}' not found in cart.")


def print_cart(cart):
    if not cart:
        print("  (cart is empty)")
        return
    for entry in cart:
        line_total = entry["price"] * entry["quantity"]
        print(f"  {entry['item']:<20} x{entry['quantity']}  ₹{line_total:.2f}")


# --- simulate the order sequence ---

print("Step 1: Add Paneer Tikka × 2")
add_to_cart(cart, "Paneer Tikka", 2)
print_cart(cart)

print("\nStep 2: Add Gulab Jamun × 1")
add_to_cart(cart, "Gulab Jamun", 1)
print_cart(cart)

print("\nStep 3: Add Paneer Tikka × 1 (should update qty, not duplicate)")
add_to_cart(cart, "Paneer Tikka", 1)
print_cart(cart)

print("\nStep 4: Try adding 'Mystery Burger' (doesn't exist)")
add_to_cart(cart, "Mystery Burger", 1)
print_cart(cart)

print("\nStep 5: Try adding 'Chicken Wings' (unavailable)")
add_to_cart(cart, "Chicken Wings", 1)
print_cart(cart)

print("\nStep 6: Remove Gulab Jamun")
remove_from_cart(cart, "Gulab Jamun")
print_cart(cart)

# --- final order summary ---
print("\n========== Order Summary ==========")
subtotal = 0
for entry in cart:
    line_total = entry["price"] * entry["quantity"]
    subtotal += line_total
    print(f"  {entry['item']:<20} x{entry['quantity']}    ₹{line_total:.2f}")

gst = round(subtotal * 0.05, 2)
total_payable = round(subtotal + gst, 2)

print("------------------------------------")
print(f"  {'Subtotal:':<28} ₹{subtotal:.2f}")
print(f"  {'GST (5%):':<28} ₹{gst:.2f}")
print(f"  {'Total Payable:':<28} ₹{total_payable:.2f}")
print("====================================")


# ============================================================
# TASK 3 — Inventory Tracker with Deep Copy
# ============================================================

print("\n\n========== TASK 3: Inventory Tracker ==========\n")

# deep copy so changes to inventory don't touch the backup
inventory_backup = copy.deepcopy(inventory)

# --- demonstrate that deep copy is independent ---
print("--- Demonstrating deep copy independence ---")
print(f"  inventory['Paneer Tikka'] stock BEFORE change : {inventory['Paneer Tikka']['stock']}")
inventory["Paneer Tikka"]["stock"] = 999  # deliberately mess with inventory
print(f"  inventory['Paneer Tikka'] stock AFTER change  : {inventory['Paneer Tikka']['stock']}")
print(f"  backup  ['Paneer Tikka'] stock (unchanged)    : {inventory_backup['Paneer Tikka']['stock']}")

# restore inventory back to original before continuing
inventory["Paneer Tikka"]["stock"] = inventory_backup["Paneer Tikka"]["stock"]
print("  Inventory restored to original.")

# --- deduct cart quantities from inventory ---
print("\n--- Deducting cart items from inventory ---")
for entry in cart:
    item_name = entry["item"]
    qty_needed = entry["quantity"]
    current_stock = inventory[item_name]["stock"]

    if qty_needed > current_stock:
        print(f"  ⚠ Not enough stock for '{item_name}'. Need {qty_needed}, have {current_stock}. Deducting what's available.")
        inventory[item_name]["stock"] = 0
    else:
        inventory[item_name]["stock"] -= qty_needed
        print(f"  ✓ Deducted {qty_needed} from '{item_name}' — new stock: {inventory[item_name]['stock']}")

# --- reorder alerts ---
print("\n--- Reorder Alerts ---")
for item_name, info in inventory.items():
    if info["stock"] <= info["reorder_level"]:
        print(f"  ⚠ Reorder Alert: {item_name} — Only {info['stock']} unit(s) left (reorder level: {info['reorder_level']})")

# --- side-by-side comparison to confirm backup is intact ---
print("\n--- Inventory vs Backup (Paneer Tikka example) ---")
print(f"  inventory : {inventory['Paneer Tikka']}")
print(f"  backup    : {inventory_backup['Paneer Tikka']}")


# ============================================================
# TASK 4 — Daily Sales Log Analysis
# ============================================================

print("\n\n========== TASK 4: Sales Log Analysis ==========\n")

# --- revenue per day (original data) ---
def print_revenue_table(log):
    print(f"  {'Date':<14} {'Revenue':>10}")
    print("  " + "-" * 26)
    for date, orders in log.items():
        day_total = sum(order["total"] for order in orders)
        print(f"  {date:<14} ₹{day_total:>9.2f}")

print("Revenue per day:")
print_revenue_table(sales_log)

# --- best selling day ---
def get_best_day(log):
    best_date  = None
    best_total = -1
    for date, orders in log.items():
        day_total = sum(order["total"] for order in orders)
        if day_total > best_total:
            best_total = day_total
            best_date  = date
    return best_date, best_total

best_date, best_total = get_best_day(sales_log)
print(f"\nBest-selling day: {best_date} (₹{best_total:.2f})")

# --- most ordered item ---
# go through every order on every day and tally how many orders each item appears in
item_order_count = {}
for date, orders in sales_log.items():
    for order in orders:
        for item in order["items"]:
            if item not in item_order_count:
                item_order_count[item] = 0
            item_order_count[item] += 1

# find the item with the highest count manually
top_item = None
top_count = -1
for item, count in item_order_count.items():
    if count > top_count:
        top_count = count
        top_item  = item

print(f"\nMost ordered item: {top_item} (appears in {top_count} orders)")

# --- add new day and reprint ---
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]

print("\n--- After adding 2025-01-05 ---")
print("Updated revenue per day:")
print_revenue_table(sales_log)

best_date, best_total = get_best_day(sales_log)
print(f"\nUpdated best-selling day: {best_date} (₹{best_total:.2f})")

# --- numbered list of all orders across all dates ---
print("\nAll Orders (numbered):")
counter = 1  # running index across all days
for date, orders in sales_log.items():
    for order in orders:
        items_str = ", ".join(order["items"])
        print(f"  {counter}. [{date}] Order #{order['order_id']}  — ₹{order['total']:.2f} — Items: {items_str}")
        counter += 1
