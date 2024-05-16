import yaml
from prometheus_client import start_http_server, Gauge
import psycopg2
import time
import argparse
import pathlib
import shutil
import sys

CONNECTIONS_PER_DB = Gauge(
    "db_connections_per_database",
    "Number of current connections per database",
    ["database", "host"],
)
CONNECTIONS_PER_USER = Gauge(
    "db_connections_per_user",
    "Number of current connections per user",
    ["user", "host"],
)
CONNECTIONS_BY_STATE = Gauge(
    "db_connections_by_state",
    "Number of current connections by state",
    ["state", "host"],
)
CONNECTIONS_PER_SOURCE = Gauge(
    "db_connections_per_source",
    "Number of current connections per source",
    ["source", "host"],
)


def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)


def get_all_databases(db_config):
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config.get("port", 5432),
        )
        cursor = conn.cursor()

        cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cursor.fetchall()

        cursor.close()
        conn.close()

        return [db[0] for db in databases]

    except Exception as e:
        print(f"Error retrieving list of databases: {e}")
        return []


def get_db_connections(db_config):
    try:
        host_identifier = db_config.get("name") or db_config["host"]

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"],
            port=db_config["port"],
        )
        cursor = conn.cursor()

        # Query to get the number of connections per database
        cursor.execute(
            """
            SELECT datname, COUNT(*) 
            FROM pg_stat_activity 
            GROUP BY datname;
        """
        )
        db_connections = cursor.fetchall()
        for db, count in db_connections:
            CONNECTIONS_PER_DB.labels(database=db, host=host_identifier).set(count)

        # Query to get the number of connections per user
        cursor.execute(
            """
            SELECT usename, COUNT(*) 
            FROM pg_stat_activity 
            GROUP BY usename;
        """
        )
        user_connections = cursor.fetchall()
        for user, count in user_connections:
            CONNECTIONS_PER_USER.labels(user=user, host=host_identifier).set(count)

        # Query to get the number of connections by state
        cursor.execute(
            """
            SELECT state, COUNT(*) 
            FROM pg_stat_activity 
            GROUP BY state;
        """
        )
        state_connections = cursor.fetchall()
        for state, count in state_connections:
            CONNECTIONS_BY_STATE.labels(state=state, host=host_identifier).set(count)

        # Query to get the number of connections per source
        cursor.execute(
            """
            SELECT client_addr, COUNT(*) 
            FROM pg_stat_activity 
            GROUP BY client_addr;
        """
        )
        source_connections = cursor.fetchall()
        for source, count in source_connections:
            CONNECTIONS_PER_SOURCE.labels(source=source, host=host_identifier).set(
                count
            )

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error retrieving data from {db_config['host']}: {e}")


def main():
    parser = argparse.ArgumentParser(description="PostgreSQL connection exporter")
    parser.add_argument(
        "--config", "-c", help="Path to the configuration file", default="config.yaml"
    )
    parser.add_argument(
        "--create", "-C", help="Create a new configuration file", action="store_true"
    )
    parser.add_argument(
        "--port",
        "-p",
        help="Port for the exporter to listen on (default: 8989, or the port specified in the configuration file)",
        type=int,
    )
    parser.add_argument(
        "--host",
        help="Host for the exporter to listen on (default: localhost, or the host specified in the configuration file)",
    )
    args = parser.parse_args()

    if args.create:
        config_file = pathlib.Path(args.config)
        if config_file.exists():
            print("Configuration file already exists.")
            sys.exit(1)

        template = pathlib.Path(__file__).parent / "config.dist.yaml"
        try:
            shutil.copy(template, config_file)
            print(f"Configuration file created at {config_file}")
            sys.exit(0)
        except Exception as e:
            print(f"Error creating configuration file: {e}")
            sys.exit(1)

    config = load_config(args.config)

    if not ("hosts" in config and config["hosts"]):
        print("No database hosts specified in the configuration file.")
        sys.exit(1)

    databases_to_query = []

    for host in config["hosts"]:
        if not all(key in host for key in ["user", "password", "host", "port"]):
            print("Database configuration is missing required fields.")
            exit(1)

        db_config = {
            "name": host.get("name"),
            "user": host["user"],
            "password": host["password"],
            "host": host["host"],
            "port": host["port"],
        }

        databases_to_query.append(db_config)

    if not databases_to_query:
        print("No databases to query.")
        exit(1)

    exporter_port = (
        args.port
        if args.port
        else (
            config["exporter"]["port"]
            if "exporter" in config and "port" in config["exporter"]
            else 8989
        )
    )

    exporter_host = (
        args.host
        if args.host
        else (
            config["exporter"]["host"]
            if "exporter" in config and "host" in config["exporter"]
            else "localhost"
        )
    )

    start_http_server(exporter_port, exporter_host)
    print(f"Prometheus exporter started on {exporter_host}:{exporter_port}")

    while True:
        for db in databases_to_query:
            get_db_connections(db)
        time.sleep(15)


if __name__ == "__main__":
    main()
