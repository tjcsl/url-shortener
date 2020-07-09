from social_core.backends.oauth import BaseOAuth2


def get_user_permissions(backend, user, response, *args, **kwargs):
    if backend.name == "ion":
        admin = response["is_eighth_admin"] or response["is_announcements_admin"]
        teacher = response['is_teacher']
        user.is_admin = admin
        user.is_student = response["is_student"]
        user.is_teacher = teacher
        user.is_staff = admin or teacher
        user.is_superuser = admin
        user.save()


class IonOauth2(BaseOAuth2):
    name = "ion"
    AUTHORIZATION_URL = "https://ion.tjhsst.edu/oauth/authorize"
    ACCESS_TOKEN_URL = "https://ion.tjhsst.edu/oauth/token"
    ACCESS_TOKEN_METHOD = "POST"
    EXTRA_DATA = [("refresh_token", "refresh_token", True), ("expires_in", "expires")]

    def get_scope(self):
        return ["read"]

    def get_user_details(self, profile):
        # fields used to populate/update User model
        return {
            "id": profile["id"],
            "username": profile["ion_username"],
            "first_name": profile["first_name"],
            "last_name": profile["last_name"],
            "full_name": profile["full_name"],
            "email": profile["tj_email"],
            "is_student": profile["is_student"],
            "is_teacher": profile["is_teacher"],
            "is_admin": profile["is_eighth_admin"] or profile["is_announcements_admin"],
        }

    def user_data(self, access_token, *args, **kwargs):
        return self.get_json(
            "https://ion.tjhsst.edu/api/profile", params={"access_token": access_token}
        )

    def get_user_id(self, details, response):
        return details["id"]
