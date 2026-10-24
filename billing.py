
def calculate_bill(products, discount, is_member=False, gift=None):
    if not products:
        raise ValueError("Add at least one product.")

    if not 0 <= discount <= 100:
        raise ValueError("Discount must be between 0 and 100.")

    cart = []
    total = 0

    for item in products:
        name = str(item["name"]).strip()
        price = float(item["price"])
        quantity = float(item["quantity"])

        if not name:
            raise ValueError("Product name cannot be empty.")

        if price <= 0 or quantity <= 0:
            raise ValueError("Price and quantity must be positive.")

        subtotal = round(price * quantity, 2)
        total += subtotal

        cart.append({
            "name": name,
            "price": price,
            "quantity": quantity,
            "subtotal": subtotal
        })

    total = round(total, 2)
    discount_amount = round(total * discount / 100, 2)
    final_bill = round(total - discount_amount, 2)

    membership_eligible = final_bill >= 1000
    offer_unlocked = membership_eligible and is_member

    selected_gift = None

    if offer_unlocked and gift in ("watch", "scent"):
        selected_gift = gift

    return {
        "products": cart,
        "total": total,
        "discount": discount,
        "discount_amount": discount_amount,
        "final_bill": final_bill,
        "membership_eligible": membership_eligible,
        "offer_unlocked": offer_unlocked,
        "gift": selected_gift
    }
