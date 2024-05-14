from psycopg_pool import ConnectionPool
from psycopg.rows import namedtuple_row

class sql():
    CONFIG_PASSWORD = 'password'
    CONFIG_USER = 'user'
    CONFIG_HOST = 'host'
    CONFIG_PORT = 'port'
    CONFIG_DBNAME = 'db_name'
    CONFIG_PARAMS = 'params'
    
    def __init__(self, application_name, logger) -> None:
        self.application_name = application_name
        self.logger = logger

    def init_sql(self, config):      
        self.logger.info(f"SQL Init for: {self.application_name}. with the following config: \
                         {self.sanitized_config(config)}")
        uri = self.build_uri_from_config(config)
        connection = self.build_connection(uri, self.application_name)
        return connection

    def sanitized_config(self, config):
        dup_config = dict(config)
        del dup_config[sql.CONFIG_PASSWORD]
        sanitized_config = dup_config
        return sanitized_config

    def build_uri_from_config(self, config):
        if self.validate_config(config):
            connection_uri = f"postgresql://{config[sql.CONFIG_USER]}:{config[sql.CONFIG_PASSWORD]}@{config[sql.CONFIG_HOST]}:{config[sql.CONFIG_PORT]}/{config[sql.CONFIG_DBNAME]}"
            if sql.CONFIG_PARAMS in config:
                connection_uri += f"?{config[sql.CONFIG_PARAMS]}"
            return connection_uri
        self.logger.error(f"SQL build_uri_from_config for {self.application_name} failed. \
                          Config failed validation {self.str_sanitized_config(config)}")
        return None
        
    def validate_config(self, config):
        required_keys = [sql.CONFIG_PASSWORD,
                         sql.CONFIG_USER, 
                         sql.CONFIG_HOST,
                         sql.CONFIG_PORT,
                         sql.CONFIG_DBNAME]
        return set(required_keys) <= set(config.keys())
    
    def build_connection(self, uri, application_name):
        '''
        postgresql://[userspec@][hostspec][/dbname][?paramspec]
        where userspec is: user[:password]
        and hostspec is:   [host][:port][,...]
        and paramspec is:  name=value[&...]
        Examples: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING
        postgresql://
        postgresql://localhost
        postgresql://localhost:5433
        postgresql://localhost/mydb
        postgresql://user@localhost
        postgresql://user:secret@localhost
        postgresql://other@localhost/otherdb?connect_timeout=10&application_name=myapp
        postgresql://host1:123,host2:456/somedb?target_session_attrs=any&application_name=myapp
        '''
        self.logger.info(f"SQL: Creating connection pool for: {application_name}")
        connection_pool_kwargs = {"row_factory": namedtuple_row}
        pool = ConnectionPool(uri, min_size=2, max_size=5, kwargs=connection_pool_kwargs)
        return pool

    