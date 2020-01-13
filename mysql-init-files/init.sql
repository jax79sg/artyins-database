
CREATE TABLE `reports` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `filename` varchar(255),
  `created_at` varchar(14),
  `ingested_at` varchar(14),
  `currentloc` varchar(255)
);

CREATE TABLE `ingests` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `text` varchar(255),
  `section` varchar(255),
  `created_at` varchar(14),
  `ingest_id` int,
  `predicted_category` varchar(255),
  `annotated_category` varchar(255)
);

ALTER TABLE `ingests` ADD FOREIGN KEY (`ingest_id`) REFERENCES `reports` (`id`);

INSERT INTO reports (filename,created_at,ingested_at,currentloc) VALUES ("hello.pdf","20191231121212","20191231121312","/home/user/reports/raw/");
INSERT INTO ingests (text, section, created_at, ingest_id, predicted_category, annotated_category) VALUES ('Hellow hellow','observation','20200121121313',1,'PERSONNEL','PERSONNEL');

commit;
