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


class Sitecodes_samhsa_ftloc(models.Model):
## Fields from source:
    service_code = models.CharField(primary_key=True, max_length=10)
    category_code = models.CharField(max_length=6)
    category_name = models.CharField(max_length=70)
    service_name = models.CharField(max_length=120)
    service_description = models.CharField(max_length=999)
## MATchMapper additions:
    sa_listings_match = models.CharField(max_length=15) ## Checking presence in siterecs_samhsa_ftloc data (found vs. missing_there/missing_here)
    mm_filters = models.CharField(max_length=15)
    ## See TableOfTables instead
        #filter_seq = models.IntegerField()
        #ui_reference = models.CharField(max_length=50)
    date_update = models.DateTimeField(default=timezone.now) ## Our addition

    class Meta:
        managed = True
        db_table = 'sitecodes_samhsa_ftloc'

    def __str__(self):
        return self.service_name

# Gave all Siterecs_ classes an oid (object id for ease of abstraction for backend) ## = Audit tables

class Siterecs_samhsa_ftloc(models.Model):
  ## MATchMapper additions: 
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Sites_ftloc')
    mat_misc = models.BooleanField(blank=True, null=True) #TODO: check with stakeholders/core users): lofexididine, clonidine
    mat_avail = models.BooleanField(blank=True, null=True)
    oi = models.BooleanField(blank=True, null=True) ## For 'Other insurance' (besides Medicaid and Medicare: private, state, military)
    dvh = models.BooleanField(blank=True, null=True) ## For 'Domestic violence help' (dvfp = safety assistance, dv = program/group for people who experienced domestic violence)
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default = "Data needs review", choices = Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    date_firstfind = models.DateField(blank=True, null=True)
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    date_update = models.DateTimeField(default=timezone.now)
  ## Fields from source:
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120)
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=120)
    tele = models.BooleanField(blank=True, null=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=120) # TODO change to Enum??? ## Downloaded data uses abbrev (not full names)
    zip5 = models.CharField(max_length=5,blank=True, null=True) # Cannot use zip (=SAMHSA source label) due to Python keyword conflict
    zip4 = models.CharField(max_length=9,blank=True, null=True)
    county = models.CharField(max_length=120)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    intake1 = models.CharField(max_length=20, blank=True, null=True)
    intake2 = models.CharField(max_length=20, blank=True, null=True)
    website = models.URLField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    type_facility = models.CharField(max_length=10) ## Data unlikely to exceed 4 characters; reduced 120 to 10
    sa = models.BooleanField(blank=True, null=True)
    dt = models.BooleanField(blank=True, null=True)
    bu = models.BooleanField(blank=True, null=True)
    bum = models.BooleanField(blank=True, null=True)
    ub = models.BooleanField(blank=True, null=True)
    bwn = models.BooleanField(blank=True, null=True)
    bwon = models.BooleanField(blank=True, null=True)
    bmw = models.BooleanField(blank=True, null=True)
    beri = models.BooleanField(blank=True, null=True)
    bsdm = models.BooleanField(blank=True, null=True)
    db_field = models.BooleanField(blank=True, null=True)
    bmo = models.BooleanField(blank=True, null=True)
    mo = models.BooleanField(blank=True, null=True)
    mu = models.BooleanField(blank=True, null=True)
    meth = models.BooleanField(blank=True, null=True)
    mm = models.BooleanField(blank=True, null=True)
    mmw = models.BooleanField(blank=True, null=True)
    dm = models.BooleanField(blank=True, null=True)
    nu = models.BooleanField(blank=True, null=True)
    un = models.BooleanField(blank=True, null=True)
    vtrl = models.BooleanField(blank=True, null=True)
    nxn = models.BooleanField(blank=True, null=True)
    rpn = models.BooleanField(blank=True, null=True)
    otp = models.BooleanField(blank=True, null=True)
    omb = models.BooleanField(blank=True, null=True)
    otpa = models.BooleanField(blank=True, null=True)
    pain = models.BooleanField(blank=True, null=True)
    ulc = models.BooleanField(blank=True, null=True)
    moa = models.BooleanField(blank=True, null=True)
    odtx = models.BooleanField(blank=True, null=True)
    ubn = models.BooleanField(blank=True, null=True)
    hh = models.BooleanField(blank=True, null=True)
    noop = models.BooleanField(blank=True, null=True)
    nmoa = models.BooleanField(blank=True, null=True)
    cbt = models.BooleanField(blank=True, null=True)
    dbt = models.BooleanField(blank=True, null=True)
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
    odt = models.BooleanField(blank=True, null=True)
    oit = models.BooleanField(blank=True, null=True)
    ort = models.BooleanField(blank=True, null=True)
    hid = models.BooleanField(blank=True, null=True)
    hit = models.BooleanField(blank=True, null=True)
    ct = models.BooleanField(blank=True, null=True)
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
    atr = models.BooleanField(blank=True, null=True)
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
    fpsy = models.BooleanField(blank=True, null=True)
    hs = models.BooleanField(blank=True, null=True)
    nrt = models.BooleanField(blank=True, null=True)
    peer = models.BooleanField(blank=True, null=True)
    stu = models.BooleanField(blank=True, null=True)
    tcc = models.BooleanField(blank=True, null=True)
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
    site_id = models.ManyToManyField('Sites_all', through = 'sites_site_recs_lookup') ## we decided Jan 26th just to reference oid from every site Audit in sites_all Production table
  ## Fields from source: 
    program_name = models.CharField(max_length=250)
    dba = models.CharField(max_length=120,blank=True, null=True)
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=120) # TODO change to Enum??? ## Match above class; downloaded data again uses abbrev (not full names)
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####) -- extended max_length to 20 to accommodate occasional extensions
    certification = models.CharField(max_length=120)
    full_certification = models.DateField(blank=True, null=True)
  ## MATchMapper additions: 
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default = "Data needs review", choices = Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    date_firstfind = models.DateField(blank=True, null=True)
    date_lastfind = models.DateField(blank=True, null=True) ## Blank unless or until source removes record
    data_review = models.CharField(max_length=250,blank=True, null=True) # Notes from manual review, e.g. "ZIP typo: corrected 19007 to 19107..."
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_samhsa_otp'

    def __str__(self):
        return self.program_name ## Renamed to match source more closely


