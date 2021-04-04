import os

from dotenv import load_dotenv
from pyfcm import FCMNotification

load_dotenv()

push_service = FCMNotification(api_key=os.getenv("serverKey"))


def send_medicine_notification(token):
    message_title = "Test medicine push"
    message_body = "test test test test test test test"
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)
    return result


def send_questionnaire_notification(token):
    message_title = "push project to github"
    message_body = "push project to github"
    result = push_service.notify_single_device(registration_id=token, message_title=message_title,
                                               message_body=message_body)
    return result

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
