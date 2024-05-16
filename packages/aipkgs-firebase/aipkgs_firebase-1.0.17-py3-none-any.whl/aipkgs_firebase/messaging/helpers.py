import datetime
from firebase_admin import messaging

from aipkgs_firebase.messaging.core import FirebaseMessagingCore
from aipkgs_firebase.messaging.enums import FirebaseMessaging


class FirebaseMessagingHelper:
    @staticmethod
    def send_to_token(token: str, data: dict):
        message = FirebaseMessagingCore.create_message(token=token, data=data)
        FirebaseMessagingCore.send_message(message=message)

    @staticmethod
    def send_to_topic(topic: str, data: dict):
        message = FirebaseMessagingCore.create_message(topic=topic, data=data)
        FirebaseMessagingCore.send_message(message)

    @staticmethod
    def send_to_condition(condition: str, notification: messaging.Notification):
        message = FirebaseMessagingCore.create_message(notification=notification, condition=condition)
        FirebaseMessagingCore.send_message(message=message)

    @staticmethod
    def send_dry_run(token: str, data: dict):
        message = FirebaseMessagingCore.create_message(token=token, data=data)
        FirebaseMessagingCore.send_message(message, dry_run=True)

    @staticmethod
    def send_multicast(data: dict, tokens: list):
        message = FirebaseMessagingCore.create_multicast_message(data=data, tokens=tokens)
        response = messaging.send_multicast(message)

    @staticmethod
    def send_multicast_and_handle_errors(data: dict, tokens: list):
        message = FirebaseMessagingCore.create_multicast_message(data=data, tokens=tokens)
        response = messaging.send_multicast(message)
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(tokens[idx])
            print('List of tokens that caused failures: {0}'.format(failed_tokens))

    @staticmethod
    def create_unity_message(title: str = None, body: str = None, badge: int = None, icon: str = None, web_icon: str = None, ios_priority: int = None,
                             android_priority: FirebaseMessaging.Enums.AndroidPriorityEnum = None, color: str = None, ttl_seconds: int = None, token: str = None,
                             topic: str = None):

        notification = FirebaseMessagingCore.create_notification(title=title, body=body)

        android_config = FirebaseMessagingCore.create_android_configuration(title=title, body=body, icon=icon, color=color, ttl_seconds=ttl_seconds, priority=android_priority)

        ios_apns_config = FirebaseMessagingCore.create_ios_apns_config(title=title, body=body, priority=ios_priority, badge=badge)

        web_push_config = FirebaseMessagingCore.create_web_push_config(title=title, body=body, icon=web_icon)

        message = FirebaseMessagingCore.create_message(token=token, notification=notification, android_config=android_config, apns_config=ios_apns_config, web_push=web_push_config, topic=topic)

        return message
