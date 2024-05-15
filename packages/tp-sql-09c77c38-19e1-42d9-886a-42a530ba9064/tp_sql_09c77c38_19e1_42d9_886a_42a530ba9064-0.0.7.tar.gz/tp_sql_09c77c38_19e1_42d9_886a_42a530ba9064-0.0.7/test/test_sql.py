import sys
print(sys.path)
import pytest
from utils.tp_sql.src.tp_sql.main import Sql
import logging
class TestSQL:

    @pytest.fixture
    def sql_util(self):
        tmp_logger = logging.getLogger()
        return Sql("Test app Name", tmp_logger)

    @pytest.fixture
    def sql_config(self):
        config = {
            Sql.CONFIG_DBNAME: 'dbName',
            Sql.CONFIG_HOST: "127.0.0.1",
            Sql.CONFIG_PASSWORD: "Pa$$wor4",
            Sql.CONFIG_PORT: 1324,
            Sql.CONFIG_USER: "UserName"
        }
        return config

    def test_str_sanitized_config(self, sql_util):
        config = {Sql.CONFIG_PASSWORD : "Pa$$wor4"}
        sanitized_config = sql_util.sanitized_config(config)
        assert Sql.CONFIG_PASSWORD not in sanitized_config
    
    def test_validate_config(self, sql_util):
        config = {
            Sql.CONFIG_DBNAME: 'db_name',
            Sql.CONFIG_HOST: "127.0.0.1",
            Sql.CONFIG_PASSWORD: "Pa$$wor4",
            Sql.CONFIG_PORT: 1324,
            Sql.CONFIG_USER: "User_Name"
        }
        assert sql_util.validate_config(config) is True

        config = {
            Sql.CONFIG_HOST: "127.0.0.1",
            Sql.CONFIG_PASSWORD: "Pa$$wor4",
            Sql.CONFIG_PORT: 1324,
            Sql.CONFIG_USER: "User_Name"
        }
        assert sql_util.validate_config(config) is False

        config = {}
        assert sql_util.validate_config(config) is False

    
    def test_build_uri_from_config(self, sql_util, sql_config):
        result = sql_util.build_uri_from_config(sql_config)
        assert result == f"postgresql://UserName:Pa$$wor4@127.0.0.1:1324/dbName"
