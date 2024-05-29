USE bootcamp_project;

CREATE TABLE suicide_data (
    country VARCHAR(100),
    year INT,
    sex VARCHAR(10),
    age VARCHAR(20),
    suicides_no INT,
    population INT,
    suicides_per_100k FLOAT,
    country_year VARCHAR(100),
    gdp_for_year_dollars BIGINT,
    gdp_per_capita_dollars INT,
    generation VARCHAR(50)
);


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/master.csv'
INTO TABLE bootcamp_project.suicide_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;


select * from suicide_data;

SELECT sex, SUM(suicides_no) AS total_suicides FROM suicide_data GROUP BY sex



