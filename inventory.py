# ================================
# Inventory Management System
# By: Fitsum (aonaran)
#
# OOP Inheritance structure:
#
# Product  ← parent class
# ├── Electronics  ← child
# ├── Food         ← child
# └── Clothing     ← child
# ================================

import json
import os
from datetime import datetime

FILE = "inventory.json"

# =============================================
# PARENT CLASS — Product
# =============================================
class Product:
    def __init__(self, pid, name, price, quantity):
        self.pid = pid
        self.name = name
        self.price = price
        self.quantity = quantity

    # Restock — add more items
    def restock(self, amount):
        if amount <= 0:
            print("❌ Amount must be positive.")
            return
        self.quantity += amount
        print(f"✅ Restocked '{self.name}'. New stock: {self.quantity}")

    # Sell — reduce stock
    def sell(self, amount):
        if amount <= 0:
            print("❌ Amount must be positive.")
            return False
        if amount > self.quantity:
            print(f"❌ Not enough stock. Only {self.quantity} available.")
            return False
        self.quantity -= amount
        total = amount * self.price
        print(f"✅ Sold {amount}x '{self.name}' for ${total:.2f}")
        return True

    # Check if stock is running low
    def is_low_stock(self):
        return self.quantity <= 5

    # Total value of this product in stock
    def get_value(self):
        return self.price * self.quantity

    # Display product info — child classes extend this
    def display(self):
        status = "⚠️ LOW STOCK" if self.is_low_stock() else "✅ In Stock"
        print(f"\n  [{self.pid}] {self.name}")
        print(f"  Price:  ${self.price:.2f}")
        print(f"  Stock:  {self.quantity} units  {status}")
        print(f"  Value:  ${self.get_value():.2f}")

    # Convert to dict for JSON saving
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "pid": self.pid,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity
        }


# =============================================
# CHILD CLASS 1 — Electronics
# =============================================
class Electronics(Product):
    def __init__(self, pid, name, price, quantity, brand, warranty_years):
        # super() calls the parent constructor — like Java's super()
        super().__init__(pid, name, price, quantity)
        self.brand = brand
        self.warranty_years = warranty_years

    # Override display — add extra electronics info
    def display(self):
        super().display()  # Call parent display first
        print(f"  Brand:    {self.brand}")
        print(f"  Warranty: {self.warranty_years} year(s) 🔌")

    def to_dict(self):
        d = super().to_dict()
        d["brand"] = self.brand
        d["warranty_years"] = self.warranty_years
        return d


# =============================================
# CHILD CLASS 2 — Food
# =============================================
class Food(Product):
    def __init__(self, pid, name, price, quantity, expiry_date, is_organic):
        super().__init__(pid, name, price, quantity)
        self.expiry_date = expiry_date
        self.is_organic = is_organic

    # Check if food has expired
    def is_expired(self):
        today = datetime.today().strftime("%Y-%m-%d")
        return self.expiry_date < today

    # Override display — add expiry and organic info
    def display(self):
        super().display()
        organic = "🌿 Organic" if self.is_organic else "Regular"
        expired = "❌ EXPIRED!" if self.is_expired() else "✅ Fresh"
        print(f"  Expiry:   {self.expiry_date}  {expired}")
        print(f"  Type:     {organic} 🍎")

    def to_dict(self):
        d = super().to_dict()
        d["expiry_date"] = self.expiry_date
        d["is_organic"] = self.is_organic
        return d


# =============================================
# CHILD CLASS 3 — Clothing
# =============================================
class Clothing(Product):
    def __init__(self, pid, name, price, quantity, size, color, material):
        super().__init__(pid, name, price, quantity)
        self.size = size
        self.color = color
        self.material = material

    # Override display — add clothing details
    def display(self):
        super().display()
        print(f"  Size:     {self.size}")
        print(f"  Color:    {self.color}")
        print(f"  Material: {self.material} 👕")

    def to_dict(self):
        d = super().to_dict()
        d["size"] = self.size
        d["color"] = self.color
        d["material"] = self.material
        return d