class Siterecs_dbhids_tad(models.Model):
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Siterecs_dbhids_sites_all_lookup')  ## we decided Jan 26th just to reference oid from every site Audit in sites_all Production table
  ## [DCS] = directly copied from source PDF. Interspersed with MATchMapper boolean additions: 
    name1 = models.CharField(max_length=120) #[DCS]: Max LEN in data = 51 char.
    coe = models.BooleanField(blank=True, null=True) ## Asterisked names (*Center of Excellence)
    ref_address = models.CharField(max_length=100, null=True) #[DCS]: Max LEN in data = 53 char.
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=30, default='Philadelphia') # Added Philadelphia as default city BY SAM
    state_usa = models.CharField(max_length=30, default='PA') ## Can replace with Enum to match above classes BY SAM
    zipcode = models.CharField(max_length=5)
    phone1 = models.CharField(max_length=20) #[DCS] but reformatted: ###-###-#### (with optional x####)
    asm = models.BooleanField(blank=True, null=True) ## Added to make page 2 entries filterable (Assessment directory)
    ba = models.BooleanField(blank=True, null=True) ## Added to make page 5 entries link-and-filterable (Bed availability! = top ask in March 2020 hackathon response)
    name_ba = models.CharField(max_length=50) #[DCS] page 5, to facilitate cross-refs | TODO: Add to model_translation.py IF frontend visibility needed (for EDITOR)
    mat_info = models.CharField(max_length=100) #[DCS]: Max LEN in data = 50 char. For line breaks, use pipe: |
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
    additional_info = models.CharField(max_length=150,blank=True, null=True) #[DCS] after separating Walk-in: Max LEN in data = 88 char. For line breaks, use pipe: |
    phone2 = models.CharField(max_length=20, blank=True, null=True) ## Added for 3 entries with second phone from additional_info
    walk_in_hours = models.CharField(max_length=80,blank=True, null=True) #[DCS] for yellow records: List '[unspecified]' if no days & times available. Max LEN in data = 38 char, but increased limit from 50 to 80 just in case.
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
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default = "Data needs review", choices = Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    data_review = models.CharField(max_length=250, null=True, blank=True) # Added null=True for now BY SAM. ## Max LEN so far = 161 char.  

    class Meta:
        managed = True
        db_table = 'siterecs_dbhids_tad'

    def __str__(self):
        #i change this to return oid instead of rec_id because rec_id doesn't exist
        #please change the returned value to rec_id if applicable later on.
        return str(self.oid)
        #return self.rec_id


