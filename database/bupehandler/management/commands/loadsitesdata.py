from csv import DictReader
from datetime import datetime

""" Removed from above list: sites_site_recs_lookup ... if needed, use new names from models.py: 
    Lookup_siterecs_samhsa_otp      WAS sites_site_recs_lookup
    Lookup_siterecs_samhsa_ftloc    WAS Sites_ftloc
    Lookup_siterecs_dbhids_tad      WAS Siterecs_dbhids_sites_all_lookup
    Lookup_ba_dbhids_tad            NEW
    Lookup_siterecs_hfp_fqhc        WAS Siterecs_hfp_fqhc_sites_all_lookup
    Lookup_siterecs_other_srcs      WAS sitesrecs_other_srcs_sitesall_lk
"""
from pytz import UTC

from django.db import models
from django.utils import timezone

Multi_Choices_Enum3 = [
('Yes','Yes'),
('No','No'),
('Unclear','Unclear'), ## Why final comma?
]

Multi_Choices_EnumWhyHide = [ ## TODO: Fine-tune this list to fit use cases
('No MAT?','No MAT?'),
('Site closed','Site closed'),
('Not a practice site','Not a practice site'),
('Record redundant' ,'Record redundant'),
('Source removed record','Source removed record'),
('Too far from Philadelphia?','Too far from Philadelphia?'),  
('Data needs review','Data needs review'),
('Other','Other'), ## Why final comma?
]

""" TODO: Review def __str__(self) references for which field(s) work best as foreign key in intermediaries for many-to-many relationships 
    (https://docs.djangoproject.com/en/3.2/topics/db/models/#extra-fields-on-many-to-many-relationships)
    Sites_all data load references oid from other classes in id_classname fields as integer or list of integers
"""

class Sitecodes_samhsa_ftloc(models.Model):
## Fields from source:
    service_code = models.CharField(primary_key=True, max_length=10)
    category_code = models.CharField(max_length=6, blank=True)
    category_name = models.CharField(max_length=70, blank=True)
    service_name = models.CharField(max_length=120, blank=True)
    service_description = models.CharField(max_length=999, blank=True)
## MATchMapper additions:
    sa_listings_match = models.CharField(max_length=15) ## Checking presence in siterecs_samhsa_ftloc data (found vs. missing_there/missing_here)
    ## See TableOfTables instead = Table_info class below
        #mm_filters = models.CharField(max_length=15)
        #filter_seq = models.IntegerField()
        #ui_reference = models.CharField(max_length=50)
    date_update = models.DateTimeField(default=timezone.now) ## Our addition

    class Meta:
        managed = True
        db_table = 'sitecodes_samhsa_ftloc'

    def __str__(self):
        return self.service_name

# Gave all Siterecs_ classes an oid (object id for ease of abstraction for backend)

