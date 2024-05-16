from firebase_admin import auth
from firebase_admin._user_mgt import GetUsersResult


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