class Siterecs_hfp_fqhc(models.Model): ## TODO
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = 'Siterecs_hfp_fqhc_sites_all_lookup')
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default="Data needs review", choices=Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    name_system = models.CharField(max_length=120)
    name_site = models.CharField(max_length=120)
    name_short = models.CharField(max_length=50)
    admin_office = models.BooleanField(blank=True, null=True)
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=50,blank=True, null=True)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) ## Can replace with Enum to match above classes
    zipcode = models.CharField(max_length=5)
    website = models.URLField()
    phone1 = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    phone2 = models.CharField(max_length=20,blank=True, null=True) # Format: ###-###-#### (with optional x####)
    date_firstfind = models.DateField()
    date_lastfind = models.DateField() ## Blank unless or until source removes record
    data_review = models.CharField(max_length=250)

    def __str__(self):
        #i change this to return oid instead of rec_id because rec_id doesn't exist
        #please change the returned value to rec_id if applicable later on.
        return str(self.name_short)
        #return self.rec_id


class Siterecs_other_srcs(models.Model): ## TODO (jkd): Clean up extraneous columns!! Note crucial links to other tables!!
    oid = models.IntegerField(primary_key=True)
    site_id = models.ManyToManyField('Sites_all', through = "sitesrecs_other_srcs_sitesall_lk")
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default="Data needs review", choices=Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120)
    name3 = models.CharField(max_length=120)
    website1 = models.URLField()
    website2 = models.URLField()
    street1 = models.CharField(max_length=120, null=True)
    street2 = models.CharField(max_length=120,null=True)
    city = models.CharField(max_length=30, default='Philadelphia')
    state_usa = models.CharField(max_length=30, default='PA') ## Can replace with Enum to match above classes   
    zipcode = models.CharField(max_length=5)
    fqhc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    mat_avail = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    bu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # was mat_bupe
    mu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # was mat_mtd
    nu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # was mat_ntrex
    bupe_type = models.CharField(max_length=120, blank=True)
    telehealth_avail = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    telehealth_notes = models.CharField(max_length=120, blank=True)
    insurance_notes = models.CharField(max_length=120, blank=True)
    pregnant_women_treated = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3)
    pregnant_women_notes = models.CharField(max_length=120, blank=True)
    # TODO not sure what to do about key listings
    insurance = models.CharField(blank=True, max_length=120)
    clients = models.CharField(blank=True, max_length=120)
    services = models.CharField(blank=True, max_length=120)
    setting = models.CharField(blank=True, max_length=120)
    corr_date = models.DateField(blank=True)
    corr_source = models.CharField(blank=True, max_length=120)
    corr_notes = models.CharField(blank=True, max_length=120)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_other_srcs'

    def __str__(self):
        return self.name1


