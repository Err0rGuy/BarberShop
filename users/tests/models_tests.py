from django.test import TestCase

from users.models import User


class TestUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', phone_number='+989156784432', password='Password111!')


    def test_password_changing(self):
        self.user.set_password('Password222!')
        self.assertFalse(self.user.check_password('Password111!'))
        self.assertTrue(self.user.check_password('Password222!'))

