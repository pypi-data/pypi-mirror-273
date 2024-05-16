from firebase_admin import auth


class FirebaseActionsCore:
    @staticmethod
    def generate_action_code_settings(url: str,
                                      handle_code_in_app: bool = False,
                                      ios_bundle_id: str = None,
                                      android_package_name: str = None,
                                      android_install_app: bool = False,
                                      android_minimum_version: str = None,
                                      dynamic_link_domain: str = None,
                                      ) -> auth.ActionCodeSettings:
        action_code_settings = auth.ActionCodeSettings(
            url=url,
            handle_code_in_app=handle_code_in_app,
            ios_bundle_id=ios_bundle_id,
            android_package_name=android_package_name,
            android_install_app=android_install_app,
            android_minimum_version=android_minimum_version,
            dynamic_link_domain=dynamic_link_domain
        )

        return action_code_settings

    @staticmethod
    def generate_password_reset_link(email: str, action_code_settings: auth.ActionCodeSettings) -> str:
        link = auth.generate_password_reset_link(email, action_code_settings)

        return link

    @staticmethod
    def generate_email_verification_link(email: str, action_code_settings: auth.ActionCodeSettings) -> str:
        link = auth.generate_email_verification_link(email, action_code_settings)

        return link

    @staticmethod
    def generate_email_sign_in_link(email: str, action_code_settings: auth.ActionCodeSettings) -> str:
        link = auth.generate_sign_in_with_email_link(email, action_code_settings)

        return link
