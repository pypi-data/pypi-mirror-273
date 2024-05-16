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

## Usage

The exporter is configured using a `config.yaml`. You can find an example in [config.dist.yaml](config.dist.yaml).

After you have created your `config.yaml`, you can start the exporter with:

```bash
postgres-connection-exporter
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.