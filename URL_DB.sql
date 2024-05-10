CREATE DATABASE url_db;

CREATE TABLE url_db.funding_opportunity_urls(
	id int(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url varchar(500) NOT NULL,
	closeDate DATE NOT NULL,
	UNIQUE (url)
);

CREATE TABLE url_db.archived_links(
	id int(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url varchar(500) NOT NULL,
	closeDate DATE,
    reason varchar(500),
	UNIQUE (url)
);

INSERT INTO url_db.funding_opportunity_urls(url, closeDate) VALUES ('https://cytokinesociety.org/about-us/honorary-members/', '9999-01-01');
INSERT INTO url_db.funding_opportunity_urls(url, closeDate) VALUES('https://www.rbc.com/community-social-impact/climate/environmental-donations/index.html', '2024-05-06');


CREATE TABLE url_db.researcher_profiles_urls(
	id int(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    url varchar(500) NOT NULL,
	email varchar(500) NOT NULL,
	UNIQUE (email)
);

CREATE TABLE url_db.users(
	id int(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username varchar(500) NOT NULL,
	password varchar(500),
	salt varchar(500),
	UNIQUE (username)
);
