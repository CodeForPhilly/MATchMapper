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
