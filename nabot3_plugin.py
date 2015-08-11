# -*- coding: utf-8 -*-
from irc3.plugins.command import command
import irc3, string, praw, time, random, requests, asyncio, randimg, redditimage


@irc3.plugin
class Plugin(object):

    def __init__(self, bot):
        self.bot = bot
        self._reloader = asyncio.Task(self._auto_reloader())
        asyncio.async(self.identify())
        if hasattr(bot, "reloaded_target"):
            print('Finished.')

    # @irc3.event(irc3.rfc.CONNECTED)
    # def pre_ident(self):
    #     self.bot.privmsg('nickserv', 'identify Ion_ hunter2')

    @irc3.event(irc3.rfc.JOIN)
    def say_hi(self, mask, channel):
        """Say hi when someone join a channel"""
        if mask.nick != self.bot.nick:
            self.bot.privmsg(channel, 'Hiya!' % mask.nick)
        else:
            self.bot.privmsg(channel, 'Hiya!')
            # self.bot.privmsg('nickserv', 'identify Ion_ {}'.format(password))


    @classmethod
    def reload(cls, old):
        old._reloader.cancel()
        return cls(old.bot)

    @asyncio.coroutine
    def identify(self):
        yield from asyncio.sleep(0.5)
        with open("password.txt") as f:
            password = f.read().strip()
            print(password)
        self.bot.privmsg('nickserv', 'identify Ion_ {}'.format(password))
        

    @command(permission='view')
    def echo(self, mask, target, args):
        """Echo

            %%echo <message>...
        """
        yield ' '.join(args['<message>'])

    @command(permission='view')
    def ballkban(self, mask, target, args):
        """ballkban

            %%ballkban <message>...
        """
        return "Ballkenende's ban from #tagpro ends in ∞ hours."

    @command(permission='view')
    def scarycat(self, mask, target, args):
        """scarycat

            %%scarycat [<message>]...
        """
        return 'http://i.imgur.com/yJHPheo.gif'

    @command(permission='view')
    def usuk(self, mask, target, args):
        """usuk

            %%usuk [<message>]...
        """
        return 'no u'

    # lol yay stealing
    @command(permission='view')
    @asyncio.coroutine
    def random(self, mask, target, args):
        """random
            %%random
        """
        randomurl = yield from randimg.randomness()
        print(randomurl)
        return 'Random imgur link, possibly NSFW: {}'.format(randomurl)
        # self.bot.privmsg(target, '{}: potentially NSFW: {}'.format(mask.nick, randomurl))

    # stealing is gr8
    @command(permission='view')
    def randnsfw(self, mask, target, args):
        """randnsfw
           %%randnsfw
        """
        link = redditimage.randnsfw()
        self.bot.privmsg(target, "Random NSFW Subreddit: {}".format(link))

    #this shit is broke as fuck yo idk how to do pythun
    #@command(permission='view')
    #def meirl(self, mask, target, args):
        #"""meirl
           #%%meirl <message>
        #"""
        #image =
        #self.bot.privmsg(target, "me irl {}".format(image))

    # i fuckin love stealing
    @command(permission='view')
    def reddit(self, mask, target, args):
        """reddit
           %%reddit <message>...
        """
        url, nsfw = redditimage.redditimage(''.join(args['<message>']))
        if nsfw == True:
            self.bot.privmsg(target, "Link is marked nsfw: {}".format(url))
        else:
            self.bot.privmsg(target, "Link to reddit: {}".format(url))


    @command(permission='view')
    def randint(self, mask, target, args):
        """randint

            %%randint
        """
        return str(random.randrange(0, 100))

    @command(permission='admin')
    @asyncio.coroutine
    def talk(self, mask, target, args):
        """talk
            %%talk <channel> <message>...
        """
        print (args)
        self.bot.privmsg(args['<channel>'], ' '.join(args['<message>']))

    @command(permission='admin')
    @asyncio.coroutine
    def join_chan(self, mask, target, args):
        """join_chan
            %%join_chan <channel>
        """
        print (args)
        self.bot.join(args['<channel>'])

    @command(permission='admin')
    def part_chan(self, mask, target, args):
        """part_chan
            %%part_chan <channel>
        """
        self.bot.part(args['<channel>'], reason=None)

    @command(permission='admin')
    def quit(self, mask, target, args):
        """quit
            %%quit
        """
        @asyncio.coroutine
        def really_quit(bot):
            bot.quit(reason="I don't like you")
            yield from asyncio.sleep(1)
            bot.loop.stop()
        asyncio.Task(really_quit(self.bot))

    @command(permission='admin')
    def reloads(self, mask, target, args):
        """reloads
            %%reloads
        """
        return self.live_reload(target)

    def live_reload(self, target):
        with open('nabot3_plugin.py') as f:
            code = f.read()
        try:
            exec(code)
        except SyntaxError:
            return "Couldn't reload! Encountered a syntax error."
        self.bot.reloaded_target = target
        self.bot.reload('nabot3_plugin')

    @asyncio.coroutine
    def _auto_reloader(self):
        file_hash = self._get_file_hash()
        while True:
            new_hash = self._get_file_hash()
            if new_hash != file_hash:
                self.live_reload("Ion_")
            yield from asyncio.sleep(1)

    def _get_file_hash(self):
        with open("nabot3_plugin.py") as f:
            file_hash = hash(f.read())
        return file_hash