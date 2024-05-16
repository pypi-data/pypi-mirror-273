# ----------------------------------------------------------
# Storage Port
# ----------------------------------------------------------
import asyncio
import os
import pickle
import re
import time
import sys
import traceback
from typing import Dict, List
from multiprocessing import Process
import yaml
from typing import Dict

# from surrealdb import Surreal
from surrealist import Surreal as Surrealist


# TODO: reallocate
UID = str
WAVE = float

# ---------------------------------------------------------
# Loggers
# ---------------------------------------------------------

from agptools.logs import logger
from agptools.helpers import parse_uri, build_uri

log = logger(__name__)

from .definitions import MONOTONIC_KEY, ALT_KEY, filter_private
from .helpers import expandpath
from .model import BaseModel


# REGEXP_FQUI = re.compile(r"((?P<ns>[^/]*?)/)?(?P<table>[^:]+):(?P<uid>.*)$")
def split_fqui(fqid):
    try:
        table, uid = fqid.split(":")
        return table, uid
    except ValueError:
        return fqid, None


class iCRUD:
    MODE_SNAPSHOT = "snap"
    MODE_TUBE = "tube"

    async def create(self, item):
        "TBD"

    async def read(self, fqid):
        "alias for get"
        return await self.get(fqid)

    async def update(self, fqid, item):
        "TBD"

    async def delete(self, fqid):
        "TBD"

    async def put(self, fqid, data: Dict) -> bool:
        "Try to create / update an item of `type_` class from raw data"

    async def list(self):
        "TBD"

    async def count(self, table):
        "TBD"

    async def exists(self, fqid):
        "TBD"

    async def get(self, fqid, kind=None) -> BaseModel | None:
        "TBD"
        pass

    async def set(self, fqid, data: Dict, merge=False):
        "TBD"
        return False

    async def put(self, fqid, data: Dict) -> bool:
        return await self.set(fqid, data)

    async def get_all(self):
        "TBD"

    async def set_all(self, items):
        "TBD"

    async def delete_all(self):
        "TBD"

    async def exists_all(self, uids):
        "TBD"

    async def get_many(self, uids):
        "TBD"

    async def set_many(self, uids, items):
        "TBD"

    async def delete_many(self, uids):
        "TBD"

    async def exists_many(self, uids):
        "TBD"

    async def save(self, nice=False, wait=False):
        "TBD"

    async def info(self):
        "TBD"
        return {}


class Storage(iCRUD):
    def __init__(self, url, mode=iCRUD.MODE_SNAPSHOT):
        super().__init__()
        self.url = url
        self.mode = mode
        self.background = []

    def running(self):
        self.background = [p for p in self.background if p.is_alive()]
        return len(self.background)

    async def info(self):
        raise NotImplementedError()


class StoragePort(Storage):
    PATH_TEMPLATE = "{self.url}/{table}"

    def __init__(self, url="./db", mode=iCRUD.MODE_SNAPSHOT):
        super().__init__(url=url, mode=mode)
        url = expandpath(url)
        if not os.path.exists(url):
            os.makedirs(url, exist_ok=True)
        self.url = url
        self.cache = {}
        self._dirty = {}

    def _file(self, table):
        return self.PATH_TEMPLATE.format_map(locals())

    def load(self, table, force=False):
        universe = self.cache.get(table)
        if force or universe is None:
            path = self._file(table)
            if os.path.exists(path):
                try:
                    universe = self._real_load(path)
                except Exception as why:
                    log.warning(why)
            if universe is None:
                universe = {}
            self.cache[table] = universe
        return universe

    _load = load

    def _save(self, table, universe=None, pause=0, force=False):
        if self._dirty.pop(table, force):
            if universe is None:
                universe = self.load(table)
            path = self._file(table)
            self._real_save(path, universe, pause=pause)

    def _real_load(self, path):
        raise NotImplementedError()

    def _real_save(self, path, universe, pause=0):
        raise NotImplementedError()

    async def get(self, fqid, query=None, **params):
        table, uid = split_fqui(fqid)
        universe = self.load(table)
        if query:
            raise NotImplementedError

        data = universe.get(fqid, {})
        return data

    async def set(self, fqid, data, merge=False):
        table, uid = split_fqui(fqid)
        universe = self.load(table)
        if merge:
            data0 = await self.get(fqid)
            # data = {** data0, ** data} # TODO: is faster?
            data0.update(data)
            data = data0

        universe[fqid] = data
        self._dirty[table] = True
        return True

    async def save(self, table=None, nice=False, wait=False):
        table = table or list(self.cache)
        if not isinstance(table, list):
            table = [table]
        for i, tab in enumerate(table):
            pause = i if nice else 0
            self._save(tab, pause=pause + 0.1)

        log.info("waiting data to be saved")
        while wait and self.running() > 0:
            await asyncio.sleep(0.1)
        return self.running() == 0

    async def info(self, ns=""):
        "Returns storage info: *tables*, etc"
        if ns:
            table = f"{ns}/.*"
        else:
            table = f".*"

        pattern = self._file(table=table)
        top = os.path.dirname(pattern)
        for root, _, files in os.walk(top):
            for file in files:
                path = os.path.join(root, file)
                m = re.match(pattern, path)
                if m:
                    relpath = os.path.relpath(path, self.url)
                    name = os.path.splitext(relpath)[0]
                    yield name


