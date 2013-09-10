###
# Copyright (c) 2005,2008, James Vega
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
###

import time
import queue as Queue
import random
import threading

import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.ircmsgs as ircmsgs
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.schedule as schedule
import supybot.callbacks as callbacks

class SqlAlchemyMarkovDB(object):
    def __init__(self, filename, engine):
        self.dbs = ircutils.IrcDict()
        self.filename = filename
        self.engine = engine

    def close(self):
        self.dbs.clear()

    def _getDb(self, channel, debug=False):
        if channel in self.dbs:
            return self.dbs[channel]

        try:
            import sqlalchemy as sql
            self.sql = sql
        except ImportError:
            raise callbacks.Error('You need to have SQLAlchemy installed to use this ' \
                    'plugin.  Download it at <http://www.sqlalchemy.org/>')

        filename = plugins.makeChannelFilename(self.filename, channel)
        engine = sql.create_engine(self.engine + filename, echo=debug)
        metadata = sql.MetaData()
        firsts = sql.Table('firsts', metadata,
                           sql.Column('id', sql.Integer, primary_key=True),
                           sql.Column('first', sql.Text, unique=True),
                           sql.Column('count', sql.Integer, default=1),
                          )
        lasts = sql.Table('lasts', metadata,
                          sql.Column('id', sql.Integer, primary_key=True),
                          sql.Column('last', sql.Text, unique=True),
                          sql.Column('count', sql.Integer, default=1),
                         )
        pairs = sql.Table('pairs', metadata,
                          sql.Column('id', sql.Integer, primary_key=True),
                          sql.Column('first', sql.Text, default=sql.null),
                          sql.Column('second', sql.Text, default=sql.null),
                          sql.Column('follow', sql.Text, default=sql.null),
                          sql.Column('count', sql.Integer, default=1),
                          sql.UniqueConstraint('first', 'second', 'follow'),
                         )
        metadata.create_all(engine)
        self.dbs[channel] = (engine, firsts, lasts, pairs)
        return self.dbs[channel]

    def _addFirst(self, db, table, first):
        s = self.sql.select([table.c.count], table.c.first==first)
        results = db.execute(s)
        r = results.fetchone()
        if r is None:
            db.execute(table.insert(), first=first).close()
        else:
            db.execute(table.update(), count=r[0]+1).close()

    def _addLast(self, db, table, last):
        s = self.sql.select([table.c.count], table.c.last==last)
        results = db.execute(s)
        r = results.fetchone()
        if r is None:
            db.execute(table.insert(), last=last).close()
        else:
            db.execute(table.update(), count=r[0]+1).close()

    def addPair(self, channel, first, second, follower, isFirst, isLast):
        (db, firsts, lasts, pairs) = self._getDb(channel)
        if isFirst:
            self._addFirst(db, firsts, follower)
            return
        if isLast:
            self._addLast(db, lasts, second)
        s = self.sql.select([pairs.c.count],
                            self.sql.and_(pairs.c.first==first,
                                          pairs.c.second==second,
                                          pairs.c.follow==follower))
        results = db.execute(s)
        r = results.fetchone()
        if r is None:
            db.execute(pairs.insert(), first=first, second=second,
                       follow=follower).close()
        else:
            db.execute(pairs.update(), count=r[0]+1).close()

    def _weightedChoice(self, results):
        L = []
        for t in results:
            c = t[-1]
            while c > 0:
                c -= 1
                L.append(t[:-1])
        return utils.iter.choice(L)

    def getFirstPair(self, channel):
        (db, _, _, pairs) = self._getDb(channel)
        s = self.sql.select([pairs.c.first, pairs.c.second, pairs.c.count],
                            pairs.c.first==None)
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            raise KeyError
        return self._weightedChoice(r)

    def getFollower(self, channel, first, second):
        (db, _, _, pairs) = self._getDb(channel)
        s = self.sql.select([pairs.c.first, pairs.c.second,
                             pairs.c.follow, pairs.c.count],
                            self.sql.and_(pairs.c.first==first,
                                          pairs.c.second==second))
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            raise KeyError
        print('foo')
        print(repr(r))
        L = self._weightedChoice(r)
        isLast = False
        if not L[-1]:
            isLast = True
        return (L[-2], isLast)

    def firsts(self, channel):
        (db, firsts, _, _) = self._getDb(channel)
        s = self.sql.select([firsts.c.count])
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            return 0
        else:
            return sum([x[0] for x in r])

    def lasts(self, channel):
        (db, _, lasts, _) = self._getDb(channel)
        s = self.sql.select([lasts.c.count])
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            return 0
        else:
            return sum([x[0] for x in r])

    def pairs(self, channel):
        (db, _, _, pairs) = self._getDb(channel)
        s = self.sql.select([pairs.c.count])
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            return 0
        else:
            return sum([x[0] for x in r])

    def follows(self, channel):
        (db, _, _, pairs) = self._getDb(channel)
        s = self.sql.select([pairs.c.count],
                            self.sql.not_(pairs.c.follow==None))
        results = db.execute(s)
        r = results.fetchall()
        results.close()
        if not r:
            return 0
        else:
            return sum([x[0] for x in r])

