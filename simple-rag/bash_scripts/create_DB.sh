sudo -u postgres psql "$DB_CONNECTION_STRING" -c "DROP TABLE IF EXISTS document;"  # drop
sudo -u postgres psql -f $MIGRATION_FP  # create
echo $MIGRATION_FP
echo "### Create DB ###"
sudo -u postgres psql "$DB_CONNECTION_STRING" -c "CREATE TABLE document (id SERIAL PRIMARY KEY, text TEXT NOT NULL, source VARCHAR(255), embedding VECTOR(1536));"  # create table