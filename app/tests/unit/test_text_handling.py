# -*- coding: utf-8 -*-
from unittest import TestCase

import lib.text_handling


class TestTextHandling(TestCase):

    def test_flattenText(self):
        flattenText = lib.text_handling.flattenText

        self.assertEqual("abc", flattenText("abc"))
        self.assertEqual("a bc", flattenText("a\r\nbc"))
        self.assertEqual("ab c", flattenText("ab\nc"))
        self.assertEqual("a;bc", flattenText("a\r\nbc", ";"))

    def test_stripSymbols(self):
        stripSymbols = lib.text_handling.stripSymbols

        cases = (
            (
                "I am a Tweet but need cleaning Why dont you help me"
                " my friend jamie123",
                "I am a #Tweet, but need cleaning! ^-^ Why don't you help me,"
                " my friend @jamie_123?",
             ),
            (
                "Im a unicode string with unicode symbol near the start",
                u"I’m a #unicode string with unicode symbol near the start!"
            ),
        )
        for expected_output, test_input in cases:
            self.assertEqual(
                expected_output.split(" "),
                stripSymbols(test_input),
            )