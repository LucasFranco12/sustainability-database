/* Show the number of solar panel installations up to 2015 for this municipality */
SELECT COUNT(*) AS num_installations
FROM installation
WHERE Year_Installed <= '2015-12-31'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of solar panel installations up to 2020 for this municipality */
SELECT COUNT(*) AS num_installations
FROM installation
WHERE Year_Installed <= '2020-12-31'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of residential solar panel installations for this municipality up to 2015 */
SELECT COUNT(*) AS num_residential_installations
FROM installation
WHERE Year_Installed <= '2015-12-31'
  AND Customer_Type = 'Residential'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of residential solar panel installations for this municipality up to 2020 */
SELECT COUNT(*) AS num_residential_installations
FROM installation
WHERE Year_Installed <= '2020-12-31'
  AND Customer_Type = 'Residential'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of commercial solar panel installations for this municipality up to 2015 */
SELECT COUNT(*) AS num_residential_installations
FROM installation
WHERE Year_Installed <= '2015-12-31'
  AND Customer_Type = 'Commercial'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of commercial solar panel installations for this municipality up to 2020 */
SELECT COUNT(*) AS num_residential_installations
FROM installation
WHERE Year_Installed <= '2020-12-31'
  AND Customer_Type = 'Commercial'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth';

/* Show the number of other solar panel installations for this municipality up to 2015 */
SELECT COUNT(*) AS num_other_installations
FROM installation
WHERE Year_Installed <= '2015-12-31'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth'
  AND Program != 'Residential'
  AND Program != 'Commercial';

/* Show the number of other solar panel installations for this municipality up to 2020 */
SELECT COUNT(*) AS num_other_installations
FROM installation
WHERE Year_Installed <= '2020-12-31'
  AND Municipality = 'Aberdeen township'
  AND County = 'Monmouth'
  AND Program != 'Residential'
  AND Program != 'Commercial';

/* Create table that shows the percentage of solar panel installations in regards to population up to 2015 for this municipality */
CREATE TABLE insallations_population_2015 AS
SELECT  *, COUNT(Solar_Installations.Municipality) AS Total_installations
	FROM Municipality
	WHERE Year = '2015'
    AND Municipality = 'Aberdeen township'
    AND County = 'Monmouth'
	JOIN Solar_Installations
	ON Municipality.Municipality = Solar_Installations.Municipality
	AND Solar_Installations.PTO_Date <= '2015-12-31';

/* Create table that show the percentage of solar panel installations in regards to population up to 2020 for this municipality */
CREATE TABLE insallations_population_2020 AS
SELECT  *, COUNT(Solar_Installations.Municipality) AS Total_installations
	FROM Municipality
	WHERE Year = '2020'
    AND Municipality = 'Aberdeen township'
    AND County = 'Monmouth'
	JOIN Solar_Installations
	ON Municipality.Municipality = Solar_Installations.Municipality
	AND Solar_Installations.PTO_Date <= '2020-12-31';

/* Create table that show the percentage of total MTCO2e in regards to population in 2015 for this municipality */
CREATE TABLE MTCO2e_population_2015
	SELECT *, CO2_Emissions.Total_MTCO2e
	FROM Municipality
	WHERE Year = '2015'
    AND Municipality = 'Aberdeen township'
    AND County = 'Monmouth'
	JOIN CO2_Emissions
	ON Municipality.Municipality = CO2_Emissions.Municipality
	AND CO2_Emissions.Year = '2015';

/* Create table that show the percentage of total MTCO2e in regards to population in 2015 for this municipality */
CREATE TABLE MTCO2e_population_2020
	SELECT *, CO2_Emissions.Total_MTCO2e
	FROM Municipality
	WHERE Year = '2020'
    AND Municipality = 'Aberdeen township'
    AND County = 'Monmouth'
	JOIN CO2_Emissions
	ON Municipality.Municipality = CO2_Emissions.Municipality
	AND CO2_Emissions.Year = '2020'

/* Show the total MTCO2e in 2020 for this municipality */
SELECT TOTAL_MTCO2e AS Total_CO2_2020
FROM C02_Emissions
WHERE Year_collected = '2020'
AND Municipality = 'Aberdeen township'
AND County = 'Monmouth';

/* Show the total MTCO2e in 2015 for this municipality */
SELECT TOTAL_MTCO2e AS Total_CO2_2015
FROM C02_Emissions
WHERE Year_collected = '2015'
AND Municipality = 'Aberdeen township'
AND County = 'Monmouth';
