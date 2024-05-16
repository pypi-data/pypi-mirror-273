import yaml
from prometheus_client import start_http_server, Gauge
import psycopg2
import time

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
            CONNECTIONS_PER_DB.labels(database=db, host=db_config["host"]).set(count)

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
            CONNECTIONS_PER_USER.labels(user=user, host=db_config["host"]).set(count)

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
            CONNECTIONS_BY_STATE.labels(state=state, host=db_config["host"]).set(count)

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
            CONNECTIONS_PER_SOURCE.labels(source=source, host=db_config["host"]).set(count)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error retrieving data from {db_config['host']}: {e}")


def main():
    config = load_config()

    if not ("hosts" in config and config["hosts"]):
        print("No database hosts specified in the configuration file.")
        exit(1)

    databases_to_query = []

    for host in config["hosts"]:
        if not all(key in host for key in ["user", "password", "host", "port"]):
            print("Database configuration is missing required fields.")
            exit(1)

        db_config = {
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
        config["exporter"]["port"]
        if "exporter" in config and "port" in config["exporter"]
        else 8989
    )

    start_http_server(exporter_port)
    print(f"Prometheus exporter started on port {exporter_port}")

    while True:
        for db in databases_to_query:
            get_db_connections(db)
        time.sleep(15)


if __name__ == "__main__":
    main()
