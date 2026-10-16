#!/usr/bin/env bash
set -e

BENCH_DIR="/home/frappe/frappe-bench"

echo "=== 1. Initializing Frappe Bench ==="
if [ ! -d "$BENCH_DIR" ]; then
    bench init --frappe-branch develop --python python3.11 "$BENCH_DIR"
fi

cd "$BENCH_DIR"

echo "=== 2. Getting WhatsApp Dependency ==="
if [ ! -d "apps/whatsapp" ]; then
    bench get-app whatsapp || true
fi

echo "=== 3. Getting CRM App ==="
if [ ! -d "apps/crm" ]; then
    bench get-app crm "/mnt/c/PACE/PC CRM"
fi

echo "=== 4. Creating Site crm.localhost ==="
if [ ! -d "sites/crm.localhost" ]; then
    bench new-site crm.localhost \
        --db-root-password root \
        --admin-password admin \
        --install-app crm
fi

echo "=== 5. Enabling Developer Mode ==="
bench --site crm.localhost set-config developer_mode 1
bench use crm.localhost

echo "=== 6. Building Assets ==="
bench build --app crm

echo "=== DONE! ==="
