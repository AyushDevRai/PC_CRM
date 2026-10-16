#!/usr/bin/env bash
set -e

echo "=== 1. System Packages ==="
export DEBIAN_FRONTEND=noninteractive

apt update -y
apt install -y \
    git \
    curl \
    build-essential \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libmariadb-dev \
    libcups2-dev \
    mariadb-server \
    mariadb-client \
    redis-server \
    python3-dev \
    python3-pip \
    python3-venv \
    software-properties-common

# Install wkhtmltopdf
apt install -y wkhtmltopdf || true

echo "=== 2. Node.js & Yarn ==="
if ! command -v node &> /dev/null; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
    apt install -y nodejs
fi
npm install -g yarn

echo "=== 3. Configure MariaDB ==="
MARIADB_CNF="/etc/mysql/mariadb.conf.d/99-frappe.cnf"
cat << 'EOF' > "$MARIADB_CNF"
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
EOF

# Start services using systemctl (or service fallback)
systemctl restart mariadb || service mariadb restart
systemctl restart redis-server || service redis-server restart

# Setup MariaDB root user password to 'root'
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED VIA mysql_native_password USING PASSWORD('root'); FLUSH PRIVILEGES;" 2>/dev/null || \
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root'; FLUSH PRIVILEGES;" 2>/dev/null || true

# Test root login
mysql -u root -proot -e "SELECT 'MariaDB connected successfully' AS status;"

echo "=== 4. Configure WSL default user and DrvFS ==="
cat << 'EOF' > /etc/wsl.conf
[boot]
systemd=true

[user]
default=frappe

[automount]
options="metadata"
EOF

# Ensure frappe user exists and has sudo
if ! id -u frappe &>/dev/null; then
    useradd -m -s /bin/bash -G sudo frappe
fi
echo 'frappe ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/frappe
chmod 0440 /etc/sudoers.d/frappe

echo "=== 5. Install Frappe Bench CLI ==="
pip3 install --break-system-packages frappe-bench

echo "=== Prerequisites setup successfully! ==="