# =============================================
# INVENTORY MANAGER CLASS
# =============================================
class Inventory:
    def __init__(self):
        self.products = {}
        self.load()

    # Load from file — rebuild correct child class
    def load(self):
        if not os.path.exists(FILE):
            return
        with open(FILE, 'r') as f:
            data = json.load(f)

        for pid, info in data.items():
            t = info["type"]
            if t == "Electronics":
                p = Electronics(
                    info["pid"], info["name"], info["price"],
                    info["quantity"], info["brand"], info["warranty_years"]
                )
            elif t == "Food":
                p = Food(
                    info["pid"], info["name"], info["price"],
                    info["quantity"], info["expiry_date"], info["is_organic"]
                )
            elif t == "Clothing":
                p = Clothing(
                    info["pid"], info["name"], info["price"],
                    info["quantity"], info["size"],
                    info["color"], info["material"]
                )
            else:
                continue
            self.products[pid] = p

    # Save all products to file
    def save(self):
        data = {pid: p.to_dict() for pid, p in self.products.items()}
        with open(FILE, 'w') as f:
            json.dump(data, f, indent=4)

    # Add new product
    def add_product(self):
        print("\n--- ADD PRODUCT ---")
        print("Category:")
        print("  1. Electronics")
        print("  2. Food")
        print("  3. Clothing")

        cat = input("Choose (1/2/3): ").strip()
        if cat not in ["1", "2", "3"]:
            print("❌ Invalid category.")
            return

        pid = input("Product ID (e.g. P001): ").strip()
        if pid in self.products:
            print("⚠️  ID already exists!")
            return

        name = input("Product name: ").strip()

        try:
            price = float(input("Price ($): "))
            quantity = int(input("Quantity: "))
        except ValueError:
            print("❌ Invalid number.")
            return

        if cat == "1":
            brand = input("Brand: ").strip()
            try:
                warranty = int(input("Warranty (years): "))
            except ValueError:
                warranty = 1
            p = Electronics(pid, name, price, quantity, brand, warranty)

        elif cat == "2":
            expiry = input("Expiry date (YYYY-MM-DD): ").strip()
            organic = input("Organic? (yes/no): ").lower() == "yes"
            p = Food(pid, name, price, quantity, expiry, organic)

        else:
            size = input("Size (S/M/L/XL): ").strip().upper()
            color = input("Color: ").strip()
            material = input("Material: ").strip()
            p = Clothing(pid, name, price, quantity, size, color, material)

        self.products[pid] = p
        self.save()
        print(f"\n✅ '{name}' added to inventory!")

    # View all products
    def view_all(self):
        print("\n--- ALL PRODUCTS ---")
        if not self.products:
            print("No products yet.")
            return
        for p in self.products.values():
            p.display()
            print("  " + "─" * 34)

    # Search by name or ID
    def search(self):
        print("\n--- SEARCH ---")
        query = input("Search by name or ID: ").strip().lower()
        found = False
        for p in self.products.values():
            if query in p.name.lower() or query in p.pid.lower():
                p.display()
                found = True
        if not found:
            print("❌ No products found.")

    # Restock a product
    def restock(self):
        print("\n--- RESTOCK ---")
        pid = input("Product ID: ").strip()
        if pid not in self.products:
            print("❌ Product not found.")
            return
        try:
            amount = int(input("Amount to add: "))
            self.products[pid].restock(amount)
            self.save()
        except ValueError:
            print("❌ Invalid amount.")

    # Sell a product
    def sell(self):
        print("\n--- SELL PRODUCT ---")
        pid = input("Product ID: ").strip()
        if pid not in self.products:
            print("❌ Product not found.")
            return
        try:
            amount = int(input("Quantity to sell: "))
            if self.products[pid].sell(amount):
                self.save()
        except ValueError:
            print("❌ Invalid amount.")

    # Show low stock alerts
    def low_stock_alert(self):
        print("\n--- LOW STOCK ALERTS ---")
        low = [p for p in self.products.values() if p.is_low_stock()]
        if not low:
            print("✅ All products are sufficiently stocked!")
            return
        print(f"⚠️  {len(low)} product(s) need restocking:\n")
        for p in low:
            print(f"  [{p.pid}] {p.name} — only {p.quantity} left!")

    # Summary report
    def summary(self):
        print("\n--- INVENTORY SUMMARY ---")
        if not self.products:
            print("No products yet.")
            return

        total_value = sum(p.get_value() for p in self.products.values())
        total_items = sum(p.quantity for p in self.products.values())

        # Group products by type
        groups = {}
        for p in self.products.values():
            t = p.__class__.__name__
            if t not in groups:
                groups[t] = {"count": 0, "value": 0.0}
            groups[t]["count"] += 1
            groups[t]["value"] += p.get_value()

        print(f"\n  Total Products: {len(self.products)}")
        print(f"  Total Items:    {total_items} units")
        print(f"  Total Value:    ${total_value:.2f}")
        print(f"\n  Breakdown by Category:")

        for cat, info in groups.items():
            bar = "█" * int((info["value"] / total_value) * 20)
            print(f"\n    {cat}")
            print(f"    {bar} {info['count']} products — ${info['value']:.2f}")


# =============================================
# MAIN MENU
# =============================================
def main():
    print("=" * 40)
    print("   INVENTORY MANAGEMENT SYSTEM ")
    print("=" * 40)

    inv = Inventory()

    while True:
        print("\nMenu:")
        print("  1. Add Product")
        print("  2. View All Products")
        print("  3. Search Product")
        print("  4. Restock Product")
        print("  5. Sell Product")
        print("  6. Low Stock Alerts")
        print("  7. Inventory Summary")
        print("  8. Exit")

        choice = input("\nChoose (1-8): ")

        if choice == "1":   inv.add_product()
        elif choice == "2": inv.view_all()
        elif choice == "3": inv.search()
        elif choice == "4": inv.restock()
        elif choice == "5": inv.sell()
        elif choice == "6": inv.low_stock_alert()
        elif choice == "7": inv.summary()
        elif choice == "8":
            print("\nGoodbye! ")
            break
        else:
            print("Invalid choice. Try again.")

main()