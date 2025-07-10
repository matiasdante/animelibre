#!/bin/bash

# Grafana Beyla Demo Script
# This script generates a docker-compose.yml file for demonstrating Grafana Beyla
# with proper AppArmor compatibility for Ubuntu/Debian systems

set -e

echo "Setting up Grafana Beyla Demo..."

# Create Beyla configuration file
cat > beyla-config.yml << EOF
# Beyla configuration
discovery:
  services:
    - name: sample-app
      namespace: default
      ports:
        - 8080

otel:
  endpoint: http://prometheus:9090/api/v1/write
  metrics:
    interval: 5s
    
routes:
  unmatched: heuristic
  patterns:
    - /health

log_level: info
EOF

# Generate docker-compose.yml with AppArmor compatibility
cat > docker-compose.yml << EOF
version: '3.8'

networks:
  beyla-demo:
    driver: bridge

services:
  # Sample application to monitor
  sample-app:
    image: nginx:alpine
    container_name: sample-app
    ports:
      - "8080:80"
    volumes:
      - ./sample-nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - beyla-demo
    restart: unless-stopped

  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
      - '--web.enable-remote-write-receiver'
    networks:
      - beyla-demo
    restart: unless-stopped

  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    networks:
      - beyla-demo
    restart: unless-stopped
    depends_on:
      - prometheus

  # Beyla eBPF observability with AppArmor compatibility
  beyla:
    image: grafana/beyla:latest
    container_name: beyla
    privileged: true
    pid: "host"
    security_opt:
      - apparmor:unconfined
    cap_add:
      - SYS_ADMIN
      - SYS_PTRACE
      - SYS_RESOURCE
    volumes:
      - /sys/kernel/debug:/sys/kernel/debug:ro
      - /sys/fs/bpf:/sys/fs/bpf
      - /proc:/proc:ro
      - ./beyla-config.yml:/etc/beyla/config.yml:ro
    environment:
      - BEYLA_CONFIG_PATH=/etc/beyla/config.yml
    depends_on:
      - sample-app
      - prometheus
    networks:
      - beyla-demo
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
EOF

# Create Prometheus configuration
cat > prometheus.yml << EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'beyla'
    static_configs:
      - targets: ['beyla:8080']

  - job_name: 'sample-app'
    static_configs:
      - targets: ['sample-app:80']
EOF

# Create sample Nginx configuration
cat > sample-nginx.conf << EOF
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    log_format main '\$remote_addr - \$remote_user [\$time_local] "\$request" '
                    '\$status \$body_bytes_sent "\$http_referer" '
                    '"\$http_user_agent" "\$http_x_forwarded_for"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log;

    sendfile on;
    keepalive_timeout 65;

    server {
        listen 80;
        server_name localhost;

        location / {
            root /usr/share/nginx/html;
            index index.html index.htm;
        }

        location /health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        location /api/test {
            return 200 "API Test Response\n";
            add_header Content-Type text/plain;
        }
    }
}
EOF

echo ""
echo "✅ Grafana Beyla Demo setup complete!"
echo ""
echo "Files created:"
echo "  - docker-compose.yml (with AppArmor compatibility)"
echo "  - beyla-config.yml"
echo "  - prometheus.yml"
echo "  - sample-nginx.conf"
echo ""
echo "🚀 To start the demo:"
echo "  sudo docker-compose up -d"
echo ""
echo "📊 Access the services:"
echo "  - Sample App: http://localhost:8080"
echo "  - Prometheus: http://localhost:9090"
echo "  - Grafana: http://localhost:3000 (admin/admin)"
echo ""
echo "🔍 To check container status:"
echo "  docker-compose ps"
echo ""
echo "📝 To view Beyla logs:"
echo "  docker-compose logs beyla"
echo ""
echo "⚠️  Note: This demo includes AppArmor compatibility settings"
echo "   (security_opt: apparmor:unconfined) for Ubuntu/Debian systems."
echo ""
echo "🛠️  Troubleshooting:"
echo "  - If Beyla fails to start, ensure Docker is running with sufficient privileges"
echo "  - On systems with AppArmor, the 'apparmor:unconfined' setting is required"
echo "  - Beyla requires access to /sys/kernel/debug and /sys/fs/bpf for eBPF functionality"
echo ""