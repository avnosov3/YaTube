import shutil
import tempfile

from django import forms
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User, Comment

AUTHOR = 'user'
ANOTHER = 'another'
TITLE = 'test title'
SLUG = 'test-slug'
DESCRIPTION = 'test description'
TEXT = 'test text'
PROFILE_URL = reverse('posts:profile', args=[AUTHOR])
POST_CREATE_URL = reverse('posts:post_create')
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
IMG_ONE = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)
IMG_TWO = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
IMG_THREE = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00'
    b'\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
    b'\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uploded_one = SimpleUploadedFile(
            name='img_one.gif',
            content=IMG_ONE,
            content_type='posts/img_one.gif'
        )
        cls.uploded_two = SimpleUploadedFile(
            name='img_two.gif',
            content=IMG_TWO,
            content_type='posts/img_two.gif'
        )
        cls.uploded_three = SimpleUploadedFile(
            name='img_three.gif',
            content=IMG_THREE,
            content_type='posts/img_three.gif'
        )
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEXT,
            image=cls.uploded_two,
            group=cls.group
        )
        cls.another_group = Group.objects.create(
            title=f'{TITLE}{ANOTHER}',
            slug=f'{SLUG}-{ANOTHER}',
            description=f'{DESCRIPTION}{ANOTHER}',
        )
        cls.post_count = Post.objects.count()
        cls.comment_count = Comment.objects.count()
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail',
            args=[cls.post.pk]
        )
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=[cls.post.pk])
        cls.COMMENT_URL = reverse('posts:add_comment', args=[cls.post.pk])
        cls.guest = Client()
        cls.author = Client()
        cls.author.force_login(cls.user)
        cls.another = Client()
        cls.user_login = User.objects.create_user(username=ANOTHER)
        cls.another.force_login(cls.user_login)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_create_post(self):
        posts_before = set(Post.objects.all())
        form_data = {
            'text': 'test text 2',
            'group': self.group.pk,
            'image': self.uploded_one
        }
        response = self.author.post(
            POST_CREATE_URL,
            data=form_data,
            reverse=True
        )
        posts_after = set(Post.objects.all())
        post_diff = posts_after.difference(posts_before)
        self.assertEqual(len(post_diff), 1)
        new_post = post_diff.pop()
        self.assertEqual(Post.objects.count(), self.post_count + 1)
        self.assertEqual(new_post.text, form_data['text'])
        self.assertEqual(new_post.group.pk, form_data['group'])
        self.assertEqual(new_post.image, form_data['image'].content_type)
        self.assertEqual(new_post.author, self.user)
        self.assertRedirects(response, PROFILE_URL)

    def test_edit_post(self):
        form_data = {
            'text': self.post.text + ANOTHER,
            'group': self.another_group.pk,
            'image': self.uploded_three,
        }
        response = self.author.post(
            self.POST_EDIT_URL,
            data=form_data,
            follow=True
        )
        edit_post = response.context['post']
        self.assertEqual(Post.objects.count(), self.post_count)
        self.assertEqual(edit_post.pk, self.post.pk)
        self.assertEqual(edit_post.text, form_data['text'])
        self.assertEqual(edit_post.image, form_data['image'].content_type)
        self.assertEqual(edit_post.group.pk, form_data['group'])
        self.assertEqual(edit_post.author, self.post.author)
        self.assertRedirects(response, self.POST_DETAIL_URL)

    def test_form_create_edit(self):
        URLS = (
            POST_CREATE_URL,
            self.POST_EDIT_URL,
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for url in URLS:
            form_field = self.author.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    self.assertIsInstance(
                        form_field.context['form'].fields[value],
                        expected
                    )

    def test_comment(self):
        comments_before = set(Comment.objects.all())
        form_data = {'text': 'new_comment'}
        self.author.post(
            self.COMMENT_URL,
            data=form_data,
            reverse=True,
        )
        comments_after = set(Comment.objects.all())
        comment_diff = comments_after.difference(comments_before)
        self.assertEqual(len(comment_diff), 1)
        new_comment = comment_diff.pop()
        self.assertEqual(Comment.objects.count(), self.comment_count + 1)
        self.assertEqual(new_comment.text, form_data['text'])
        self.assertEqual(new_comment.author, self.user)

    def test_guest_comment_and_post(self):
        cases = (
            (Comment, {'text': 'new_comment'}, self.COMMENT_URL),
            (Post, {'text': 'new_text'}, POST_CREATE_URL),
        )
        for model, form_data, url in cases:
            with self.subTest(model=model):
                model.objects.all().delete()
                self.guest.post(
                    url,
                    data=form_data,
                    reverse=True,
                )
                self.assertEqual(
                    model.objects.count(),
                    0
                )

    def test_not_author_edit_post(self):
        clients = (self.guest, self.another)
        post_before = self.post
        for client in clients:
            with self.subTest(client=client):
                client.post(
                    self.POST_EDIT_URL,
                    data={'text': 'changed_text'},
                    follow=True
                )
                post_after = Post.objects.get(pk=post_before.pk)
                self.assertEqual(post_after.text, post_before.text)
                self.assertEqual(post_after.author, post_before.author)
                self.assertEqual(post_after.group.pk, post_before.group.pk)
                self.assertEqual(post_after.image, post_before.image)
