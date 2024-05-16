import enum
from typing import Optional

from firebase_admin import auth
from firebase_admin._user_mgt import GetUsersResult


class FirebaseUserTokenStateEnum(enum.Enum):
    valid = 0
    revoked = 1
    invalid = 2
    expired = 3


class FirebaseUser:
    # get
    @staticmethod
    def get_user(uid: str) -> auth.UserRecord:
        user = auth.get_user(uid)

        return user

    @staticmethod
    def get_user_by_email(email: str) -> auth.UserRecord:
        user = auth.get_user_by_email(email)

        return user

    @staticmethod
    def get_user_by_phone_number(phone_number: str) -> auth.UserRecord:
        user = auth.get_user_by_phone_number(phone_number)

        return user

    @staticmethod
    def bulk_retrieve_users(uids: list) -> GetUsersResult:
        users = auth.get_users(uids)

        return users

    @staticmethod
    def get_users() -> auth.ListUsersPage:
        users = auth.list_users()

        return users

    # check
    @staticmethod
    def user_exists(uid: str) -> bool:
        try:
            FirebaseUser.get_user(uid)
            return True
        except auth.UserNotFoundError:
            return False

    @staticmethod
    def user_exists_by_email(email: str) -> bool:
        try:
            FirebaseUser.get_user_by_email(email)
            return True
        except auth.UserNotFoundError:
            return False

    @staticmethod
    def user_exists_by_phone_number(phone_number: str) -> bool:
        try:
            FirebaseUser.get_user_by_phone_number(phone_number)
            return True
        except auth.UserNotFoundError:
            return False

    # create
    @staticmethod
    def create_user(email: str,
                    password: str,
                    phone_number: str = None,
                    email_verified: bool = False,
                    display_name: str = None,
                    disabled: bool = False,
                    photo_url: str = None,
                    ) -> auth.UserRecord:
        user = auth.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            email_verified=email_verified,
            display_name=display_name,
            disabled=disabled,
            photo_url=photo_url
        )

        return user

    @staticmethod
    def update_user(uid: str,
                    email: str = None,
                    phone_number: str = None,
                    email_verified: bool = None,
                    display_name: str = None,
                    disabled: bool = None,
                    photo_url: str = None,
                    ) -> auth.UserRecord:
        user = auth.update_user(
            uid=uid,
            email=email,
            phone_number=phone_number,
            email_verified=email_verified,
            display_name=display_name,
            disabled=disabled,
            photo_url=photo_url
        )

        return user

    @staticmethod
    def delete_user(uid: str):
        auth.delete_user(uid)

        return True

    @staticmethod
    def delete_users(uids: list):
        auth.delete_users(uids)

        return True

    @staticmethod
    def verify_id_token(id_token: str, app=None, check_revoked=False, clock_skew_seconds=0) -> dict:
        decoded_token = auth.verify_id_token(id_token, app=app, check_revoked=check_revoked, clock_skew_seconds=clock_skew_seconds)

        return decoded_token

    @staticmethod
    def is_id_token_revoked(id_token: str) -> bool:
        try:
            FirebaseUser.verify_id_token(id_token=id_token, check_revoked=True)
            return False
        except auth.RevokedIdTokenError:
            return True

    @staticmethod
    def is_id_token_valid(id_token: str) -> bool:
        try:
            FirebaseUser.verify_id_token(id_token=id_token, check_revoked=False)
            return True
        except Exception:
            return False

    @staticmethod
    def id_token_state(id_token: str) -> FirebaseUserTokenStateEnum:
        try:
            FirebaseUser.verify_id_token(id_token=id_token, check_revoked=True)
            return FirebaseUserTokenStateEnum.valid
        except auth.RevokedIdTokenError:
            return FirebaseUserTokenStateEnum.revoked
        except auth.InvalidIdTokenError:
            return FirebaseUserTokenStateEnum.invalid
        except auth.ExpiredIdTokenError:
            return FirebaseUserTokenStateEnum.expired

    @staticmethod
    def get_uid_from_id_token(id_token: str) -> Optional[str]:
        try:
            decoded_token = FirebaseUser.verify_id_token(id_token)
        except auth.InvalidIdTokenError:
            return None

        uid = decoded_token['uid']

        return uid

    @staticmethod
    def create_custom_token(uid: str, claims: dict = None) -> str:
        token = auth.create_custom_token(uid, claims)

        return token.decode()

    @staticmethod
    def revoke_refresh_tokens(uid: str):
        auth.revoke_refresh_tokens(uid)

        return True

    @staticmethod
    def set_custom_user_claims(uid: str, claims: dict):
        auth.set_custom_user_claims(uid, claims)

        return True

    @staticmethod
    def get_custom_user_claims(uid: str) -> dict:
        user = FirebaseUser.get_user(uid)
        claims = user.custom_claims

        return claims
