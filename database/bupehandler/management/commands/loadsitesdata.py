from csv import DictReader
from datetime import datetime
from django.core.management import BaseCommand

# C:\Users\Samuel\PycharmProjects\MATchMapper\database\bupehandler\management\commands> python ..\..\..\manage.py loadsitesdata


""" Removed from above list: sites_site_recs_lookup ... if needed, use new names from models.py: 
    Lookup_siterecs_samhsa_otp      WAS sites_site_recs_lookup
    Lookup_siterecs_samhsa_ftloc    WAS Sites_ftloc
    Lookup_siterecs_dbhids_tad      WAS Siterecs_dbhids_sites_all_lookup
    Lookup_ba_dbhids_tad            NEW
    Lookup_siterecs_hfp_fqhc        WAS Siterecs_hfp_fqhc_sites_all_lookup
    Lookup_siterecs_other_srcs      WAS sitesrecs_other_srcs_sitesall_lk
"""
from pytz import UTC

from bupehandler.models import Sites_all, Siterecs_samhsa_ftloc, Siterecs_dbhids_tad, Siterecs_hfp_fqhc, Siterecs_samhsa_otp, Siterecs_other_srcs, Ba_dbhids_tad, Sitecodes_samhsa_ftloc

DATETIME_FORMAT = '%Y-%m-%d'

""" Load Sites_all with row & sites (as before), then
        Siterecs_samhsa_ftloc with r2 & ftl, 
        Siterecs_samhsa_otp with r3 & otp, 
        Siterecs_dbhids_tad with r4 & tad, 
        Ba_dbhids_tad with r5 & ba, 
        Siterecs_hfp_fqhc with r6 & hfp, 
        Siterecs_other_srcs with r7 & oth, and 
    DIFFERENT ENTITY: Sitecodes_samhsa_ftloc with sc & codes
"""

