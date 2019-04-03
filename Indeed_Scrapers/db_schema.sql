create database jobcasedb ; 
use jobcasedb;
SET SQL_SAFE_UPDATES = 0;
/*DROP DATABASE IF EXISTS jobcasedb;*/


CREATE TABLE job_post (
    id  INT AUTO_INCREMENT PRIMARY KEY,
    date_posted VARCHAR(200) NOT NULL,
    companyID INT NOT NULL, 
    job_title INT NOT NULL,
    description VARCHAR(500) NULL, 
    URL VARCHAR(500) NOT  NULL,
    location INT NOT NULL,
    job_type_id INT NOT NULL,
    comptype INT NOT NULL
);
ALTER TABLE job_post
ADD FOREIGN KEY (location) references job_location(id),
ADD FOREIGN KEY(job_type_id) references job_type(jobtypeID),
ADD FOREIGN KEY(comptype) references compensation(comp_id),
ADD FOREIGN KEY (job_title) references posting_info(job_title_id),
ADD FOREIGN KEY (companyID) references posting_info(company_ID);

CREATE TABLE job_location(
location_id  INT AUTO_INCREMENT PRIMARY KEY,
city VARCHAR(500),
state VARCHAR(500)
);

CREATE TABLE job_type (
jobtypeID  INT AUTO_INCREMENT PRIMARY KEY,
job_type VARCHAR(200)
);

CREATE TABLE compensation( 
comp_id  INT AUTO_INCREMENT PRIMARY KEY, 
hourly VARCHAR(100), 
monthly VARCHAR(100),
yearly VARCHAR(100), 
salary_high INT,
salary_low INT
);

CREATE TABLE posting_info(
company_ID  INT, 
job_title_id INT NOT NULL, 
company_name VARCHAR(200) NOT NULL, 
job_title VARCHAR(200) NOT NULL);

ALTER TABLE posting_info
ADD PRIMARY KEY( company_ID, job_title_id);