class Sites_all(models.Model):
    oid = models.CharField(primary_key=True, max_length=120) # TODO integer or varchar? ## Probably serialized varchar?
    id_samhsa_ftloc = models.ManyToManyField('Siterecs_samhsa_ftloc',blank=True, null=True)
    id_samhsa_otp = models.ManyToManyField('Siterecs_samhsa_otp',blank=True, null=True)
    id_dbhids_tad = models.ManyToManyField('Siterecs_dbhids_tad',blank=True, null=True)
    id_ba_tad
    id_hfp_fqhc = models.ManyToManyField('Siterecs_hfp_fqhc',blank=True, null=True) ## Renamed to make all inner-MATchMapper links start with id_
    id_hrsa_fqhc
    ## id_other_srcs = models.ManyToManyField('Siterecs_other_srcs',blank=True, null=True)  ## TODO: reincorporate after IDs are checked
    name1 = models.CharField(max_length=120) ## WAS name_program
    name2 = models.CharField(max_length=120) ## WAS name_site
    website1 = models.URLField() ## Important addition: functions with address fields as composite primary key
    website2 = models.URLField(null=True) # Added just in case (to match siterecs_other_srcs)
    phone1 = models.CharField(max_length=30, null=True, blank=True)  ## Format: ###-###-#### with optional x####
    phone2 = models.CharField(max_length=30, null=True, blank=True)  ## Format: ###-###-#### with optional x####
    street1 = models.CharField(max_length=120, null=True, blank=True) 
    street2 = models.CharField(max_length=120,blank=True, null=True)
    city = models.CharField(max_length=30, default='Philadelphia')
    state_usa = models.CharField(max_length=30, default='PA') ## Can replace with Enum to match above classes
    zipcode = models.CharField(max_length=120)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    ## TODO: Identify how to link relevant fields from Audit tables to Enum fields below!! June 2021: Revising to consistent fieldnames helps
    mat_avail = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    bu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    mu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    nu = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    fqhc = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    prim_care = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    telehealth = models.CharField(max_length=20, default = 'Unclear', choices = Multi_Choices_Enum3) # June 6: empty for now
    archival_only = models.BooleanField(blank=True, null=True) ## For admin (EDITOR) to mark records not approved for FINDER
    why_hidden = models.CharField(max_length=150, default = "Data needs review", choices = Multi_Choices_EnumWhyHide, blank=True) # Require only if archival_only = True
    data_review = models.CharField(max_length=250, null=True, blank=True) # Added per TODO in data-load sheet
    ## TODO: Add other fields for key filters (insurance, services, etc.)!!
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'sites_all'

    def __str__(self):
        return ', '.join([self.oid, self.name1, self.name2]) ## Updated to match renaming consistency


class sitesrecs_other_srcs_sitesall_lk(models.Model):
    samhsa_oid = models.ForeignKey(Siterecs_other_srcs, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all,on_delete=models.CASCADE)

class sites_site_recs_lookup(models.Model):
    samhsa_oid = models.ForeignKey(Siterecs_samhsa_otp, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all,on_delete=models.CASCADE)

class Siterecs_dbhids_sites_all_lookup(models.Model):
    samhsa_oid = models.ForeignKey(Siterecs_dbhids_tad, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all,on_delete=models.CASCADE)

class Siterecs_hfp_fqhc_sites_all_lookup(models.Model):
    samhsa_oid = models.ForeignKey(Siterecs_hfp_fqhc, on_delete=models.CASCADE)
    sites_all_id = models.ForeignKey(Sites_all,on_delete=models.CASCADE)

class Sites_ftloc(models.Model):
    samhsa_oid = models.ForeignKey(Siterecs_samhsa_ftloc, on_delete=models.CASCADE)
    sites_all_id= models.ForeignKey(Sites_all, on_delete=models.CASCADE)


# class Address(models.Model):
#     id = models.CharField(primary_key=True, max_length=30)
#     listed_street1 = models.CharField(max_length=50, blank=True, null=True)
#     listed_street2 = models.CharField(max_length=50, blank=True, null=True)
#     city = models.CharField(max_length=30, blank=True, null=True)
#     state_address = models.CharField(max_length=30, blank=True, null=True)
#     zip = models.CharField(max_length=10, blank=True, null=True)
#     region1 = models.CharField(max_length=30, blank=True, null=True)
#     region2 = models.CharField(max_length=30, blank=True, null=True)
#     primary_address = models.BooleanField(blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'address'

#     def __str__(self):
#         return ', '.join([self.listed_street1, self.listed_street2, self.city, self.state_address, self.zip, self.region1, self.region2])


# class Affiliate(models.Model):
#     affiliate_id = models.CharField(primary_key=True, max_length=30)
#     shortname = models.CharField(max_length=30, blank=True, null=True)
#     listed_name = models.CharField(max_length=75, blank=True, null=True)
#     provider = models.ForeignKey('Provider', models.DO_NOTHING, blank=True, null=True)
#     site = models.ForeignKey('Site', models.DO_NOTHING, blank=True, null=True)
#     ejpt_phila = models.CharField(max_length=30, blank=True, null=True)
#     mat_types = models.FloatField(blank=True, null=True)
#     hours = models.IntegerField(blank=True, null=True)
#     other_svcs = models.IntegerField(blank=True, null=True)
#     url = models.IntegerField(blank=True, null=True)
#     cert = models.IntegerField(blank=True, null=True)
#     num_bupr = models.IntegerField(blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'affiliate'

