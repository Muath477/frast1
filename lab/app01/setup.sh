#!/usr/bin/env bash
# APP-01 bootstrap (run on lab VM with temporary NAT)
set -euo pipefail
sudo apt update
sudo apt install -y bind9 bind9-utils nginx iperf3 stress-ng python3-psutil snmpd
sudo cp "$(dirname "$0")/named.conf.local" /etc/bind/named.conf.local
sudo cp "$(dirname "$0")/db.rootiq.lab" /etc/bind/db.rootiq.lab
sudo sed -i 's/^\s*listen-on-v6.*/\tlisten-on { any; };\n\tallow-query { any; };\n\trecursion no;/' /etc/bind/named.conf.options || true
sudo named-checkconf
sudo named-checkzone rootiq.lab /etc/bind/db.rootiq.lab
sudo systemctl enable --now named
if ! grep -q 'location = /health' /etc/nginx/sites-available/default; then
  sudo sed -i 's#location / {#location = /health { default_type text/plain; return 200 "ok"; }\n\tlocation / {#' /etc/nginx/sites-available/default
fi
sudo nginx -t && sudo systemctl reload nginx
sudo systemctl enable --now iperf3 2>/dev/null || (iperf3 -s -D)
echo "APP-01 setup done — disconnect NAT after verification"
