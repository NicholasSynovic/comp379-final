# COMP 379 Final Project Report

> Written by Nicholas Synovic, Emmanuel Amobi, Zac Neuhardt, Brian Nguyen, and Jake Palmer

## Table of Contents

- [COMP 379 Final Project Report](#comp-379-final-project-report)
  - [Table of Contents](#table-of-contents)
  - [Goal](#goal)
  - [Team Contributions](#team-contributions)
  - [Background](#background)
  - [Data Preperation](#data-preperation)
  - [Clustering or Classification](#clustering-or-classification)
    - [Feature Importance with Random Forest Modeling](#feature-importance-with-random-forest-modeling)
      - [Discovery](#discovery)
  - [Clustering](#clustering)
    - [Elbow Method](#elbow-method)
  - [Conclusion](#conclusion)

## Goal

Cluster analysis of what features best determine if an incident resulted in an arrest or not. Goal is to find interesting relationships between features and labels

## Team Contributions

- Brian Nguyen - Feature importance using a random forest model to determine what features would result in the best labels. Meant to prove that clustering is the proper way of analyzing this dataset because none of the features of predictive of the labels in question
- Jacob Palmer - Preprocessing the dataset to reduce the feature set. Turning descriptive data into quantifiable values. Has a CSV to convert descriptions into digits
- Emmanel Amobi - Taking different features and creating clusters using K-means. This gets multiple different clustsers to present
- Zac Neuhardt - Correlating crimes across community areas. Clustering with K-means
- Nicholas Synovic - Working on the report and presentation

## Background

## Data Preperation

1. Removing redundant columns
a. Location
i. Can be removed as it serves as a combination of the Latitude and Longitude
b. Year
i. 2021 is the only year listed, therefore can be removed
c. Case Number
i. Arbitrary tracking key value, not indicative feature of the dataset
d. ID
i. Same as Case Number
e. Block
i. Information might be too correlated to features like beat, district
ii. X and Y coordinates/Longitude and Latitude are more effective and require less data preprocessing to be viable
f. Updated On
i. Not a value indicative of the crime therefore not valuable to assessment of the crime
2. Columns Included
a. IUCR -> Illinois Uniform Crime Reporting code
i. Approx. 410 unique IUCR
ii. Feature Column includes letters and numbers, requires transformation into quantitative data
iii. Consider summing these columns into simpler categories, which are highly similar to that of the Primary Type category, such as below:
iv. https://data.cityofchicago.org/Public-Safety/Chicago-Police-Department-Illinois-Uniform-Crime-R/c7ck-438e

![quantifiedIUCRCodes](assets/images/dataPreperation/quantifiedIUCRCodes.png)

b. Primary Type
i. Summarized qualitative data of the IUCR report.
ii. Data contains ~31 different Primary Types
iii. Requires quantifying

![quantifiedPrimaryType](assets/images/dataPreperation/quantifiedPrimaryType.png)

1. Location Description
a. 125 distinct quantitative descriptions of where incident occurred
b. Requires quantifying
2. Arrest
a. Boolean value indicating whether an arrest was made or not
b. Set arrest occurred to 1 and not occurred to 0
3. Domestic
a. Indicates whether the incident was domestic-related as defined by the Illinois domestic violence act using
b. Set domestic-related occurrences (True) to 1 and otherwise (false) to 0
4. Beat/District/Ward/Community Area/X and Y/Latitude and Longitude
a. Beat -> smallest geographic unit of police distributive breakdown
b. District -> larger geographic breakdown of police (22 districts in Chicago)
c. Ward -> area broken up by city council districts
   i. Map: https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Wards-2015-/sp34-6z76
d. Community Area -> designated “community areas” of Chicago, broken up into a total of 77 community areas
   i. Community Area boundaries are not political (not susceptible to redistricting or red-lining/gerrymandering), so very consistent for long term collection and analysis.
   ii. https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Community-Areas-current-/cauq-8yn6
e. X and Y -> X and Y coordinates of the location where the incident occurred as mapped to the State Plane Illinois East NAD 1983 projection (basically an isolated Latitude Longitude for the City of Chicago).
   i. Partial reprojection of actual location occurs to redact exact location of incident. Reprojection done to the center of the nearest block.
f. Latitude and Longitude -> Global latitude and longitude of incident location
   i. Partial reprojection of the actual location occurs to redact exact location of incident. Reprojection done to the center of the nearest block.
g. FBI Codes
   i. Crime classification as outlined in the FBI’s National Incident-Based Reporting System.
   ii. Text-data format
   iii. Contains 26 unique FBI codes, similar in meaning to that of the Primary Type column
Recommended Column Usages
• Primary Type
◦ Mapped randomly to an arbitrary range of quantifiable values based on their distinct counts
◦ Utilize a translation table to transform data
• Location Description
◦ Mapped randomly to an arbitrary range of quantifiable values based on their distinct counts
◦ Utilize a translation table to transform data
• Domestic
◦ Boolean value true or false mapped to 1 (True) or 0 (False)
• Arrest
◦ Boolean value true or false mapped to 1 (True) or 0 (False)
• Location Column
◦ Use Community Area identifier
   ▪ No data transformation necessary, each community area corresponds to a number between 1 and 77

In order to better visualize what I was discussing today and our justification for dropping certain features, I created a pairwise correlation analysis matrix. Basically, it shows the correlation values between different features. If they are heavily correlated, it just means that the features are essentially linked and therefore it is redundant to have both. For instance, a good example is Latitude and Y-coordinate (and vice versa with X and longitude). They both have a correlation value of 1.0 which is essentially completely linked features, which is expected as the x-y coordinates are essentially remapped latitude and longitude. It also shows, as we agreed, to drop either beat or district, as they also have a 1.0 correlation value. I think for the final dataset, I'll go ahead and keep District and Community Area as they dont seem to be that correlated so could be interesting to see what's up there. Further, as we expected, the FBI code is heavily correlated with the Primary Type (since they pretty much say the same thing) so I'd say since our scope is just Chicago, we should remove the FBI code.

![Processed Data Pairwise Coorelation](Processed%20Data%20Pairwise%20Coorelation%20Matrix.png)

I went ahead and converted pretty much all the columns I could to a quantifiable integer value and will upload that file with less columns dropped incase anyone wants to mess around with it. For the simplified dataset, I will go ahead and drop the columns we discussed. I did, however, format the date to be a readable format and separated it into Date_day (day of the year out of 365), Date,month, Date_week (out of the year), Date_hour, Date_minute, and Date_dayofweek (Monday - Sunday mapped to integer values). I'll likely remove the Date_week as it essentially says the same thing as Date_month, as seen in the correlation matrix.

My idea here was to create a more simplified dataset that you all can just use as well as provide you with one that has more columns that might turn out to be fruitful incase you want to mess around with that too. I'm going to run a few more tests then I should have these csvs and python scripts uploaded tonight. Let me know if yall have any questions in the meantime!

## Clustering or Classification

### Feature Importance with Random Forest Modeling

#### Discovery

## Clustering

### Elbow Method

## Conclusion
