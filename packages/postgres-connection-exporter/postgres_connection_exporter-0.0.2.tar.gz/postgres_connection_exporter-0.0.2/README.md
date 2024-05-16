# PostgreSQL Connection Exporter for Prometheus

This is a simple server that exports PostgreSQL connection metrics in a format that can be scraped by Prometheus.

It outputs the following metrics:

- The number of connections per database
- The number of connections per user
- The number of connections per client address
- The number of connections per state

## Installation

You can install the exporter from PyPI. Within a virtual environment, run:

```bash
pip install postgres-connection-exporter
```

## Configuration

The exporter is configured using a `config.yaml`. You can create a default configuration file in the current working directory with:

```bash
postgres-connection-exporter --create-config
```

Now, edit the `config.yaml` file to match your PostgreSQL connection settings. Here is an example configuration:

```yaml
hosts:
  host: localhost
  port: 5432
  user: postgres
  password: postgres
```

The user must have the `pg_monitor` role to access the `pg_stat_activity` view.

## Usage

After you have created your `config.yaml`, you can start the exporter with:

```bash
postgres-connection-exporter
```

By default, the exporter listens on `localhost:8989`. You can change the address in the `config.yaml` file, or using the `--host` and `--port` flags:

```bash
postgres-connection-exporter --host 0.0.0.0 --port 9898
```

You can also specify a different configuration file with the `--config` flag:

```bash
postgres-connection-exporter --config /path/to/config.yaml
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.