from django.db import models
from django.utils import timezone

# def increment_provider_id():
#     last_provider = Provider.objects.all().order_by('provider_id').last()
#     if not last_provider:
#         return 'P00000000'

#     provider_id = last_provider.provider_id
#     provider_int = provider_id[1:]
#     new_provider_int = int(provider_int) + 1
#     new_provider_id = 'P' + str(new_provider_int).zfill(8)
#     return new_provider_id





class Sitecodes_samhsa_ftloc(models.Model):
    service_code = models.CharField(primary_key=True, max_length=10)
    category_code = models.CharField(max_length=6)
    category_name = models.CharField(max_length=70)
    service_name = models.CharField(max_length=120)
    service_description = models.CharField(max_length=999)
    sa_listings_match = models.CharField(max_length=15) ## Our addition
    mm_filters = models.CharField(max_length=15) ## Our addition -- renamed _highlights to _filters here and in data table
    filter_seq = models.IntegerField() ## NEW: Our addition -- fill col from ForMostFilters tab; TODO: does () need parameters??
    ui_reference = models.CharField(max_length=50) ## NEW: Our addition -- fill col from ForMostFilters tab
    date_update = models.DateTimeField(default=timezone.now) ## Our addition

    class Meta:
        managed = True
        db_table = 'sitecodes_samhsa_ftloc'

    def __str__(self):
        return self.service_name

# Gave all Siterecs_ classes an oid (object id for ease of abstraction for backend) ## = Audit tables

class Siterecs_samhsa_ftloc(models.Model): ## TODO: In all the Boolean fields, shouldn't we have blank=False, null=False (neither True)??
    oid = models.IntegerField(primary_key=True)
    ###site_id = models.ManyToManyField('Sites_all', through = Sites_ftloc) ## we decided Jan 26th just to reference oid from every site Audit in sites_all Production table
    date_firstfind = models.DateField(blank=True, null=True)
    date_lastfind = models.DateField(blank=True, null=True)
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120)
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=120) # TODO change to Enum??? ## Here and for other state_usa: Check whether downloaded data uses abbrev or full names
    zip5 = models.CharField(max_length=5,blank=True, null=True)
    zip4 = models.CharField(max_length=9,blank=True, null=True)
    county = models.CharField(max_length=120)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    phone_intake1 = models.CharField(max_length=20,blank=True, null=True)
    phone_intake2 = models.CharField(max_length=20,blank=True, null=True)
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
    mat_bupe = models.IntegerField(blank=True, null=True)
    mat_ntrex = models.IntegerField(blank=True, null=True)
    mat_mtd = models.IntegerField(blank=True, null=True)
    mat_misc = models.IntegerField(blank=True, null=True)
    mat_avail = models.IntegerField(blank=True, null=True)



    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_samhsa_ftloc'

    def __str__(self):
        return ', '.join([self.street1, self.street2, self.city, self.state_usa, self.zip5])

class Siterecs_samhsa_otp(models.Model):
    oid = models.IntegerField(primary_key=True)
    ## site_id = models.ForeignKey('Sites_all', models.DO_NOTHING) ## we decided Jan 26th just to reference oid from every site Audit in sites_all Production table
    name_program = models.CharField(max_length=250)
    name_dba = models.CharField(max_length=120,blank=True, null=True)
    street_address = models.CharField(max_length=120)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=120) # TODO change to Enum??? ## Match above class
    zipcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####) -- extended max_length to 20 to accommodate occasional extensions
    certification_status = models.CharField(max_length=120)
    date_full_certification = models.DateField(blank=True, null=True)
    date_firstfind = models.DateField()
    date_lastfind = models.DateField()
    data_review = models.CharField(max_length=250,blank=True, null=True) # TODO what is this again??? ## Notes from manual review, e.g. "ZIP typo: corrected 19007 to 19107..."
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'siterecs_samhsa_otp'

    def __str__(self):
        return self.name_program

class Siterecs_dbhids_tad(models.Model): ## TODO (jkd): Update fields to match actual data compilation!!
    oid = models.IntegerField(primary_key=True)
    ## site_id = models.ForeignKey('Sites_all', models.DO_NOTHING)  ## we decided Jan 26th just to reference oid from every site Audit in sites_all Production table
    name_listed = models.CharField(max_length=120)
    street_address = models.CharField(max_length=120)
    loc_suppl = models.CharField(max_length=50)
    zip5 = models.CharField(max_length=5)
    phone = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    mat_info = models.CharField(max_length=100) ## Current max = 50char, so 100 is just for flex
    mat_bupe = models.BooleanField(blank=False) ## blank=False preferred: ok? (same for each BooleanField in this class)
    mat_mtd = models.BooleanField(blank=False)
    mat_ntrex = models.BooleanField(blank=False)
    iop = models.BooleanField(blank=False)
    op = models.BooleanField(blank=False)
    mh_tx = models.BooleanField(blank=False)
    wih_induction = models.BooleanField(blank=False)
    # walk_in_hours ## TODO: Retain for reference or delete as unreliable?
    coe = models.BooleanField(blank=False)
    other_notes = models.CharField(max_length=150) ## Current max = 111char but second = just 52char
    date_firstfind = models.DateField()
    date_lastfind = models.DateField()
    data_review = models.CharField(max_length=250) # TODO what is this again??? ## As above (notes from manual review)
    date_update = models.DateTimeField(default=timezone.now) ## TODO why/is this necessary for this table? (source = PDF with data updated only 1x/yr or less)

    class Meta:
        managed = True
        db_table = 'siterecs_dbhids_tad'

    def __str__(self):
        return self.rec_id