class DbmMarkovDB(object):
    def __init__(self, filename):
        self.dbs = ircutils.IrcDict()
        self.filename = filename

    def close(self):
        for db in self.dbs.values():
            db.close()

    def _getDb(self, channel):
        import anydbm
        if channel not in self.dbs:
            filename = plugins.makeChannelFilename(self.filename, channel)
            # To keep the code simpler for addPair, I decided not to make
            # self.dbs[channel]['firsts'] and ['lasts'].  Instead, we'll pad
            # the words list being sent to addPair such that ['\n \n'] will be
            # ['firsts'] and ['\n'] will be ['lasts'].
            self.dbs[channel] = anydbm.open(filename, 'c')
        return self.dbs[channel]

    def _flush(self, db):
        if hasattr(db, 'sync'):
            db.sync()
        if hasattr(db, 'flush'):
            db.flush()

    def _addPair(self, channel, pair, follow):
        db = self._getDb(channel)
        # EW! but necessary since not all anydbm backends support
        # "combined in db"
        if db.has_key(pair):
            db[pair] = ' '.join([db[pair], follow])
        else:
            db[pair] = follow
        self._flush(db)

    def _combine(self, first, second):
        first = first or '\n'
        second = second or '\n'
        return '%s %s' % (first, second)

    def addPair(self, channel, first, second, follower, isFirst, isLast):
        combined = self._combine(first, second)
        self._addPair(channel, combined, follower or '\n')
        if isLast:
            self._addPair(channel, '\n', second)

    def getFirstPair(self, channel):
        db = self._getDb(channel)
        firsts = db['\n \n'].split()
        if firsts:
            return (None, utils.iter.choice(firsts))
        else:
            raise KeyError('No firsts for %s.' % channel)

    def getFollower(self, channel, first, second):
        db = self._getDb(channel)
        followers = db[self._combine(first, second)]
        follower = utils.iter.choice(followers.split(' '))
        last = False
        if follower == '\n':
            follower = None
            last = True
        return (follower, last)

    def firsts(self, channel):
        db = self._getDb(channel)
        if db.has_key('\n \n'):
            return len(set(db['\n \n'].split()))
        else:
            return 0

    def lasts(self, channel):
        db = self._getDb(channel)
        if db.has_key('\n'):
            return len(set(db['\n'].split()))
        else:
            return 0

    def pairs(self, channel):
        db = self._getDb(channel)
        pairs = [k for k in db.keys() if '\n' not in k]
        return len(pairs)

    def follows(self, channel):
        db = self._getDb(channel)
        # anydbm sucks in that we're not guaranteed to have .iteritems()
        # *cough*gdbm*cough*, so this has to be done the stupid way
        follows = [len([f for f in db[k].split() if f != '\n'])
                   for k in db.keys() if '\n' not in k]
        return sum(follows)

MarkovDB = plugins.DB('Markov', {'anydbm': DbmMarkovDB,
                                 'sqlalchemy': SqlAlchemyMarkovDB})

class MarkovWorkQueue(threading.Thread):
    def __init__(self, *args, **kwargs):
        name = 'Thread #%s (MarkovWorkQueue)' % world.threadsSpawned
        world.threadsSpawned += 1
        threading.Thread.__init__(self, name=name)
        self.db = MarkovDB(*args, **kwargs)
        self.q = Queue.Queue()
        self.killed = False
        self.setDaemon(True)
        self.start()

    def die(self):
        self.killed = True
        self.q.put(None)

    def enqueue(self, f):
        self.q.put(f)

    def run(self):
        while not self.killed:
            f = self.q.get()
            if f is not None:
                f(self.db)
        self.db.close()

