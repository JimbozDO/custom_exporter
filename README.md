testted on CentOS Linux 7

1. cp cert_exporter.py /usr/local/bin/cert_exporter.py
2. cp cert_exporter.service /etc/systemd/system/cert_exporter.service
3. systemctl daemon-reload
4. check in browser http://localhost:9101/metrics or curl -v http://your_host:9101/metrics
