from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Не более 15 символов может уместиться в превью'
        )

    def test_post_model_has__str__(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        self.assertEqual(self.post.text[:15], str(self.post))


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )

    def test_models_have__str_group(self):
        """Проверяем, что у модели Group корректно работает __str__. group"""
        self.assertEqual(self.group.title, str(self.group))
