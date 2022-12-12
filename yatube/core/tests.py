from http import HTTPStatus

from django.test import Client, TestCase


class ViewTestClass(TestCase):

    def setUp(self):
        self.guest_client = Client()

    def test_unexisting_page_status(self):
        """Несуществующая страница выдаёт ошибку."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_unexisting_page_uses_correct_template(self):
        """Несуществующая страница использует соответствующий шаблон."""
        template = 'core/404.html'
        response = self.guest_client.get('/unexisting_page/')
        self.assertTemplateUsed(response, template)
