from django.test import TestCase

from ..models import Group, Post, User

AUTHOR = 'user'
TITLE = 'test title'
SLUG = 'test-slug'
DESCRIPTION = 'test description'
TEXT = 'test text'


class PostModelsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=AUTHOR)
        cls.group = Group.objects.create(
            title=TITLE,
            slug=SLUG,
            description=DESCRIPTION,
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEXT,
            group=cls.group
        )

    def test_models_have_correct_object_names(self):
        cases = (
            (Post.OUT.format(
                text=self.post.text,
                pub_date=self.post.pub_date,
                author=self.post.author.username,
                group=self.post.group,
            ), str(self.post)),
            (self.group.title, str(self.group)),
        )
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(value, expected)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа'
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).verbose_name, expected)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    Post._meta.get_field(value).help_text, expected)
