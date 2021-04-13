from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from bupehandler.models import Siterecs_samhsa_otp, Sites_all
from pytz import UTC


DATETIME_FORMAT = '%Y-%m-%d'

class Command(BaseCommand):
    def handle(self, *args, **options):
        sites_all = Sites_all()
        if sites_all.oid == 'S00084':
            print(sites_all.oid)
        for row in DictReader(open('./sitesrecotp.csv')):
            sites = Siterecs_samhsa_otp()
            sites_all = Sites_all()
            #print(sites_all)
            sitesallid = sites_all.oid
            #print(sites_all.oid)
        #    for sit in sites_all.oid:
        #        print(sit)
            #print(sites_all.oid)

            #print(row['rec_id'])
            sites.oid = row['rec_id']
            #for s in sitesallid:
            #    print(s.oid)

                #sites.site_id.samhsa_oid = sites_all.samhsa_otp_id

            sites.name_program = row['name_program']
            if row['name_dba'] != '':
                sites.name_dba = row['name_dba']
            sites.street_address = row['address']
            sites.city = row['city']
            sites.state_usa = row['state_usa']
            sites.zipcode = row['zipcode']
            sites.phone = row['phone']
            sites.certification_status = row['certification_status']
            sites.date_full_certification = row['date_full_certification']
            if row['date_full_certification'] != '':
                fdate = row['date_full_certification']
                sites.date_full_certification = datetime.strptime(fdate,DATETIME_FORMAT)

            if row['date_firstfind'] != '':
                ffdate = row['date_firstfind']
                sites.date_firstfind = datetime.strptime(ffdate,DATETIME_FORMAT)

            if row['date_lastfind'] != '':
                ldate = row['date_lastfind']
                sites.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
            ##sites.save()
