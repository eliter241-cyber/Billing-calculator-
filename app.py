
from flask import Flask, render_template, request, session
from billing import calculate_bill

app = Flask(__name__)
app.secret_key = "cartcraft-dev-key-change-before-deployment"


@app.route("/", methods=["GET", "POST"])
def home():
    cart = session.get("cart", [])
    result = session.get("result")
    error = None

    if request.method == "POST":
        action = request.form.get("action")

        try:
            if action == "add_product":
                name = request.form.get("name", "").strip()
                price = float(request.form.get("price", "0"))
                quantity = float(request.form.get("quantity", "0"))

                if not name:
                    raise ValueError("Enter a product name.")
                if price <= 0:
                    raise ValueError("Price must be greater than zero.")
                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")

                cart.append({
                    "name": name,
                    "price": price,
                    "quantity": quantity
                })

                session["cart"] = cart
                session.pop("result", None)
                session.pop("discount", None)
                result = None

            elif action == "remove_product":
                index = int(request.form.get("index", "-1"))

                if 0 <= index < len(cart):
                    cart.pop(index)

                session["cart"] = cart
                session.pop("result", None)
                session.pop("discount", None)
                result = None

            elif action == "calculate":
                if not cart:
                    raise ValueError("Add at least one product first.")

                discount = float(request.form.get("discount", "0"))

                result = calculate_bill(cart, discount)
                session["discount"] = discount
                session["result"] = result
                session.pop("member_answer", None)
                session.pop("gift", None)

            elif action == "membership":
                result = session.get("result")

                if not result:
                    raise ValueError("Calculate the bill first.")

                is_member = request.form.get("is_member") == "yes"
                gift = request.form.get("gift", "").lower()

                result["offer_unlocked"] = (
                    result["final_bill"] >= 1000 and is_member
                )

                result["gift"] = (
                    gift if result["offer_unlocked"]
                    and gift in ("watch", "scent")
                    else None
                )

                session["result"] = result
                session["member_answer"] = (
                    "yes" if is_member else "no"
                )

        except (ValueError, TypeError) as exc:
            error = str(exc) or "Please check your entries."

    cart = session.get("cart", [])
    result = session.get("result")

    running_total = sum(
        float(item["price"]) * float(item["quantity"])
        for item in cart
    )

    return render_template(
        "index.html",
        cart=cart,
        running_total=round(running_total, 2),
        result=result,
        error=error,
        discount=session.get("discount", 0),
        member_answer=session.get("member_answer")
    )


if __name__ == "__main__":
    app.run(debug=True)
