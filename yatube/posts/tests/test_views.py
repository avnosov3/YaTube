import shutil
import tempfile

from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User, Follow
from yatube.settings import POSTS_PER_PAGE

AUTHOR = 'user'
ANOTHER = 'another'
TITLE = 'test title'
SLUG = 'test-slug'
SLUG_ANOTHER = 'test-slug-another'
DESCRIPTION = 'test description'
TEXT = 'test text'
INDEX_URL = reverse('posts:index')
GROUP_LIST_URL = reverse('posts:group_list', args=[SLUG])
GROUP_ANOTHER_URL = reverse('posts:group_list', args=[SLUG_ANOTHER])
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])
POST_CREATE_URL = reverse('posts:post_create')
FOLLOW_URL = reverse('posts:follow_index')
PROFILE_FOLLLOW = reverse('posts:profile_follow', args=[AUTHOR])
PROFILE_UNFOLLOW = reverse('posts:profile_unfollow', args=[AUTHOR])
IMG = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.another_user = User.objects.create_user(username=ANOTHER)
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        cls.group_another = Group.objects.create(
            title=TITLE + ANOTHER,
            slug=SLUG_ANOTHER,
            description=DESCRIPTION + ANOTHER,
        )
        cls.uploded = SimpleUploadedFile(
            name='img.gif',
            content=IMG,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEXT,
            group=cls.group,
            image=cls.uploded,
        )
        cls.follow = Follow.objects.create(
            user=cls.another_user,
            author=cls.user
        )
        cls.POST_DETAIL_URL = reverse('posts:post_detail', args=[cls.post.pk])
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.pk])
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.another.force_login(cls.another_user)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()

    def test_context(self):
        cases = (
            (INDEX_URL, 'page_obj', self.author),
            (GROUP_LIST_URL, 'page_obj', self.author),
            (PROFILE_URL, 'page_obj', self.author),
            (self.POST_DETAIL_URL, 'post', self.author),
            (FOLLOW_URL, 'page_obj', self.another)
        )
        for url, context, client in cases:
            with self.subTest(url=url):
                post = client.get(url).context[context]
                if context == 'page_obj':
                    self.assertEqual(len(post), 1)
                    post = post[0]
                self.assertEqual(post.text, self.post.text)
                self.assertEqual(post.group, self.post.group)
                self.assertEqual(post.author, self.post.author)
                self.assertEqual(post.image, self.post.image)
                self.assertEqual(post.pk, self.post.pk)

    def test_paginator(self):
        PAGE = '?page=2'
        Post.objects.bulk_create(
            [
                Post(
                    author=self.user,
                    text='Test text' + str(i),
                    group=self.group,
                )
                for i in range(1, POSTS_PER_PAGE + 1)
            ]
        )
        cases = (
            (INDEX_URL, POSTS_PER_PAGE, self.author),
            (GROUP_LIST_URL, POSTS_PER_PAGE, self.author),
            (PROFILE_URL, POSTS_PER_PAGE, self.author),
            (FOLLOW_URL, POSTS_PER_PAGE, self.another),
            (INDEX_URL + PAGE, 1, self.author),
            (GROUP_LIST_URL + PAGE, 1, self.author),
            (PROFILE_URL + PAGE, 1, self.author),
            (FOLLOW_URL + PAGE, 1, self.another),
        )
        for url, expected, client in cases:
            self.assertEqual(
                len(
                    client.get(url).context['page_obj']
                ),
                expected
            )

    def test_author_in_profile(self):
        self.assertEqual(
            self.author.get(PROFILE_URL).context['author'],
            self.user,
        )

    def test_group_in_group_list(self):
        group = self.author.get(GROUP_LIST_URL).context['group']
        self.assertEqual(group.title, self.group.title),
        self.assertEqual(group.slug, self.group.slug),
        self.assertEqual(group.description, self.group.description)
        self.assertEqual(group.pk, self.group.pk)

    def test_post_in_correct_group_and_follow_index(self):
        urls = (GROUP_ANOTHER_URL, FOLLOW_URL)
        for url in urls:
            with self.subTest(url=url):
                self.assertNotIn(
                    self.post,
                    self.author.get(url).context['page_obj'],
                )

    def test_cache(self):
        content_old = self.author.get(INDEX_URL).content
        Post.objects.all().delete()
        content_new = self.author.get(INDEX_URL).content
        self.assertEqual(content_new, content_old)
        cache.clear()
        self.assertNotEqual(content_old, self.author.get(INDEX_URL).content)

    def test_profile_follow(self):
        Follow.objects.all().delete()
        self.another.get(PROFILE_FOLLLOW)
        self.assertTrue(
            Follow.objects.filter(
                user=self.another_user,
                author=self.user
            ).exists()
        )

    def test_profile_unfollow(self):
        Follow.objects.all().delete()
        Follow.objects.create(
            user=self.another_user,
            author=self.user,
        )
        self.another.get(PROFILE_UNFOLLOW)
        self.assertFalse(
            Follow.objects.filter(
                user=self.another_user,
                author=self.user
            ).exists()
        )
