from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_group',
            description='Тестовое описание')

        cls.user_author = User.objects.create_user(
            username='user_auth')
        cls.user_not_author = User.objects.create_user(
            username='user_not_auth')

        cls.post = Post.objects.create(
            author=cls.user_author,
            text='Тестовое описание поста')

    def setUp(self):
        self.guest_client = Client()
        self.post_author = Client()
        self.post_author.force_login(self.user_author)
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_not_author)

    def test_urls_guest_client(self):
        """Доступ неавторизованного пользователя"""
        pages = {
            reverse(
                'posts:index'),
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}),
            reverse(
                'posts:profile',
                kwargs={'username': self.user_author}),
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id})
        }
        for page in pages:
            with self.subTest(page=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_authorized_client(self):
        """Доступ авторизованного пользователя"""
        pages = {
            reverse(
                'posts:post_create'),
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}),
            reverse(
                'posts:follow_index')
        }
        for page in pages:
            with self.subTest(page=page):
                response = self.post_author.get(page)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_redirect_guest_client(self):
        """Редирект неавторизованного пользователя"""
        pages = {
            reverse(
                'posts:post_create'): '/auth/login/?next=/create/',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}):
                    f'/auth/login/?next=/posts/{self.post.id}/edit/',
            reverse(
                'posts:follow_index'): '/auth/login/?next=/follow/'
        }
        for page, value in pages.items():
            response = self.guest_client.get(page, follow=True)
            self.assertRedirects(response, value)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse(
                'posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': self.user_author}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}): 'posts/post_detail.html',
            reverse(
                'posts:post_create'): 'posts/create.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}): 'posts/create.html',
            reverse(
                'posts:follow_index'): 'posts/follow.html'
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.post_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_not_post_author_redirected(self):
        """Редирект пользователя не являющегося автором поста"""
        response = self.authorized_client.get(reverse(
            'posts:post_edit',
            kwargs={'post_id': self.post.id}),
            follow=True)
        self.assertRedirects(
            response, reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}))
