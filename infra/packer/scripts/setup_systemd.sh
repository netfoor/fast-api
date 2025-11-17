#!/bin/bash
set -e

sudo tee /etc/systemd/system/fastapi.service > /dev/null <<EOF
[Unit]
Description=FastAPI App Service
After=docker.service
Wants=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --pull always \
  -p 80:8000 \
  --name fastapi \
  fortino/fastapi:latest

ExecStop=/usr/bin/docker stop fastapi
ExecStopPost=/usr/bin/docker rm fastapi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fastapi.service
