import pandas as pd
from geopy.geocoders import ArcGIS

# setup geocoder
geolocator = ArcGIS(user_agent="matchmapper")
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=0.1)

# load sites_all
sites_all = pd.read_csv('database/sites_all.csv', encoding='cp1252')

# collapse address to single vector
addresses = sites_all['street1'] + " " + sites_all['city'] + " " + sites_all['state_usa'] + " " + sites_all['zipcode'].astype(str)

# geocode
locations = addresses.apply(geocode)

# extract lat and lon and fill into sites_all
sites_all['latitude'] = locations.apply(lambda x: x.latitude)
sites_all['longitude'] = locations.apply(lambda x: x.longitude)

# write new csv
sites_all.to_csv('database/sites_all_geocoded.csv', index=False) 