class PickleStorage(StoragePort):
    PATH_TEMPLATE = "{self.url}/{table}.pickle"

    def _real_load(self, path):
        try:
            universe = pickle.load(open(path, "rb"))
        except Exception as why:
            log.error("%s: Error loading: %s: %s", self, path, why)
            universe = {}
        return universe

    def _real_save(self, path, universe, pause=0):
        try:
            log.debug("[%s] saving: %s", self.__class__.__name__, path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            pickle.dump(universe, open(path, "wb"))
        except Exception as why:
            log.error("%s: Error savig: %s: %s", self, path, why)


class YamlStorage(StoragePort):
    PATH_TEMPLATE = "{self.url}/{table}.yaml"

    def __init__(self, url="./db", mode=iCRUD.MODE_SNAPSHOT):
        super().__init__(url=url, mode=mode)
        self.lock = 0

    def _real_load(self, path):
        try:
            universe = yaml.load(
                open(path, encoding="utf-8"), Loader=yaml.Loader
            )
        except Exception as why:
            log.error("%s: Error loading: %s: %s", self, path, why)
            universe = {}
        return universe

    def _real_save(self, path, universe, pause=0, nice=False):
        def main(path, universe, pause):
            # name = os.path.basename(path)
            # log.debug(">> ... saving [%s] in %s secs ...", name, pause)
            time.sleep(pause)
            try:
                log.debug("[%s] saving: %s", self.__class__.__name__, path)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                yaml.dump(
                    universe,
                    open(path, "w", encoding="utf-8"),
                    Dumper=yaml.Dumper,
                )
            except Exception as why:
                log.error("%s: Error savig: %s: %s", self, path, why)
            # log.debug("<< ... saving [%s] in %s secs DONE", name, pause)

        if nice:
            # uses a background thread to save in YAML format
            # because is too slow to block the main thread
            # th = threading.Thread(target=main)
            # th.start()
            p = Process(
                target=main, args=(path, universe, pause), daemon=True
            )
            self.background.append(p)
            p.start()
            # log.debug("saving daemon is running:  %s", p.is_alive())
            foo = 1
        else:
            main(path, universe, pause=0)


# class SurrealStorage(StoragePort):
#     def __init__(self, url="./db", user="root", password="root", ns="test", db="test"):
#         # super().__init__(url) # TODO: FIXME: DO NOT CALL BASE CLASS, will corrupt url
#         self.url = url
#         self.cache = {}
#         self.user = user
#         self.password = password
#         self.ns = ns
#         self.db = db
#         self.connection = None

#     async def _connect(self):
#         self.connection = Surreal(self.url)

#         # TODO: use credentials
#         await self.connection.connect()
#         await self.connection.signin({"user": self.user, "pass": self.password})
#         await self.connection.use(self.ns, self.db)

#     async def get(self, fqid, cache=False):
#         if cache:
#             data = self.cache.get(fqid)
#         else:
#             data = None
#         if data is None:
#             if not self.connection:
#                 await self._connect()
#             try:
#                 data = await self.connection.select(fqid)
#             except Exception as why:
#                 log.warning(why)

#             if not cache:
#                 self.cache[fqid] = data

#         return data

#     async def put(self, fqui, data: Dict) -> bool:
#         if not self.connection:
#             await self._connect()
#         try:
#             thing = data.pop("id")
#             result = await self.connection.update(thing, data)
#         except Exception as why:
#             print(f"ERROR: {why}")

#         # t1 = time.time()
#         # print(f"{self.__class__}.set() : elapsed = {t1-t0} seconds")

#     async def set(self, fqid, data, merge=False):
#         t0 = time.time()
#         if merge:
#             data0 = self.get(table)
#             # data = {** data0, ** data} # TODO: is faster?
#             data0.update(data)
#             data = data0

#         if not self.connection:
#             await self._connect()

#         # await self.connection.query(f"USE DB {table.replace('.', '_')};")

#         for kind, items in data.items():
#             for id_, item in items.items():
#                 result = await self.connection.update(
#                     kind,
#                     item,
#                 )
#         t1 = time.time()
#         print(f"{self.__class__}.set() : elapsed = {t1-t0} seconds")


# TODO: move this definitinos and DB_LAYOUT to a common place
TUBE_META = "TubeMeta"
TUBE_WAVE = "TubeWave"
TUBE_SYNC = "TubeSync"
QUERY_UPDATE_TUBE_SYNC = "UPDATE $record_id SET wave__ = $wave__;"
QUERY_SELECT_TUBE_SYNC = (
    f"SELECT * FROM {TUBE_SYNC} WHERE source=$source AND target=$target" ""
)


class iWaves:
    """Swarm Flows / Waves storage.
    Base implementation is for Surreal, but can be
    overriden by subclassing
    """

    DB_INFO = """
    INFO FOR DB;
    """
    DB_LAYOUT = {
        TUBE_META: f"""
        DEFINE TABLE IF NOT EXISTS {TUBE_META} SCHEMALESS;
        DEFINE FIELD id ON TABLE {TUBE_META} TYPE string;
        """,
        # TUBE_WAVE: f"""
        # DEFINE TABLE IF NOT EXISTS {TUBE_WAVE} SCHEMAFULL;
        # DEFINE FIELD id ON TABLE {TUBE_WAVE} TYPE string;
        # DEFINE FIELD wave ON TABLE {TUBE_WAVE} TYPE int;
        # """,
        TUBE_SYNC: f"""
        DEFINE TABLE IF NOT EXISTS {TUBE_SYNC} SCHEMAFULL;
        DEFINE FIELD source ON TABLE {TUBE_SYNC} TYPE string;
        DEFINE FIELD target ON TABLE {TUBE_SYNC} TYPE string;
        DEFINE FIELD {MONOTONIC_KEY} ON TABLE {TUBE_SYNC} TYPE int;
        """,
        f"{TUBE_SYNC}Index": f"""
        DEFINE INDEX IF NOT EXISTS {TUBE_SYNC}Index ON {TUBE_SYNC} COLUMNS source, target UNIQUE;
        """,
    }
    TUBE_SYNC_WAVES = {}

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.connection = None

    async def _connect(self):
        pass

    async def _update_database_layout(self):
        """
        Check / Create the expected database layout
        """
        self.connection or await self._connect()
        info = self.connection.query(self.DB_INFO)
        tables = info.result["tables"]
        for table, schema in self.DB_LAYOUT.items():
            # TODO: check tables and individual indexes
            if True or table not in tables:
                # TODO: delete # schema = "USE NS test DB test;" + schema
                result = self.connection.query(schema)
                if result.status in ("OK",):
                    log.info("[%s] : %s", schema, result.status)
                else:
                    log.error("[%s] : %s", schema, result.status)

    async def last_wave(self, klass) -> WAVE:
        "TBD"
        query = f"""
        SELECT * FROM {TUBE_WAVE} WHERE
        source = $source AND
        target = $target
        """

        tube_name = f"{klass.__module__.replace('.', '_')}_{klass.__name__}"

        self.connection or await self._connect()
        res = self.connection.select(TUBE_WAVE, record_id=tube_name)
        result = res.result
        assert len(result) <= 1
        if result:
            return result[0]
        return {}

    async def last_waves(self, sources: List, uid: UID) -> Dict[str, WAVE]:
        "TBD"
        query = f"""
        SELECT * FROM {TUBE_SYNC} WHERE
        source = $source AND
        target = $target
        """
        self.connection or await self._connect()
        waves = {}
        for source in sources:
            res = self.connection.query(
                query,
                variables={
                    "source": source,
                    "target": uid,
                },
            )

            result = res.result
            if result:
                waves[source] = result[0][MONOTONIC_KEY]
            else:
                waves[source] = 0
        return waves

    async def since(self, fqid, wave, max_results=100):
        query = f"""
        SELECT *
        FROM {fqid}
        WHERE  {MONOTONIC_KEY} > {wave}
        ORDER BY _wave ASC
        LIMIT {max_results}
        """
        self.connection or await self._connect()
        res = self.connection.query(query)
        return res.result


class WaveStorage(iWaves, Storage):
    def __init__(
        self,
        url="./db",
        mode=iCRUD.MODE_SNAPSHOT,
    ):
        super().__init__(url=url, mode=mode)

    async def start(self):
        "any action related to start storage operations"

    async def stop(self):
        "any action related to stop storage operations"

    async def update_sync_wave(self, sources, target, wave):
        """Update the synchronization wave
        of some sources for a particular target
        """


class SurrealistStorage(WaveStorage):

    def __init__(
        self,
        url="./db",
        user="root",
        password="root",
        ns="test",
        db="test",
        mode=iCRUD.MODE_SNAPSHOT,
    ):
        super().__init__(url=url, mode=mode)
        self.cache = {}
        self.user = user
        self.password = password
        self.ns = ns
        self.db = db
        self.surreal = None
        self.connection = None

    def close(self):
        if self.connection:
            self.connection.close()

    def __del__(self):
        self.close()

    async def start(self):
        "any action related to start storage operations"
        await super().start()
        self.connection or await self._connect()

    async def stop(self):
        "any action related to stop storage operations"
        await super().stop()
        self.connection.close()

    async def _connect(self):
        await super()._connect()
        url = parse_uri(self.url)
        url["fscheme"] = "http"
        url["path"] = ""
        url = build_uri(**url)

        self.surreal = Surrealist(
            url,
            namespace=self.ns,
            database=self.db,
            credentials=(self.user, self.password),
            use_http=False,
            timeout=10,
            log_level="ERROR",
        )
        print(self.url)
        print(self.surreal.is_ready())
        print(self.surreal.version())

        self.connection = self.surreal.connect()

        # create initial database layout
        await self._update_database_layout()

        # TODO: use credentials
        # await self.connection.connect()
        # await self.connection.signin({"user": self.user, "pass": self.password})
        # await self.connection.use(self.ns, self.db)

    async def get(self, fqid, cache=True, mode=None) -> Dict:
        mode = mode or self.mode
        if mode in (self.MODE_SNAPSHOT,):
            if cache:
                data = self.cache.get(fqid)
            else:
                data = None
            if data is None:
                self.connection or await self._connect()
                try:
                    res = self.connection.select(fqid)
                    result = res.result
                    if result:
                        data = result[0]
                except Exception as why:
                    log.warning(why)

                if not cache:
                    self.cache[fqid] = data
            return data
        else:
            raise RuntimeError(f"UNKOWN mode: {mode} for get()")

    async def put(self, fqid, data: Dict, mode=None) -> bool:
        self.connection or await self._connect()
        assert self.connection, "surreal connection has failed"
        mode = mode or self.mode
        try:
            if mode in (self.MODE_SNAPSHOT,):
                current = await self.get(fqid)
                # compare object, to detect if must be updated or not
                # TODO: remove MONOTONIC_KEY for comparison
                # TODO: maybe all keys that match '.*__$' ?
                if current:
                    # create both dict and let python do the comparisson
                    # Note: private keywords in nested data will not be
                    # filtered, just 1st level
                    _current = filter_private(current)
                    _data = filter_private(data)
                    if _current == _data and MONOTONIC_KEY in _current:
                        return True  # do nothing, the object is not modified

                # I need to create / update the object
                if MONOTONIC_KEY not in data:
                    # preserve value is it was provided already
                    data[MONOTONIC_KEY] = time.time_ns()

                thing = data.pop("id", None)
                if thing == fqid:
                    assert (
                        ":" in fqid
                    ), "updating an item must have valid fqui, i.e. 'table:id' "
                    result = self.connection.update(fqid, data)
                else:
                    # Note: if fqid hasn't ':', surreal will create one
                    result = self.connection.create(fqid, data)

            elif mode in (self.MODE_TUBE,):
                # Note: in `tube` mode, surreal id must change to wave
                # and set `id` to `fqid`
                alt_id = data.pop("id", None)
                if alt_id is not None:
                    data[ALT_KEY] = alt_id
                monotonic = data.setdefault(MONOTONIC_KEY, time.time_ns())
                tube_name = fqid.split(":")[0]
                thing = f"{tube_name}:{monotonic}"

                # in `tube` mode, always create a new record
                result = self.connection.create(thing, data)

                # update TUBE_WAVE table
                # thing = f"{TUBE_WAVE}:{tube_name}"
                result = self.connection.update(
                    TUBE_WAVE,
                    # {MONOTONIC_KEY: monotonic},
                    data,
                    record_id=tube_name,
                )
            else:
                raise RuntimeError(f"UNKNOWN mode: {mode} for put()")
            return result.status in ("OK",)

        except Exception as why:
            log.error(why)
            log.error("".join(traceback.format_exception(*sys.exc_info())))

    async def update_sync_wave(self, sources, target, wave):
        for source in sources:
            record_id = self.TUBE_SYNC_WAVES.setdefault(
                target, {}
            ).setdefault(source)
            data = {
                "source": source,
                "target": target,
                MONOTONIC_KEY: wave,
            }
            if record_id:
                # already in memory
                result = self.connection.query(
                    QUERY_UPDATE_TUBE_SYNC,
                    {"record_id": record_id, MONOTONIC_KEY: wave},
                )
                assert (
                    result.result and result.result[0][MONOTONIC_KEY] == wave
                ), f"Update {TUBE_SYNC} for {record_id} doesn't work!!"

            else:
                # Try to get the fquid for this TubeSync wave
                # query = f"""
                # SELECT * FROM {TUBE_SYNC} WHERE source=$source AND target=$target"""
                result = self.connection.query(
                    QUERY_SELECT_TUBE_SYNC, variables=data
                )
                if not result.result:
                    # record doesn't exists, I need to create the 1st one
                    result = self.connection.create(
                        table_name=TUBE_SYNC,
                        data=data,
                    )
                    record_id = result.result["id"]
                else:
                    # record exists
                    assert len(result.result) == 1
                    record_id = result.result[0]["id"]

                    # TODO: why doesn't work?=
                    # result = self.connection.update(TUBE_SYNC, {MONOTONIC_KEY: wave}, record_id=record_id)

                    result = self.connection.query(
                        QUERY_UPDATE_TUBE_SYNC,
                        {"record_id": record_id, MONOTONIC_KEY: wave},
                    )
                    assert (
                        result.result
                        and result.result[0][MONOTONIC_KEY] == wave
                    ), f"Update {TUBE_SYNC} for {record_id} doesn't work!!"

                self.TUBE_SYNC_WAVES[target][source] = record_id

    async def set(self, fqid, data, merge=False):
        # TODO: used??
        t0 = time.time()
        table, uid = split_fqui(fqid)
        if merge:
            data0 = await self.get(table)
            # data = {** data0, ** data} # TODO: is faster?
            data0.update(data)
            data = data0

        self.connection or await self._connect()

        # await self.connection.query(f"USE DB {table.replace('.', '_')};")
        # TODO: review this code
        for kind, items in data.items():
            for _, item in items.items():
                _ = self.connection.update(
                    kind,
                    item,
                )
        t1 = time.time()
        print(f"{self.__class__}.set() : elapsed = {t1-t0} seconds")

    async def save(self, nice=False, wait=False):
        "TBD"
        return True

    async def info(self):
        "TBD"
        result = self.connection.query("INFO FOR DB;")
        return result.result

    async def count(self, table):
        result = self.connection.count(table)
        return result.result


class DualStorage(PickleStorage):
    """Storage for debugging and see all data in yaml
    Low performance, but is just for testing
    """

    def __init__(
        self, url="./db", mode=iCRUD.MODE_SNAPSHOT, klass=YamlStorage
    ):
        super().__init__(url=url, mode=mode)
        self.other = klass(url)
        self.background = self.other.background

    async def get(self, fqid, query=None, **params):
        other_mtime = None
        if not self.other.lock:
            table, uid = split_fqui(fqid)
            other_path = self.other._file(table)
            mine_path = self._file(table)
            if os.access(other_path, os.F_OK):
                other_mtime = os.stat(other_path).st_mtime
            else:
                other_mtime = 0
            if os.access(mine_path, os.F_OK):
                mine_mtime = os.stat(mine_path).st_mtime
            else:
                mine_mtime = 0

        if other_mtime is not None:
            if other_mtime > mine_mtime:
                # replace table from newer to older one
                universe = self.other._load(table)
                super()._save(table, universe, force=True)
                self.cache[table] = universe
            data = await super().get(fqid, query=None, **params)
        else:
            data = {}
        return data

    async def set(self, fqid, data, merge=False):
        """
        other.mtime < mine.mtime
        otherwise user has modifier `yaml` file and `pickle` will be updated
        """
        res1 = await self.other.set(fqid, data, merge)
        res2 = await super().set(fqid, data, merge)
        return all([res1, res2])

    async def put(self, fqid, data: Dict) -> bool:
        res1 = await super().put(fqid, data)
        res2 = await self.other.put(fqid, data)
        return all([res1, res2])

    def _save(self, table, universe=None, pause=0):
        self.other._save(table, universe, pause=pause)
        super()._save(table, universe, pause=pause)

    def running(self):
        return super().running() + self.other.running()
