#!/bin/bash
# Install postgres
sudo apt install -y wget ca-certificates
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

RELEASE=$(lsb_release -cs)
echo "deb http://apt.postgresql.org/pub/repos/apt ${RELEASE}-pgdg main" \
  sudo tee /etc/apt/sources.list.d/pgdg.list
sudo apt update -y && sudo apt install -y postgresql postgresql-contrib

# Install pgvector
sudo apt install -y postgresql-server-dev-17
cd /tmp
rm -rf pgvector
git clone --branch v0.4.4 https://github.com/pgvector/pgvector.git 
cd pgvector 
make PG_CONFIG=/usr/lib/postgresql/17/bin/pg_config 
sudo make install

# Activate pgvector and the database
echo 'ray ALL=(ALL:ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/ray
sudo service postgresql start
# pragma: allowlist nextline secret
sudo -u postgres psql -c "ALTER USER postgres with password 'postgres';"
sudo -u postgres psql -c "CREATE EXTENSION vector;"