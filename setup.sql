CREATE TABLE "lost_cats" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "lost_dogs" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "lost_others" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "adoptable_cats" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "adoptable_dogs" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE "adoptable_others" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"animal_type"	TEXT,
	"days_since_found"	INTEGER,
	"breed"	TEXT,
	"weight"	REAL,
	"lost_or_found"	TEXT,
	"location"	TEXT,
	"located_at"	TEXT,
	"date_found"	TEXT,
	"description"	TEXT,
	"age"	INTEGER,
	"more_info"	TEXT,
	"location_found"	TEXT,
	"date_scraped"	TEXT,
	"date_last_website"	TEXT,
	PRIMARY KEY("id")
);