class Siterecs_samhsa_ftloc(models.Model):
  ## MATchMapper additions: 
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Lookup_siterecs_samhsa_ftloc')
    mat_misc = models.BooleanField(blank=True, null=True) #TODO: Check with stakeholders/core users): lofexididine, clonidine
    mat_avail = models.BooleanField(blank=True, null=True)
    oi = models.BooleanField(blank=True, null=True) ## For 'Other insurance' (besides Medicaid and Medicare: private, state, military)
    dvh = models.BooleanField(blank=True, null=True) ## For 'Domestic violence help' (dvfp = safety assistance, dv = program/group for people who experienced domestic violence)
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    date_firstfind = models.DateField()
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    date_update = models.DateTimeField(default=timezone.now)
  ## Fields from source:
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120, blank=True)
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) # TODO change to Enum??? ## Downloaded data uses abbrev (not full names)
    zip5 = models.CharField(max_length=5) # Cannot use zip (=SAMHSA source label) due to Python keyword conflict
    zip4 = models.CharField(max_length=4,blank=True)
    county = models.CharField(max_length=120)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    intake_prompt = models.CharField(max_length=10, blank=True) # Not useful, but added to mirror data SAMHSA provides
    intake1 = models.CharField(max_length=20, blank=True)
    intake2 = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type_facility = models.CharField(max_length=10) ## Data unlikely to exceed 4 characters; reduced 120 to 10
  ## 222 fields below now exactly matched to sequence in SAMHSA downloads, for ease of audit:
    sa = models.BooleanField(blank=True, null=True)
    dt = models.BooleanField(blank=True, null=True)
    mm = models.BooleanField(blank=True, null=True)
    mmw = models.BooleanField(blank=True, null=True)
    dm = models.BooleanField(blank=True, null=True)
    bum = models.BooleanField(blank=True, null=True)
    bmw = models.BooleanField(blank=True, null=True)
    db_field = models.BooleanField(blank=True, null=True)
    rpn = models.BooleanField(blank=True, null=True)
    bu = models.BooleanField(blank=True, null=True)
    nxn = models.BooleanField(blank=True, null=True)
    vtrl = models.BooleanField(blank=True, null=True)
    meth = models.BooleanField(blank=True, null=True)
    hh = models.BooleanField(blank=True, null=True)
    noop = models.BooleanField(blank=True, null=True)
    pain = models.BooleanField(blank=True, null=True)
    nmoa = models.BooleanField(blank=True, null=True)
    moa = models.BooleanField(blank=True, null=True)
    ubn = models.BooleanField(blank=True, null=True) ## Unexplained field, all False
    otpa = models.BooleanField(blank=True, null=True)
    otp = models.BooleanField(blank=True, null=True)
    cbt = models.BooleanField(blank=True, null=True)
    dbt = models.BooleanField(blank=True, null=True)
    tele = models.BooleanField(blank=True, null=True) ## SAMHSA corrected this gap in 2021
    saca = models.BooleanField(blank=True, null=True)
    trc = models.BooleanField(blank=True, null=True)
    rebt = models.BooleanField(blank=True, null=True)
    smon = models.BooleanField(blank=True, null=True)
    smpd = models.BooleanField(blank=True, null=True)
    smop = models.BooleanField(blank=True, null=True)
    hi = models.BooleanField(blank=True, null=True)
    res = models.BooleanField(blank=True, null=True)
    op = models.BooleanField(blank=True, null=True)
    rs = models.BooleanField(blank=True, null=True)
    rl = models.BooleanField(blank=True, null=True)
    rd = models.BooleanField(blank=True, null=True)
    od = models.BooleanField(blank=True, null=True)
    omb = models.BooleanField(blank=True, null=True)
    odt = models.BooleanField(blank=True, null=True)
    oit = models.BooleanField(blank=True, null=True)
    ort = models.BooleanField(blank=True, null=True)
    hid = models.BooleanField(blank=True, null=True)
    hit = models.BooleanField(blank=True, null=True)
    ct = models.BooleanField(blank=True, null=True) ## Unexplained field, all False
    gh = models.BooleanField(blank=True, null=True)
    psyh = models.BooleanField(blank=True, null=True)
    vamc = models.BooleanField(blank=True, null=True)
    tbg = models.BooleanField(blank=True, null=True)
    ih = models.BooleanField(blank=True, null=True)
    stg = models.BooleanField(blank=True, null=True)
    lccg = models.BooleanField(blank=True, null=True)
    ddf = models.BooleanField(blank=True, null=True)
    stag = models.BooleanField(blank=True, null=True)
    stmh = models.BooleanField(blank=True, null=True)
    stdh = models.BooleanField(blank=True, null=True)
    hla = models.BooleanField(blank=True, null=True)
    jc = models.BooleanField(blank=True, null=True)
    carf = models.BooleanField(blank=True, null=True)
    ncqa = models.BooleanField(blank=True, null=True)
    coa = models.BooleanField(blank=True, null=True)
    hfap = models.BooleanField(blank=True, null=True)
    np = models.BooleanField(blank=True, null=True)
    sf = models.BooleanField(blank=True, null=True)
    md = models.BooleanField(blank=True, null=True)
    mc = models.BooleanField(blank=True, null=True)
    si = models.BooleanField(blank=True, null=True)
    pi_field = models.BooleanField(blank=True, null=True)
    mi = models.BooleanField(blank=True, null=True)
    atr = models.BooleanField(blank=True, null=True) ## Unexplained field, all False
    fsa = models.BooleanField(blank=True, null=True)
    ss = models.BooleanField(blank=True, null=True)
    pa = models.BooleanField(blank=True, null=True)
    ah = models.BooleanField(blank=True, null=True)
    sp = models.BooleanField(blank=True, null=True)
    co = models.BooleanField(blank=True, null=True)
    gl = models.BooleanField(blank=True, null=True)
    vet = models.BooleanField(blank=True, null=True)
    adm = models.BooleanField(blank=True, null=True)
    mf = models.BooleanField(blank=True, null=True)
    cj = models.BooleanField(blank=True, null=True)
    se = models.BooleanField(blank=True, null=True)
    ad = models.BooleanField(blank=True, null=True)
    pw = models.BooleanField(blank=True, null=True)
    wn = models.BooleanField(blank=True, null=True)
    mn = models.BooleanField(blank=True, null=True)
    hv = models.BooleanField(blank=True, null=True)
    trma = models.BooleanField(blank=True, null=True)
    xa = models.BooleanField(blank=True, null=True)
    dv = models.BooleanField(blank=True, null=True)
    tay = models.BooleanField(blank=True, null=True)
    nsc = models.BooleanField(blank=True, null=True)
    adtx = models.BooleanField(blank=True, null=True)
    bdtx = models.BooleanField(blank=True, null=True)
    cdtx = models.BooleanField(blank=True, null=True)
    mdtx = models.BooleanField(blank=True, null=True)
    odtx = models.BooleanField(blank=True, null=True)
    tgd = models.BooleanField(blank=True, null=True)
    tid = models.BooleanField(blank=True, null=True)
    ico = models.BooleanField(blank=True, null=True)
    gco = models.BooleanField(blank=True, null=True)
    fco = models.BooleanField(blank=True, null=True)
    mco = models.BooleanField(blank=True, null=True)
    twfa = models.BooleanField(blank=True, null=True)
    bia = models.BooleanField(blank=True, null=True)
    cmi = models.BooleanField(blank=True, null=True)
    moti = models.BooleanField(blank=True, null=True)
    ang = models.BooleanField(blank=True, null=True)
    mxm = models.BooleanField(blank=True, null=True)
    crv = models.BooleanField(blank=True, null=True)
    relp = models.BooleanField(blank=True, null=True)
    bc = models.BooleanField(blank=True, null=True)
    chld = models.BooleanField(blank=True, null=True)
    yad = models.BooleanField(blank=True, null=True)
    adlt = models.BooleanField(blank=True, null=True)
    fem = models.BooleanField(blank=True, null=True)
    male = models.BooleanField(blank=True, null=True)
    bmo = models.BooleanField(blank=True, null=True)
    mo = models.BooleanField(blank=True, null=True)
    du = models.BooleanField(blank=True, null=True)
    duo = models.BooleanField(blank=True, null=True)
    acc = models.BooleanField(blank=True, null=True)
    acm = models.BooleanField(blank=True, null=True)
    acu = models.BooleanField(blank=True, null=True)
    add_field = models.BooleanField(blank=True, null=True)
    baba = models.BooleanField(blank=True, null=True)
    ccc = models.BooleanField(blank=True, null=True)
    cmha = models.BooleanField(blank=True, null=True)
    csaa = models.BooleanField(blank=True, null=True)
    daut = models.BooleanField(blank=True, null=True)
    dp = models.BooleanField(blank=True, null=True)
    dsf = models.BooleanField(blank=True, null=True)
    dvfp = models.BooleanField(blank=True, null=True)
    eih = models.BooleanField(blank=True, null=True)
    emp = models.BooleanField(blank=True, null=True)
    haec = models.BooleanField(blank=True, null=True)
    heoh = models.BooleanField(blank=True, null=True)
    hivt = models.BooleanField(blank=True, null=True)
    isc = models.BooleanField(blank=True, null=True)
    itu = models.BooleanField(blank=True, null=True)
    mhs = models.BooleanField(blank=True, null=True)
    mpd = models.BooleanField(blank=True, null=True)
    opc = models.BooleanField(blank=True, null=True)
    sae = models.BooleanField(blank=True, null=True)
    shb = models.BooleanField(blank=True, null=True)
    shc = models.BooleanField(blank=True, null=True)
    shg = models.BooleanField(blank=True, null=True)
    smhd = models.BooleanField(blank=True, null=True)
    ssa = models.BooleanField(blank=True, null=True)
    ssd = models.BooleanField(blank=True, null=True)
    stdt = models.BooleanField(blank=True, null=True)
    ta = models.BooleanField(blank=True, null=True)
    taec = models.BooleanField(blank=True, null=True)
    tbs = models.BooleanField(blank=True, null=True)
    cm = models.BooleanField(blank=True, null=True)
    fpsy = models.BooleanField(blank=True, null=True) ## Unexplained field, all False
    hs = models.BooleanField(blank=True, null=True)
    nrt = models.BooleanField(blank=True, null=True)
    peer = models.BooleanField(blank=True, null=True)
    stu = models.BooleanField(blank=True, null=True)
    tcc = models.BooleanField(blank=True, null=True)
    bsdm = models.BooleanField(blank=True, null=True)
    nu = models.BooleanField(blank=True, null=True)
    mu = models.BooleanField(blank=True, null=True)
    bwn = models.BooleanField(blank=True, null=True)
    bwon = models.BooleanField(blank=True, null=True)    
    ub = models.BooleanField(blank=True, null=True)
    un = models.BooleanField(blank=True, null=True)
    beri = models.BooleanField(blank=True, null=True)
    pvtp = models.BooleanField(blank=True, null=True)
    pvtn = models.BooleanField(blank=True, null=True)
    vo = models.BooleanField(blank=True, null=True)
    sumh = models.BooleanField(blank=True, null=True)
    inpe = models.BooleanField(blank=True, null=True)
    rpe = models.BooleanField(blank=True, null=True)
    pc = models.BooleanField(blank=True, null=True)
    naut = models.BooleanField(blank=True, null=True)
    nmaut = models.BooleanField(blank=True, null=True)
    acma = models.BooleanField(blank=True, null=True)
    pmat = models.BooleanField(blank=True, null=True)
    auinpe = models.BooleanField(blank=True, null=True)
    aurpe = models.BooleanField(blank=True, null=True)
    aupc = models.BooleanField(blank=True, null=True)
    ulc = models.BooleanField(blank=True, null=True)
    mhiv = models.BooleanField(blank=True, null=True)
    mhcv = models.BooleanField(blank=True, null=True)
    lfxd = models.BooleanField(blank=True, null=True)
    clnd = models.BooleanField(blank=True, null=True)
    copsu = models.BooleanField(blank=True, null=True)
    daof = models.BooleanField(blank=True, null=True)
    mst = models.BooleanField(blank=True, null=True)
    noe = models.BooleanField(blank=True, null=True)
    ofd = models.BooleanField(blank=True, null=True)
    rc = models.BooleanField(blank=True, null=True)
    piec = models.BooleanField(blank=True, null=True)
    mdet = models.BooleanField(blank=True, null=True)
    voc = models.BooleanField(blank=True, null=True)
    hav = models.BooleanField(blank=True, null=True)
    hbv = models.BooleanField(blank=True, null=True)
    audo = models.BooleanField(blank=True, null=True)
    f17 = models.BooleanField(blank=True, null=True)
    f19 = models.BooleanField(blank=True, null=True)
    f25 = models.BooleanField(blank=True, null=True)
    f28 = models.BooleanField(blank=True, null=True)
    f30 = models.BooleanField(blank=True, null=True)
    f31 = models.BooleanField(blank=True, null=True)
    f35 = models.BooleanField(blank=True, null=True)
    f36 = models.BooleanField(blank=True, null=True)
    f37 = models.BooleanField(blank=True, null=True)
    f4 = models.BooleanField(blank=True, null=True)
    f42 = models.BooleanField(blank=True, null=True)
    f43 = models.BooleanField(blank=True, null=True)
    f47 = models.BooleanField(blank=True, null=True)
    f66 = models.BooleanField(blank=True, null=True)
    f67 = models.BooleanField(blank=True, null=True)
    f70 = models.BooleanField(blank=True, null=True)
    f81 = models.BooleanField(blank=True, null=True)
    f92 = models.BooleanField(blank=True, null=True)
    n13 = models.BooleanField(blank=True, null=True)
    n18 = models.BooleanField(blank=True, null=True)
    n23 = models.BooleanField(blank=True, null=True)
    n24 = models.BooleanField(blank=True, null=True)
    n40  = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'siterecs_samhsa_ftloc'

    def __str__(self):
        return ', '.join([self.street1, self.street2, self.city, self.state_usa, self.zip5]) ## Reverted zipcode to zip5 (disambiguate from zip4)


