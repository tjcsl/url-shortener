from social_core.backends.oauth import BaseOAuth2


class IonOauth2(BaseOAuth2):  # pylint: disable=abstract-method
    name = "ion"
    AUTHORIZATION_URL = "https://ion.tjhsst.edu/oauth/authorize"
    ACCESS_TOKEN_URL = "https://ion.tjhsst.edu/oauth/token"
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [("refresh_token", "refresh_token", True), ("expires_in", "expires")]

    def get_scope(self):
        return ["read"]

    def get_user_details(self, response):
        # fields used to populate/update User model
        admin = response["is_eighth_admin"]
        return {
            "id": response["id"],
            "username": response["ion_username"],
            "first_name": response["first_name"],
            "last_name": response["last_name"],
            "full_name": response["full_name"],
            "email": response["tj_email"],
            "is_student": response["is_student"],
            "is_teacher": response["is_teacher"],
            "is_staff": admin,
            "is_superuser": admin,
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            "https://ion.tjhsst.edu/api/profile", params={"access_token": access_token}
        )

    def get_user_id(self, details, response):
        return details["id"]
