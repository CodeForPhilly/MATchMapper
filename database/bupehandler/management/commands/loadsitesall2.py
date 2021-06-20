from csv import DictReader
from datetime import datetime

from django.core.management import BaseCommand

from bupehandler.models import Sites_all,Siterecs_samhsa_otp,sites_site_recs_lookup,Siterecs_hfp_fqhc,Siterecs_samhsa_ftloc,Siterecs_dbhids_tad
from pytz import UTC

#TODO: update the csv to include why_hidden, archival only field for siterecs_samhsa_otp 
DATETIME_FORMAT = '%Y-%m-%d'

class Command(BaseCommand):
    def handle(self, *args, **options):
        for row in DictReader(open('./0607_sites_all.csv')):
            sites= Sites_all()
            #otp = Siterecs_samhsa_otp()
            #tad = Siterecs_dbhids_tad()

        #    print(row['site_id'])
            sites.oid = row['site_id']

    
            sites.id_dbhids_tad.sites_all_id = row['site_id']
            sites.id_hfp_fqhc.sites_all_id = row['site_id']
            if row['name1'] != '':
                sites.name1 = row['name1']
            if row['name2'] != '':
                sites.name2 = row['name2']
            if row['website1'] != '':
                sites.website1 = row['website1']
            if row['website2'] != '':
                sites.website2 = row['website2']
            if row['telehealth'] == '':
                sites.telehealth = 'Unclear'
            else:
                sites.telehealth = row['telehealth']
            if row['phone1'] != '':
                sites.phone1 = row['phone1']
            if row['phone2'] != '':
                sites.phone2 = row['phone2']
            if row['street1'] != '':
                sites.street1 = row['street1']
            if row['street2'] != '':
                sites.street2 = row['street2']
            if row['city'] == '':
                sites.city= 'Philadelphia'
            else:
                sites.city = row['city']
            if row['state_usa'] == '':
                sites.state_usa= 'PA'
            else:
                sites.state_usa = row['state_usa']
            if row['zipcode'] != '':
                sites.zipcode = row['zipcode']
            if row['latitude'] != '':
                sites.latitude = row['latitude']
            if row['longitude'] != '':
                sites.longitude = row['longitude']
            if row['bu'] == '':
                sites.bu = 'Unclear'
            else:
                sites.bu = row['bu']
            if row['mu'] == '':
                sites.mu = 'Unclear'
            else:
                sites.mu = row['mu']
            if row['nu'] == '':
                sites.nu = 'Unclear'
            else:
                sites.nu = row['nu']
            if row['fqhc'] == '':
                sites.fqhc = 'Unclear'
            else:
                sites.fqhc = row['fqhc']
            if row['prim_care'] == '':
                sites.prim_care = 'Unclear'
            else:
                sites.prim_care = row['prim_care']
            if row['archival_only'] != '':
                sites.archival_only = row['archival_only']
            if row['why_hidden'] == '':
                sites.why_hidden = "Data needs review" 
            else:
                sites.why_hidden = row['why_hidden']
            if row['data_review'] != '':
                sites.data_review= row['data_review']
            if row['mat_avail'] == '':
                sites.mat_avail = 'Unknown'
            else:
                sites.mat_avail = row['mat_avail']
            #sites.samhsa_otp_id.samhsa_oid = sites
            for r1 in DictReader(open('./0607_siterecs_samhsa_otp.csv')):
                if r1['site_id'] == row['site_id']:
                    #print(r1['site_id'])

                    siteotp = Siterecs_samhsa_otp()
                #    print(siteotp)

                    siteotp.oid = r1['oid']
                    #for s in sitesallid:
                    #    print(s.oid)

                    #sites.site_id.samhsa_oid = sites_all.samhsa_otp_id

                    siteotp.name_program = r1['name_program']
                    if r1['name_dba'] != '':
                        siteotp.name_dba = r1['name_dba']
                    siteotp.street = r1['address']
                    siteotp.archival_only = None 
                    siteotp.why_hidden = "Data needs review" 
                    siteotp.dba = r1['name_dba'] 
                    siteotp.data_review = r1['data_review']
                    siteotp.city = r1['city']
                    siteotp.state_usa = r1['ci']
                    siteotp.zipcode = r1['zipcode']
                    siteotp.phone = r1['phone']
                    siteotp.certification = r1['certification']
                    if r1['full_certification'] != '':
                        fdate = r1['full_certification']
                        siteotp.date_full_certification = datetime.strptime(fdate,DATETIME_FORMAT)

                    if r1['date_firstfind'] != '':
                        ffdate = r1['date_firstfind']
                        siteotp.date_firstfind = datetime.strptime(ffdate,DATETIME_FORMAT)

                    if r1['date_lastfind'] != '':
                        ldate = r1['date_lastfind']
                        siteotp.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
                    #    print(siteotp)
                    #sites.save()
                    siteotp.save()
                    sites.save()
                    siteotp.site_id.add(Sites_all.objects.get(pk=r1['site_id']))

                    sites.id_samhsa_otp.add(siteotp)

                    sites.save()
                    siteotp.save()


                else:
                    sites.save()

            for r1 in DictReader(open('./0607_siterecs_hfp_fqhc.csv')):
                if r1['site_id'] == row['site_id']:
                    print(r1['site_id'])
                    hfp = Siterecs_hfp_fqhc()
                    hfp.oid = r1['oid']
                    hfp.name_short = r1['name_short']
                    hfp.name_system = r1['name_system']
                    hfp.name_site = r1['name_site']
                    hfp.website = r1['website']
                    if r1['admin_office'] !='':
                        hfp.admin_office = r1['admin_office']
                    hfp.street1 = r1['street1']
                    hfp.steet2 = r1['street2']
                    hfp.city = r1['city']
                    hfp.state_usa = r1['state_usa']
                    hfp.zipcode = r1['zipcode']
                    hfp.phone1 = r1['phone1']
                    if r1['phone2'] != '':
                        hfp.phone2 = r1['phone2']
                    if r1['archival_only'] != '':
                        hfp.archival_only = r1['archival_only']
                    if r1['why_hidden'] == '':
                        hfp.why_hidden = "Data needs review" 
                    else:
                        hfp.why_hidden = r1['why_hidden']
                    if r1['why_hidden'] != '':
                        hfp.why_hidden = r1['why_hidden']
                    if r1['data_review'] != '':
                        hfp.data_review = r1['data_review']
                    if r1['date_firstfind'] != '':
                        fdate = r1['date_firstfind']
                        hfp.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)

                    if r1['date_lastfind'] !='':
                        ldate = r1['date_lastfind']
                        hfp.date_lastfind  = datetime.strptime(ldate,DATETIME_FORMAT)
                    sites.save()
                    hfp.save()
                    hfp.site_id.add(Sites_all.objects.get(pk=r1['site_id']))
                    sites.id_hfp_fqhc.add(hfp)
                    sites.save()
                    hfp.save()
            for r3 in DictReader(open('./0607_siterecs_dbhids_tad.csv')):
                if r3['site_id'] == row['site_id']:
                    tad = Siterecs_dbhids_tad()
                    tad.oid = r3['oid']
                    tad.name1 = r3['name1']
                    tad.street1 = r3['street1']
                    if r3['street2'] != '':
                        tad.street2 = r3['street2']
                    if r3['city'] == '':
                        tad.city= 'Philadelphia'
                    else:
                        tad.city = r3['city']
                    if r3['state_usa'] == '':
                        tad.state_usa= 'PA'
                    else:
                        tad.state_usa = r3['state_usa']
                    tad.zipcode = r3['zipcode']
                    tad.ref_address = r3['ref_address']
                    tad.phone = r3['phone']
                    tad.mat_info = r3['mat_info']
                    if r3['bu'] != '':
                        tad.bu = r3['bu']
                    if r3['bui'] != '':
                        tad.bui = r3['bui']
                    if r3['bum'] !='':
                        tad.bum = r3['bum']
                    if r3['bwn'] != '':
                        tad.bwn = r3['bwn']
                    if r3['buu'] != '':
                        tad.buu = r3['buu']
                    if r3['mu'] !='':
                        tad.mu = r3['mu']
                    if r3['mui'] != '':
                        tad.mui = r3['mui']
                    if r3['mm'] != '':
                        tad.mm = r3['mm']
                    if r3['nu'] !='':
                        tad.nu = r3['nu']
                    if r3['vti'] !='':
                        tad.vti = r3['vti']
                    if r3['vtm'] != '':
                        tad.vtm = r3['vtm']
                    if r3['vtrl'] != '':
                        tad.vtrl = r3['vtrl']
                    if r3['iop'] !='':
                        tad.iop = r3['iop']
                    if r3['op'] != '':
                        tad.op = r3['op']
                    if r3['mh_tx'] !='':
                        tad.mh_tx = r3['mh_tx']
                    if r3['wih_induction'] != '':
                        tad.wih_induction = r3['wih_induction']
                    tad.walk_in_hours = r3['walk_in_hours']
                    if r3['coe'] != '':
                        tad.coe = r3['coe']
                    if r3['other_notes'] != '':
                        tad.other_notes = r3['other_notes']
                    if r3['data_review'] != '':
                        tad.data_review = r3['data_review']
                    sites.save()
                    tad.save()
                    tad.site_id.add(Sites_all.objects.get(pk=r3['site_id']))
                    sites.id_dbhids_tad.add(tad)
                    sites.save()
                    tad.save()



            for r2 in DictReader(open('./0607_siterecs_samhsa_ftloc.csv')):
                if r2['site_id'] == row['site_id']:
                    Sam_site = Siterecs_samhsa_ftloc()
                    print(r2)

                    Sam_site.oid = r2['oid']
                    if r2['date_firstfind'] != '':
                        fdate = r2['date_firstfind']
                        Sam_site.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r2['date_lastfind']  != '':
                        ldate = r2['date_lastfind']
                        Sam_site.lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
                    if r2['name1']!= '':
                        Sam_site.name1 = r2['name1']
                    if r2['name2']!= '':
                        Sam_site.name2 = r2['name2']
                    if r2['street1'] !='':
                        Sam_site.street1 = r2['street1']
                    if r2['street2']!='':
                        Sam_site.street2 = r2['street2']
                    if r2['tele']!='':
                        Sam_site.tele= r2['tele'] 
                    if r2['city']!= '':
                        Sam_site.city = r2['city']
                    if r2['state_usa']!= '':
                        Sam_site.state_usa = r2['state_usa']
                    if r2['zip5']!='':
                        Sam_site.zipcode = r2['zip5']
                    if r2['zip4']!='':
                        Sam_site.zip4 = r2['zip4']
                    if r2['county']!='':
                        Sam_site.county = r2['county']
                    if r2['phone']!='':
                        Sam_site.phone = r2['phone']
                    Sam_site.intake1 = r2['intake1']
                    Sam_site.intake2 = r2['intake2']
                    if r2['website']!='':
                        Sam_site.website = r2['website']
                    if r2['latitude']!='':
                        Sam_site.latitude = r2['latitude']
                    if r2['longitude']!= '':
                        Sam_site.longitude = r2['longitude']
                    if r2['type_facility']:
                        Sam_site.type_facility = r2['type_facility']
                    Sam_site.tele = r2['tele']
                    Sam_site.sa = r2['sa']
                    Sam_site.dt = r2['dt']
                    Sam_site.bu = r2['bu']
                    Sam_site.bum = r2['bum']
                    Sam_site.ub = r2['ub']
                    Sam_site.bwn = r2['bwn']
                    Sam_site.bwon = r2['bwon']
                    Sam_site.bmw = r2['bmw']
                    Sam_site.beri = r2['beri']
                    Sam_site.bsdm = r2['bsdm']
                    Sam_site.db_field = r2['db_field']
                    Sam_site.bmo = r2['bmo']
                    Sam_site.mo = r2['mo']
                    Sam_site.mu = r2['mu']
                    Sam_site.meth = r2['meth']
                    Sam_site.mm = r2['mm']
                    Sam_site.mmw = r2['mmw']
                    Sam_site.dm = r2['dm']
                    Sam_site.nu = r2['nu']
                    Sam_site.un = r2['un']
                    Sam_site.vtrl = r2['vtrl']
                    Sam_site.nxn = r2['nxn']
                    Sam_site.rpn = r2['rpn']
                    Sam_site.otp = r2['otp']
                    Sam_site.omb = r2['omb']
                    Sam_site.otpa = r2['otpa']
                    Sam_site.pain = r2['pain']
                    Sam_site.ulc = r2['ulc']
                    Sam_site.moa = r2['moa']
                    Sam_site.odtx = r2['odtx']
                    Sam_site.ubn = r2['ubn']
                    Sam_site.hh = r2['hh']
                    Sam_site.noop = r2['noop']
                    Sam_site.nmoa = r2['nmoa']
                    Sam_site.cbt = r2['cbt']
                    Sam_site.dbt = r2['dbt']
                    Sam_site.saca = r2['saca']
                    Sam_site.trc = r2['trc']
                    Sam_site.rebt = r2['rebt']
                    Sam_site.smon = r2['smon']
                    Sam_site.smpd = r2['smpd']
                    Sam_site.smop = r2['smop']
                    Sam_site.hi = r2['hi']
                    Sam_site.res = r2['res']
                    Sam_site.op = r2['op']
                    Sam_site.rs = r2['rs']
                    Sam_site.rl = r2['rl']
                    Sam_site.rd = r2['rd']
                    Sam_site.od = r2['od']
                    Sam_site.odt = r2['odt']
                    Sam_site.oit = r2['oit']
                    Sam_site.ort = r2['ort']
                    Sam_site.hid = r2['hid']
                    Sam_site.hit = r2['hit']
                    Sam_site.ct = r2['ct']
                    Sam_site.gh = r2['gh']
                    Sam_site.psyh = r2['psyh']
                    Sam_site.vamc = r2['vamc']
                    Sam_site.tbg = r2['tbg']
                    Sam_site.ih = r2['ih']
                    Sam_site.stg = r2['stg']
                    Sam_site.lccg = r2['lccg']
                    Sam_site.ddf = r2['ddf']
                    Sam_site.stag = r2['stag']
                    Sam_site.stmh = r2['stmh']
                    Sam_site.stdh = r2['stdh']
                    Sam_site.hla = r2['hla']
                    Sam_site.jc = r2['jc']
                    Sam_site.carf = r2['carf']
                    Sam_site.ncqa = r2['ncqa']
                    Sam_site.coa = r2['coa']
                    Sam_site.hfap = r2['hfap']
                    Sam_site.np = r2['np']
                    Sam_site.sf = r2['sf']
                    Sam_site.md = r2['md']
                    Sam_site.mc = r2['mc']
                    Sam_site.si = r2['si']
                    Sam_site.pi_field = r2['pi_field']
                    Sam_site.mi = r2['mi']
                    Sam_site.atr = r2['atr']
                    Sam_site.fsa = r2['fsa']
                    Sam_site.ss = r2['ss']
                    Sam_site.pa = r2['pa']
                    Sam_site.ah = r2['ah']
                    Sam_site.sp = r2['sp']
                    Sam_site.co = r2['co']
                    Sam_site.gl = r2['gl']
                    Sam_site.vet = r2['vet']
                    Sam_site.adm = r2['adm']
                    Sam_site.mf = r2['mf']
                    Sam_site.cj = r2['cj']
                    Sam_site.se = r2['se']
                    Sam_site.ad = r2['ad']
                    Sam_site.pw = r2['pw']
                    Sam_site.wn = r2['wn']
                    Sam_site.mn = r2['mn']
                    Sam_site.hv = r2['hv']
                    Sam_site.trma = r2['trma']
                    Sam_site.xa = r2['xa']
                    Sam_site.dv = r2['dv']
                    Sam_site.tay = r2['tay']
                    Sam_site.nsc = r2['nsc']
                    Sam_site.adtx = r2['adtx']
                    Sam_site.bdtx = r2['bdtx']
                    Sam_site.cdtx = r2['cdtx']
                    Sam_site.mdtx = r2['mdtx']
                    Sam_site.tgd = r2['tgd']
                    Sam_site.tid = r2['tid']
                    Sam_site.ico = r2['ico']
                    Sam_site.gco = r2['gco']
                    Sam_site.fco = r2['fco']
                    Sam_site.mco = r2['mco']
                    Sam_site.twfa = r2['twfa']
                    Sam_site.bia = r2['bia']
                    Sam_site.cmi = r2['cmi']
                    Sam_site.moti = r2['moti']
                    Sam_site.ang = r2['ang']
                    Sam_site.mxm = r2['mxm']
                    Sam_site.crv = r2['crv']
                    Sam_site.relp = r2['relp']
                    Sam_site.bc = r2['bc']
                    Sam_site.chld = r2['chld']
                    Sam_site.yad = r2['yad']
                    Sam_site.adlt = r2['adlt']
                    Sam_site.fem = r2['fem']
                    Sam_site.male = r2['male']
                    Sam_site.du = r2['du']
                    Sam_site.duo = r2['duo']
                    Sam_site.acc = r2['acc']
                    Sam_site.acm = r2['acm']
                    Sam_site.acu = r2['acu']
                    Sam_site.add_field = r2['add_field']
                    Sam_site.baba = r2['baba']
                    Sam_site.ccc = r2['ccc']
                    Sam_site.cmha = r2['cmha']
                    Sam_site.csaa = r2['csaa']
                    Sam_site.daut = r2['daut']
                    Sam_site.dp = r2['dp']
                    Sam_site.dsf = r2['dsf']
                    Sam_site.dvfp = r2['dvfp']
                    Sam_site.eih = r2['eih']
                    Sam_site.emp = r2['emp']
                    Sam_site.haec = r2['haec']
                    Sam_site.heoh = r2['heoh']
                    Sam_site.hivt = r2['hivt']
                    Sam_site.isc = r2['isc']
                    Sam_site.itu = r2['itu']
                    Sam_site.mhs = r2['mhs']
                    Sam_site.mpd = r2['mpd']
                    Sam_site.opc = r2['opc']
                    Sam_site.sae = r2['sae']
                    Sam_site.shb = r2['shb']
                    Sam_site.shc = r2['shc']
                    Sam_site.shg = r2['shg']
                    Sam_site.smhd = r2['smhd']
                    Sam_site.ssa = r2['ssa']
                    Sam_site.ssd = r2['ssd']
                    Sam_site.stdt = r2['stdt']
                    Sam_site.ta = r2['ta']
                    Sam_site.taec = r2['taec']
                    Sam_site.tbs = r2['tbs']
                    Sam_site.cm = r2['cm']
                    Sam_site.fpsy = r2['fpsy']
                    Sam_site.hs = r2['hs']
                    Sam_site.nrt = r2['nrt']
                    Sam_site.peer = r2['peer']
                    Sam_site.stu = r2['stu']
                    Sam_site.tcc = r2['tcc']
                    Sam_site.pvtp = r2['pvtp']
                    Sam_site.pvtn = r2['pvtn']
                    Sam_site.vo = r2['vo']
                    Sam_site.sumh = r2['sumh']
                    Sam_site.inpe = r2['inpe']
                    Sam_site.rpe = r2['rpe']
                    Sam_site.pc = r2['pc']
                    Sam_site.naut = r2['naut']
                    Sam_site.nmaut = r2['nmaut']
                    Sam_site.acma = r2['acma']
                    Sam_site.pmat = r2['pmat']
                    Sam_site.auinpe = r2['auinpe']
                    Sam_site.aurpe = r2['aurpe']
                    Sam_site.aupc = r2['aupc']
                    Sam_site.mhiv = r2['mhiv']
                    Sam_site.mhcv = r2['mhcv']
                    Sam_site.lfxd = r2['lfxd']
                    Sam_site.clnd = r2['clnd']
                    Sam_site.copsu = r2['copsu']
                    Sam_site.daof = r2['daof']
                    Sam_site.mst = r2['mst']
                    Sam_site.noe = r2['noe']
                    Sam_site.ofd = r2['ofd']
                    Sam_site.rc = r2['rc']
                    Sam_site.piec = r2['piec']
                    Sam_site.mdet = r2['mdet']
                    Sam_site.voc = r2['voc']
                    Sam_site.hav = r2['hav']
                    Sam_site.hbv = r2['hbv']
                    Sam_site.audo = r2['audo']
                    Sam_site.f17 = r2['f17']
                    Sam_site.f19 = r2['f19']
                    Sam_site.f25 = r2['f25']
                    Sam_site.f28 = r2['f28']
                    Sam_site.f30 = r2['f30']
                    Sam_site.f31 = r2['f31']
                    Sam_site.f35 = r2['f35']
                    Sam_site.f36 = r2['f36']
                    Sam_site.f37 = r2['f37']
                    Sam_site.f4 = r2['f4']
                    Sam_site.f42 = r2['f42']
                    Sam_site.f43 = r2['f43']
                    Sam_site.f47 = r2['f47']
                    Sam_site.f66 = r2['f66']
                    Sam_site.f67 = r2['f67']
                    Sam_site.f70 = r2['f70']
                    Sam_site.f81 = r2['f81']
                    Sam_site.f92 = r2['f92']
                    Sam_site.n13 = r2['n13']
                    Sam_site.n18 = r2['n18']
                    Sam_site.n23 = r2['n23']
                    Sam_site.n24 = r2['n24']
                    print(Sam_site.n40)
                    print(r2['n40 '])
                    Sam_site.n40 = r2['n40 ']
                    sites.save()
                    Sam_site.save()
                    sites.id_samhsa_ftloc.add(Sam_site)
                    sites.save()
                    Sam_site.save()