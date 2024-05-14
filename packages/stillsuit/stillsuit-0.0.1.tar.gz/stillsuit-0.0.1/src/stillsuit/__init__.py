from dataclasses import dataclass
import sqlite3
import yaml
import os


@dataclass
class StillSuit:
    """

    NOTE: according to documentation:
    https://www.sqlite.org/lang_createtable.html#rowid, the primary keys defined in
    the schema all follow the convention that they will be an alias for the built
    in rowid.
    """

    config: dict = None
    dbname: str = ":memory:"


    BASE_SCHEMA = {
      "filter": {
        "columns": [
          {"name":"__filter_id", "type":"INTEGER", "constraints": "PRIMARY KEY"}
        ],
        "relationships": [],
        "static": True
      },
      "simulation": {
        "columns": [
          {"name":"__simulation_id", "type":"INTEGER", "constraints": "PRIMARY KEY"}
        ],
        "relationships": [],
        "static": True
      },
      "data": {
        "columns": [
          {"name":"__data_id", "type":"INTEGER", "constraints": "PRIMARY KEY"}
        ],
        "relationships": [],
        "static": False
      },
      "trigger": {
        "columns": [
          {"name":"__trigger_id", "type":"INTEGER", "constraints": "PRIMARY KEY"},
          {"name":"__filter_id", "type":"INTEGER", "constraints": ""},
          {"name":"__data_id", "type":"INTEGER", "constraints": ""},
        ],
        "relationships": [{"filter":"__filter_id"}, {"data":"__data_id"}],
        "static": False
      },
      "event": {
        "columns": [
          {"name":"__event_id", "type":"INTEGER", "constraints": "PRIMARY KEY"},
          {"name":"__simulation_id", "type":"INTEGER", "constraints": ""},
        ],
        "relationships": [{"simulation":"__simulation_id"},],
        "static": False
      },
      "trigger_map": {
        "columns": [
          {"name":"__trigger_map_id", "type":"INTEGER", "constraints": "PRIMARY KEY"},
          {"name":"__event_id", "type":"INTEGER", "constraints": ""},
          {"name":"__trigger_id", "type":"INTEGER", "constraints": ""},
        ],
        "relationships": [{"event":"__event_id"}, {"trigger":"__trigger_id"}],
        "static": False
      },
    }

    REQUIRED_TABLES = set(BASE_SCHEMA) - set(("trigger_map",))
    STATIC_SCHEMA = {k:v for k, v in BASE_SCHEMA.items() if v['static']}
    

    def __post_init__(self):
        self.db, self.schema = self.connect(self.config, self.dbname)
        self.cursor = self.db.cursor()
 
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()

    def flush(self):
        self.db.commit()

    def __insert_dict(self, t, d):
        sql = "INSERT INTO %s(%s) VALUES (%s);" % (t, ",".join(d), ",".join(["?"] * len(d)))
        self.cursor.execute(sql, tuple(d.values()))
        return self.cursor

    def insert_static(self, d):
        # FIXME do any sort of sanity checking
        for t, td in d.items():
            self.__insert_dict(t, td)
            

    def insert_event(self, d):
        """
        Required format
        {"data": [{...}, ...],
         "trigger": [{...}, ...],
         "event": {...}
        }

        Furthermore, data and trigger must have the same length and be 1:1.

	NOTE: this method modifies the trigger and event dictionaries to add
        references to internal keys.  If you don't want that behavior save a copy
        before you insert or otherwise deal with it.
        """
        assert not (set(d) - set(("data", "trigger", "event")))
        event_id = self.__insert_dict("event", d["event"]).lastrowid
        for n,r in enumerate(d["data"]):
            d['trigger'][n]["__data_id"] = self.__insert_dict("data", r).lastrowid
            self.__insert_dict("trigger_map", {"__event_id":event_id, "__trigger_id": self.__insert_dict("trigger", d['trigger'][n]).lastrowid})
            

    @classmethod
    def db_schema(cls, db):
        return {n:s  for n, s in db.cursor().execute("SELECT name, sql FROM sqlite_master WHERE type='table';")}

    @classmethod
    def load_schema_from_config(cls, config):
        with open(config) as f:
            user_schema = yaml.safe_load(f)
        assert not (cls.REQUIRED_TABLES - set(user_schema))
        # put in a trigger_map table which is required but should not be provided by the user.
        user_schema["trigger_map"] = {"columns":[]}
        for t in cls.BASE_SCHEMA:
            user_schema[t]['columns'] += cls.BASE_SCHEMA[t]['columns']
            user_schema[t].setdefault('relationships',[]).extend(cls.BASE_SCHEMA[t]['relationships'])
            for c in user_schema[t]['columns']:
                if "constraints" not in c:
                    c["constraints"] = ""
        return user_schema

    @classmethod
    def connect(cls, config, dbname):
        def init_tables(__schema, __db):
            def column(c):
                return "%s %s %s" % (
                    c['name'], 
                    c['type'], 
                    c['constraints']
                )
         
            def foreign_keys(table, relationships):
                x = ["FOREIGN KEY (%s) REFERENCES %s(%s)" % (c,t,c) for d in relationships for t,c in d.items()]
                return x
            for t in __schema:
                fs = [column(c) for c in __schema[t]['columns']]
                fs += foreign_keys(t, __schema[t]['relationships'])
                q = "CREATE TABLE IF NOT EXISTS %s (%s)" % (t, ", ".join(fs))
                __db.cursor().execute(q)
        
            __db.commit()

        def new_db(_schema, _dbname = ":memory:"):
            _db = sqlite3.connect(_dbname)
            init_tables(_schema, _db)
            return _db, _schema

        schema = cls.load_schema_from_config(config)

        if os.path.exists(dbname):
            db_ref, _ = new_db(schema)
            db = sqlite3.connect(dbname)
            if cls.db_schema(db_ref) == cls.db_schema(db):
                 db_ref.close()
                 return db, schema
            else:
                 db_ref.close()
                 db.close()
                 raise ValueError("Database schema does not match")
        else:
            return new_db(schema, dbname)
