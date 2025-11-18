#!/bin/bash
set -e

sudo tee /etc/systemd/system/fastapi.service > /dev/null <<EOF
[Unit]
Description=FastAPI App Service
After=docker.service
Wants=docker.service

[Service]
Restart=always

# Fetch all SSM parameters and run Alembic migrations
ExecStartPre=/bin/bash -c 'SECRET_KEY=\$(aws ssm get-parameter --name "/fastapi/dev/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
ALGORITHM=\$(aws ssm get-parameter --name "/fastapi/dev/ALGORITHM" --query "Parameter.Value" --output text --region us-east-1) && \\
ACCESS_TOKEN_EXPIRE_MINUTES=\$(aws ssm get-parameter --name "/fastapi/dev/ACCESS_TOKEN_EXPIRE_MINUTES" --query "Parameter.Value" --output text --region us-east-1) && \\
POSTGRESQL_URL=\$(aws ssm get-parameter --name "/fastapi/dev/POSTGRESQL_URL" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
SUPABASE_URL=\$(aws ssm get-parameter --name "/fastapi/dev/SUPABASE_URL" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
SUPABASE_KEY=\$(aws ssm get-parameter --name "/fastapi/dev/SUPABASE_KEY" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
docker run --rm \\
  -e SECRET_KEY="\$SECRET_KEY" \\
  -e ALGORITHM="\$ALGORITHM" \\
  -e ACCESS_TOKEN_EXPIRE_MINUTES="\$ACCESS_TOKEN_EXPIRE_MINUTES" \\
  -e POSTGRESQL_URL="\$POSTGRESQL_URL" \\
  -e SUPABASE_URL="\$SUPABASE_URL" \\
  -e SUPABASE_KEY="\$SUPABASE_KEY" \\
  fortino/fastapi:latest alembic upgrade head'

# Start the FastAPI application
ExecStart=/bin/bash -c 'SECRET_KEY=\$(aws ssm get-parameter --name "/fastapi/dev/SECRET_KEY" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
ALGORITHM=\$(aws ssm get-parameter --name "/fastapi/dev/ALGORITHM" --query "Parameter.Value" --output text --region us-east-1) && \\
ACCESS_TOKEN_EXPIRE_MINUTES=\$(aws ssm get-parameter --name "/fastapi/dev/ACCESS_TOKEN_EXPIRE_MINUTES" --query "Parameter.Value" --output text --region us-east-1) && \\
POSTGRESQL_URL=\$(aws ssm get-parameter --name "/fastapi/dev/POSTGRESQL_URL" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
SUPABASE_URL=\$(aws ssm get-parameter --name "/fastapi/dev/SUPABASE_URL" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
SUPABASE_KEY=\$(aws ssm get-parameter --name "/fastapi/dev/SUPABASE_KEY" --with-decryption --query "Parameter.Value" --output text --region us-east-1) && \\
docker run --pull always -p 80:8000 --name fastapi \\
  -e SECRET_KEY="\$SECRET_KEY" \\
  -e ALGORITHM="\$ALGORITHM" \\
  -e ACCESS_TOKEN_EXPIRE_MINUTES="\$ACCESS_TOKEN_EXPIRE_MINUTES" \\
  -e POSTGRESQL_URL="\$POSTGRESQL_URL" \\
  -e SUPABASE_URL="\$SUPABASE_URL" \\
  -e SUPABASE_KEY="\$SUPABASE_KEY" \\
  fortino/fastapi:latest'

ExecStop=/usr/bin/docker stop fastapi
ExecStopPost=/usr/bin/docker rm fastapi

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable fastapi.service