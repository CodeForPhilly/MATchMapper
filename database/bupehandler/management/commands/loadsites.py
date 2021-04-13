from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from bupehandler.models import Sites_all
from pytz import UTC


DATETIME_FORMAT = '%m/%d/%Y'

class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('./sites_all.csv')):
            sites= Sites_all()
            #otp = Siterecs_samhsa_otp()
            #tad = Siterecs_dbhids_tad()

            print(row['site_id'])
            sites.oid = row['site_id']
            sites.samhsa_ftloc_id.sites_all_id = row['site_id']
            sites.samhsa_otp_id.sites_all_id = row['site_id']
            sites.dbhids_tad_id.sites_all_id = row['site_id']
            sites.hfp_fqhc_id.sites_all_id = row['site_id']
            sites.other_srcs_id.sites_all_id = row['site_id']

            if row['url_site'] != '':
                sites.url_site = row['url_site']
            if row['street_address'] != '':
                sites.street_address = row['street_address']
            if row['address_suppl']  !='':
                sites.address_suppl = row['address_suppl']
            if row['zip5'] != '':
                sites.zip5 = row['zip5']
            if row['name_system'] != '':
                sites.name_program = row['name_system']
            if row['name_site'] != '':
                sites.name_site = row['name_site']
            if row['mat_avail'] == '':
                sites.mat_avail = 'Unknown'
            else:
                sites.mat_avail = row['mat_avail']
            if row['mat_bupe'] == '':
                sites.mat_bupe = 'Unknown'
            else:
                sites.mat_bupe = row['mat_bupe']
            if row['mat_mtd'] == '':
                sites.mat_mtd = 'Unknown'
            else:
                sites.mat_mtd = row['mat_mtd']
            if row['mat_ntrex'] == '':
                sites.mat_ntrex = 'Unknown'
            else:
                sites.mat_ntrex = row['mat_ntrex']
            if row['fqhc'] == '':
                sites.fqhc = 'Unknown'
            if row['archival_only'] != '':
                sites.archival_only = row['archival_only']

            sites.save()
