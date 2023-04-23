from django.test import TestCase
from django.urls import reverse

from ..urls import app_name

USERNAME = 'user'
SLUG = 'test-slug'
POST_ID = 1
CASES = (
    ('/', 'index', None),
    (f'/group/{SLUG}/', 'group_list', [SLUG]),
    (f'/profile/{USERNAME}/', 'profile', [USERNAME]),
    ('/create/', 'post_create', None),
    (f'/posts/{POST_ID}/edit/', 'post_edit', [POST_ID]),
    (f'/posts/{POST_ID}/', 'post_detail', [POST_ID]),
    (f'/posts/{POST_ID}/comment/', 'add_comment', [POST_ID]),
    ('/follow/', 'follow_index', None),
    (f'/profile/{USERNAME}/follow/', 'profile_follow', [USERNAME]),
    (f'/profile/{USERNAME}/unfollow/', 'profile_unfollow', [USERNAME]),
)


class PostRoutesTest(TestCase):
    def test_routes(self):
        for obvious, route, args in CASES:
            with self.subTest(obvious=obvious):
                self.assertEqual(
                    obvious,
                    reverse(f'{app_name}:{route}', args=args)
                )
