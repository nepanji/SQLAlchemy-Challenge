# SQLAlchemy-Challenge

## Step 1 - Climate Analysis and Exploration
This step demonstrates how to use SQLAlchemy and Python to execute a basic exploration of a database.

### Precipitation Analysis
* Record the last date listed in the dataset
* Create a query to retreive the last 12 months of precipitation data and plot the results.
* Save the query results as a Pandas DataFrame
* Use Pandas Plotting with Matplotlib to plot the data
* Complete a describe to calculate the summary statistics

<img width="870" alt="Daily Precipitation" src="https://user-images.githubusercontent.com/89491352/142747183-d58356eb-29c8-4f89-b834-3ffccd44fc2e.png">

### Station Analysis
* Design a query to calculate the total number stations in the dataset
* Design a query to find the most active stations (i.e. what stations have the most rows?)
* Calculate the lowest, highest, and average temperature using the most active station
* Query the last 12 months of temperature observation data for this station
* Save the query results as a Pandas DataFrame
* Plot the results as a histogram

<img width="870" alt="Annual Temperature" src="https://user-images.githubusercontent.com/89491352/142747172-8c26b8bf-662b-41c0-8c10-15f74fbbc8c5.png">

## Step 2 - Climate App
This step demonstrates how to use Flask to design a Flask API based on the queries.
### Routes
Create flask routes that include:
* /api/v1.0/precipitation
* /api/v1.0/stations
* /api/v1.0/tobs
* /api/v1.0/<start>
* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>
