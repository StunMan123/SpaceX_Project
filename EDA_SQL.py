"""
pip needed to install:
!pip install sqlalchemy==1.3.9
!pip install ipython-sql
!pip install -q pandas


"""
import csv, sqlite3
import pandas as pd

%load_ext sql
%sql sqlite:///my_data1.db

#sql command
%sql DROP TABLE IF EXISTS SPACEXTABLE;
%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null


con = sqlite3.connect("my_data1.db") #connect
cur = con.cursor() #cursor object: execute SQL commands within database connected by 'con'

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")


#1. names of unique launch sites
%sql SELECT DISTINCT Launch_Site, COUNT(Launch_Site) AS Frequency FROM SPACEXTABLE GROUP BY Launch_Site;


#2.Display 5 records where launch sites begin with the string 'CCA'
%sql SELECT DISTINCT Launch_Site FROM SPACEXTABLE WHERE Launch_Site LIKE '%CCA%' LIMIT 5;


#3. Display the total payload mass carried by boosters launched by NASA (CRS)
%sql SELECT SUM(PAYLOAD_MASS__KG_) AS 'total payload mass' FROM SPACEXTABLE WHERE Customer LIKE '%NASA (CRS)%';


#4.Display average payload mass carried by booster version F9 v1.1
%sql SELECT ROUND(AVG(PAYLOAD_MASS__KG_),2) AS 'average payload mass' FROM SPACEXTABLE WHERE Booster_Version LIKE '%f9 v1.1%';


#5.List the date when the first succesful landing outcome in ground pad was acheived.
%sql SELECT MIN(Date) AS 'Date of first successful landing' FROM SPACEXTABLE WHERE Landing_Outcome LIKE '%Success (ground pad)%';


#6. List the names of the boosters which have success in drone ship and have payload mass greater than 4000 but less than 6000
%sql SELECT Booster_Version AS 'success boosters' FROM SPACEXTABLE WHERE Landing_Outcome LIKE '%Success (drone ship)%' AND PAYLOAD_MASS__KG_ > 4000 AND PAYLOAD_MASS__KG_ < 6000;


#7. List the total number of successful and failure mission outcomes
%sql SELECT DISTINCT Landing_Outcome, COUNT(Landing_Outcome) AS Frequency FROM SPACEXTABLE GROUP BY Landing_Outcome;
"""
SELECT 
    CASE 
        WHEN Landing_Outcome LIKE '%Success%' THEN 'Success Landing'
        WHEN Landing_Outcome LIKE '%Fail%' THEN 'Failed Landing'
        ELSE 'Other'
    END AS Landing_Status,
    COUNT(Landing_Outcome) AS Frequency
FROM SPACEXTBL
GROUP BY Landing_Status;
"""

#8. List the names of the booster_versions which have carried the maximum payload mass. Use a subquery
%sql SELECT Booster_Version FROM SPACEXTABLE WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTABLE);


#9. List the records which will display the month names, failure landing_outcomes in drone ship ,booster versions, launch_site for the months in year 2015.
%sql SELECT Date, Landing_Outcome, Booster_Version, Launch_Site FROM SPACEXTABLE WHERE Landing_Outcome LIKE '%Failure (drone ship)%' AND strftime('%Y', Date) = '2015';
"""
SELECT 
    CASE strftime('%m', Date)
        WHEN '01' THEN 'January'
        WHEN '02' THEN 'February'
        WHEN '03' THEN 'March'
        WHEN '04' THEN 'April'
        WHEN '05' THEN 'May'
        WHEN '06' THEN 'June'
        WHEN '07' THEN 'July'
        WHEN '08' THEN 'August'
        WHEN '09' THEN 'September'
        WHEN '10' THEN 'October'
        WHEN '11' THEN 'November'
        WHEN '12' THEN 'December'
    END AS Month,
    Booster_Version,
    Launch_Site,
    'Failure (drone ship)' AS Failure_Landing_Outcome
FROM 
    SPACEXTBL
WHERE 
    strftime('%Y', Date) = '2015' 
    AND Landing_Outcome LIKE '%Failure (drone ship)%';
"""


#10. Rank the count of landing outcomes (such as Failure (drone ship) or Success (ground pad)) between the date 2010-06-04 and 2017-03-20, in descending order.
%sql SELECT Landing_Outcome, COUNT(Landing_Outcome) AS Frequency FROM SPACEXTABLE WHERE (Landing_Outcome LIKE '%Failure (drone ship)%' OR Landing_Outcome LIKE '%Success (ground pad)%') AND Date > '2010-06-04' AND Date < '2017-03-20' GROUP BY Landing_Outcome ORDER BY Frequency DESC;

