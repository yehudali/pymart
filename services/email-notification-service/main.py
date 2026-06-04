import asyncio
import json
import logging
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

import aio_pika

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --- Config (from environment variables) ---
RABBITMQ_URL   = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
QUEUE_NAME     = os.getenv("QUEUE_NAME", "order.place")
SMTP_HOST      = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT      = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER      = os.getenv("SMTP_USER")       # your Gmail address
SMTP_PASSWORD  = os.getenv("SMTP_PASSWORD")   # Gmail app password
FROM_EMAIL     = os.getenv("FROM_EMAIL", SMTP_USER)
STORE_NAME     = os.getenv("STORE_NAME", "Our Store")


# --- Email Templates ---

STATUS_LABELS = {
    "pending":    "⏳ Pending",
    "confirmed":  "✅ Confirmed",
    "shipped":    "🚚 Shipped",
    "delivered":  "📦 Delivered",
    "cancelled":  "❌ Cancelled",
}

def format_cart(cart: dict) -> str:
    lines = []
    total = 0.0
    for item in cart.values():
        name     = item.get("name", "Unknown")
        price    = float(item.get("price", 0))
        quantity = int(item.get("quantity", 1))
        subtotal = price * quantity
        total   += subtotal
        lines.append(f"  • {name} × {quantity}  —  ₪{subtotal:.2f}")
    lines.append(f"\n  Total: ₪{total:.2f}")
    return "\n".join(lines)

def build_email(order: dict) -> tuple[str, str]:
    """Returns (subject, html_body)"""
    order_id   = order.get("order_id", "N/A")
    status_key = order.get("status", "pending")
    status     = STATUS_LABELS.get(status_key, status_key.capitalize())
    cart       = order.get("cart", {})
    created_at = order.get("created_at", "")

    try:
        dt = datetime.fromisoformat(created_at)
        created_str = dt.strftime("%B %d, %Y at %H:%M")
    except Exception:
        created_str = created_at

    cart_rows = ""
    total = 0.0
    for item in cart.values():
        name     = item.get("name", "Unknown")
        price    = float(item.get("price", 0))
        quantity = int(item.get("quantity", 1))
        subtotal = price * quantity
        total   += subtotal
        cart_rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid #eee">{name}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:center">{quantity}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">₪{subtotal:.2f}</td>
        </tr>"""

    subject = f"[{STORE_NAME}] Order #{order_id[:8].upper()} — {status}"

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;color:#333">
      <div style="background:#4F46E5;padding:24px;border-radius:8px 8px 0 0">
        <h1 style="color:#fff;margin:0;font-size:22px">{STORE_NAME}</h1>
      </div>
      <div style="background:#fff;padding:32px;border:1px solid #e5e7eb;border-top:none;border-radius:0 0 8px 8px">

        <h2 style="margin-top:0">Order Update</h2>
        <p>Hi there! Here's the latest update on your order.</p>

        <table style="width:100%;border-collapse:collapse;margin-bottom:24px">
          <tr>
            <td style="padding:6px 0;color:#6b7280">Order ID</td>
            <td style="padding:6px 0;font-weight:bold">{order_id}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#6b7280">Placed on</td>
            <td style="padding:6px 0">{created_str}</td>
          </tr>
          <tr>
            <td style="padding:6px 0;color:#6b7280">Status</td>
            <td style="padding:6px 0;font-weight:bold;font-size:16px">{status}</td>
          </tr>
        </table>

        <h3 style="border-bottom:2px solid #4F46E5;padding-bottom:8px">Your Items</h3>
        <table style="width:100%;border-collapse:collapse">
          <thead>
            <tr style="background:#f9fafb">
              <th style="padding:8px 12px;text-align:left">Item</th>
              <th style="padding:8px 12px;text-align:center">Qty</th>
              <th style="padding:8px 12px;text-align:right">Price</th>
            </tr>
          </thead>
          <tbody>{cart_rows}</tbody>
          <tfoot>
            <tr>
              <td colspan="2" style="padding:12px;font-weight:bold;text-align:right">Total</td>
              <td style="padding:12px;font-weight:bold;text-align:right">₪{total:.2f}</td>
            </tr>
          </tfoot>
        </table>

        <p style="margin-top:32px;color:#6b7280;font-size:13px">
          Not reply to this email.<br>
          Thank you for shopping with {STORE_NAME}!
        </p>
      </div>
    </div>
    """
    return subject, html


# --- SMTP Sender ---

def send_email(to_email: str, subject: str, html_body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = FROM_EMAIL
    msg["To"]      = to_email
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, to_email, msg.as_string())


# --- RabbitMQ Consumer ---

async def handle_message(message: aio_pika.IncomingMessage) -> None:
    async with message.process():
        try:
            order = json.loads(message.body.decode())
            to_email = order.get("email")
            if not to_email:
                logger.warning("Message has no email field, skipping.")
                return

            subject, html_body = build_email(order)
            send_email(to_email, subject, html_body)
            logger.info(f"Email sent to {to_email} | order {order.get('order_id')} | status: {order.get('status')}")

        except json.JSONDecodeError:
            logger.error("Failed to parse message as JSON")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise  # re-raise so aio_pika nacks and requeues


async def main() -> None:
    logger.info("Connecting to RabbitMQ...")

    # Retry loop — RabbitMQ may not be ready immediately on startup
    for attempt in range(10):
        try:
            connection = await aio_pika.connect_robust(RABBITMQ_URL)
            break
        except Exception as e:
            logger.warning(f"RabbitMQ not ready (attempt {attempt + 1}/10): {e}")
            await asyncio.sleep(5)
    else:
        raise RuntimeError("Could not connect to RabbitMQ after 10 attempts")

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        logger.info(f"Listening on queue '{QUEUE_NAME}'...")

        await queue.consume(handle_message)
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
