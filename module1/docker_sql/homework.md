## Question 1. Understanding docker first run

Docker command to run python container:

    docker run -it python:3.12.8 bash

Followed by this to check the version of *pip*:

    pip --version

## Question 3. Trip Segmentation Count

During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips,  **respectively**, happened:

1.  Up to 1 mile
2.  In between 1 (exclusive) and 3 miles (inclusive),
3.  In between 3 (exclusive) and 7 miles (inclusive),
4.  In between 7 (exclusive) and 10 miles (inclusive),
5.  Over 10 miles

#### Answer queries:

1. 
~~~
SELECT COUNT(1) from green_taxi_data gtd
WHERE (CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (CAST(gtd.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (gtd.trip_distance <= 1);
~~~

2. 
~~~
SELECT COUNT(1) from green_taxi_data gtd
WHERE (CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (CAST(gtd.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (gtd.trip_distance > 1 AND gtd.trip_distance <= 3);
~~~


3. 
~~~
SELECT COUNT(1) from green_taxi_data gtd
WHERE (CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (CAST(gtd.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (gtd.trip_distance > 3 AND gtd.trip_distance <= 7);
~~~

4. 
~~~
SELECT COUNT(1) from green_taxi_data gtd
WHERE (CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (CAST(gtd.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (gtd.trip_distance > 7 AND gtd.trip_distance <= 10);
~~~

5. 
~~~
SELECT COUNT(1) from green_taxi_data gtd
WHERE (CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (CAST(gtd.lpep_dropoff_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31')
	AND (gtd.trip_distance > 10);
~~~


## Question 4. Longest trip for each day


Which was the pick up day with the longest trip distance? Use the pick up time for your calculations.

Tip: For every day, we only care about one single trip with the longest distance.

-   2019-10-11
-   2019-10-24
-   2019-10-26
-   2019-10-31

#### Answer:

~~~
SELECT MAX(gtd.trip_distance), CAST(gtd.lpep_pickup_datetime AS DATE) as pu from green_taxi_data gtd
GROUP BY pu
ORDER BY 1 DESC
LIMIT 1;
~~~

## Question 5. Three biggest pickup zones

Which were the top pickup locations with over 13,000 in  `total_amount`  (across all trips) for 2019-10-18?

Consider only  `lpep_pickup_datetime`  when filtering by date.

#### Answer:

~~~
SELECT tz."Zone", SUM(gtd.total_amount) FROM green_taxi_data gtd
JOIN taxi_zones tz
ON gtd."PULocationID" = tz."LocationID"
WHERE CAST(gtd.lpep_pickup_datetime as date) = '2019-10-18'
GROUP BY 1
ORDER BY 2 DESC;
~~~

## Question 6. Largest tip

For the passengers picked up in October 2019 in the zone named "East Harlem North" which was the drop off zone that had the largest tip?

Note: it's  `tip`  , not  `trip`

We need the name of the zone, not the ID.

#### Answer:

~~~
SELECT 
    tzd."Zone" AS DropoffZone, 
    gtd.tip_amount AS TipAmount
FROM 
    green_taxi_data gtd
JOIN 
    taxi_zones tzp ON gtd."PULocationID" = tzp."LocationID"
JOIN 
    taxi_zones tzd ON gtd."DOLocationID" = tzd."LocationID"
WHERE 
    tzp."Zone" = 'East Harlem North'
    AND CAST(gtd.lpep_pickup_datetime AS DATE) BETWEEN '2019-10-01' AND '2019-10-31'
ORDER BY 
    gtd.tip_amount DESC
LIMIT 1;
~~~