#     def __str__(self):
#         return self.listed_name

# class Email(models.Model):
#     id = models.CharField(primary_key=True, max_length=30)
#     primary_email = models.CharField(max_length=50, blank=True, null=True)
#     secondary_email = models.CharField(max_length=50, blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'email'

#     def __str__(self):
#         return self.primary_email


# class Licence(models.Model):
#     provider = models.OneToOneField('Provider', models.DO_NOTHING, primary_key=True)
#     cert_state = models.CharField(max_length=5, blank=True, null=True)
#     cert_date = models.DateField(blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'licence'

#     def __str__(self):
#         return self.provider + ' ' + self.cert_state


# class Npi(models.Model):
#     npi = models.IntegerField(primary_key=True)
#     provider = models.ForeignKey('Provider', models.DO_NOTHING)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'npi'

#     def __str__(self):
#         return self.npi


# class Phone(models.Model):
#     id = models.CharField(primary_key=True, max_length=30)
#     phone_1 = models.CharField(max_length=15, blank=True, null=True)
#     phone_2 = models.CharField(max_length=15, blank=True, null=True)
#     intake_phone_1 = models.CharField(max_length=15, blank=True, null=True)
#     intake_phone_2 = models.CharField(max_length=15, blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'phone'

#     def __str__(self):
#         return self.phone_1


# class ProvSiteRef(models.Model):
#     provider = models.ForeignKey('Provider', models.DO_NOTHING, blank=True, null=True)
#     site = models.ForeignKey('Site', models.DO_NOTHING, blank=True, null=True)

#     class Meta:
#         managed = True
#         db_table = 'prov_site_ref'

#     def __str__(self):
#         return self.provider + ' ' + self.site


# class Provider(models.Model):
#     provider_id = models.CharField(primary_key=True, max_length=30, unique=True, default=increment_provider_id, editable=False)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     prefix_name = models.CharField(max_length=5, blank=True, null=True)
#     suffix = models.CharField(max_length=20, blank=True, null=True)
#     degree = models.CharField(max_length=15, blank=True, null=True)
#     who_id = models.CharField(max_length=20, blank=True, null=True)
#     est_rx_cap = models.IntegerField(blank=True, null=True)
#     patient_max = models.CharField(max_length=15, blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'provider'

#     def __str__(self):
#         return self.first_name + ' ' + self.last_name


