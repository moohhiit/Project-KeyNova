from .utils import send_sms

def send_sms_alert(phone_number, details, username="Unknown User"):
    msg = f"""
🚨 ALERT: Inappropriate content detected for {username}
🧠 Category: {details.get('category', 'Unknown')}
💬 Reason: {details.get('reason', 'Not specified')}
"""
    if "sentiment" in details:
        msg += f"🙂 Sentiment: {details['sentiment']['label']} ({details['sentiment']['score']:.2f})\n"
    if "emotion" in details:
        msg += f"😢 Emotion: {details['emotion']['label']} ({details['emotion']['score']:.2f})\n"
    msg += f"🔍 Source: {details.get('source', 'N/A')}"

    send_sms(phone_number, msg)
