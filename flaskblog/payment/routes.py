from flask import Blueprint, jsonify, render_template, request
import stripe
from flask_login import current_user
from flaskblog import db
from sqlalchemy import exc

from flaskblog.config import Stripe_keys
from flaskblog.models import StripeCustomer

payment = Blueprint("payment", __name__)


stripe.api_key = Stripe_keys.secret_key


@payment.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": Stripe_keys.publishable_key}
    return jsonify(stripe_config)


@payment.route("/create-checkout-session")
def create_checkout_session():
    # breakpoint()
    global user_id
    user_id = current_user.id
    domain_url = "http://localhost:5000/"
    stripe.api_key = Stripe_keys.secret_key
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=current_user.id,
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": Stripe_keys.price_id,
                    "quantity": 1,
                }
            ],
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


@payment.route("/success")
def success():
    return render_template("success.html")


@payment.route("/cancel")
def cancelled():
    return render_template("cancel.html")


@payment.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, Stripe_keys.endpoint_secret
        )

    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        handle_checkout_session(session)

    return "Success", 200


def handle_checkout_session(session):
    # breakpoint()
    st_customer = session["customer"]
    sub_id = session["subscription"]
    stripe_customer = StripeCustomer(
        user_id=user_id, stripeCustomerId=st_customer, stripeSubscriptionId=sub_id
    )
    db.session.add(stripe_customer)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
    print("Subscription was successful.")