# class Site(models.Model):
#     site_id = models.CharField(primary_key=True, max_length=30)
#     shortname = models.CharField(max_length=20, blank=True, null=True)
#     listed_name = models.CharField(max_length=75, blank=True, null=True)
#     name2 = models.CharField(max_length=75, blank=True, null=True)
#     website = models.CharField(max_length=30, blank=True, null=True)
#     intake_prompt = models.CharField(max_length=30, blank=True, null=True)
#     otpa = models.BooleanField(blank=True, null=True)
#     otp = models.BooleanField(blank=True, null=True)
#     bu = models.BooleanField(blank=True, null=True)
#     ub = models.BooleanField(blank=True, null=True)
#     bum = models.BooleanField(blank=True, null=True)
#     bmw = models.BooleanField(blank=True, null=True)
#     bsdm = models.BooleanField(blank=True, null=True)
#     bwn = models.BooleanField(blank=True, null=True)
#     bwon = models.BooleanField(blank=True, null=True)
#     beri = models.BooleanField(blank=True, null=True)
#     db_field = models.BooleanField(db_column='db_', blank=True, null=True)  # Changed source field label to avoid SQL keyword conflict
#     mu = models.BooleanField(blank=True, null=True)
#     meth = models.BooleanField(blank=True, null=True)
#     mm = models.BooleanField(blank=True, null=True)
#     mmw = models.BooleanField(blank=True, null=True)
#     dm = models.BooleanField(blank=True, null=True)
#     nu = models.BooleanField(blank=True, null=True)
#     un = models.BooleanField(blank=True, null=True)
#     nxn = models.BooleanField(blank=True, null=True)
#     vtrl = models.BooleanField(blank=True, null=True)
#     rpn = models.BooleanField(blank=True, null=True)
#     dt = models.BooleanField(blank=True, null=True)
#     any_mat = models.IntegerField(blank=True, null=True)
#     moa = models.BooleanField(blank=True, null=True)
#     noop = models.BooleanField(blank=True, null=True)
#     nmoa = models.BooleanField(blank=True, null=True)
#     pain = models.BooleanField(blank=True, null=True)
#     hh = models.BooleanField(blank=True, null=True)
#     ubn = models.BooleanField(blank=True, null=True)
#     cbt = models.BooleanField(blank=True, null=True)
#     dbt = models.BooleanField(blank=True, null=True)
#     saca = models.BooleanField(blank=True, null=True)
#     trc = models.BooleanField(blank=True, null=True)
#     rebt = models.BooleanField(blank=True, null=True)
#     smon = models.BooleanField(blank=True, null=True)
#     smpd = models.BooleanField(blank=True, null=True)
#     smop = models.BooleanField(blank=True, null=True)
#     hi = models.BooleanField(blank=True, null=True)
#     res = models.BooleanField(blank=True, null=True)
#     op = models.BooleanField(blank=True, null=True)
#     rs = models.BooleanField(blank=True, null=True)
#     rl = models.BooleanField(blank=True, null=True)
#     rd = models.BooleanField(blank=True, null=True)
#     od = models.BooleanField(blank=True, null=True)
#     omb = models.BooleanField(blank=True, null=True)
#     odt = models.BooleanField(blank=True, null=True)
#     oit = models.BooleanField(blank=True, null=True)
#     ort = models.BooleanField(blank=True, null=True)
#     hid = models.BooleanField(blank=True, null=True)
#     hit = models.BooleanField(blank=True, null=True)
#     ct = models.BooleanField(blank=True, null=True)
#     gh = models.BooleanField(blank=True, null=True)
#     psyh = models.BooleanField(blank=True, null=True)
#     vamc = models.BooleanField(blank=True, null=True)
#     tbg = models.BooleanField(blank=True, null=True)
#     ih = models.BooleanField(blank=True, null=True)
#     stg = models.BooleanField(blank=True, null=True)
#     lccg = models.BooleanField(blank=True, null=True)
#     ddf = models.BooleanField(blank=True, null=True)
#     stag = models.BooleanField(blank=True, null=True)
#     stmh = models.BooleanField(blank=True, null=True)
#     stdh = models.BooleanField(blank=True, null=True)
#     hla = models.BooleanField(blank=True, null=True)
#     jc = models.BooleanField(blank=True, null=True)
#     carf = models.BooleanField(blank=True, null=True)
#     ncqa = models.BooleanField(blank=True, null=True)
#     coa = models.BooleanField(blank=True, null=True)
#     hfap = models.BooleanField(blank=True, null=True)
#     np = models.BooleanField(blank=True, null=True)
#     sf = models.BooleanField(blank=True, null=True)
#     md = models.BooleanField(blank=True, null=True)
#     mc = models.BooleanField(blank=True, null=True)
#     si = models.BooleanField(blank=True, null=True)
#     pi_field = models.BooleanField(db_column='pi_', blank=True, null=True)  # Changed source field label to avoid SQL keyword conflict
#     mi = models.BooleanField(blank=True, null=True)
#     atr = models.BooleanField(blank=True, null=True)
#     fsa = models.BooleanField(blank=True, null=True)
#     ss = models.BooleanField(blank=True, null=True)
#     pa = models.BooleanField(blank=True, null=True)
#     ah = models.BooleanField(blank=True, null=True)
#     sp = models.BooleanField(blank=True, null=True)
#     co = models.BooleanField(blank=True, null=True)
#     gl = models.BooleanField(blank=True, null=True)
#     vet = models.BooleanField(blank=True, null=True)
#     adm = models.BooleanField(blank=True, null=True)
#     mf = models.BooleanField(blank=True, null=True)
#     cj = models.BooleanField(blank=True, null=True)
#     se = models.BooleanField(blank=True, null=True)
#     ad = models.BooleanField(blank=True, null=True)
#     pw = models.BooleanField(blank=True, null=True)
#     wn = models.BooleanField(blank=True, null=True)
#     mn = models.BooleanField(blank=True, null=True)
#     hv = models.BooleanField(blank=True, null=True)
#     trma = models.BooleanField(blank=True, null=True)
#     xa = models.BooleanField(blank=True, null=True)
#     dv = models.BooleanField(blank=True, null=True)
#     tay = models.BooleanField(blank=True, null=True)
#     nsc = models.BooleanField(blank=True, null=True)
#     adtx = models.BooleanField(blank=True, null=True)
#     bdtx = models.BooleanField(blank=True, null=True)
#     cdtx = models.BooleanField(blank=True, null=True)
#     mdtx = models.BooleanField(blank=True, null=True)
#     odtx = models.BooleanField(blank=True, null=True)
#     tgd = models.BooleanField(blank=True, null=True)
#     tid = models.BooleanField(blank=True, null=True)
#     ico = models.BooleanField(blank=True, null=True)
#     gco = models.BooleanField(blank=True, null=True)
#     fco = models.BooleanField(blank=True, null=True)
#     mco = models.BooleanField(blank=True, null=True)
#     twfa = models.BooleanField(blank=True, null=True)
#     bia = models.BooleanField(blank=True, null=True)
#     cmi = models.BooleanField(blank=True, null=True)
#     moti = models.BooleanField(blank=True, null=True)
#     ang = models.BooleanField(blank=True, null=True)
#     mxm = models.BooleanField(blank=True, null=True)
#     crv = models.BooleanField(blank=True, null=True)
#     relp = models.BooleanField(blank=True, null=True)
#     bc = models.BooleanField(blank=True, null=True)
#     chld = models.BooleanField(blank=True, null=True)
#     yad = models.BooleanField(blank=True, null=True)
#     adlt = models.BooleanField(blank=True, null=True)
#     fem = models.BooleanField(blank=True, null=True)
#     male = models.BooleanField(blank=True, null=True)
#     bmo = models.BooleanField(blank=True, null=True)
#     mo = models.BooleanField(blank=True, null=True)
#     du = models.BooleanField(blank=True, null=True)
#     duo = models.BooleanField(blank=True, null=True)
#     acc = models.BooleanField(blank=True, null=True)
#     acm = models.BooleanField(blank=True, null=True)
#     acu = models.BooleanField(blank=True, null=True)
#     add_field = models.BooleanField(db_column='add_', blank=True, null=True)  # Changed source field label to avoid SQL keyword conflict
#     baba = models.BooleanField(blank=True, null=True)
#     ccc = models.BooleanField(blank=True, null=True)
#     cmha = models.BooleanField(blank=True, null=True)
#     csaa = models.BooleanField(blank=True, null=True)
#     daut = models.BooleanField(blank=True, null=True)
#     dp = models.BooleanField(blank=True, null=True)
#     dsf = models.BooleanField(blank=True, null=True)
#     dvfp = models.BooleanField(blank=True, null=True)
#     eih = models.BooleanField(blank=True, null=True)
#     emp = models.BooleanField(blank=True, null=True)
#     haec = models.BooleanField(blank=True, null=True)
#     heoh = models.BooleanField(blank=True, null=True)
#     hivt = models.BooleanField(blank=True, null=True)
#     isc = models.BooleanField(blank=True, null=True)
#     itu = models.BooleanField(blank=True, null=True)
#     mhs = models.BooleanField(blank=True, null=True)
#     mpd = models.BooleanField(blank=True, null=True)
#     opc = models.BooleanField(blank=True, null=True)
#     sae = models.BooleanField(blank=True, null=True)
#     shb = models.BooleanField(blank=True, null=True)
#     shc = models.BooleanField(blank=True, null=True)
#     shg = models.BooleanField(blank=True, null=True)
#     smhd = models.BooleanField(blank=True, null=True)
#     ssa = models.BooleanField(blank=True, null=True)
#     ssd = models.BooleanField(blank=True, null=True)
#     stdt = models.BooleanField(blank=True, null=True)
#     ta = models.BooleanField(blank=True, null=True)
#     taec = models.BooleanField(blank=True, null=True)
#     tbs = models.BooleanField(blank=True, null=True)
#     cm = models.BooleanField(blank=True, null=True)
#     fpsy = models.BooleanField(blank=True, null=True)
#     hs = models.BooleanField(blank=True, null=True)
#     nrt = models.BooleanField(blank=True, null=True)
#     peer = models.BooleanField(blank=True, null=True)
#     stu = models.BooleanField(blank=True, null=True)
#     tcc = models.BooleanField(blank=True, null=True)
#     pvtp = models.BooleanField(blank=True, null=True)
#     pvtn = models.BooleanField(blank=True, null=True)
#     vo = models.BooleanField(blank=True, null=True)
#     sumh = models.BooleanField(blank=True, null=True)
#     inpe = models.BooleanField(blank=True, null=True)
#     rpe = models.BooleanField(blank=True, null=True)
#     pc = models.BooleanField(blank=True, null=True)
#     naut = models.BooleanField(blank=True, null=True)
#     nmaut = models.BooleanField(blank=True, null=True)
#     acma = models.BooleanField(blank=True, null=True)
#     pmat = models.BooleanField(blank=True, null=True)
#     auinpe = models.BooleanField(blank=True, null=True)
#     aurpe = models.BooleanField(blank=True, null=True)
#     aupc = models.BooleanField(blank=True, null=True)
#     ulc = models.BooleanField(blank=True, null=True)
#     mhiv = models.BooleanField(blank=True, null=True)
#     mhcv = models.BooleanField(blank=True, null=True)
#     lfxd = models.BooleanField(blank=True, null=True)
#     clnd = models.BooleanField(blank=True, null=True)
#     copsu = models.BooleanField(blank=True, null=True)
#     daof = models.BooleanField(blank=True, null=True)
#     mst = models.BooleanField(blank=True, null=True)
#     noe = models.BooleanField(blank=True, null=True)
#     ofd = models.BooleanField(blank=True, null=True)
#     rc = models.BooleanField(blank=True, null=True)
#     piec = models.BooleanField(blank=True, null=True)
#     mdet = models.BooleanField(blank=True, null=True)
#     voc = models.BooleanField(blank=True, null=True)
#     hav = models.BooleanField(blank=True, null=True)
#     hbv = models.BooleanField(blank=True, null=True)
#     audo = models.BooleanField(blank=True, null=True)
#     f17 = models.BooleanField(blank=True, null=True)
#     f19 = models.BooleanField(blank=True, null=True)
#     f25 = models.BooleanField(blank=True, null=True)
#     f28 = models.BooleanField(blank=True, null=True)
#     f30 = models.BooleanField(blank=True, null=True)
#     f31 = models.BooleanField(blank=True, null=True)
#     f35 = models.BooleanField(blank=True, null=True)
#     f36 = models.BooleanField(blank=True, null=True)
#     f37 = models.BooleanField(blank=True, null=True)
#     f4 = models.BooleanField(blank=True, null=True)
#     f42 = models.BooleanField(blank=True, null=True)
#     f43 = models.BooleanField(blank=True, null=True)
#     f47 = models.BooleanField(blank=True, null=True)
#     f66 = models.BooleanField(blank=True, null=True)
#     f67 = models.BooleanField(blank=True, null=True)
#     f70 = models.BooleanField(blank=True, null=True)
#     f81 = models.BooleanField(blank=True, null=True)
#     f92 = models.BooleanField(blank=True, null=True)
#     n13 = models.BooleanField(blank=True, null=True)
#     n18 = models.BooleanField(blank=True, null=True)
#     n23 = models.BooleanField(blank=True, null=True)
#     n24 = models.BooleanField(blank=True, null=True)
#     n40 = models.BooleanField(blank=True, null=True)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'site'

#     def __str__(self):
#         return self.listed_name


# class Xwaiver(models.Model):
#     dea_num = models.CharField(primary_key=True, max_length=10)
#     provider = models.ForeignKey(Provider, models.DO_NOTHING)
#     date_update = models.DateTimeField(default=timezone.now)

#     class Meta:
#         managed = True
#         db_table = 'xwaiver'

#     def __str__(self):
#         return self.dea_num
