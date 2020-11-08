from django.test import TestCase

from shortener.apps.auth.models import User


class ShortnerTestCase(TestCase):
    def login(
        self,
        username="awilliam",
        make_teacher=False,
        make_student=False,
        make_superuser=False,
    ) -> User:
        """
        Log in as the specified user.

        Args:
            username: The username to log in as.
            make_teacher: Whether to make this user a teacher.
            make_student: Whether to make this user a student.
            make_superuser: Whether to make this user a superuser.

        Return:
            The user.

        """
        user = User.objects.update_or_create(
            username=username,
            defaults={
                "is_teacher": make_teacher,
                "is_student": make_student,
                "is_staff": make_superuser,
                "is_superuser": make_superuser,
            },
        )[0]
        self.client.force_login(user)
        return user
