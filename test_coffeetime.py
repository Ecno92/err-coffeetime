"""
CoffeeTime tests
================

This file contains several tests for various cases that are supported
by the CoffeeTime plugin.

The idea is that all cases that may occur are covered by tests.
Unfortunately I was not able to do this properly since the ErrBot
test framework is still very limited.

At the moment of writing there seems to be a major refactor ongoing.
So it will be a good idea to improve the tests of CoffeeTime
once this is finished.
"""

from unittest.mock import patch, PropertyMock
from errbot.backends.test import (testbot,
                                  pop_message,
                                  push_message)
from coffeetime import CoffeeTime


class TestCoffeeTimeBot(object):
    extra_plugin_dir = "."

    def test_coffeetime_dm(self, testbot):
        push_message('!coffeetime')
        assert "Get your own coffee" in pop_message()

    @patch('errbot.backends.base.Message.type',
           new_callable=PropertyMock,
           return_value='groupchat')
    def test_coffeetime_muc(self, patch_msg_type, testbot):
        """TODO:
        Also test the other message if more than 1 user is present
        Unfortunately I was not able to patch this correctly yet."""

        push_message('!coffeetime')
        assert ("You are the only online person in the group :( \n"
                "What about getting your own coffee?"
                ) in pop_message()

    @patch('errbot.BotPlugin.mode',
           new_callable=PropertyMock,
           return_value='hipchat')
    def test_hipchat_icon(self, patch_hipchat_mode, testbot):
        push_message('!coffeetime')
        assert pop_message().startswith('(coffee) ')

    @patch('errbot.BotPlugin.mode',
           new_callable=PropertyMock,
           return_value='slack')
    def test_no_hipchat_icon(self, patch_hipchat_mode, testbot):
        push_message('!coffeetime')
        assert not pop_message().startswith('(coffee) ')


class TestCoffeeTimeBotStaticMethods(object):

    @patch('random.choice', return_value='b')
    def test_pick_lucky_one(self, patch):
        """Rather silly test to since it only contains a random choice
        and it is completely mocked right now."""
        test_list = ['a', 'b', 'c']
        assert CoffeeTime.pick_lucky_one(test_list) == 'b'
