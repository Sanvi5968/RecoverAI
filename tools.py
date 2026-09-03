def retry_payment(transaction_id, amount):
    return {
        "action": "Retry Payment",
        "transaction_id": transaction_id,
        "amount": float(amount),
        "status": "Retry Initiated",
        "message": "Payment retry initiated successfully."
    }


def generate_payment_link(transaction_id, amount):
    payment_link_id = f"PL-{transaction_id}"

    return {
        "action": "Generate Payment Link",
        "transaction_id": transaction_id,
        "amount": float(amount),
        "payment_link_id": payment_link_id,
        "status": "Payment Link Created",
        "message": "New payment link generated."
    }


def send_notification(transaction_id, amount):
    return {
        "action": "Send Notification",
        "transaction_id": transaction_id,
        "amount": float(amount),
        "status": "Notification Sent",
        "message": "Recovery notification sent to customer."
    }


def defer_recovery(transaction_id, amount):
    return {
        "action": "Defer Recovery",
        "transaction_id": transaction_id,
        "amount": float(amount),
        "status": "Deferred",
        "message": "Recovery action deferred for later review."
    }