class Siterecs_samhsa_otp(models.Model):
  ## MATchMapper additions: 
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Lookup_siterecs_samhsa_otp')
  ## Fields from source: 
    program_name = models.CharField(max_length=250)
    dba = models.CharField(max_length=120, blank=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) # TODO change to Enum??? ## Match above class; downloaded data again uses abbrev (not full names)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20, blank=True) # Format: ###-###-#### (with optional x####) -- extended max_length to 20 to accommodate occasional extensions
    certification = models.CharField(max_length=120)
    full_certification = models.DateField(blank=True, null=True)
  ## MATchMapper additions: 
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    date_firstfind = models.DateField()
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    data_review = models.CharField(max_length=250, blank=True) # Notes from manual review, e.g. "ZIP typo: corrected 19007 to 19107..."
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_samhsa_otp'

    def __str__(self):
        return self.program_name ## Renamed to match source more closely


class Siterecs_dbhids_tad(models.Model):
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Lookup_siterecs_dbhids_tad')
  ## [DCS] = directly copied from source PDF. Interspersed with MATchMapper boolean additions: 
    name1 = models.CharField(max_length=120) #[DCS]: Max LEN in data = 51 char.
    coe = models.BooleanField(blank=True, null=True) ## Asterisked names (*Center of Excellence)
    ref_address = models.CharField(max_length=100) #[DCS]: Max LEN in data = 53 char.
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, default='Philadelphia') # Added Philadelphia as default city BY SAM
    state_usa = models.CharField(max_length=30, default='PA') ## Can replace with Enum to match above classes BY SAM
    zipcode = models.CharField(max_length=5)
    phone1 = models.CharField(max_length=20) #[DCS] but reformatted: ###-###-#### (with optional x####)
    asm = models.BooleanField(blank=True, null=True) ## Added to make page 2 entries filterable (Assessment directory)
    ba = models.BooleanField(blank=True, null=True) ## Added to make page 5 entries link-and-filterable (Bed availability! = top ask in March 2020 hackathon response)
    name_ba = models.CharField(max_length=50, blank=True) #[DCS] page 5, to facilitate cross-refs | TODO: Add to model_translation.py IF frontend visibility needed (for EDITOR)
    mat_info = models.CharField(max_length=100, blank=True) #[DCS]: Max LEN in data = 50 char. For line breaks, use pipe: |
    bu = models.BooleanField(blank=True, null=True)
    bui = models.BooleanField(blank=True, null=True)
    #bum = models.BooleanField(blank=True, null=True)
    #buu = models.BooleanField(blank=True, null=True)
    #bwn = models.BooleanField(blank=True, null=True)
    nu = models.BooleanField(blank=True, null=True)
    vti = models.BooleanField(blank=True, null=True)
    #vtm = models.BooleanField(blank=True, null=True)
    #vtrl = models.BooleanField(blank=True, null=True) # Renamed to match SAMHSA sitecodes
    mu = models.BooleanField(blank=True, null=True)
    #mui = models.BooleanField(blank=True, null=True)
    #mm = models.BooleanField(blank=True, null=True)
    additional_info = models.CharField(max_length=150, blank=True) #[DCS] after separating Walk-in: Max LEN in data = 88 char. For line breaks, use pipe: |
    phone2 = models.CharField(max_length=20, blank=True) ## Added for 3 entries with second phone from additional_info
    walk_in_hours = models.CharField(max_length=80, blank=True) #[DCS] for yellow records: List '[unspecified]' if no days & times available. Max LEN in data = 38 char, but increased limit from 50 to 80 just in case.
    wih_induction = models.BooleanField(blank=True, null=True) # True if PDF record is yellow (vs. blue or white)
    oit = models.BooleanField(blank=True, null=True)
    op = models.BooleanField(blank=True, null=True)
    mhs = models.BooleanField(blank=True, null=True)
    ccc = models.BooleanField(blank=True, null=True)
    hs = models.BooleanField(blank=True, null=True)
    pw = models.BooleanField(blank=True, null=True)
    male = models.BooleanField(blank=True, null=True)
    sp = models.BooleanField(blank=True, null=True)
    ales = models.BooleanField(blank=True, null=True)
    f47 = models.BooleanField(blank=True, null=True)
    f92 = models.BooleanField(blank=True, null=True)
    f17 = models.BooleanField(blank=True, null=True)
    f44 = models.BooleanField(blank=True, null=True)
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    date_firstfind = models.DateField()
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    data_review = models.CharField(max_length=250, blank=True) ## Max LEN so far = 161 char.  

    class Meta:
        managed = True
        db_table = 'siterecs_dbhids_tad'

    def __str__(self):
        return str(self.oid)


