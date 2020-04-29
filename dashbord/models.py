from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AllDataBase(models.Model):
    data_base_type = models.ForeignKey('DataBaseType', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255)
    techname = models.CharField(max_length=64)
    datecreation = models.DateTimeField()
    active = models.BooleanField()
    deletedate = models.DateTimeField(blank=True, null=True)
    emailfield = models.CharField(max_length=255, blank=True, null=True)
    mobilephonefield = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    displayjoin = models.BooleanField(blank=True, null=True)
    datelastcount = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_data_base'


class AllDataBaseStats(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    optin = models.ForeignKey('Optin', models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    nbtotal = models.IntegerField()
    nboptin = models.IntegerField()
    nbhard = models.IntegerField()
    nbsoft = models.IntegerField()
    nbadressableemail = models.IntegerField(blank=True, null=True)
    nbadressablesms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_data_base_stats'
        unique_together = (('date', 'optin', 'data_base'),)


class AllowedWs(models.Model):
    hostname = models.CharField(max_length=255, blank=True, null=True)
    enable = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'allowed_ws'


class Campagne(models.Model):
    datecreation = models.DateTimeField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'campagne'


class Clic(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    link = models.ForeignKey('Link', models.DO_NOTHING, blank=True, null=True)
    support_type = models.ForeignKey('SupportType', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()
    ip = models.CharField(max_length=255)
    userid = models.IntegerField(blank=True, null=True)
    mobile = models.BooleanField(blank=True, null=True)
    tablet = models.BooleanField(blank=True, null=True)
    desktop = models.BooleanField(blank=True, null=True)
    device = models.CharField(max_length=500, blank=True, null=True)
    browser = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clic'


class ContactAnniversaireKpg(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    prnom = models.CharField(max_length=20, blank=True, null=True)
    nom = models.CharField(max_length=20, blank=True, null=True)
    date_de_naissance = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_anniversaire_kpg'


class ContactBase1TestMsz(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_base1_test_msz'


class ContactBaseTest(models.Model):
    id = models.IntegerField(primary_key=True)
    c_id = models.CharField(db_column='c__id', unique=True, max_length=100, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    civilite = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_base_test'
# Unable to inspect table 'contact_bdd_test_0304'
# The error was: ERREUR:  droit refus� pour la table contact_bdd_test_0304



class ContactEmailNonUnique(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=190, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prnom = models.CharField(max_length=100, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_email_non_unique'


class ContactFichier(models.Model):
    id = models.IntegerField(primary_key=True)
    hela = models.CharField(unique=True, max_length=190, blank=True, null=True)
    hela2 = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_fichier'


class ContactHachTest(models.Model):
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    dater = models.DateTimeField(blank=True, null=True)
    c_id = models.CharField(db_column='c__id', max_length=100, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.

    class Meta:
        managed = False
        db_table = 'contact_hach_test'


class ContactHubcontact(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    civilit = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    prnom = models.CharField(max_length=46, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    structure_un = models.BooleanField(blank=True, null=True)
    structure_deux = models.BooleanField(blank=True, null=True)
    structure_trois = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_hubcontact'


class ContactListeKpg(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    nom = models.CharField(max_length=50, blank=True, null=True)
    prnom = models.CharField(max_length=50, blank=True, null=True)
    test = models.CharField(max_length=150, blank=True, null=True)
    optin_sms = models.BooleanField(blank=True, null=True)
    optin_3 = models.BooleanField(blank=True, null=True)
    tl_port = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_liste_kpg'


class ContactTestManel(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test__manel'


class ContactTestAymen(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    civilit = models.CharField(max_length=20, blank=True, null=True)
    desabo = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_aymen'


class ContactTestBddAscLaJuillet2018(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    opt_in = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_bdd_asc_la_juillet_2018'


class ContactTestBdddHubscore(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_bddd_hubscore'


class ContactTestFormulaire(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    prnom = models.CharField(max_length=100, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_formulaire'


class ContactTestHachem(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    nom = models.CharField(max_length=255, blank=True, null=True)
    prenom = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_hachem'


class ContactTestHub(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prnom = models.CharField(max_length=100, blank=True, null=True)
    civilite = models.CharField(max_length=100, blank=True, null=True)
    ville = models.CharField(max_length=100, blank=True, null=True)
    code_postal = models.IntegerField(blank=True, null=True)
    societe = models.CharField(max_length=100, blank=True, null=True)
    statut = models.BooleanField(blank=True, null=True)
    pays = models.CharField(max_length=100, blank=True, null=True)
    portable = models.CharField(max_length=45, blank=True, null=True)
    secteur = models.CharField(max_length=250, blank=True, null=True)
    date_danniversaire = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_hub'
# Unable to inspect table 'contact_test_import'
# The error was: ERREUR:  droit refus� pour la table contact_test_import



class ContactTestImportDeLaBaseBatiactuQuiMarche(models.Model):
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    marketing_direct = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    date_inscription = models.DateTimeField(blank=True, null=True)
    recevoir_news_quoti = models.CharField(max_length=100, blank=True, null=True)
    recevoir_dossier = models.CharField(max_length=100, blank=True, null=True)
    blacklist = models.BooleanField(blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    optin_cipmd = models.BooleanField(blank=True, null=True)
    territorial = models.BooleanField(blank=True, null=True)
    terr = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_import_de_la_base_batiactu_qui_marche'


class ContactTestListField(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    telephone = models.CharField(max_length=45, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)
    float = models.FloatField(blank=True, null=True)
    varchar = models.CharField(max_length=50, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    boolean = models.BooleanField(blank=True, null=True)
    test = models.CharField(max_length=203, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_list_field'


class ContactTestManel(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_manel'


class ContactTestMathieu(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    nom = models.CharField(max_length=100, blank=True, null=True)
    prnom = models.CharField(max_length=100, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    test = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_mathieu'
# Unable to inspect table 'contact_test_opt_in'
# The error was: ERREUR:  droit refus� pour la table contact_test_opt_in



class ContactTestPld(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_test_pld'


class ContactTesteurs(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    groupe_test1 = models.BooleanField(blank=True, null=True)
    groupe_test2 = models.BooleanField(blank=True, null=True)
    groupe_test3 = models.BooleanField(blank=True, null=True)
    test = models.BooleanField(blank=True, null=True)
    test_texte = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_testeurs'


class ContactTkiTest(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(unique=True, max_length=190, blank=True, null=True)
    adulte = models.BooleanField(blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_tki_test'


class DataBaseType(models.Model):
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=10)
    deletable = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'data_base_type'


class DelivrabilityBounce(models.Model):
    mail_sending_resume = models.ForeignKey('MailSendingResume', models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField()
    gabouncetype = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'delivrability_bounce'


class Domain(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'domain'


class Event(models.Model):
    date = models.DateTimeField()
    user_id = models.IntegerField()
    type = models.CharField(max_length=255)
    database_name = models.CharField(max_length=190)
    database_id = models.IntegerField()
    email = models.CharField(max_length=190, blank=True, null=True)
    user_name = models.CharField(max_length=190, blank=True, null=True)
    line_id = models.IntegerField(blank=True, null=True)
    contact_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'event'


class Folder(models.Model):
    name = models.CharField(max_length=255)
    datecreation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'folder'


class Form(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    data_base_answer = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    datecreation = models.DateTimeField()
    archive = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    jsonform = models.TextField()
    theme = models.CharField(max_length=50, blank=True, null=True)
    sendtext = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'form'


class FormHommeFr(models.Model):
    id = models.IntegerField(primary_key=True)
    voulez_vous_vous_inscire_la_newsletter = models.CharField(db_column='voulez_vous_vous_inscire___la_newsletter', max_length=255, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    userid = models.ForeignKey(ContactListeKpg, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_homme_fr'


class FormTestApi(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(ContactListeKpg, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_test_api'


class FormTestFormulaire(models.Model):
    quel_est_votre_nom_de_famille_field = models.CharField(db_column='quel_est_votre_nom_de_famille_', max_length=255, blank=True, null=True)  # Field renamed because it ended with '_'.
    userid = models.ForeignKey(ContactBaseTest, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_test_formulaire'


class FormTestForward(models.Model):
    id = models.IntegerField(primary_key=True)
    votre_email = models.CharField(max_length=255, blank=True, null=True)
    prnom = models.CharField(max_length=255, blank=True, null=True)
    poste = models.CharField(max_length=255, blank=True, null=True)
    vous_serez_prsent_e_field = models.CharField(db_column='vous_serez_prsent(e)_', max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    userid = models.ForeignKey(ContactTestFormulaire, models.DO_NOTHING, db_column='userid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'form_test_forward'
# Unable to inspect table 'hard_bounce'
# The error was: ERREUR:  correspondance utilisateur non trouv�e pour � mog �



class Import(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    directory = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    initialfilename = models.CharField(max_length=255)
    datecreation = models.DateTimeField()
    start = models.DateTimeField(blank=True, null=True)
    finish = models.DateTimeField(blank=True, null=True)
    nbrecords = models.IntegerField(blank=True, null=True)
    nbduplicates = models.IntegerField(blank=True, null=True)
    nbupdates = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'import'


class Link(models.Model):
    mail_sending = models.ForeignKey('MailSending', models.DO_NOTHING, blank=True, null=True)
    url = models.TextField()
    nb = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'link'


class LoggedUser(models.Model):
    userid = models.IntegerField()
    userlogin = models.CharField(max_length=255)
    ip = models.CharField(max_length=45)
    logindate = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'logged_user'


class Mail(models.Model):
    support_type = models.ForeignKey('SupportType', models.DO_NOTHING, blank=True, null=True)
    folder = models.ForeignKey(Folder, models.DO_NOTHING, blank=True, null=True)
    datecreation = models.DateTimeField()
    dateupdate = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255)
    htmlfile = models.CharField(max_length=255, blank=True, null=True)
    smscontent = models.TextField(blank=True, null=True)
    grabimg = models.BooleanField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    iswysiwyg = models.BooleanField(blank=True, null=True)
    istemplate = models.BooleanField(blank=True, null=True)
    addstop = models.BooleanField(blank=True, null=True)
    isnotification = models.BooleanField(blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail'


class MailHeaderFooter(models.Model):
    name = models.CharField(max_length=255)
    htmlheaderfile = models.CharField(max_length=255)
    htmlfooterfile = models.CharField(max_length=255)
    datecreation = models.DateTimeField()
    dateupdate = models.DateTimeField(blank=True, null=True)
    iswysiwyg = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_header_footer'


class MailSending(models.Model):
    tracking_ndd = models.ForeignKey('TrackingNdd', models.DO_NOTHING, blank=True, null=True)
    campagne = models.ForeignKey(Campagne, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('Type', models.DO_NOTHING, blank=True, null=True)
    sender_mail = models.ForeignKey('SenderMail', models.DO_NOTHING, blank=True, null=True)
    mail = models.ForeignKey(Mail, models.DO_NOTHING, blank=True, null=True)
    database = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    support_type = models.ForeignKey('SupportType', models.DO_NOTHING, blank=True, null=True)
    test = models.BooleanField(blank=True, null=True)
    name = models.CharField(max_length=255)
    htmlfile = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    datecreation = models.DateTimeField()
    dateendcalculateresume = models.DateTimeField(blank=True, null=True)
    dateupdate = models.DateTimeField(blank=True, null=True)
    finish = models.IntegerField(blank=True, null=True)
    sendername = models.CharField(max_length=255, blank=True, null=True)
    replytoname = models.CharField(max_length=255, blank=True, null=True)
    replytomail = models.CharField(max_length=255, blank=True, null=True)
    datesend = models.DateTimeField(blank=True, null=True)
    limitation = models.IntegerField(blank=True, null=True)
    trigg = models.BooleanField(blank=True, null=True)
    triggerdatestart = models.DateField(blank=True, null=True)
    triggerdateend = models.DateField(blank=True, null=True)
    triggersendhour = models.IntegerField(blank=True, null=True)
    triggersendminute = models.IntegerField(blank=True, null=True)
    triggersendlimitdays = models.IntegerField(blank=True, null=True)
    triggersendrecurence = models.IntegerField(blank=True, null=True)
    segmentscount = models.IntegerField(blank=True, null=True)
    sendmails = models.IntegerField(blank=True, null=True)
    archive = models.BooleanField(blank=True, null=True)
    vmtatechname = models.CharField(max_length=45, blank=True, null=True)
    firstattachmentfilename = models.CharField(max_length=255, blank=True, null=True)
    secondattachmentfilename = models.CharField(max_length=255, blank=True, null=True)
    firstattachmentfilepath = models.CharField(max_length=255, blank=True, null=True)
    secondattachmentfilepath = models.CharField(max_length=255, blank=True, null=True)
    urlarguments = models.CharField(max_length=255, blank=True, null=True)
    mail_header_footer = models.ForeignKey(MailHeaderFooter, models.DO_NOTHING, blank=True, null=True)
    deduplicated = models.IntegerField()
    url_test = models.CharField(max_length=255, blank=True, null=True)
    email_on_acid = models.BooleanField(blank=True, null=True)
    mail_sending_az_testing = models.ForeignKey('MailSendingAzTesting', models.DO_NOTHING, blank=True, null=True)
    testing = models.CharField(max_length=255, blank=True, null=True)
    mail_sending_import = models.ForeignKey('MailSendingImport', models.DO_NOTHING, blank=True, null=True)
    draft = models.BooleanField(blank=True, null=True)
    trackcookie = models.BooleanField(blank=True, null=True)
    file = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_sending'


class MailSendingAzTesting(models.Model):
    datecreation = models.DateTimeField(blank=True, null=True)
    dateupdate = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255)
    test = models.IntegerField()
    changing = models.IntegerField()
    datesend = models.DateTimeField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)
    dateresult = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_sending_az_testing'


class MailSendingExclude(models.Model):
    mail_sending = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    exclude = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    open = models.BooleanField()
    clic = models.BooleanField()
    recieve = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mail_sending_exclude'


class MailSendingGlobalStats(models.Model):
    mail_sending = models.OneToOneField(MailSending, models.DO_NOTHING, blank=True, null=True)
    clic = models.IntegerField(blank=True, null=True)
    uniquclic = models.IntegerField(blank=True, null=True)
    uniqclicbysend = models.IntegerField(blank=True, null=True)
    open = models.IntegerField(blank=True, null=True)
    uniqopenbysend = models.IntegerField(blank=True, null=True)
    uniqopen = models.IntegerField(blank=True, null=True)
    mobileopen = models.IntegerField(blank=True, null=True)
    uniqmobileopen = models.IntegerField(blank=True, null=True)
    mobileclic = models.IntegerField(blank=True, null=True)
    uniqmobileclic = models.IntegerField(blank=True, null=True)
    tabletopen = models.IntegerField(blank=True, null=True)
    uniqtabletopen = models.IntegerField(blank=True, null=True)
    tabletclic = models.IntegerField(blank=True, null=True)
    uniqtabletclic = models.IntegerField(blank=True, null=True)
    dektopopen = models.IntegerField(blank=True, null=True)
    uniqdesktopopen = models.IntegerField(blank=True, null=True)
    desktopclic = models.IntegerField(blank=True, null=True)
    uniqdesktopclic = models.IntegerField(blank=True, null=True)
    hardbefore = models.IntegerField(blank=True, null=True)
    hardafter = models.IntegerField(blank=True, null=True)
    softbefore = models.IntegerField(blank=True, null=True)
    softafter = models.IntegerField(blank=True, null=True)
    scompafter = models.IntegerField(blank=True, null=True)
    repoussoirbefore = models.IntegerField(blank=True, null=True)
    delivrabilityafter = models.IntegerField(blank=True, null=True)
    notoptinbefore = models.IntegerField(blank=True, null=True)
    unsubscribeafter = models.IntegerField(blank=True, null=True)
    badformatedemail = models.IntegerField(blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    volumesend = models.IntegerField(blank=True, null=True)
    volumerecieved = models.IntegerField(blank=True, null=True)
    datelastupdate = models.DateTimeField()
    volumeprecalculated = models.IntegerField(blank=True, null=True)
    datecalculevolumeprecalculated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_sending_global_stats'


class MailSendingImport(models.Model):
    csv_relations = models.TextField(blank=True, null=True)  # This field type is a guess.
    separators = models.CharField(max_length=255, blank=True, null=True)
    endline = models.CharField(max_length=255, blank=True, null=True)
    enclosure = models.CharField(max_length=255, blank=True, null=True)
    encoding = models.CharField(max_length=255, blank=True, null=True)
    ignored_rows = models.CharField(max_length=255, blank=True, null=True)
    path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'mail_sending_import'


class MailSendingOptin(models.Model):
    mail_sending = models.OneToOneField(MailSending, models.DO_NOTHING, primary_key=True)
    optin = models.ForeignKey('Optin', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mail_sending_optin'
        unique_together = (('mail_sending', 'optin'),)


class MailSendingResume(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    mail_sending = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, blank=True, null=True)
    support_type = models.ForeignKey('SupportType', models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=190, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    userid = models.IntegerField(blank=True, null=True)
    datesend = models.DateTimeField(blank=True, null=True)
    open = models.IntegerField()
    clic = models.IntegerField()
    bounce = models.IntegerField(blank=True, null=True)
    nbsms = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mail_sending_resume'


class MailSendingSegmentation(models.Model):
    mail_sending = models.OneToOneField(MailSending, models.DO_NOTHING, primary_key=True)
    segmentation = models.ForeignKey('Segmentation', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mail_sending_segmentation'
        unique_together = (('mail_sending', 'segmentation'),)


class Open(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    mail_sending = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    support_type = models.ForeignKey('SupportType', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()
    ip = models.CharField(max_length=255)
    userid = models.IntegerField(blank=True, null=True)
    mobile = models.BooleanField(blank=True, null=True)
    tablet = models.BooleanField(blank=True, null=True)
    desktop = models.BooleanField(blank=True, null=True)
    device = models.CharField(max_length=500, blank=True, null=True)
    browser = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'open'


class Optin(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    field = models.CharField(max_length=255)
    unsubscribelabel = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'optin'


class OtherBase2TestMsz(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    optin = models.BooleanField(blank=True, null=True)
    num_demande = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_base2_test_msz'


class OtherDmoMdicale(models.Model):
    id = models.IntegerField(primary_key=True)
    contact_id = models.IntegerField(unique=True, blank=True, null=True)
    spcialit = models.CharField(max_length=50, blank=True, null=True)
    diplme_franais = models.CharField(max_length=50, blank=True, null=True)
    exprience = models.CharField(max_length=255, blank=True, null=True)
    ordre_des_mdecins = models.BooleanField(blank=True, null=True)
    commentaires = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_dmo_mdicale'


class OtherHommeFr(models.Model):
    id = models.IntegerField(primary_key=True)
    id_contrat = models.IntegerField(unique=True, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_homme_fr'


class OtherHubcontactStructures(models.Model):
    id = models.IntegerField(primary_key=True)
    filter_id = models.IntegerField(unique=True, blank=True, null=True)
    filter_name = models.CharField(max_length=255, blank=True, null=True)
    filter_techname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_hubcontact_structures'


class OtherHubcontactUsersStructures(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(blank=True, null=True)
    filter_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_hubcontact_users_structures'


class OtherNouveauxTalents(models.Model):
    id = models.IntegerField(primary_key=True)
    contact_id = models.IntegerField(unique=True)
    cration_entreprise = models.BooleanField(blank=True, null=True)
    reprise_entreprise = models.BooleanField(blank=True, null=True)
    domaine = models.CharField(max_length=50, blank=True, null=True)
    secteur_gographique = models.CharField(max_length=50, blank=True, null=True)
    budget = models.BooleanField(blank=True, null=True)
    dtail_budget = models.CharField(max_length=20, blank=True, null=True)
    date_d_echeance = models.DateField(blank=True, null=True)
    date_consentement = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_nouveaux_talents'


class OtherTestLeaPersoAsc(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.ForeignKey(ContactTestBddAscLaJuillet2018, models.DO_NOTHING, db_column='email', blank=True, null=True)
    prenom = models.CharField(max_length=190, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_test_lea_-_perso_asc'
# Unable to inspect table 'other_test_msz_120320'
# The error was: ERREUR:  droit refus� pour la table other_test_msz_120320



class OtherVisionnaires(models.Model):
    id = models.IntegerField(primary_key=True)
    contact_id = models.IntegerField(blank=True, null=True)
    date_demande = models.DateField(blank=True, null=True)
    projet = models.CharField(max_length=255, blank=True, null=True)
    montant = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'other_visionnaires'


class ProductCommandes(models.Model):
    id = models.IntegerField(primary_key=True)
    identifiant_cmd = models.IntegerField(blank=True, null=True)
    date_cmd = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=120, blank=True, null=True)
    montant = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_commandes'


class ProductHommeFr(models.Model):
    id = models.IntegerField(primary_key=True)
    id_contrat = models.IntegerField(unique=True, blank=True, null=True)
    source = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_homme_fr'


class Repoussoir(models.Model):
    email = models.CharField(unique=True, max_length=190)
    dateadd = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'repoussoir'


class Scomp(models.Model):
    mail_sending_resume = models.ForeignKey(MailSendingResume, models.DO_NOTHING, blank=True, null=True)
    domain = models.ForeignKey(Domain, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'scomp'


class SegmentFolder(models.Model):
    datecreation = models.DateTimeField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'segment_folder'


class Segmentation(models.Model):
    data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    dateupdate = models.DateTimeField(blank=True, null=True)
    datecreation = models.DateTimeField()
    name = models.CharField(max_length=255)
    count = models.IntegerField(blank=True, null=True)
    datecount = models.DateTimeField(blank=True, null=True)
    timecount = models.IntegerField(blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    archive = models.BooleanField()
    deduplicated = models.BooleanField()
    historic = models.BooleanField(blank=True, null=True)
    folder = models.ForeignKey(SegmentFolder, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segmentation'


class SegmentationDetail(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    segmentation = models.ForeignKey(Segmentation, models.DO_NOTHING, blank=True, null=True)
    associate_data_base = models.ForeignKey(AllDataBase, models.DO_NOTHING, blank=True, null=True)
    stype = models.CharField(max_length=30)
    scondition = models.CharField(max_length=30, blank=True, null=True)
    fieldname = models.CharField(max_length=255, blank=True, null=True)
    operator = models.CharField(max_length=15, blank=True, null=True)
    svalue = models.CharField(max_length=255, blank=True, null=True)
    scomportement = models.CharField(max_length=50, blank=True, null=True)
    stimenb = models.IntegerField(blank=True, null=True)
    stimetype = models.CharField(max_length=20, blank=True, null=True)
    scampagneids = models.CharField(max_length=255, blank=True, null=True)
    sthemeids = models.CharField(max_length=255, blank=True, null=True)
    operations = models.CharField(max_length=255, blank=True, null=True)
    sorder = models.IntegerField()
    sthematiqueids = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segmentation_detail'


class SegmentationStats(models.Model):
    segmentation = models.ForeignKey(Segmentation, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    nbtotal = models.IntegerField()
    nbhard = models.IntegerField(blank=True, null=True)
    nbsoft = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'segmentation_stats'


class SenderMail(models.Model):
    mail = models.CharField(max_length=255)
    archive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sender_mail'


class SocialFbAccounts(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'social_fb_accounts'


class SoftBounce(models.Model):
    mail_sending_resume = models.ForeignKey(MailSendingResume, models.DO_NOTHING, blank=True, null=True)
    text = models.TextField()
    date = models.DateTimeField()
    gabouncetype = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'soft_bounce'


class SpamAssassin(models.Model):
    mail_sending = models.OneToOneField(MailSending, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()
    score = models.FloatField()
    details = models.TextField()

    class Meta:
        managed = False
        db_table = 'spam_assassin'


class StatHour(models.Model):
    mail_sending = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    date = models.DateField()
    hour = models.IntegerField()
    nbmailsend = models.IntegerField(blank=True, null=True)
    recieved = models.IntegerField(blank=True, null=True)
    opens = models.IntegerField(blank=True, null=True)
    clics = models.IntegerField(blank=True, null=True)
    clicsmobile = models.IntegerField(blank=True, null=True)
    opensmobile = models.IntegerField(blank=True, null=True)
    clicstablet = models.IntegerField(blank=True, null=True)
    openstablet = models.IntegerField(blank=True, null=True)
    clicsdesktop = models.IntegerField(blank=True, null=True)
    opensdesktop = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stat_hour'
        unique_together = (('date', 'hour', 'mail_sending'),)


class SupportType(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'support_type'


class Thematique(models.Model):
    name = models.CharField(max_length=255)
    datecreation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'thematique'


class ThematiqueLink(models.Model):
    thematique = models.OneToOneField(Thematique, models.DO_NOTHING, primary_key=True)
    link = models.ForeignKey(Link, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'thematique_link'
        unique_together = (('thematique', 'link'),)


class TrackingNdd(models.Model):
    nddimg = models.CharField(max_length=255)
    nddtrack = models.CharField(max_length=255)
    nddunsubscribe = models.CharField(max_length=255)
    quality = models.IntegerField(blank=True, null=True)
    type = models.IntegerField()
    archive = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'tracking_ndd'


class TriggerSendLimit(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'trigger_send_limit'


class Type(models.Model):
    datecreation = models.DateTimeField()
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'type'


class Unsubscribe(models.Model):
    mail_sending = models.ForeignKey(MailSending, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()
    userid = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    optin_field = models.CharField(max_length=255, blank=True, null=True)
    mail_sending_resume_id = models.IntegerField(blank=True, null=True)
    database_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unsubscribe'


class UserAgent(models.Model):
    open = models.OneToOneField(Open, models.DO_NOTHING, blank=True, null=True)
    clic = models.OneToOneField(Clic, models.DO_NOTHING, blank=True, null=True)
    useragent = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_agent'


class WebserviceData(models.Model):
    date = models.DateTimeField()
    databaseid = models.IntegerField()
    rowid = models.IntegerField()
    tag = models.CharField(max_length=255, blank=True, null=True)
    mailsendid = models.IntegerField(blank=True, null=True)
    data = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'webservice_data'
