import random
from errbot import BotPlugin, botcmd


class CoffeeTime(BotPlugin):
    """Tells the people in the chatroom who has to bring the coffee."""

    @botcmd
    def coffeetime(self, msg, args):
        if msg.type == 'chat':
            ret = "Get your own coffee!"
        else:
            other_occupants = self.helper_other_occupants_in_room(msg)
            # TODO: len(other_ocupants) is in real life always
            # 1 or higher. During tests it is 0.
            # I could not get it properly patched for testing yet.
            if len(other_occupants) <= 1:
                ret = ("You are the only online person in the group :( \n"
                       "What about getting your own coffee?")
            else:
                lucky_one = self.pick_lucky_one(other_occupants)
                ret = "@{} should bring the coffee!".format(
                    lucky_one)

        if self.mode == 'hipchat':
            ret = "(coffee) " + ret

        return ret

    def helper_other_occupants_in_room(self, msg):
        """returns all mention names of other occupants in the room"""
        bot_username = self.bot_config.BOT_IDENTITY['username']
        occupants = self.query_room(msg.frm.stripped).occupants
        other_occupants = [o.mention_name for o in occupants
                           if o.stripped != bot_username]
        return other_occupants

    @staticmethod
    def pick_lucky_one(occupants_list):
        """Returns a random occupant name from the list"""
        return random.choice(occupants_list)