class Ba_dbhids_tad(models.Model):   ## Added as bridge to link sites_all to 3x/weekly DBHIDS updates
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Lookup_ba_dbhids_tad')
    name_ba = models.CharField(max_length=50)
    hh = models.BooleanField(blank=True, null=True)
    hwm = models.BooleanField(blank=True, null=True)
    rhl = models.BooleanField(blank=True, null=True)
    rhs = models.BooleanField(blank=True, null=True)
    wm = models.BooleanField(blank=True, null=True)
    uo = models.BooleanField(blank=True, null=True)
    date_firstfind = models.DateField()
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    date_update = models.DateTimeField(default=timezone.now)
    archival_only = models.BooleanField(blank=False)
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    data_review = models.CharField(max_length=250, blank=True)

    
class Siterecs_hfp_fqhc(models.Model):   ## TODO: Reload in July 2021 prototype to save time -- may nix in next major iteration
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Lookup_siterecs_hfp_fqhc')
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    name_system = models.CharField(max_length=120, blank=True)
    name_site = models.CharField(max_length=120)
    name_short = models.CharField(max_length=50, blank=True)
    admin_office = models.BooleanField(blank=True, null=True)
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30, default='PA') ## Can replace with Enum to match above classes
    zipcode = models.CharField(max_length=5)
    website = models.URLField(blank=True, null=True)
    phone1 = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    phone2 = models.CharField(max_length=20, blank=True) # Format: ###-###-#### (with optional x####)
    date_firstfind = models.DateField()
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    data_review = models.CharField(max_length=250)

    def __str__(self):
        return str(self.name_short)

