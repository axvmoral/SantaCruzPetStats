CREATE TABLE IF NOT EXISTS "cats" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"color"	TEXT,
	"breed"	TEXT,
	"day_age_when_scraped"	TEXT,
	"shelter_since"	TEXT,
	"date_first_lost_website"	TEXT,
	"date_first_adopt_website"	TEXT,
	"comment"	TEXT,
	"url"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "cats_time" (
	"id"	TEXT NOT NULL,
	"date"	TEXT,
	"lb_weight"	TEXT,
	"located"	TEXT,
	"steralized"	INTEGER,
	FOREIGN KEY("id") REFERENCES "cats"("id")
);

CREATE TABLE IF NOT EXISTS "dogs" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"color"	TEXT,
	"breed"	TEXT,
	"day_age_when_scraped"	TEXT,
	"shelter_since"	TEXT,
	"date_first_lost_website"	TEXT,
	"date_first_adopt_website"	TEXT,
	"comment"	TEXT,
	"url"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "dogs_time" (
	"id"	TEXT NOT NULL,
	"date"	TEXT,
	"lb_weight"	TEXT,
	"located"	TEXT,
	"steralized"	INTEGER,
	FOREIGN KEY("id") REFERENCES "dogs"("id")
);

CREATE TABLE IF NOT EXISTS "others" (
	"id"	TEXT NOT NULL UNIQUE,
	"name"	TEXT,
	"gender"	TEXT,
	"color"	TEXT,
	"breed"	TEXT,
	"day_age_when_scraped"	TEXT,
	"shelter_since"	TEXT,
	"date_first_lost_website"	TEXT,
	"date_first_adopt_website"	TEXT,
	"comment"	TEXT,
	"url"	TEXT,
	PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "others_time" (
	"id"	TEXT NOT NULL,
	"date"	TEXT,
	"lb_weight"	TEXT,
	"located"	TEXT,
	"steralized"	INTEGER,
	FOREIGN KEY("id") REFERENCES "others"("id")
);
