#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting Frappe CRM Automated Setup"
echo "=========================================================="

export DEBIAN_FRONTEND=noninteractive

echo "==> 1. Updating APT repositories..."
sudo apt update -y

echo "==> 2. Installing system dependencies..."
sudo apt install -y \
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
    pipx \
    software-properties-common \
    wkhtmltopdf || true

echo "==> 3. Installing Node.js (v24 LTS) and Yarn..."
if ! command -v node &> /dev/null || [ "$(node -v | cut -d'.' -f1)" != "v24" ]; then
    curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
    sudo apt install -y nodejs
fi
sudo npm install -g yarn

echo "==> 4. Configuring MariaDB for Frappe..."
MARIADB_CNF="/etc/mysql/mariadb.conf.d/99-frappe.cnf"
sudo tee "$MARIADB_CNF" > /dev/null << 'EOF'
[mysqld]
character-set-client-handshake = FALSE
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

[mysql]
default-character-set = utf8mb4
EOF

echo "==> 5. Starting MariaDB and Redis..."
sudo systemctl restart mariadb || sudo service mariadb restart
sudo systemctl restart redis-server || sudo service redis-server restart

# Set MariaDB root password to 'root'
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'root'; FLUSH PRIVILEGES;" || true

echo "==> 6. Installing Frappe Bench CLI..."
pipx install frappe-bench || true
pipx ensurepath

export PATH="$HOME/.local/bin:$PATH"

echo "==> 7. Initializing Frappe Bench (develop)..."
BENCH_DIR="$HOME/frappe-bench"
if [ ! -d "$BENCH_DIR" ]; then
    bench init --frappe-branch develop --python python3 "$BENCH_DIR"
fi

cd "$BENCH_DIR"

echo "==> 8. Fetching dependencies and Frappe CRM..."
if [ ! -d "apps/whatsapp" ]; then
    bench get-app whatsapp || true
fi

if [ ! -d "apps/crm" ]; then
    bench get-app crm "https://github.com/frappe/crm"
fi

echo "==> 9. Creating site 'crm.localhost' and installing CRM..."
if [ ! -d "sites/crm.localhost" ]; then
    bench new-site crm.localhost \
        --db-root-password root \
        --admin-password admin \
        --install-app crm
fi

bench --site crm.localhost set-config developer_mode 1
bench use crm.localhost

echo "=========================================================="
echo " SETUP COMPLETE!"
echo " To start your CRM:"
echo "   cd ~/frappe-bench"
echo "   bench start"
echo ""
echo " Access URL: http://localhost:8000/crm"
echo " Login:      Administrator / admin"
echo "=========================================================="