## This class seems superfluous for FINDER (substantially similar to sites_all), but might help EDITOR.
class Siterecs_other_srcs(models.Model): ## What is this: Central table for direct research on FQHCs and other BP Locs (incl. 2020 work, integration underway)
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = "Lookup_siterecs_other_srcs")
    ## TODO: Do cross-referencing id_ fields need to be integrated in ManyToMany model?
    #id_ba_tad = models.ManyToManyField('Ba_dbhids_tad',blank=True, null=True)
    #id_hfp_fqhc = models.ManyToManyField('Siterecs_hfp_fqhc',blank=True, null=True)
    #id_hrsa_fqhc = models.ManyToManyField('Siterecs_hrsa_fqhc',blank=True, null=True) ## Class not yet created
    #id_bploc = models.ManyToManyField('Bplocs_samhsa_npi_etc',blank=True, null=True) ## Class not yet created
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120, blank=True)
    name3 = models.CharField(max_length=120, blank=True)
    website1 = models.URLField(blank=True, null=True) ## Would prefer to require, but optional is more scalable (e.g. if DBHIDS adds program that lacks working URL)
    website2 = models.URLField(blank=True, null=True)
    phone1 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    phone2 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    phone3 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    street1 = models.CharField(max_length=120, blank=True) 
    street2 = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) ## Optional: replace with Enum eventually (across classes)
    zipcode = models.CharField(max_length=5, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    bu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    nu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    mu = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    otp = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    mat_avail = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    asm = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Assessment site
    ba = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3) ## Link to DBHIDS Bed Availability (BA) data, updated 2-3x weekly
    ref_notes = models.CharField(max_length=299, blank=True) ## Notes to display for users (FINDER)
    hh = models.BooleanField(blank=True, null=True) ## BA: Halfway house
    hwm = models.BooleanField(blank=True, null=True) ## BA: Hospital withdrawal management
    rhl = models.BooleanField(blank=True, null=True) ## BA: Long-term rehab
    rhs = models.BooleanField(blank=True, null=True) ## BA: Short-term rehab
    wm = models.BooleanField(blank=True, null=True) ##: BA: Withdrawal management
    uo = models.BooleanField(blank=True, null=True) ## BA: Unspecified type
    fqhc = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    prim_care = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    telehealth = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    md = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Medicaid
    mc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Medicare
    oi = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Other insurance (for details, cross-ref SAMHSA FT Loc or Other Sources table(s))
    pa = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Payment assistance
    oit = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Intensive outpatient
    op = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Outpatient
    ta = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Transportation assistance
    hs = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Housing services TODO: Clarify = help to find housing (vs. residential program)?
    mhs = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Mental health services
    ccc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Child care
    dvh = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Domestic violence (safety assistance [25], group [15], or both [35])
    pw = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Pregnant/postpartum women
    ad = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Adolescents
    se = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Program for older adults (seniors, 65+)
    gl = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Program for LGBTQ+
    sp = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Spanish
    ah = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Deaf and hard of hearing assistance
    fem = models.CharField(max_length=20, default = 'Yes', choices = Multi_Choices_Enum3) ## Women (included to mark non-coed facilities)
    male = models.CharField(max_length=20, default = 'Yes', choices = Multi_Choices_Enum3) ## Men (included to mark non-coed facilities)
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    data_review = models.CharField(max_length=1000) ## Added in case: For EDITOR use
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_other_srcs'

    def __str__(self):
        return self.name1


