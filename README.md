## Port Scanner
Command line TCP/IP scanner for specific IP address.

### Usage
```bash
git clone https://github.com/fkkarakurt/portscanner
cd portscanner
pip install -r requirements.txt
python3 scanner.py
```

> Ports are specified in `ports.json` and `tcpports.json` files. By default, the scanner scans for ports in the `ports.json` file. To use the `tcpports.json` file, update the `PORTS_DATA_FILE` value in the `scanner.py` file.