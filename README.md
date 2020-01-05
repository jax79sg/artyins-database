[![Database](https://github.com/jax79sg/artyins-database/raw/master/images/SoftwareArchitectureDatabase.jpg)]()

# Database For artyins deployment architecture
This is a submodule for the artyins architecture. Please refer to [main module](https://github.com/jax79sg/artyins) for full build details.

[![Build Status](https://travis-ci.com/jax79sg/artyins-database.svg?branch=master)](https://travis-ci.com/jax79sg/artyins-database)

Refer to [Trello Task list](https://trello.com/c/gMsgraQm) for running tasks.

---

## Table of Contents (Optional)

- [Schema](#Schema)
- [Setup](#Setup)
- [Virtualenv](#Virtualenv)
- [Tests](#Tests)

---
## Schema
The database schema is designed as follows. The reports table refers to the reports in their raw form. After ingestion, details are stored in the ingests table. Relevant statistics can be drawn from these 2 tables for analysis.
[![Database](https://github.com/jax79sg/artyins-database/raw/master/images/Reports.png)]()
```sql
CREATE TABLE `reports` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `filename` varchar(255),
  `created_at` timestamp,
  `ingested_at` timestamp,
  `currentloc` varchar(255)
);

CREATE TABLE `ingests` (
  `id` int PRIMARY KEY,
  `text` varchar(255),
  `section` varchar(255),
  `created_at` timestamp,
  `ingest_id` int,
  `predicted_category` varchar(255),
  `annotated_category` varchar(255)
);

ALTER TABLE `ingests` ADD FOREIGN KEY (`ingest_id`) REFERENCES `reports` (`id`);
```


## Setup
### MySQL server
The setup is done by creating a Docker image. The image can be downloaded with the following command.
```bash
docker pull quay.io/jax79sg/artyins-database
```

Alternatively, you may build your docker image with the following Dockerfile, which include creating the database and loading the schema with test data.
```docker
```
---

## Tests 
This repository is linked to [Travis CI/CD](https://travis-ci.com/jax79sg/artyins-classifierservice). You are required to write the necessary unit tests if you make changes to the database schema.

### Unit Tests
```python
import unittest

class TestModels(unittest.TestCase):

    def test_reports(self):
        print("Running TestModel reports table")
        pass #Kah Siong to insert
        
    def test_ingests(self):
        print("Running TestModel ingests table")
        pass #Kah Siong to insert

if __name__ == '__main__':
    unittest.main()
```