class Sites_all(models.Model):
    oid = models.CharField(primary_key=True, max_length=120) # TODO integer or varchar? ## Probably serialized varchar?
    id_samhsa_ftloc = models.ManyToManyField('Siterecs_samhsa_ftloc', blank=True, null=True)
    id_dbhids_tad = models.ManyToManyField('Siterecs_dbhids_tad', blank=True, null=True)
    id_ba_tad = models.ManyToManyField('Ba_dbhids_tad', blank=True, null=True)
    id_samhsa_otp = models.ManyToManyField('Siterecs_samhsa_otp', blank=True, null=True)
    id_hfp_fqhc = models.ManyToManyField('Siterecs_hfp_fqhc', blank=True, null=True)
    id_other_srcs = models.ManyToManyField('Siterecs_other_srcs', blank=True, null=True)
    name1 = models.CharField(max_length=120) ## WAS name_program
    name2 = models.CharField(max_length=120, blank=True) ## WAS name_site
    name3 = models.CharField(max_length=120, blank=True)
    website1 = models.URLField(blank=True, null=True) ## Important addition: functions with address fields as composite primary key
    website2 = models.URLField(blank=True, null=True) # Added just in case (to match siterecs_other_srcs)
    phone1 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    phone2 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    phone3 = models.CharField(max_length=80, blank=True)  ## Format: ###-###-#### with optional x#### or note re: purpose
    street1 = models.CharField(max_length=120, blank=True) 
    street2 = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) ## Optional: replace with Enum eventually (across classes)
    zipcode = models.CharField(max_length=5, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
  ## TODO: Documentation for connecting relevant fields from Audit tables to Enum fields below + records linkage for above
    bu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    nu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    mu = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    otp = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    mat_avail = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    asm = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Assessment site
    ba = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3) ## Link to DBHIDS Bed Availability (BA) data, updated 2-3x weekly
    ref_notes = models.CharField(max_length=299, blank=True) ## Notes to display for users (FINDER)
    hh = models.BooleanField(blank=True, null=True) ## BA: Halfway house
    hwm = models.BooleanField(blank=True, null=True) ## BA: Hospital withdrawal management
    rhl = models.BooleanField(blank=True, null=True) ## BA: Long-term rehab
    rhs = models.BooleanField(blank=True, null=True) ## BA: Short-term rehab
    wm = models.BooleanField(blank=True, null=True) ##: BA: Withdrawal management
    uo = models.BooleanField(blank=True, null=True) ## BA: Unspecified type
    fqhc = models.CharField(max_length=20, default = 'No', choices = Multi_Choices_Enum3)
    prim_care = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    telehealth = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    md = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Medicaid
    mc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Medicare
    oi = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Other insurance (for details, cross-ref SAMHSA FT Loc or Other Sources table(s))
    pa = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Payment assistance
    oit = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Intensive outpatient
    op = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Outpatient
    ta = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Transportation assistance
    hs = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Housing services TODO: Clarify = help to find housing (vs. residential program)?
    mhs = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Mental health services
    ccc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Child care
    dvh = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Domestic violence (safety assistance [25], group [15], or both [35])
    pw = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Pregnant/postpartum women
    ad = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Adolescents
    se = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Program for older adults (seniors, 65+)
    gl = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Program for LGBTQ+
    sp = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Spanish
    ah = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) ## Deaf and hard of hearing assistance
    fem = models.CharField(max_length=20, default = 'Yes', choices = Multi_Choices_Enum3) ## Women (included to mark non-coed facilities)
    male = models.CharField(max_length=20, default = 'Yes', choices = Multi_Choices_Enum3) ## Men (included to mark non-coed facilities)
    archival_only = models.BooleanField(blank=False) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, blank=True, default="Data needs review", choices=Multi_Choices_EnumWhyHide) # Require only if archival_only = True
    data_review = models.CharField(max_length=499, null=True, blank=True) ## Notes for admin/data management (EDITOR)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'sites_all'

    def __str__(self):
        return ', '.join([self.oid, self.name1, self.name2]) ## Updated to match renaming consistency

    
class Table_info(models.Model):
    oid = models.IntegerField(primary_key=True)
    table_name = models.CharField(max_length=120)
    display_name = models.CharField(max_length=120)
    source_url = models.URLField(blank=True)
    update_recency = models.DateField() ## TBD: set default as .now?
    records_count = models.IntegerField(blank=True, null=True)
    facility_type = models.CharField(max_length=250)
    source_range = models.CharField(max_length=120)
    notes = models.CharField(max_length=500, blank=True)
    filters = models.CharField(max_length=5000, blank=True)
    display_cols = models.CharField(max_length=500, blank=True) # Just colnames (max = 273)
    hide_cols = models.CharField(max_length=500, blank=True)
    annual_updates = models.IntegerField()

    def __str__(self):
        return str(self.display_name)


##/ Renamed the below for consistency and resequenced to match sequence above.
##/ TODO: Figure out which parts of codebase invoke the below and update naming there. Use this template to add other class(es) as needed, e.g. Ba_dbhids_tad => Lookup_ba_dbhids_tad
    
class Lookup_siterecs_samhsa_ftloc(models.Model): #/Renamed: WAS Sites_ftloc
    samhsa_oid = models.ForeignKey(Siterecs_samhsa_ftloc, on_delete=models.CASCADE)
    sites_all_id= models.ForeignKey(Sites_all, on_delete=models.CASCADE)

class Lookup_siterecs_samhsa_otp(models.Model): #/Renamed: WAS sites_site_recs_lookup
    samhsa_oid = models.ForeignKey(Siterecs_samhsa_otp, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all, on_delete=models.CASCADE)

class Lookup_siterecs_dbhids_tad(models.Model): #/Renamed: WAS Siterecs_dbhids_sites_all_lookup
    samhsa_oid = models.ForeignKey(Siterecs_dbhids_tad, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all, on_delete=models.CASCADE)

