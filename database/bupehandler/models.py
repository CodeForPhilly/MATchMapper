from django.db import models
from django.utils import timezone

def increment_provider_id():
    last_provider = Provider.objects.all().order_by('provider_id').last()
    if not last_provider:
        return 'P00000000'

    provider_id = last_provider.provider_id
    provider_int = provider_id[1:]
    new_provider_int = int(provider_int) + 1
    new_provider_id = 'P' + str(new_provider_int).zfill(8)
    return new_provider_id

class Address(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    listed_street1 = models.CharField(max_length=50, blank=True, null=True)
    listed_street2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state_address = models.CharField(max_length=30, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    region1 = models.CharField(max_length=30, blank=True, null=True)
    region2 = models.CharField(max_length=30, blank=True, null=True)
    primary_address = models.BooleanField(blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'address'

    def __str__(self):
        return ', '.join([self.listed_street1, self.listed_street2, self.city, self.state_address, self.zip, self.region1, self.region2])


class Affiliate(models.Model):
    affiliate_id = models.CharField(primary_key=True, max_length=30)
    shortname = models.CharField(max_length=30, blank=True, null=True)
    listed_name = models.CharField(max_length=75, blank=True, null=True)
    provider = models.ForeignKey('Provider', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('Site', models.DO_NOTHING, blank=True, null=True)
    ejpt_phila = models.CharField(max_length=30, blank=True, null=True)
    mat_types = models.FloatField(blank=True, null=True)
    hours = models.IntegerField(blank=True, null=True)
    other_svcs = models.IntegerField(blank=True, null=True)
    url = models.IntegerField(blank=True, null=True)
    cert = models.IntegerField(blank=True, null=True)
    num_bupr = models.IntegerField(blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'affiliate'

    def __str__(self):
        return self.listed_name

class Email(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    primary_email = models.CharField(max_length=50, blank=True, null=True)
    secondary_email = models.CharField(max_length=50, blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'email'

    def __str__(self):
        return self.primary_email


class Licence(models.Model):
    provider = models.OneToOneField('Provider', models.DO_NOTHING, primary_key=True)
    cert_state = models.CharField(max_length=5, blank=True, null=True)
    cert_date = models.DateField(blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'licence'

    def __str__(self):
        return self.provider + ' ' + self.cert_state


class Npi(models.Model):
    npi = models.IntegerField(primary_key=True)
    provider = models.ForeignKey('Provider', models.DO_NOTHING)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'npi'
    
    def __str__(self):
        return self.npi


class Phone(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    phone_1 = models.CharField(max_length=15, blank=True, null=True)
    phone_2 = models.CharField(max_length=15, blank=True, null=True)
    intake_phone_1 = models.CharField(max_length=15, blank=True, null=True)
    intake_phone_2 = models.CharField(max_length=15, blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'phone'

    def __str__(self):
        return self.phone_1


class ProvSiteRef(models.Model):
    provider = models.ForeignKey('Provider', models.DO_NOTHING, blank=True, null=True)
    site = models.ForeignKey('Site', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'prov_site_ref'

    def __str__(self):
        return self.provider + ' ' + self.site


class Provider(models.Model):
    provider_id = models.CharField(primary_key=True, max_length=30, unique=True, default=increment_provider_id, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    prefix_name = models.CharField(max_length=5, blank=True, null=True)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    degree = models.CharField(max_length=15, blank=True, null=True)
    who_id = models.CharField(max_length=20, blank=True, null=True)
    est_rx_cap = models.IntegerField(blank=True, null=True)
    patient_max = models.CharField(max_length=15, blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'provider'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Site(models.Model):
    site_id = models.CharField(primary_key=True, max_length=30)
    shortname = models.CharField(max_length=20, blank=True, null=True)
    listed_name = models.CharField(max_length=75, blank=True, null=True)
    name2 = models.CharField(max_length=75, blank=True, null=True)
    website = models.CharField(max_length=30, blank=True, null=True)
    intake_prompt = models.CharField(max_length=30, blank=True, null=True)
    otpa = models.BooleanField(blank=True, null=True)
    otp = models.BooleanField(blank=True, null=True)
    bu = models.BooleanField(blank=True, null=True)
    ub = models.BooleanField(blank=True, null=True)
    bum = models.BooleanField(blank=True, null=True)
    bmw = models.BooleanField(blank=True, null=True)
    bsdm = models.BooleanField(blank=True, null=True)
    bwn = models.BooleanField(blank=True, null=True)
    bwon = models.BooleanField(blank=True, null=True)
    beri = models.BooleanField(blank=True, null=True)
    db_field = models.BooleanField(db_column='db_', blank=True, null=True)  # Field renamed because it ended with '_'.
    mu = models.BooleanField(blank=True, null=True)
    meth = models.BooleanField(blank=True, null=True)
    mm = models.BooleanField(blank=True, null=True)
    mmw = models.BooleanField(blank=True, null=True)
    dm = models.BooleanField(blank=True, null=True)
    nu = models.BooleanField(blank=True, null=True)
    un = models.BooleanField(blank=True, null=True)
    nxn = models.BooleanField(blank=True, null=True)
    vtrl = models.BooleanField(blank=True, null=True)
    rpn = models.BooleanField(blank=True, null=True)
    dt = models.BooleanField(blank=True, null=True)
    any_mat = models.IntegerField(blank=True, null=True)
    moa = models.BooleanField(blank=True, null=True)
    noop = models.BooleanField(blank=True, null=True)
    nmoa = models.BooleanField(blank=True, null=True)
    pain = models.BooleanField(blank=True, null=True)
    hh = models.BooleanField(blank=True, null=True)
    ubn = models.BooleanField(blank=True, null=True)
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
    omb = models.BooleanField(blank=True, null=True)
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
    pi_field = models.BooleanField(db_column='pi_', blank=True, null=True)  # Field renamed because it ended with '_'.
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
    add_field = models.BooleanField(db_column='add_', blank=True, null=True)  # Field renamed because it ended with '_'.
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
    n40 = models.BooleanField(blank=True, null=True)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'site'

    def __str__(self):
        return self.listed_name


class Xwaiver(models.Model):
    dea_num = models.CharField(primary_key=True, max_length=10)
    provider = models.ForeignKey(Provider, models.DO_NOTHING)
    date_update = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'xwaiver'

    def __str__(self):
        return self.dea_num
