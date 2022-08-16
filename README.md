# Natural-Amenity-Dash-Map

### Personal data science project that I host on my [personal website](http://map.israelsenlab.org).

This is an interactive choropleth map, built using Dash/Plotly, that displays various natural amenities by county for the 
contiguous United States. This map was inspired by the [USDA ERS Natural Amenities 
Scale](https://www.ers.usda.gov/data-products/natural-amenities-scale/) and displays some of the data used in the original 
study (*Natural Amenities Drive Rural Population Change*, by David A. McGranahan); both the study and original data tables can 
be found at the previous link.

The natural amenities shown on the map are environmantal factors or variables that may influence one's enjoyment of living in a 
certain location. The variables shown on the map include the following:
- USDA Natural Amenity Rank (composite score from the USDA study, including the 
following*)
	- Winter Temperature*
	- Sun in Winter*
	- Summer Temperature*
	- Summer Humidity*
	- Water Area*
	- Topographic Variation*
- Urban Influence (a measure of county population size and proximity to areas of 
high 
population, from the USDA study)
- Chance of White Christmas
 
I have thus far added an addtional data set (the probability of snow coverage on Dec 25, 
or "Chance of a White Christmas"). I plan to add additional data that interest me, such as surface water 
hardness, night sky darkness, air quality, percent tree cover, availability of public lands, etc.

### Dec 25th Data Set

Chance of White Christmas is the probability of snow depth >= 1 inch on Christmas Day, according to 1991-2020 
Climate Normals data from the NOAA NCEI. I mapped the weather station coordinates from the [raw 
data](https://www.ncei.noaa.gov/media/3501) to county 
FIPS codes using the [FCC API](https://geo.fcc.gov/api/census/) census data. I averaged the probabilities if 
more 
than one station was persent per county. Some counties had no station data, so I interpolated probabilities 
for those counties from available neighboring counties using the [US Census Bureau County 
Adjacency File](https://www.census.gov/geographies/reference-files/2010/geo/county-adjacency.html).

See my Jupyter Notebook in /white_christmas-data in this repository.

### Dash App

This is an interactive Dash app that I am currently running on AWS Elastic Beanstalk (Python 3.8).

The deployed version is in /dash-app in this repository.

### Planned Updates

I have additional improvements planned, which will occur as I have time.
- Add more data, as listed above.
- Fix issues when viewing on mobile, including:
	- Get click to work (instead of hover(?)) so that the zoom reset button works.
	- Initial map sizing on small mobile screens
- Deploy capability to combine factors of interest into a custom "natural amenity scale"
	- Use same method as in USDA paper (summation of z-scores)
 
 