class Lookup_ba_dbhids_tad(models.Model): #/Added for new class
    samhsa_oid = models.ForeignKey(Ba_dbhids_tad, on_delete=models.CASCADE)
    sites_all_id= models.ForeignKey(Sites_all, on_delete=models.CASCADE)

class Lookup_siterecs_hfp_fqhc(models.Model): #/Renamed: WAS Siterecs_hfp_fqhc_sites_all_lookup
    samhsa_oid = models.ForeignKey(Siterecs_hfp_fqhc, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all, on_delete=models.CASCADE)

class Lookup_siterecs_other_srcs(models.Model): #/Renamed: WAS sitesrecs_other_srcs_sitesall_lk
    samhsa_oid = models.ForeignKey(Siterecs_other_srcs, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all, on_delete=models.CASCADE)


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

        for row in DictReader(open('./0717_sites_all.csv')):
            sites = Sites_all()
            sites.oid = row['site_id']
            #? sites.id_dbhids_tad.sites_all_id = row['site_id'] ## What was this for?
            #? sites.id_hfp_fqhc.sites_all_id = row['site_id'] ## What was this for?
            if row['id_samhsa_ftloc'] != '':
                sites.id_samhsa_ftloc = row['id_samhsa_ftloc']
            if row['id_dbhids_tad'] != '':
                sites.id_dbhids_tad = row['id_dbhids_tad']
            if row['id_ba_tad'] != '':
                sites.id_ba_tad = row['id_ba_tad']
            if row['id_samhsa_otp'] != '':
                sites.id_samhsa_otp = row['id_samhsa_otp']
            if row['id_hfp_fqhc'] != '':
                sites.id_hfp_fqhc = row['id_hfp_fqhc']
            if row['id_other_srcs'] != '':
                sites.id_other_srcs = row['id_other_srcs']
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
                sites.bu = 'Unclear'
            else:
                sites.bu = row['bu']
            if row['nu'] != '':
                sites.nu = 'Unclear'
            else:
                sites.nu = row['nu']
            if row['mu'] != '':
                sites.mu = 'No'
            else:
                sites.mu = row['mu']
            if row['otp'] != '':
                sites.otp = 'No'
            else:
                sites.otp = row['otp']
            if row['mat_avail'] != '':
                sites.mat_avail = 'Unclear'
            else:
                sites.mat_avail = row['mat_avail']
            if row['asm'] != '':
                sites.asm = 'Unclear'
            else:
                sites.asm = row['asm']
            if row['ba'] != '':
                sites.ba = 'No'
            else:
                sites.ba = row['ba']
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
                sites.fqhc = 'No'
            else:
                sites.fqhc = row['fqhc']
            if row['prim_care'] != '':
                sites.prim_care = 'Unclear'
            else:
                sites.prim_care = row['prim_care']
            if row['telehealth'] != '':
                sites.telehealth = 'Unclear'
            else:
                sites.telehealth = row['telehealth']
            if row['md'] != '':
                sites.md = 'Unclear'
            else:
                sites.md = row['md']
            if row['mc'] != '':
                sites.mc = 'Unclear'
            else:
                sites.mc = row['mc']
            if row['oi'] != '':
                sites.oi = 'Unclear'
            else:
                sites.oi = row['oi']
            if row['pa'] != '':
                sites.pa = 'Unclear'
            else:
                sites.pa = row['pa']
            if row['oit'] != '':
                sites.oit = 'Unclear'
            else:
                sites.oit = row['oit']
            if row['op'] != '':
                sites.op = 'Unclear'
            else:
                sites.op = row['op']
            if row['ta'] != '':
                sites.ta = 'Unclear'
            else:
                sites.ta = row['ta']
            if row['hs'] != '':
                sites.hs = 'Unclear'
            else:
                sites.hs = row['hs']
            if row['mhs'] != '':
                sites.mhs = 'Unclear'
            else:
                sites.mhs = row['mhs']
            if row['ccc'] != '':
                sites.ccc = 'Unclear'
            else:
                sites.ccc = row['ccc']
            if row['dvh'] != '':
                sites.dvh = 'Unclear'
            else:
                sites.dvh = row['dvh']
            if row['pw'] != '':
                sites.pw = 'Unclear'
            else:
                sites.pw = row['pw']
            if row['ad'] != '':
                sites.ad = 'Unclear'
            else:
                sites.ad = row['ad']
            if row['se'] != '':
                sites.se = 'Unclear'
            else:
                sites.se = row['se']
            if row['gl'] != '':
                sites.gl = 'Unclear'
            else:
                sites.gl = row['gl']
            if row['sp'] != '':
                sites.sp = 'Unclear'
            else:
                sites.sp = row['sp']
            if row['ah'] != '':
                sites.ah = 'Unclear'
            else:
                sites.ah = row['ah']
            if row['fem'] != '':
                sites.fem = 'Yes'
            else:
                sites.fem = row['fem']
            if row['male'] != '':
                sites.male = 'Yes'
            else:
                sites.male = row['male']
            sites.archival_only = row['archival_only']
            if row['why_hidden'] != '':
                sites.why_hidden = row['why_hidden']
            if row['data_review'] != '':
                sites.data_review = row['data_review']

        ## Siterecs_samhsa_ftloc with r2 & ftl
            for r2 in DictReader(open('./0717_siterecs_samshsa_ftloc.csv')):
                if r2['site_id'] == row['site_id']:
                    ftl = Siterecs_samha_ftloc()
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
                        ftl.date_firstfind = datetime.strptime(fdate,DATETIME_FORMAT)
                    if r2['date_lastfind'] != '':
                        ldate = r2['date_lastfind']
                        ftl.date_lastfind = datetime.strptime(ldate,DATETIME_FORMAT)
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
            for r3 in DictReader(open('./0717_siterecs_samshsa_otp.csv')):
                if r3['site_id'] == row['site_id']:
                    otp = Siterecs_samha_otp()
                    otp.oid = r3['oid']
                    otp.program_name = r3['program_name']
                    if r3['dba'] != '':
                        otp.dba = r3['dba']
                    otp.street = r3['street']
                    otp.city = r3['city']
                    otp.state_usa = r3['state_usa']
                    otp.zipcode = r3['zipcode']
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
            for r4 in DictReader(open('./0717_siterecs_dbhids_tad.csv')):
                if r4['site_id'] == row['site_id']:
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
            for r5 in DictReader(open('./0717_ba_dbhids_tad.csv')):
                if r5['site_id'] == row['site_id']:
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
            for r6 in DictReader(open('./0717_siterecs_hfp_fqhc.csv')):
                if r6['site_id'] == row['site_id']:
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
            for r7 in DictReader(open('./0717_siterecs_other_srcs.csv')):
                if r7['site_id'] == row['site_id']:
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
                        oth.bu = 'Unclear'
                    else:
                        oth.bu = r7['bu']
                    if r7['nu'] != '':
                        oth.nu = 'Unclear'
                    else:
                        oth.nu = r7['nu']
                    if r7['mu'] != '':
                        oth.mu = 'No'
                    else:
                        oth.mu = r7['mu']
                    if r7['otp'] != '':
                        oth.otp = 'No'
                    else:
                        oth.otp = r7['otp']
                    if r7['mat_avail'] != '':
                        oth.mat_avail = 'Unclear'
                    else:
                        oth.mat_avail = r7['mat_avail']
                    if r7['asm'] != '':
                        oth.asm = 'Unclear'
                    else:
                        oth.asm = r7['asm']
                    if r7['ba'] != '':
                        oth.ba = 'No'
                    else:
                        oth.ba = r7['ba']
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
                        oth.fqhc = 'No'
                    else:
                        oth.fqhc = r7['fqhc']
                    if r7['prim_care'] != '':
                        oth.prim_care = 'Unclear'
                    else:
                        oth.prim_care = r7['prim_care']
                    if r7['telehealth'] != '':
                        oth.telehealth = 'Unclear'
                    else:
                        oth.telehealth = r7['telehealth']
                    if r7['md'] != '':
                        oth.md = 'Unclear'
                    else:
                        oth.md = r7['md']
                    if r7['mc'] != '':
                        oth.mc = 'Unclear'
                    else:
                        oth.mc = r7['mc']
                    if r7['oi'] != '':
                        oth.oi = 'Unclear'
                    else:
                        oth.oi = r7['oi']
                    if r7['pa'] != '':
                        oth.pa = 'Unclear'
                    else:
                        oth.pa = r7['pa']
                    if r7['oit'] != '':
                        oth.oit = 'Unclear'
                    else:
                        oth.oit = r7['oit']
                    if r7['op'] != '':
                        oth.op = 'Unclear'
                    else:
                        oth.op = r7['op']
                    if r7['ta'] != '':
                        oth.ta = 'Unclear'
                    else:
                        oth.ta = r7['ta']
                    if r7['hs'] != '':
                        oth.hs = 'Unclear'
                    else:
                        oth.hs = r7['hs']
                    if r7['mhs'] != '':
                        oth.mhs = 'Unclear'
                    else:
                        oth.mhs = r7['mhs']
                    if r7['ccc'] != '':
                        oth.ccc = 'Unclear'
                    else:
                        oth.ccc = r7['ccc']
                    if r7['dvh'] != '':
                        oth.dvh = 'Unclear'
                    else:
                        oth.dvh = r7['dvh']
                    if r7['pw'] != '':
                        oth.pw = 'Unclear'
                    else:
                        oth.pw = r7['pw']
                    if r7['ad'] != '':
                        oth.ad = 'Unclear'
                    else:
                        oth.ad = r7['ad']
                    if r7['se'] != '':
                        oth.se = 'Unclear'
                    else:
                        oth.se = r7['se']
                    if r7['gl'] != '':
                        oth.gl = 'Unclear'
                    else:
                        oth.gl = r7['gl']
                    if r7['sp'] != '':
                        oth.sp = 'Unclear'
                    else:
                        oth.sp = r7['sp']
                    if r7['ah'] != '':
                        oth.ah = 'Unclear'
                    else:
                        oth.ah = r7['ah']
                    if r7['fem'] != '':
                        oth.fem = 'Yes'
                    else:
                        oth.fem = r7['fem']
                    if r7['male'] != '':
                        oth.male = 'Yes'
                    else:
                        oth.male = r7['male']
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
        for sc in DictReader(open('./0717_sitecodes_samhsa_ftloc.csv')):
            codes = Sitecodes_samhsa_ftloc()
            codes.service_code = sc['service_code']
            if sc['category_code'] != '':
                codes.category_code = row['category_code']
            if sc['category_name'] != '':
                codes.category_name = row['category_name']
            if sc['service_name'] != '':
                codes.service_name = row['service_name']
            if sc['service_description'] != '':
                codes.service_description = row['service_description']
            codes.sa_listings_match = sc['sa_listings_match']

            codes.save()
