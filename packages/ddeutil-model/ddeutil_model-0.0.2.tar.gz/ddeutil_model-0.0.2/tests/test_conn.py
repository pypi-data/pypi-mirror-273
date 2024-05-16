import ddeutil.model.conn as conn


def test_db_conn_from_url():
    t = conn.DbConn.from_url(
        url=(
            "postgres+psycopg://demo:P%40ssw0rd@localhost:5432/db"
            "?echo=True&timeout=10"
        )
    )
    assert "postgres+psycopg" == t.driver

    t = conn.DbConn.from_url(
        url="mssql://demo:P@ssw0rd@127.0.0.1:5432/postgres"
    )
    assert "mssql" == t.driver
    assert "127.0.0.1" == t.host
    assert "P@ssw0rd" == t.pwd.get_secret_value()


def test_db_conn():
    t = conn.DbConn(
        **{
            "driver": "postgres",
            "host": "127.0.0.1",
            "port": "5432",
            "user": "postgres",
            "pwd": "P@ssw0rd",
            "db": "sales",
        }
    )
    assert "postgres" == t.driver
    assert "P@ssw0rd" == t.pwd.get_secret_value()


def test_fl_conn_from_url():
    t = conn.FlConn.from_url(
        url="sqlite:///D:/data/warehouse/main.sqlite?echo=True"
    )
    assert "sqlite" == t.sys
    assert "/D:/data/warehouse/main.sqlite" == t.path
    assert {"echo": "True"} == t.options


def test_fl_conn():
    t = conn.FlConn(
        **{
            "sys": "file",
            "pointer": "~/usr/myname/data/raw",
            "path": "warehouse/sales",
            "options": {
                "compress": "snippet",
                "partition": ["year", "month", "day"],
            },
        }
    )
    assert "file" == t.sys
    assert "~/usr/myname/data/raw" == t.pointer
    assert "warehouse/sales" == t.path
    assert {
        "compress": "snippet",
        "partition": ["year", "month", "day"],
    } == t.options
