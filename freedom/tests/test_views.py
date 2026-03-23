from django.test import TestCase
from django.urls import reverse

class PostFlowTests(TestCase):
    def test_post_creates_entry_and_renders_color(self):
        resp = self.client.post(reverse('index'), {'text': "I'm angry and upset", 'emotion': ''}, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, '<strong>angry</strong>')
        # check that bg_color is present in the response (used by template for fading)
        self.assertContains(resp, 'data-bg-color')
