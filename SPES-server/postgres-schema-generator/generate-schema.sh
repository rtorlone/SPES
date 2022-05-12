#! /bin/sh
java -jar schemaspy-6.1.0.jar -t pgsql \
  -s public -db spes -u root -p root \
  -host localhost -o output/ \
  -vizjs \
  -dp postgresql-42.3.3.jar
