# posts/tests/test_urls.py
from http import HTTPStatus
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


AUTHOR = 'user'
ANOTHER = 'another'
TITLE = 'test title'
SLUG = 'test-slug'
DESCRIPTION = 'test description'
TEXT = 'test text'
INDEX_URL = reverse('posts:index')
GROUP_LIST_URL = reverse('posts:group_list', args=[SLUG])
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])
POST_CREATE_URL = reverse('posts:post_create')
UNEXISTING_URL = '/unexisting_page/'
USER_URL = reverse('users:login')
FOLLOW_URL = reverse('posts:follow_index')
NEXT = '?next='
POST_CREATE_REDIRECT = f'{USER_URL}{NEXT}{POST_CREATE_URL}'
FOLLOW_REDIRECT = f'{USER_URL}{NEXT}{FOLLOW_URL}'


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.user_login = User.objects.create_user(username=ANOTHER)
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEXT,
        )
        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.pk])
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.pk])
        cls.POST_EDIT_REDIRECT = f'{USER_URL}{NEXT}{cls.POST_EDIT_URL}'
        cls.guest = Client()
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.another.force_login(cls.user_login)

    def setUp(self):
        cache.clear()

    def test_urls(self):
        cases = (
            (INDEX_URL, self.guest, HTTPStatus.OK),
            (GROUP_LIST_URL, self.guest, HTTPStatus.OK),
            (PROFILE_URL, self.guest, HTTPStatus.OK),
            (POST_CREATE_URL, self.author, HTTPStatus.OK),
            (POST_CREATE_URL, self.guest, HTTPStatus.FOUND),
            (self.POST_EDIT_URL, self.author, HTTPStatus.OK),
            (self.POST_EDIT_URL, self.guest, HTTPStatus.FOUND),
            (self.POST_EDIT_URL, self.another, HTTPStatus.FOUND),
            (self.POST_DETAIL_URL, self.guest, HTTPStatus.OK),
            (UNEXISTING_URL, self.guest, HTTPStatus.NOT_FOUND),
            (FOLLOW_URL, self.guest, HTTPStatus.FOUND),
            (FOLLOW_URL, self.author, HTTPStatus.OK),

        )
        for url, client, status in cases:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, status)

    def test_templates(self):
        template_urls = {
            INDEX_URL: 'posts/index.html',
            GROUP_LIST_URL: 'posts/group_list.html',
            PROFILE_URL: 'posts/profile.html',
            self.POST_DETAIL_URL: 'posts/post_detail.html',
            self.POST_EDIT_URL: 'posts/create_post.html',
            POST_CREATE_URL: 'posts/create_post.html',
            FOLLOW_URL: 'posts/follow.html',
        }
        for url, template in template_urls.items():
            with self.subTest(url=url):
                self.assertTemplateUsed(
                    self.author.get(url),
                    template
                )

    def test_redirects(self):
        redirect_urls = (
            (POST_CREATE_URL, self.guest, POST_CREATE_REDIRECT),
            (self.POST_EDIT_URL, self.guest, self.POST_EDIT_REDIRECT),
            (self.POST_EDIT_URL, self.another, INDEX_URL),
            (FOLLOW_URL, self.guest, FOLLOW_REDIRECT),
        )
        for url, client, redirect in redirect_urls:
            with self.subTest(url=url, redirect=redirect):
                self.assertRedirects(client.get(url), redirect)
