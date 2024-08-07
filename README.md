# DNSProbe

A Simple and Efficient DNS Scanning Tool

## Description

DNSProbe is a command-line tool designed to perform DNS lookups for a specified domain and record type. It supports various record types, including A, AAAA, CNAME, MX, NS, SOA, and TXT.

## Features

*   Perform DNS lookups for a specified domain and record type
*   Supports multiple record types
*   Configurable DNS server and record types
*   Colorized output for console
*   Logging with rotating file handler and detailed format

## Requirements

*   Python 3.x
*   `dnspython` library
*   `tabulate` library
*   `pyyaml` library
*   `colorama` library

## Installation

1.  Install the required libraries using pip:

    ```bash
    pip install dnspython tabulate pyyaml colorama
    ```

2.  Clone the repository:

    ```bash
    git clone https://github.com/your-username/dnsprobe.git
    ```

3.  Navigate to the project directory:

    ```bash
    cd dnsprobe
    ```

## Usage

1.  Run the tool using the following command:

    ```bash
    python scanner.py example.com
    ```

2.  You can specify the record type using the `--record-type` option:

    ```bash
      python scanner.py example.com --record-type A
    ```

3.  You can configure the DNS server and record types using a YAML configuration file. See the `config.yaml` file for an example.

## Configuration

The tool uses a YAML configuration file to store settings. You can modify the `config.yaml` file to change the DNS server and record types.

## Logging

The tool logs events to a rotating file handler and the console. You can modify the log level and format using the `setup_logging` function.

## Contributing

Contributions are welcome! If you find any issues or have feature requests, please submit a pull request or open an issue on the GitHub page.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Authors

*   [Abhishek Pokhrel](https://github.com/abhishek-pokhrel)