class Command(BaseCommand):
    
    def handle(self, *args, **options):

        for row in DictReader(open('./0729_sites_all.csv', encoding='utf-8-sig')):
            sites = Sites_all()
            sites.oid = 'S' + str(row['oid']).zfill(5)
            # sites.id_dbhids_tad.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            # sites.id_hfp_fqhc.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_samhsa_ftloc'] != '':
                sites.id_samhsa_ftloc.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_dbhids_tad'] != '':
                sites.id_dbhids_tad.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_ba_tad'] != '':
                sites.id_ba_tad.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_samhsa_otp'] != '':
                sites.id_samhsa_otp.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_hfp_fqhc'] != '':
                sites.id_hfp_fqhc.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            if row['id_other_srcs'] != '':
                sites.id_other_srcs.sites_all_id = 'S' + str(row['oid']).zfill(5) 
            sites.name1 = row['name1']
            if row['name2'] != '':
                sites.name2 = row['name2']
            if row['name3'] != '':
                sites.name3 = row['name3']
            if row['website1'] != '':
                sites.website1 = row['website1']
            if row['website2'] != '':
                sites.website2 = row['website2']
            if row['phone1'] != '':
                sites.phone1 = row['phone1']
            if row['phone2'] != '':
                sites.phone2 = row['phone2']
            if row['phone3'] != '':
                sites.phone3 = row['phone3']
            if row['street1'] != '':
                sites.street1 = row['street1']
            if row['street2'] != '':
                sites.street2 = row['street2']
            sites.city = row['city']
            sites.state_usa = row['state_usa']
            if row['zipcode'] != '':
                sites.zipcode = row['zipcode']
            if row['latitude'] != '':
                sites.latitude = row['latitude']
            if row['longitude'] != '':
                sites.longitude = row['longitude']
            if row['bu'] != '':
                sites.bu = row['bu']
            else:
                sites.bu = 'Unclear'
            if row['nu'] != '':
                sites.nu = row['nu']
            else:
                sites.nu = 'Unclear'
            if row['mu'] != '':
                sites.mu = row['mu']
            else:
                sites.mu = 'No'
            if row['otp'] != '':
                sites.otp = row['otp']
            else:
                sites.otp = 'No'
            if row['mat_avail'] != '':
                sites.mat_avail = row['mat_avail']
            else:
                sites.mat_avail = 'Unclear'
            if row['asm'] != '':
                sites.asm = row['asm']
            else:
                sites.asm = 'Unclear'
            if row['ba'] != '':
                sites.ba = row['ba']
            else:
                sites.ba = 'No'
            if row['ref_notes'] != '':
                sites.ref_notes = row['ref_notes']
            if row['hh'] != '':
                sites.hh = row['hh']
            if row['hwm'] != '':
                sites.hwm = row['hwm']
            if row['rhl'] != '':
                sites.rhl = row['rhl']
            if row['rhs'] != '':
                sites.rhs = row['rhs']
            if row['wm'] != '':
                sites.wm = row['wm']
            if row['uo'] != '':
                sites.uo = row['uo']
            if row['fqhc'] != '':  ## Update default from Unclear to No in models.py (2x)
                sites.fqhc = row['fqhc']
            else:
                sites.fqhc = 'No'
            if row['prim_care'] != '':
                sites.prim_care = row['prim_care']
            else:
                sites.prim_care = 'Unclear'
            if row['telehealth'] != '':
                sites.telehealth = row['telehealth']
            else:
                sites.telehealth = 'Unclear'
            if row['md'] != '':
                sites.md = row['md']
            else:
                sites.md = 'Unclear'
            if row['mc'] != '':
                sites.mc = row['mc']
            else:
                sites.mc = 'Unclear'
            if row['oi'] != '':
                sites.oi = row['oi']
            else:
                sites.oi ='Unclear' 
            if row['pa'] != '':
                sites.pa = row['pa']
            else:
                sites.pa = 'Unclear'
            if row['oit'] != '':
                sites.oit = row['oit']
            else:
                sites.oit = 'Unclear'
            if row['op'] != '':
                sites.op = row['op']
            else:
                sites.op = 'Unclear'
            if row['ta'] != '':
                sites.ta = row['ta']
            else:
                sites.ta = 'Unclear'
            if row['hs'] != '':
                sites.hs = row['hs']
            else:
                sites.hs = 'Unclear'
            if row['mhs'] != '':
                sites.mhs = row['mhs']
            else:
                sites.mhs = 'Unclear'
            if row['ccc'] != '':
                sites.ccc = row['ccc']
            else:
                sites.ccc = 'Unclear'
            if row['dvh'] != '':
                sites.dvh = row['dvh']
            else:
                sites.dvh = 'Unclear'
            if row['pw'] != '':
                sites.pw = row['pw']
            else:
                sites.pw = 'Unclear'
            if row['ad'] != '':
                sites.ad = row['ad']
            else:
                sites.ad = 'Unclear'
            if row['se'] != '':
                sites.se = row['se']
            else:
                sites.se = 'Unclear'
            if row['gl'] != '':
                sites.gl = row['gl']
            else:
                sites.gl = 'Unclear'
            if row['sp'] != '':
                sites.sp = row['sp']
            else:
                sites.sp = 'Unclear'
            if row['ah'] != '':
                sites.ah = row['ah']
            else:
                sites.ah = 'Unclear'
            if row['fem'] != '':
                sites.fem = row['fem']
            else:
                sites.fem = 'Yes'
            if row['male'] != '':
                sites.male = row['male']
            else:
                sites.male = 'Yes'
            sites.archival_only = row['archival_only']
            if row['why_hidden'] != '':
                sites.why_hidden = row['why_hidden']
            if row['data_review'] != '':
                sites.data_review = row['data_review']

        ## Siterecs_samhsa_ftloc with r2 & ftl
            for r2 in DictReader(open('./0729_siterecs_samhsa_ftloc.csv', encoding='utf-8-sig')):
                if r2['site_id'] == 'S' + str(row['oid']).zfill(5):
                    ftl = Siterecs_samhsa_ftloc()
                    ftl.oid = r2['oid']
                    if r2['mat_misc'] != '':
                        ftl.mat_misc = r2['mat_misc']
                    if r2['mat_avail'] != '':
                        ftl.mat_avail = r2['mat_avail']
                    if r2['oi'] != '':
                        ftl.oi = r2['oi']
                    if r2['dvh'] != '':
                        ftl.dvh = r2['dvh']
                    ftl.archival_only = r2['archival_only']
                    if r2['why_hidden'] != '':
                        ftl.why_hidden = r2['why_hidden']
                    if r2['date_firstfind'] != '':
                        fdate = r2['date_firstfind']
                        ftl.date_firstfind = datetime.strptime(fdate,'%d-%m-%y')
                    if r2['date_lastfind'] != '':
                        ldate = r2['date_lastfind']
                        ftl.date_lastfind = datetime.strptime(ldate,'%d-%m-%y')
                    ftl.name1 = r2['name1']
                    if r2['name2'] != '':
                        ftl.name2 = r2['name2']
                    ftl.street1 = r2['street1']
                    if r2['street2'] != '':
                        ftl.street2 = r2['street2']
                    ftl.city = r2['city']
                    ftl.state_usa = r2['state_usa']
                    ftl.zip5 = r2['zip5'] ## Update models.py: remove blank=True on zip5
                    if r2['zip4'] != '':
                        ftl.zip4 = r2['zip4']
                    ftl.county = r2['county']
                    ftl.phone = r2['phone']
                    if r2['intake_prompt'] != '': ## Update models.py: add blank=True for intake_prompt
                        ftl.intake_prompt = r2['intake_prompt']
                    if r2['intake1'] != '':
                        ftl.intake1 = r2['intake1']
                    if r2['intake2'] != '':
                        ftl.intake2 = r2['intake2']
                    if r2['website'] != '': ## Update models.py: add blank=True for website
                        ftl.website = r2['website']
                    ftl.latitude = r2['latitude']
                    ftl.longitude = r2['longitude']
                    ftl.type_facility = r2['type_facility']
                    ## Auto-concatenated list of 222 :)
                    if r2['sa'] != '':
                        ftl.sa = r2['sa']
                    if r2['dt'] != '':
                        ftl.dt = r2['dt']
                    if r2['mm'] != '':
                        ftl.mm = r2['mm']
                    if r2['mmw'] != '':
                        ftl.mmw = r2['mmw']
                    if r2['dm'] != '':
                        ftl.dm = r2['dm']
                    if r2['bum'] != '':
                        ftl.bum = r2['bum']
                    if r2['bmw'] != '':
                        ftl.bmw = r2['bmw']
                    if r2['db_field'] != '':
                        ftl.db_field = r2['db_field']
                    if r2['rpn'] != '':
                        ftl.rpn = r2['rpn']
                    if r2['bu'] != '':
                        ftl.bu = r2['bu']
                    if r2['nxn'] != '':
                        ftl.nxn = r2['nxn']
                    if r2['vtrl'] != '':
                        ftl.vtrl = r2['vtrl']
                    if r2['meth'] != '':
                        ftl.meth = r2['meth']
                    if r2['hh'] != '':
                        ftl.hh = r2['hh']
                    if r2['noop'] != '':
                        ftl.noop = r2['noop']
                    if r2['pain'] != '':
                        ftl.pain = r2['pain']
                    if r2['nmoa'] != '':
                        ftl.nmoa = r2['nmoa']
                    if r2['moa'] != '':
                        ftl.moa = r2['moa']
                    if r2['ubn'] != '':
                        ftl.ubn = r2['ubn']
                    if r2['otpa'] != '':
                        ftl.otpa = r2['otpa']
                    if r2['otp'] != '':
                        ftl.otp = r2['otp']
                    if r2['cbt'] != '':
                        ftl.cbt = r2['cbt']
                    if r2['dbt'] != '':
                        ftl.dbt = r2['dbt']
                    if r2['tele'] != '':
                        ftl.tele = r2['tele']
                    if r2['saca'] != '':
                        ftl.saca = r2['saca']
                    if r2['trc'] != '':
                        ftl.trc = r2['trc']
                    if r2['rebt'] != '':
                        ftl.rebt = r2['rebt']
                    if r2['smon'] != '':
                        ftl.smon = r2['smon']
                    if r2['smpd'] != '':
                        ftl.smpd = r2['smpd']
                    if r2['smop'] != '':
                        ftl.smop = r2['smop']
                    if r2['hi'] != '':
                        ftl.hi = r2['hi']
                    if r2['res'] != '':
                        ftl.res = r2['res']
                    if r2['op'] != '':
                        ftl.op = r2['op']
                    if r2['rs'] != '':
                        ftl.rs = r2['rs']
                    if r2['rl'] != '':
                        ftl.rl = r2['rl']
                    if r2['rd'] != '':
                        ftl.rd = r2['rd']
                    if r2['od'] != '':
                        ftl.od = r2['od']
                    if r2['omb'] != '':
                        ftl.omb = r2['omb']
                    if r2['odt'] != '':
                        ftl.odt = r2['odt']
                    if r2['oit'] != '':
                        ftl.oit = r2['oit']
                    if r2['ort'] != '':
                        ftl.ort = r2['ort']
                    if r2['hid'] != '':
                        ftl.hid = r2['hid']
                    if r2['hit'] != '':
                        ftl.hit = r2['hit']
                    if r2['ct'] != '':
                        ftl.ct = r2['ct']
                    if r2['gh'] != '':
                        ftl.gh = r2['gh']
                    if r2['psyh'] != '':
                        ftl.psyh = r2['psyh']
                    if r2['vamc'] != '':
                        ftl.vamc = r2['vamc']
                    if r2['tbg'] != '':
                        ftl.tbg = r2['tbg']
                    if r2['ih'] != '':
                        ftl.ih = r2['ih']
                    if r2['stg'] != '':
                        ftl.stg = r2['stg']
                    if r2['lccg'] != '':
                        ftl.lccg = r2['lccg']
                    if r2['ddf'] != '':
                        ftl.ddf = r2['ddf']
                    if r2['stag'] != '':
                        ftl.stag = r2['stag']
                    if r2['stmh'] != '':
                        ftl.stmh = r2['stmh']
                    if r2['stdh'] != '':
                        ftl.stdh = r2['stdh']
                    if r2['hla'] != '':
                        ftl.hla = r2['hla']
                    if r2['jc'] != '':
                        ftl.jc = r2['jc']
                    if r2['carf'] != '':
                        ftl.carf = r2['carf']
                    if r2['ncqa'] != '':
                        ftl.ncqa = r2['ncqa']
                    if r2['coa'] != '':
                        ftl.coa = r2['coa']
                    if r2['hfap'] != '':
                        ftl.hfap = r2['hfap']
                    if r2['np'] != '':
                        ftl.np = r2['np']
                    if r2['sf'] != '':
                        ftl.sf = r2['sf']
                    if r2['md'] != '':
                        ftl.md = r2['md']
                    if r2['mc'] != '':
                        ftl.mc = r2['mc']
                    if r2['si'] != '':
                        ftl.si = r2['si']
                    if r2['pi_field'] != '':
                        ftl.pi_field = r2['pi_field']
                    if r2['mi'] != '':
                        ftl.mi = r2['mi']
                    if r2['atr'] != '':
                        ftl.atr = r2['atr']
                    if r2['fsa'] != '':
                        ftl.fsa = r2['fsa']
                    if r2['ss'] != '':
                        ftl.ss = r2['ss']
                    if r2['pa'] != '':
                        ftl.pa = r2['pa']
                    if r2['ah'] != '':
                        ftl.ah = r2['ah']
                    if r2['sp'] != '':
                        ftl.sp = r2['sp']
                    if r2['co'] != '':
                        ftl.co = r2['co']
                    if r2['gl'] != '':
                        ftl.gl = r2['gl']
                    if r2['vet'] != '':
                        ftl.vet = r2['vet']
                    if r2['adm'] != '':
                        ftl.adm = r2['adm']
                    if r2['mf'] != '':
                        ftl.mf = r2['mf']
                    if r2['cj'] != '':
                        ftl.cj = r2['cj']
                    if r2['se'] != '':
                        ftl.se = r2['se']
                    if r2['ad'] != '':
                        ftl.ad = r2['ad']
                    if r2['pw'] != '':
                        ftl.pw = r2['pw']
                    if r2['wn'] != '':
                        ftl.wn = r2['wn']
                    if r2['mn'] != '':
                        ftl.mn = r2['mn']
                    if r2['hv'] != '':
                        ftl.hv = r2['hv']
                    if r2['trma'] != '':
                        ftl.trma = r2['trma']
                    if r2['xa'] != '':
                        ftl.xa = r2['xa']
                    if r2['dv'] != '':
                        ftl.dv = r2['dv']
                    if r2['tay'] != '':
                        ftl.tay = r2['tay']
                    if r2['nsc'] != '':
                        ftl.nsc = r2['nsc']
                    if r2['adtx'] != '':
                        ftl.adtx = r2['adtx']
                    if r2['bdtx'] != '':
                        ftl.bdtx = r2['bdtx']
                    if r2['cdtx'] != '':
                        ftl.cdtx = r2['cdtx']
                    if r2['mdtx'] != '':
                        ftl.mdtx = r2['mdtx']
                    if r2['odtx'] != '':
                        ftl.odtx = r2['odtx']
                    if r2['tgd'] != '':
                        ftl.tgd = r2['tgd']
                    if r2['tid'] != '':
                        ftl.tid = r2['tid']
                    if r2['ico'] != '':
                        ftl.ico = r2['ico']
                    if r2['gco'] != '':
                        ftl.gco = r2['gco']
                    if r2['fco'] != '':
                        ftl.fco = r2['fco']
                    if r2['mco'] != '':
                        ftl.mco = r2['mco']
                    if r2['twfa'] != '':
                        ftl.twfa = r2['twfa']
                    if r2['bia'] != '':
                        ftl.bia = r2['bia']
                    if r2['cmi'] != '':
                        ftl.cmi = r2['cmi']
                    if r2['moti'] != '':
                        ftl.moti = r2['moti']
                    if r2['ang'] != '':
                        ftl.ang = r2['ang']
                    if r2['mxm'] != '':
                        ftl.mxm = r2['mxm']
                    if r2['crv'] != '':
                        ftl.crv = r2['crv']
                    if r2['relp'] != '':
                        ftl.relp = r2['relp']
                    if r2['bc'] != '':
                        ftl.bc = r2['bc']
                    if r2['chld'] != '':
                        ftl.chld = r2['chld']
                    if r2['yad'] != '':
                        ftl.yad = r2['yad']
                    if r2['adlt'] != '':
                        ftl.adlt = r2['adlt']
                    if r2['fem'] != '':
                        ftl.fem = r2['fem']
                    if r2['male'] != '':
                        ftl.male = r2['male']
                    if r2['bmo'] != '':
                        ftl.bmo = r2['bmo']
                    if r2['mo'] != '':
                        ftl.mo = r2['mo']
                    if r2['du'] != '':
                        ftl.du = r2['du']
                    if r2['duo'] != '':
                        ftl.duo = r2['duo']
                    if r2['acc'] != '':
                        ftl.acc = r2['acc']
                    if r2['acm'] != '':
                        ftl.acm = r2['acm']
                    if r2['acu'] != '':
                        ftl.acu = r2['acu']
                    if r2['add_field'] != '':
                        ftl.add_field = r2['add_field']
                    if r2['baba'] != '':
                        ftl.baba = r2['baba']
                    if r2['ccc'] != '':
                        ftl.ccc = r2['ccc']
                    if r2['cmha'] != '':
                        ftl.cmha = r2['cmha']
                    if r2['csaa'] != '':
                        ftl.csaa = r2['csaa']
                    if r2['daut'] != '':
                        ftl.daut = r2['daut']
                    if r2['dp'] != '':
                        ftl.dp = r2['dp']
                    if r2['dsf'] != '':
                        ftl.dsf = r2['dsf']
                    if r2['dvfp'] != '':
                        ftl.dvfp = r2['dvfp']
                    if r2['eih'] != '':
                        ftl.eih = r2['eih']
                    if r2['emp'] != '':
                        ftl.emp = r2['emp']
                    if r2['haec'] != '':
                        ftl.haec = r2['haec']
                    if r2['heoh'] != '':
                        ftl.heoh = r2['heoh']
                    if r2['hivt'] != '':
                        ftl.hivt = r2['hivt']
                    if r2['isc'] != '':
                        ftl.isc = r2['isc']
                    if r2['itu'] != '':
                        ftl.itu = r2['itu']
                    if r2['mhs'] != '':
                        ftl.mhs = r2['mhs']
                    if r2['mpd'] != '':
                        ftl.mpd = r2['mpd']
                    if r2['opc'] != '':
                        ftl.opc = r2['opc']
                    if r2['sae'] != '':
                        ftl.sae = r2['sae']
                    if r2['shb'] != '':
                        ftl.shb = r2['shb']
                    if r2['shc'] != '':
                        ftl.shc = r2['shc']
                    if r2['shg'] != '':
                        ftl.shg = r2['shg']
                    if r2['smhd'] != '':
                        ftl.smhd = r2['smhd']
                    if r2['ssa'] != '':
                        ftl.ssa = r2['ssa']
                    if r2['ssd'] != '':
                        ftl.ssd = r2['ssd']
                    if r2['stdt'] != '':
                        ftl.stdt = r2['stdt']
                    if r2['ta'] != '':
                        ftl.ta = r2['ta']
                    if r2['taec'] != '':
                        ftl.taec = r2['taec']
                    if r2['tbs'] != '':
                        ftl.tbs = r2['tbs']
                    if r2['cm'] != '':
                        ftl.cm = r2['cm']
                    if r2['fpsy'] != '':
                        ftl.fpsy = r2['fpsy']
                    if r2['hs'] != '':
                        ftl.hs = r2['hs']
                    if r2['nrt'] != '':
                        ftl.nrt = r2['nrt']
                    if r2['peer'] != '':
                        ftl.peer = r2['peer']
                    if r2['stu'] != '':
                        ftl.stu = r2['stu']
                    if r2['tcc'] != '':
                        ftl.tcc = r2['tcc']
                    if r2['bsdm'] != '':
                        ftl.bsdm = r2['bsdm']
                    if r2['nu'] != '':
                        ftl.nu = r2['nu']
                    if r2['mu'] != '':
                        ftl.mu = r2['mu']
                    if r2['bwn'] != '':
                        ftl.bwn = r2['bwn']
                    if r2['bwon'] != '':
                        ftl.bwon = r2['bwon']
                    if r2['ub'] != '':
                        ftl.ub = r2['ub']
                    if r2['un'] != '':
                        ftl.un = r2['un']
                    if r2['beri'] != '':
                        ftl.beri = r2['beri']
                    if r2['pvtp'] != '':
                        ftl.pvtp = r2['pvtp']
                    if r2['pvtn'] != '':
                        ftl.pvtn = r2['pvtn']
                    if r2['vo'] != '':
                        ftl.vo = r2['vo']
                    if r2['sumh'] != '':
                        ftl.sumh = r2['sumh']
                    if r2['inpe'] != '':
                        ftl.inpe = r2['inpe']
                    if r2['rpe'] != '':
                        ftl.rpe = r2['rpe']
                    if r2['pc'] != '':
                        ftl.pc = r2['pc']
                    if r2['naut'] != '':
                        ftl.naut = r2['naut']
                    if r2['nmaut'] != '':
                        ftl.nmaut = r2['nmaut']
                    if r2['acma'] != '':
                        ftl.acma = r2['acma']
                    if r2['pmat'] != '':
                        ftl.pmat = r2['pmat']
                    if r2['auinpe'] != '':
                        ftl.auinpe = r2['auinpe']
                    if r2['aurpe'] != '':
                        ftl.aurpe = r2['aurpe']
                    if r2['aupc'] != '':
                        ftl.aupc = r2['aupc']
                    if r2['ulc'] != '':
                        ftl.ulc = r2['ulc']
                    if r2['mhiv'] != '':
                        ftl.mhiv = r2['mhiv']
                    if r2['mhcv'] != '':
                        ftl.mhcv = r2['mhcv']
                    if r2['lfxd'] != '':
                        ftl.lfxd = r2['lfxd']
                    if r2['clnd'] != '':
                        ftl.clnd = r2['clnd']
                    if r2['copsu'] != '':
                        ftl.copsu = r2['copsu']
                    if r2['daof'] != '':
                        ftl.daof = r2['daof']
                    if r2['mst'] != '':
                        ftl.mst = r2['mst']
                    if r2['noe'] != '':
                        ftl.noe = r2['noe']
                    if r2['ofd'] != '':
                        ftl.ofd = r2['ofd']
                    if r2['rc'] != '':
                        ftl.rc = r2['rc']
                    if r2['piec'] != '':
                        ftl.piec = r2['piec']
                    if r2['mdet'] != '':
                        ftl.mdet = r2['mdet']
                    if r2['voc'] != '':
                        ftl.voc = r2['voc']
                    if r2['hav'] != '':
                        ftl.hav = r2['hav']
                    if r2['hbv'] != '':
                        ftl.hbv = r2['hbv']
                    if r2['audo'] != '':
                        ftl.audo = r2['audo']
                    if r2['f17'] != '':
                        ftl.f17 = r2['f17']
                    if r2['f19'] != '':
                        ftl.f19 = r2['f19']
                    if r2['f25'] != '':
                        ftl.f25 = r2['f25']
                    if r2['f28'] != '':
                        ftl.f28 = r2['f28']
                    if r2['f30'] != '':
                        ftl.f30 = r2['f30']
                    if r2['f31'] != '':
                        ftl.f31 = r2['f31']
                    if r2['f35'] != '':
                        ftl.f35 = r2['f35']
                    if r2['f36'] != '':
                        ftl.f36 = r2['f36']
                    if r2['f37'] != '':
                        ftl.f37 = r2['f37']
                    if r2['f4'] != '':
                        ftl.f4 = r2['f4']
                    if r2['f42'] != '':
                        ftl.f42 = r2['f42']
                    if r2['f43'] != '':
                        ftl.f43 = r2['f43']
                    if r2['f47'] != '':
                        ftl.f47 = r2['f47']
                    if r2['f66'] != '':
                        ftl.f66 = r2['f66']
                    if r2['f67'] != '':
                        ftl.f67 = r2['f67']
                    if r2['f70'] != '':
                        ftl.f70 = r2['f70']
                    if r2['f81'] != '':
                        ftl.f81 = r2['f81']
                    if r2['f92'] != '':
                        ftl.f92 = r2['f92']
                    if r2['n13'] != '':
                        ftl.n13 = r2['n13']
                    if r2['n18'] != '':
                        ftl.n18 = r2['n18']
                    if r2['n23'] != '':
                        ftl.n23 = r2['n23']
                    if r2['n24'] != '':
                        ftl.n24 = r2['n24']
                    if r2['n40'] != '':
                        ftl.n40 = r2['n40']

                # Emulating syntax from loadsitesall2.py
                    sites.save()
                    ftl.save()
                    ftl.site_id.add(Sites_all.objects.get(pk=r2['site_id']))
                    sites.id_samhsa_ftloc.add(ftl)
                    sites.save()
                    ftl.save()

        ## Siterecs_samhsa_otp with r3 & otp
            for r3 in DictReader(open('./0729_siterecs_samhsa_otp.csv', encoding='utf-8-sig')):
                if r3['site_id'] == 'S' + str(row['oid']).zfill(5):
                    otp = Siterecs_samhsa_otp()
                    otp.oid = r3['oid']
                    otp.program_name = r3['program_name']
                    if r3['dba'] != '':
                        otp.dba = r3['dba']
                    otp.street = r3['street']
                    otp.city = r3['city']
                    otp.state_usa = r3['state_usa']
                    otp.zipcode = r3['zipcode']
                    otp.longitude = r3['longitude']
                    otp.latitude = r3['latitude']
                    if r3['phone'] != '':
                        otp.phone = r3['phone']
                    otp.certification = r3['certification']
                    if r3['full_certification'] != '':
                        fcdate = r3['full_certification']
                        otp.full_certification = datetime.strptime(fcdate,DATETIME_FORMAT)
                    otp.archival_only = r3['archival_only']
                    if r3['why_hidden'] != '':
                        otp.why_hidden = r3['why_hidden']
                    if r3['date_firstfind'] != '':
                        fdate = r3['date_firstfind']
                        otp.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r3['date_lastfind'] != '':
                        ldate = r3['date_lastfind']
                        otp.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
                    if r3['data_review'] != '':
                        otp.data_review = r3['data_review']
                    
                    sites.save()
                    otp.save()
                    otp.site_id.add(Sites_all.objects.get(pk=r3['site_id']))
                    sites.id_samhsa_otp.add(otp)
                    sites.save()
                    otp.save()

        ## Siterecs_dbhids_tad with r4 & tad
            for r4 in DictReader(open('./0729_siterecs_dbhids_tad.csv', encoding='utf-8-sig')):
                if r4['site_id'] == 'S' + str(row['oid']).zfill(5):
                    tad = Siterecs_dbhids_tad()
                    tad.oid = r4['oid']
                    tad.name1 = r4['name1']
                    if r4['coe'] != '':
                        tad.coe = r4['coe']
                    tad.ref_address = r4['ref_address']
                    tad.street1 = r4['street1']
                    if r4['street2'] != '':
                        tad.street2 = r4['street2']
                    if r4['city'] != '':
                        tad.city = 'Philadelphia'
                    else:
                        tad.city = r4['city']
                    if r4['state_usa'] != '':
                        tad.state_usa = 'PA'
                    else:
                        tad.state_usa = r4['state_usa']
                    tad.zipcode = r4['zipcode']
                    tad.latitude = r4['latitude']
                    tad.longitude = r4['longitude']
                    tad.phone1 = r4['phone1']
                    if r4['asm'] != '':
                        tad.asm = r4['asm']
                    if r4['ba'] != '':
                        tad.ba = r4['ba']
                    if r4['name_ba'] != '':
                        tad.name_ba = r4['name_ba']
                    if r4['mat_info'] != '':
                        tad.mat_info = r4['mat_info']
                    if r4['bu'] != '':
                        tad.bu = r4['bu']
                    if r4['bui'] != '':
                        tad.bui = r4['bui']
                    if r4['nu'] != '':
                        tad.nu = r4['nu']
                    if r4['vti'] != '':
                        tad.vti = r4['vti']
                    if r4['mu'] != '':
                        tad.mu = r4['mu']
                    if r4['additional_info'] != '':
                        tad.additional_info = r4['additional_info']
                    if r4['phone2'] != '':
                        tad.phone2 = r4['phone2']
                    if r4['walk_in_hours'] != '':
                        tad.walk_in_hours = r4['walk_in_hours']
                    if r4['wih_induction'] != '':
                        tad.wih_induction = r4['wih_induction']
                    if r4['oit'] != '':
                        tad.oit = r4['oit']
                    if r4['op'] != '':
                        tad.op = r4['op']
                    if r4['mhs'] != '':
                        tad.mhs = r4['mhs']
                    if r4['ccc'] != '':
                        tad.ccc = r4['ccc']
                    if r4['hs'] != '':
                        tad.hs = r4['hs']
                    if r4['pw'] != '':
                        tad.pw = r4['pw']
                    if r4['male'] != '':
                        tad.male = r4['male']
                    if r4['sp'] != '':
                        tad.sp = r4['sp']
                    if r4['ales'] != '':
                        tad.ales = r4['ales']
                    if r4['f47'] != '':
                        tad.f47 = r4['f47']
                    if r4['f92'] != '':
                        tad.f92 = r4['f92']
                    if r4['f17'] != '':
                        tad.f17 = r4['f17']
                    if r4['f44'] != '':
                        tad.f44 = r4['f44']
                    tad.archival_only = r4['archival_only']
                    if r4['why_hidden'] != '':
                        tad.why_hidden = r4['why_hidden']
                    if r4['data_review'] != '':
                        tad.data_review = r4['data_review']
                    if r4['date_firstfind'] != '':  # ADD to models.py AND (ok) dataset
                        fdate = r4['date_firstfind']
                        tad.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r4['date_lastfind'] != '':  # ADD to models.py AND (ok) dataset
                        ldate = r4['date_lastfind']
                        tad.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)

                    sites.save()
                    tad.save()
                    tad.site_id.add(Sites_all.objects.get(pk=r4['site_id']))
                    sites.id_dbhids_tad.add(tad)
                    sites.save()
                    tad.save()
                    
        ## Ba_dbhids_tad with r5 & ba
            for r5 in DictReader(open('./0729_ba_dbhids_tad.csv', encoding='utf-8-sig')):
                if r5['site_id'] == 'S' + str(row['oid']).zfill(5):
                    ba = Ba_dbhids_tad()
                    ba.oid = r5['oid']
                    ba.name_ba = r5['name_ba']
                    if r5['hh'] != '':
                        ba.hh = r5['hh']
                    if r5['hwm'] != '':
                        ba.hwm = r5['hwm']
                    if r5['rhl'] != '':
                        ba.rhl = r5['rhl']
                    if r5['rhs'] != '':
                        ba.rhs = r5['rhs']
                    if r5['wm'] != '':
                        ba.wm = r5['wm']
                    if r5['uo'] != '':
                        ba.uo = r5['uo']
                    if r5['date_firstfind'] != '':
                        fdate = r5['date_firstfind']
                        ba.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r5['date_lastfind'] != '':
                        ldate = r5['date_lastfind']
                        ba.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
                    ba.archival_only = r5['archival_only']
                    if r5['why_hidden'] != '':
                        ba.why_hidden = r5['why_hidden']
                    if r5['data_review'] != '':
                        ba.data_review = r5['data_review']

                    sites.save()
                    ba.save()
                    ba.site_id.add(Sites_all.objects.get(pk=r5['site_id']))
                    sites.id_ba_tad.add(ba)
                    sites.save()
                    ba.save()

        ## Siterecs_hfp_fqhc with r6 & hfp
            for r6 in DictReader(open('./0729_siterecs_hfp_fqhc.csv', encoding='utf-8-sig')):
                if r6['site_id'] == 'S' + str(row['oid']).zfill(5):
                    hfp = Siterecs_hfp_fqhc()
                    hfp.oid = r6['oid']
                    hfp.archival_only = r6['archival_only']
                    if r6['why_hidden'] != '':
                        hfp.why_hidden = r6['why_hidden']
                    if r6['name_system'] != '': # This is name1 in model_translation, but models.py requires ...
                        hfp.name_system = r6['name_system']
                    hfp.name_site = r6['name_site'] # ... name2 equivalent
                    if r6['name_short'] != '':
                        hfp.name_short = r6['name_short']
                    if r6['admin_office'] != '':
                        hfp.admin_office = r6['admin_office']
                    hfp.street1 = r6['street1']
                    if r6['street2'] != '':
                        hfp.street2 = r6['street2']
                    hfp.city = r6['city']
                    if r6['state_usa'] != '':
                        hfp.state_usa = 'PA'
                    else:
                        hfp.state_usa = r6['state_usa']
                    hfp.zipcode = r6['zipcode']
                    hfp.latitude = r6['latitude']
                    hfp.longitude = r6['longitude']
                    if r6['website'] != '':
                        hfp.website = r6['website']
                    hfp.phone1 = r6['phone1']
                    if r6['phone2'] != '':
                        hfp.phone2 = r6['phone2']
                    if r6['date_firstfind'] != '':
                        fdate = r6['date_firstfind']
                        hfp.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r6['date_lastfind'] != '':
                        ldate = r6['date_lastfind']
                        hfp.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
                    if r6['data_review'] != '':
                        hfp.data_review = r6['data_review']

                    sites.save()
                    hfp.save()
                    hfp.site_id.add(Sites_all.objects.get(pk=r6['site_id']))
                    sites.id_hfp_fqhc.add(hfp)
                    sites.save()
                    hfp.save()

        ## Siterecs_other_srcs with r7 & oth
            for r7 in DictReader(open('./0729_siterecs_other_srcs.csv', encoding='utf-8-sig')):
                if r7['site_id'] == 'S' + str(row['oid']).zfill(5):
                    oth = Siterecs_other_srcs()
                    oth.oid = r7['oid']
                    oth.name1 = r7['name1']
                    if r7['name2'] != '': # Update models.py to make name2, name3, and website2 optional
                        oth.name2 = r7['name2']
                    if r7['name3'] != '':
                        oth.name3 = r7['name3']
                    if r7['website1'] != '':
                        oth.website1 = r7['website1']
                    if r7['website2'] != '':
                        oth.website2 = r7['website2']
                    if r7['phone1'] != '':
                        oth.phone1 = r7['phone1']
                    if r7['phone2'] != '':
                        oth.phone2 = r7['phone2']
                    if r7['phone3'] != '':
                        oth.phone3 = r7['phone3']
                    if r7['street1'] != '':
                        oth.street1 = r7['street1']
                    if r7['street2'] != '':
                        oth.street2 = r7['street2']
                    oth.city = r7['city']
                    oth.state_usa = r7['state_usa']
                    if r7['zipcode'] != '':
                        oth.zipcode = r7['zipcode']
                    if r7['latitude'] != '':
                        oth.latitude = r7['latitude']
                    if r7['longitude'] != '':
                        oth.longitude = r7['longitude']
                    if r7['bu'] != '':
                        oth.bu = r7['bu']
                    else:
                        oth.bu = 'Unclear'
                    if r7['nu'] != '':
                        oth.nu = r7['nu']
                    else:
                        oth.nu = 'Unclear'
                    if r7['mu'] != '':
                        oth.mu = r7['mu']
                    else:
                        oth.mu = 'No'
                    if r7['otp'] != '':
                        oth.otp = r7['otp']
                    else:
                        oth.otp = 'No'
                    if r7['mat_avail'] != '':
                        oth.mat_avail = r7['mat_avail']
                    else:
                        oth.mat_avail = 'Unclear'
                    if r7['asm'] != '':
                        oth.asm = r7['asm']
                    else:
                        oth.asm = 'Unclear'
                    if r7['ba'] != '':
                        oth.ba = r7['ba']
                    else:
                        oth.ba = 'No'
                    if r7['ref_notes'] != '':
                        oth.ref_notes = r7['ref_notes']
                    if r7['hh'] != '':
                        oth.hh = r7['hh']
                    if r7['hwm'] != '':
                        oth.hwm = r7['hwm']
                    if r7['rhl'] != '':
                        oth.rhl = r7['rhl']
                    if r7['rhs'] != '':
                        oth.rhs = r7['rhs']
                    if r7['wm'] != '':
                        oth.wm = r7['wm']
                    if r7['uo'] != '':
                        oth.uo = r7['uo']
                    if r7['fqhc'] != '':  ## Update default from Unclear to No in models.py (2x)
                        oth.fqhc = r7['fqhc']
                    else:
                        oth.fqhc = 'No'
                    if r7['prim_care'] != '':
                        oth.prim_care = r7['prim_care']
                    else:
                        oth.prim_care = 'Unclear'
                    if r7['telehealth'] != '':
                        oth.telehealth = r7['telehealth']
                    else:
                        oth.telehealth = 'Unclear'
                    if r7['md'] != '':
                        oth.md = r7['md']
                    else:
                        oth.md = 'Unclear'
                    if r7['mc'] != '':
                        oth.mc = r7['mc']
                    else:
                        oth.mc = 'Unclear'
                    if r7['oi'] != '':
                        oth.oi = r7['oi']
                    else:
                        oth.oi = 'Unclear'
                    if r7['pa'] != '':
                        oth.pa = r7['pa']
                    else:
                        oth.pa = 'Unclear'
                    if r7['oit'] != '':
                        oth.oit = r7['oit']
                    else:
                        oth.oit = 'Unclear'
                    if r7['op'] != '':
                        oth.op = r7['op']
                    else:
                        oth.op = 'Unclear'
                    if r7['ta'] != '':
                        oth.ta = r7['ta']
                    else:
                        oth.ta = 'Unclear'
                    if r7['hs'] != '':
                        oth.hs = r7['hs']
                    else:
                        oth.hs = 'Unclear'
                    if r7['mhs'] != '':
                        oth.mhs = r7['mhs']
                    else:
                        oth.mhs = 'Unclear'
                    if r7['ccc'] != '':
                        oth.ccc = r7['ccc']
                    else:
                        oth.ccc = 'Unclear'
                    if r7['dvh'] != '':
                        oth.dvh = r7['dvh']
                    else:
                        oth.dvh = 'Unclear'
                    if r7['pw'] != '':
                        oth.pw = r7['pw']
                    else:
                        oth.pw = 'Unclear'
                    if r7['ad'] != '':
                        oth.ad = r7['ad']
                    else:
                        oth.ad = 'Unclear'
                    if r7['se'] != '':
                        oth.se = r7['se']
                    else:
                        oth.se = 'Unclear'
                    if r7['gl'] != '':
                        oth.gl = r7['gl']
                    else:
                        oth.gl = 'Unclear'
                    if r7['sp'] != '':
                        oth.sp = r7['sp']
                    else:
                        oth.sp = 'Unclear'
                    if r7['ah'] != '':
                        oth.ah = r7['ah']
                    else:
                        oth.ah = 'Unclear'
                    if r7['fem'] != '':
                        oth.fem = r7['fem']
                    else:
                        oth.fem = 'Yes'
                    if r7['male'] != '':
                        oth.male = r7['male']
                    else:
                        oth.male = 'Yes'
                    oth.archival_only = r7['archival_only']
                    if r7['why_hidden'] != '':
                        oth.why_hidden = r7['why_hidden']
                    if r7['data_review'] != '':
                        oth.data_review = r7['data_review'] # Belatedly added to models.py
                        
                    sites.save()
                    oth.save()
                    oth.site_id.add(Sites_all.objects.get(pk=r7['site_id']))
                    sites.id_other_srcs.add(oth)
                    sites.save()
                    oth.save()
                    

    #DIFFERENT ENTITY: Sitecodes_samhsa_ftloc with sc & codes
        for sc in DictReader(open('./0729_sitecodes_samhsa_ftloc.csv', encoding='utf-8-sig')):
            codes = Sitecodes_samhsa_ftloc()
            codes.service_code = sc['service_code']
            if sc['category_code'] != '':
                codes.category_code = sc['category_code']
            if sc['category_name'] != '':
                codes.category_name = sc['category_name']
            if sc['service_name'] != '':
                codes.service_name = sc['service_name']
            if sc['service_description'] != '':
                codes.service_description = sc['service_description']
            codes.sa_listings_match = sc['sa_listings_match']

            codes.save()