class Markov(callbacks.Plugin):
    def __init__(self, irc):
        self.q = MarkovWorkQueue()
        self.__parent = super(Markov, self)
        self.__parent.__init__(irc)
        self.lastSpoke = time.time()

    def die(self):
        self.q.die()
        self.__parent.die()

    def tokenize(self, m):
        if ircmsgs.isAction(m):
            return ircmsgs.unAction(m).split()
        elif ircmsgs.isCtcp(m):
            return []
        else:
            return m.args[1].split()

    def doPrivmsg(self, irc, msg):
        if irc.isChannel(msg.args[0]):
            speakChan = msg.args[0]
            dbChan = plugins.getChannel(speakChan)
            canSpeak = False
            now = time.time()
            throttle = self.registryValue('randomSpeaking.throttleTime',
                                          speakChan)
            prob = self.registryValue('randomSpeaking.probability', speakChan)
            delay = self.registryValue('randomSpeaking.maxDelay', speakChan)
            if now > self.lastSpoke + throttle:
                canSpeak = True
            if canSpeak and random.random() < prob:
                f = self._markov(speakChan, irc, prefixNick=False,
                                 to=speakChan, Random=True)
                schedule.addEvent(lambda: self.q.enqueue(f), now + delay)
                self.lastSpoke = now + delay
            words = self.tokenize(msg)
            # This shouldn't happen often (CTCP messages being the possible
            # exception)
            if not words:
                return
            if self.registryValue('ignoreBotCommands', speakChan) and \
                    callbacks.addressed(irc.nick, msg):
                return
            words.insert(0, None)
            words.insert(0, None)
            words.append(None)
            def doPrivmsg(db):
                for (first, second, follower) in utils.seq.window(words, 3):
                    db.addPair(dbChan, first, second, follower,
                               isFirst=(first is None and second is None),
                               isLast=(follower is None))
            self.q.enqueue(doPrivmsg)

    def _markov(self, channel, irc, word1=None, word2=None, **kwargs):
        def f(db):
            minLength = self.registryValue('minChainLength', channel)
            maxTries = self.registryValue('maxAttempts', channel)
            Random = kwargs.pop('Random', None)
            while maxTries > 0:
                maxTries -= 1
                if word1 and word2:
                    words = [word1, word2]
                    resp = [word1]
                    follower = word2
                elif word1 or word2:
                    words = [None, word1 or word2]
                    resp = []
                    follower = words[-1]
                else:
                    try:
                        # words is of the form [None, word]
                        words = list(db.getFirstPair(channel))
                        resp = []
                        follower = words[-1]
                    except KeyError:
                        irc.error(
                            format('I don\'t have any first pairs for %s.',
                                   channel))
                        return # We can't use raise here because the exception
                               # isn't caught and therefore isn't sent to the
                               # server
                last = False
                while not last:
                    resp.append(follower)
                    try:
                        (follower, last) = db.getFollower(channel, words[-2],
                                                          words[-1])
                    except KeyError:
                        irc.error('I found a broken link in the Markov chain. '
                                  ' Maybe I received two bad links to start '
                                  'the chain.')
                        return # ditto here re: Raise
                    words.append(follower)
                if len(resp) >= minLength:
                    irc.reply(' '.join(resp), **kwargs)
                    return
                else:
                    continue
            if not Random:
                irc.error(
                    format('I was unable to generate a Markov chain at least '
                           '%n long.', (minLength, 'word')))
            else:
                self.log.debug('Not randomSpeaking.  Unable to generate a '
                               'Markov chain at least %n long.',
                               (minLength, 'word'))
        return f

    def markov(self, irc, msg, args, channel, word1, word2):
        """[<channel>] [word1 [word2]]

        Returns a randomly-generated Markov Chain generated sentence from the
        data kept on <channel> (which is only necessary if not sent in the
        channel itself).  If word1 and word2 are specified, they will be used
        to start the Markov chain.
        """
        f = self._markov(channel, irc, word1, word2,
                         prefixNick=False, Random=False)
        self.q.enqueue(f)
    markov = wrap(markov, ['channeldb', optional('something'),
                           additional('something')])

    def firsts(self, irc, msg, args, channel):
        """[<channel>]

        Returns the number of Markov's first links in the database for
        <channel>.
        """
        def firsts(db):
            irc.reply(
                format('There are %s firsts in my Markov database for %s.',
                       db.firsts(channel), channel))
        self.q.enqueue(firsts)
    firsts = wrap(firsts, ['channeldb'])

    def lasts(self, irc, msg, args, channel):
        """[<channel>]

        Returns the number of Markov's last links in the database for
        <channel>.
        """
        def lasts(db):
            irc.reply(
                format('There are %i lasts in my Markov database for %s.',
                       db.lasts(channel), channel))
        self.q.enqueue(lasts)
    lasts = wrap(lasts, ['channeldb'])

    def pairs(self, irc, msg, args, channel):
        """[<channel>]

        Returns the number of Markov's chain links in the database for
        <channel>.
        """
        def pairs(db):
            irc.reply(
                format('There are %i pairs in my Markov database for %s.',
                       db.pairs(channel), channel))
        self.q.enqueue(pairs)
    pairs = wrap(pairs, ['channeldb'])

    def follows(self, irc, msg, args, channel):
        """[<channel>]

        Returns the number of Markov's third links in the database for
        <channel>.
        """
        def follows(db):
            irc.reply(
                format('There are %i follows in my Markov database for %s.',
                       db.follows(channel), channel))
        self.q.enqueue(follows)
    follows = wrap(follows, ['channeldb'])

    def stats(self, irc, msg, args, channel):
        """[<channel>]

        Returns all stats (firsts, lasts, pairs, follows) for <channel>'s
        Markov database.
        """
        def stats(db):
            irc.reply(
                format('Firsts: %i; Lasts: %i; Pairs: %i; Follows: %i',
                       db.firsts(channel), db.lasts(channel),
                       db.pairs(channel), db.follows(channel)))
        self.q.enqueue(stats)
    stats = wrap(stats, ['channeldb'])


Class = Markov


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