class Siterecs_hfp_fqhc(models.Model): ## TODO
    oid = models.IntegerField(primary_key=True)
    name_short = models.CharField(max_length=50)
    name_system = models.CharField(max_length=120)
    name_site = models.CharField(max_length=120)
    admin_office = models.BooleanField(blank=False) ## blank=False preferred: ok?
    street_address = models.CharField(max_length=120)
    loc_suppl = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state_usa = models.CharField(max_length=30) ## Can replace with Enum to match above classes
    zip5 = models.CharField(max_length=5)
    website = models.URLField()
    phone1 = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    phone2 = models.CharField(max_length=20) # Format: ###-###-#### (with optional x####)
    ## why_hidden = models... ## TODO: Add as Enum (same 5 options as in Sites_all: "Site closed", "Data needs review", "Not a practice site", "Record redundant", "Other")
    ## mat_avail = models... ## TODO: Add as Enum with 3 options: "Yes", "Unclear", "No"
    date_firstfind = models.DateField()
    date_lastfind = models.DateField()
    data_review = models.CharField(max_length=250)

class Siterecs_other_srcs(models.Model): ## TODO (jkd): Clean up extraneous columns!! Note crucial links to other tables!!
    oid = models.IntegerField(primary_key=True)
    # site_id = models.ForeignKey('Sites_all', models.DO_NOTHING) DO WE NEED site_id for this? ## As in all the other Site Audit tables: nixed Jan 26th
    name1 = models.CharField(max_length=120)
    name2 = models.CharField(max_length=120)
    website1 = models.URLField()
    website2 = models.URLField()
    street_address = models.CharField(max_length=120)
    address_suppl = models.CharField(max_length=120)
    zip5 = models.CharField(max_length=5)
    fqhc = models.BooleanField(blank=True) ## Change all BooleanFields for this table to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No) -- blank="Unclear"!!
    mat_avail = models.BooleanField(blank=True)
    mat_bupe = models.BooleanField(blank=True)
    mat_mtd = models.BooleanField(blank=True)
    mat_ntrex = models.BooleanField(blank=True)
    bupe_type = models.CharField(max_length=120, blank=True)
    telehealth_avail = models.CharField(max_length=120, blank=True) # TODO should this be boolean too?
    telehealth_notes = models.CharField(max_length=120, blank=True)
    insurance_notes = models.CharField(max_length=120, blank=True)
    pregnant_women_treated = models.CharField(max_length=120, blank=True) # TODO should this be boolean too?
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



Multi_Choices_Enum3 = [
('Yes','Yes'),
('No','No'),
('Unclear','Unclear'),
]

Multi_Choices_Enum5 = [
('Site closed','Site closed'),
('Data needs review','Data needs review'),
('Not a practice site','Not a practice site'),
('Record redundant' ,'Record redundant'),
('Other','Other'),
]



class Sites_all(models.Model):
    oid = models.CharField(primary_key=True, max_length=120) # TODO integer or varchar? ## Probably serialized varchar?
    samhsa_ftloc_id = models.ManyToManyField('Siterecs_samhsa_ftloc')

    #samhsa_ftloc_id = models.ForeignKey('Siterecs_samhsa_ftloc', blank=True, null=True,on_delete=models.CASCADE)
    samhsa_otp_id = models.ManyToManyField('Siterecs_samhsa_otp', blank=True, null=True)
    dbhids_tad_id = models.ForeignKey('Siterecs_dbhids_tad', blank=True, null=True,on_delete=models.CASCADE)
    hfp_fqhc_id = models.ForeignKey('Siterecs_hfp_fqhc', blank=True, null=True,on_delete=models.CASCADE) ## Added
    other_srcs_id = models.ForeignKey('Siterecs_other_srcs', blank=True, null=True,on_delete=models.CASCADE)
    name_program = models.CharField(max_length=120)
    name_site = models.CharField(max_length=120)
    url_site = models.URLField() ## Important addition: functions with address fields as composite primary key
    street_address = models.CharField(max_length=120)
    address_suppl = models.CharField(max_length=120)
    zip5 = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()
    ## TODO: Identify how to link relevant fields from Audit tables to Enum fields below!!
    mat_avail = models.CharField(max_length = 20, default = 'Unclear', choices = Multi_Choices_Enum3) ## TODO: Change to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    mat_bupe = models.CharField(max_length = 20, default = 'Unclear', choices = Multi_Choices_Enum3) ## TODO: Change to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    mat_mtd = models.CharField(max_length = 20, default = 'Unclear', choices = Multi_Choices_Enum3) ## TODO: Change to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    mat_ntrex = models.CharField(max_length = 20, default = 'Unclear', choices = Multi_Choices_Enum3) ## TODO: Change to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    fqhc = models.CharField(max_length = 20, default = 'Unclear', choices = Multi_Choices_Enum3) ## TODO: Change to Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    ## primary_care = models...  ## TODO: Add as Enum with 3 options: TRUE, Unclear, FALSE (or Yes, Unclear, No)
    archival_only = models.BooleanField(blank=True) ## Added to mark records not approved for Finder listings
    ## why_hidden = models... ## TODO: Add as Enum to identify reason(s) for non-approval (5 options to start: "Site closed", "Data needs review", "Not a practice site", "Record redundant", "Other")
    ## TODO: Add other fields for key filters (age, insurance, services, etc.)!!
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'sites_all'

    def __str__(self):
        return self.name_site



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
#     db_field = models.BooleanField(db_column='db_', blank=True, null=True)  # Field renamed because it ended with '_'.
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
#     pi_field = models.BooleanField(db_column='pi_', blank=True, null=True)  # Field renamed because it ended with '_'.
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
#     add_field = models.BooleanField(db_column='add_', blank=True, null=True)  # Field renamed because it ended with '_'.
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
