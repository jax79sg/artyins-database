# Database For artyins deployment architecture
This is a submodule for the artyins architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-database.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-database)

Refer to [Trello Task list](https://trello.com/c/gMsgraQm) for running tasks.

---

## Table of Contents

- [Schema](#Schema)
- [Setup](#Setup)
- [Tests](#Tests)

---
## Schema
The database schema is designed as follows. The reports table refers to the reports in their raw form. After ingestion, details are stored in the ingests table. Relevant statistics can be drawn from these 2 tables for analysis.
```sql
CREATE TABLE `reports` (
  #`id` int PRIMARY KEY AUTO_INCREMENT,
  `filename` varchar(255) PRIMARY KEY,
  `created_at` varchar(14),
  `ingested_at` varchar(14),
  `currentloc` varchar(255)
);

CREATE TABLE `ingests` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `text` text,
  `section` varchar(255),
  `created_at` varchar(14),
  `ingest_id` varchar(1000),
  `predicted_category` varchar(255),
  `annotated_category` varchar(255)
);

ALTER TABLE `ingests` ADD FOREIGN KEY (`ingest_id`) REFERENCES `reports` (`filename`);
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%' identified by 'password';
INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES ("hello.pdf","20191231121212","20191231121312","/home/user/reports/raw/");
INSERT INTO ingests (text, section, created_at, ingest_id, predicted_category, annotated_category) VALUES ('Hellow hellow','observation','20200121121313','hello.pdf','PERSONNEL','PERSONNEL');

commit;
```

## Setup
### MySQL server
The setup is done by creating a Docker image. You may build your docker image with the following docker-compose.yml, which include creating the database and loading the schema with test data, as described in init.sql.
docker-compose.yml
```yml
version: '2.1'
services:

  mysqldb:
    image: mysql
    restart: always
    volumes:
      - ./mysql-data:/var/lib/mysql
      - ./mysql-init-files:/docker-entrypoint-initdb.d  #init.sql in this folder will be executed once
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: password
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_DATABASE: reportdb
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin" ,"ping", "-h", "localhost"]
      timeout: 5s
      retries: 3
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-database). You are required to write the necessary unit tests if you make changes to the database schema.

### Unit Tests
test.py
```python
import unittest
import time
class TestConnections(unittest.TestCase):

    def setUp(self):
        print("Waiting for mySQL to finish booting")
        time.sleep(15)
        import mysql.connector as mysql
        db = mysql.connect(
           host = "127.0.0.1",
           database = "reportdb",
           user = "user",
           passwd = "password"
        )
        
    def test_connectdb(self):
        print("Running ConnectDB test")
        print(db)

    def test_readdata(self):
        print("Running Read Data")
        print("Checking reports table")
        cursor = db.cursor()
        cursor.execute("select * from reports")
        records = cursor.fetchall()
        assert cursor.rowcount>=1,"There should be one or more reports records"
        cursor.execute("select * from ingests")
        records = cursor.fetchall()
        assert cursor.rowcount>=1,"There should be one or more ingests records"
        cursor.close()

    def test_writedata(self):
        print("Running Write Data")
        cursor = db.cursor()
        cursor.execute("INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES (%s, %s, %s, %s)",("abc.pdf","2020-01-06 15:55:55","2020-01-06 16:33:33","/mnt/raw/reports/"))
        db.commit()
        assert cursor.rowcount>=1,"There should be one report inserted"
        cursor.execute("INSERT INTO ingests (text,section,created_at,ingest_id,predicted_category,annotated_category) VALUES (%s, %s, %s, %s,%s,%s)",("This is the weather for singapore","observation","2020-01-06 15:55:55","1","DOCTRINE","DOCTRINE")) 
        cursor.close()

if __name__ == '__main__':
    unittest.main()
```

