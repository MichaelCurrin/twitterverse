from unittest import TestCase

import lib.text_handling


class TestTextHandling(TestCase):

    def test_flattenText(self):
        flattenText = lib.text_handling.flattenText

        self.assertEqual(flattenText("abc"), "abc")
        self.assertEqual(flattenText("a\r\nbc"), "a bc")
        self.assertEqual(flattenText("ab\nc"), "ab c")
        self.assertEqual(flattenText("a\r\nbc", ";"), "a;bc")
