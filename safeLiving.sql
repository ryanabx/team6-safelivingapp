SET sql_mode='ANSI_QUOTES';

CREATE TABLE States(
	"name" VARCHAR(64),
    abreviation CHAR(2),
    PRIMARY KEY(abreviation),
    UNIQUE("name")
);

CREATE TABLE Regions(
	num INT,
    "name" VARCHAR(64),
    safetyScore FLOAT(52),
    PRIMARY KEY ("name"),
    FOREIGN KEY (state) REFERENCES States(abreviation)
);

/* 
CREATE TABLE FELONIES();

CREATE TABLE CRIMES():
*/	