# MATchMapper

## Introduction to the MATchMapper project

The project hopes to identify data-based insights regarding the opioids crisis in Philadelphia for the Health Federation of Philadelphia and the Substance Abuse and Mental Health Services Administration (SAMHSA) and develop interfaces for both patients and healthcare providers to be better informed about buprenorphine availability. We developed tools (a combination of Google Distance Matrix API and self-modified Haversine-Manhattan distance calculation algorithm) to build matrices for distance analysis between census tracts with high overdosage incidents and nearest buprenorphine providers. We also contributed to data collection, processing, and geocoding which mapped access and need for buprenorphine as the "gold standard" in medication-assisted treatment (MAT) by using Social Explorer, Python, Pandas, and GeoPandas. My biggest contribution is leading the team in building and automating the scraping process to update data for >500 healthcare providers in Philadelphia

![Full pipeline](https://github.com/samueltan97/MATchMapper/blob/master/database/Capture.JPG)

## MATchMapper end-to-end data pipeline

Using Pandas, GeoPandas, PostgreSQL, Docker, and Django, we have also developed an end-to-end data pipeline that scrapes healthcare provider data from National Provider Identifier (NPI) Registry, Pennsylvania Licensing System, etc. and directs the data through a series of preprocessing and conflict resolution process before storing them into our PostgreSQL database hosted on Linode. This allows patients and healthcare providers to access updated information regarding buprenorphine availability in their vicinity. Right now, MATchMapper is discussing with the Philadelphia Department of Public Health to get them to adopt our data pipeline before we share our data product with other states.

![Tech pipeline](https://github.com/samueltan97/MATchMapper/blob/master/database/CAPTURE.png)

## MATchMapper Entity Relationship Diagram (Truncated due to length)

![ERD](https://github.com/CodeForPhilly/MATchMapper/blob/master/database/ERD_truncated.png)

## How to use

Start virtualenv and run pipenv shell to use virtual environment. Contact the team at matchmapper.philadelphia@gmail.com to get access to the Django application and the PostgreSQL database.
