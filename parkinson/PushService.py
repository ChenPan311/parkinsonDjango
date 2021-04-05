import os

from dotenv import load_dotenv
from pyfcm import FCMNotification

load_dotenv()

push_service = FCMNotification(api_key=os.getenv("serverKey"))


def send_medicine_notification(token):
    message_title = "התבצעו שינויים בתרופותיך!"
    message_body = "שלום, הרופא ביצע שינוי בתרופותיך, אנא שים לב."
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)
    return result


def send_questionnaire_notification(token):
    message_title = "עדכון שאלון"
    message_body = "שלום, נדרש עדכון בשאלונך, אנא בצע זאת בהקדם."
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)
    return result