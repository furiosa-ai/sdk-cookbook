# Save index
rm -rf $SQL_DUMP_FP
mkdir -p $(dirname "$SQL_DUMP_FP") && touch $SQL_DUMP_FP
sudo -u postgres pg_dump -c > $SQL_DUMP_FP  # save