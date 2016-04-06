# -*- coding: utf-8 -*-
import glob,os
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
    #db = DAL('sqlite://storage.sqlite')
    db = DAL('sqlite://'+glob.glob(os.getcwd()+'/applications/TEMPLATE/tmp/*db')[0])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

#auth = Auth(db)
# pour utiliser serveur cas bordeaux
auth = Auth(db,cas_provider = 'https://cas.u-bordeaux.fr')
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
from gluon.tools import Mail
mail = Mail()
mail.settings.server = '127.0.0.1:25'
mail.settings.sender = 'service@service.u-bordeaux2.fr'
mail.settings.login = None

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# DEFINE TABLE HERE

db.define_table("Produits_chimiques",Field("Nom_francais"),Field("Nom_anglais"),Field("Synonyme"),Field("N_CAS"),Field("Formule"),Field("Masse_molaire"),Field("Forme"),Field("Symbole"),Field("Mentions_de_danger"),Field("Conseils_de_prudence"),Field("FDS_piece_jointe"),Field("Hazard_statements"),Field("Precautionary_tatements"),Field("MSDS_piece_jointe"),Field("Lien_FDS"),Field("Lien_MSDS"))
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('(+)-Bicuculline','(+)-Bicuculline','','485-49-4','C20H17NO6','367,35 g/mol','Solide','SGH06 | SGH09','H300 | H311 | H331 | H400','P261 | P264 | P273 | P280 | P301+P310 | P311','(+)-Bicuculline','H300 | H311 | H331 | H400','P261 | P264 | P273 | P280 | P301+P310 | P311','(+)-Bicuculline_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=FR&productNumber=14340&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2F14340%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=14340&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2F14340%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('(±)-AMPA','(±)-AMPA','(±)-α-Amino-3-hydroxy-5-methylisoxazole-4-propionic acidhydrate','74341-63-2','C7H10N2O4','186,17 g/mol','Solide','','','','(±)-AMPA','','','(±)-AMPA_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=A6816&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fa6816%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=A6816&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fa6816%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('','(±)-Nipecotic acid','(±)-3-Piperidine carboxylic acid','60252-41-7','C6H11NO2','129,16g/mol','Solide','','','','','','','(±)-Nipecotic_acid_(anglais)','','')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('(±)-α-Tocopherol','(±)-α-Tocopherol','Vitamin E | DL-all-rac-α-Tocopherol','10191-41-0','C29H50O2','430,71 g/mol','Solide','','','','(±)-α-Tocopherol','','','(±)-α-Tocopherol_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=T3251&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Ft3251%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=T3251&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Ft3251%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('(RS)-Baclofen','','(RS)-4-Amino-3-(4-chlorophenyl)butanoic acid','1134-47-0','C10H12CINO2','213,66g/mol','Solide','SGH06','H301','P264 | P301+P310','','H301','P264 | P301+P310','(RS)-Baclofen_(anglais)','','')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('','(S)-(-)-5-Iodowillardiine','(2S)-2-Amino-3-(5-iodo-2,4-dioxopyrimidin-1-yl)propanoic acid','140187-25-3','C7H8IN3O4','325,06g/mol','Solide','','','','','','','(S)-(-)-5-Iodowillardiine_(anglais)','','')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('1,3-Bis-(diphénylphosphino)-propane','','dppp','6737-42-4','C27H26P2','412,44 g/mol','Solide','SGH07','H315 |H319 | H335','P261 | P305+P351+P338','1,3-Bis-(diphénylphosphino)-propane','H315 |H319 | H335','P261 | P305+P351+P338','1,3-Bis-(diphenylphosphino)-propane_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=262048&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F262048%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=262048&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F262048%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('1,4-Phenylenediamine','','1,4-Diaminobenzene | 1,4-Benzenediamine | p-Phenylenediamine','106-50-3','C6H8N2','108,14 g/mol','Solide','SGH06 | SGH09','H301 | H311 | H317 | H319 |H331 | H410','P261 | P273 | P280 | P301+P310 | P305+P351+P338','1,4-Phenylenediamine','H301 | H311 | H317 | H319 |H331 | H410','P261 | P273 | P280 | P301+P310 | P305+P351+P338','1,4-Phenylenediamine_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=78429&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F78429%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=78429&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F78429%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('2,2''-Thiodiéthanol','2,2''-Thiodiethanol','2,2′-Thiobis(ethanol) | Bis(2-hydroxyethyl) sulfide | Thiodiethylene glycol | Thiodiglycol','111-48-8','C4H10O2S','122,19 g/mol','Solide','SGH07','H319','P305+P351+P338','2,2''-Thiodiéthanol','H319','P305+P351+P338','2,2''-Thiodiethanol_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=166782&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F166782%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=166782&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F166782%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('','2-Bromohexadecanoic acid','2-Bromopalmitic acid','18263-25-7','C16H31BrO2','335,32 g/mol','Solide','SGH07','H315 |H319 | H335','P261 | P305+P351+P338','2-Bromohexadecanoic_acid','H315 |H319 | H335','P261 | P305+P351+P338','2-Bromohexadecanoic_acid (anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=21604&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F21604%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=21604&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F21604%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('2-Chloroadenosine','','2-CADO | 6-Amino-2-chloropurine riboside','146-77-0','C10H12ClN5O4','301,69 g/mol','Solide','','','','2-Chloroadenosine','','','2-Chloroadenosine_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=C5134&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fc5134%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=C5134&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fc5134%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('2-Mercapto-éthanesulfonate de sodium','Sodium 2-mercaptoethanesulfonate','MESNA | HS-CoM Na | 2-Mercaptoethanesulfonic acidsodium salt | Coenzyme Msodium salt','19767-45-4','C2H5NaO3S2C2H5NaO3S2','164,18 g/mol','Solide','SGH07','H315 | H319 | H335','P261 | P305+P351+P338','2-Mercapto-éthanesulfonate_de_sodium','','','2-Mercapto-éthanesulfonate_de_sodium_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=M1511&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Fm1511%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=M1511&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Fm1511%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('3,3´-Diaminobenzidine','','DAB | 3,3′,4,4′-Biphenyltetramine | 3,3′,4,4′-Tetraaminobiphenyl','91-95-2','C12H14N4','214,27 g/mol','Solide','SGH08','H341 | H350','P201 | P281 | P308+P313','3,3´-Diaminobenzidine','','','3,3´-Diaminobenzidine_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=D8001&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Fd8001%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=D8001&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Fd8001%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('3,3`-dioctadecyloxacarbocyanine perchlorate','','DiOC18(3) | ‘DiO’','34215-57-1','C53H85ClN2O6','881,70 g/mol','Solide','SGH07','H315 | H319 | H335','P261 | P305+P351+P338','3,3''-Dioctadecyloxacarbocyanine_perchlorate','','','3,3''-Dioctadecyloxacarbocyanine_perchlorate_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=D4292&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fd4292%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/PleaseWaitMSDSPage.do?language=EN-generic&country=FR&brand=SIGMA&productNumber=D4292&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Fd4292%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('4-Aminopyridine','','Fampridine | 4-Pyridylamine | 4-Pyridinamine','504-24-5','C5H6N2','94,11 g/mo','Solide','SGH06','H300 | H315 | H319 | H335','P261 | P264 | P301+P310 | P305+P351+P338','4-Aminopyridine','','','4-Aminopyridine_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=275875&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F275875%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=275875&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2F275875%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('4-Bromo-3,5-dimethylphenol','','4-Bromo-3,5-xylenol','7463-51-6','C8H9BrO','201,06 g/mol','Solide','SGH07','H315 | H319 | H335','P261 | P305+P351+P338','4-Bromo-3,5-dimethylphenol','','','4-Bromo-3,5-dimethylphenol_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=B64202&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2Fb64202%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=B64202&brand=ALDRICH&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Faldrich%2Fb64202%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('4-Hydroxytamoxifen','','4-(1-[4-(Dimethylaminoethoxy)phenyl]-2-phenyl-1-butenyl)phenol | 4-OHT | cis/trans-4-Hydroxytamoxifen','68392-35-8','C26H29NO2 C26H29NO2','387,51 g/mol','Solide','SGH08 | SGH07','H302 | H312 | H332 | H361','P280','4-Hydroxytamoxifen','','','4-Hydroxytamoxifen_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=T176&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Ft176%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=T176&brand=SIAL&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsial%2Ft176%3Flang%3Dfr')")
db.executesql("INSERT INTO Produits_chimiques(Nom_francais,Nom_anglais,Synonyme,N_CAS,Formule,Masse_molaire,Forme,Symbole,Mentions_de_danger,Conseils_de_prudence,FDS_piece_jointe,Hazard_statements,Precautionary_tatements,MSDS_piece_jointe,Lien_FDS,Lien_MSDS) VALUES('5-Fluoro-2′-deoxyuridine','','FUDR | Floxuridine | 2′-Deoxy-5-fluorouridine','50-91-9','C9H11FN2O5','246,19 g/mol','Solide','SGH06','H301','P301+P310','5-Fluoro-2′-deoxyuridine','','','5-Fluoro-2′-deoxyuridine_(anglais)','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=fr&productNumber=F0503&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Ff0503%3Flang%3Dfr','http://www.sigmaaldrich.com/MSDS/MSDS/DisplayMSDSPage.do?country=FR&language=EN-generic&productNumber=F0503&brand=SIGMA&PageToGoToURL=http%3A%2F%2Fwww.sigmaaldrich.com%2Fcatalog%2Fproduct%2Fsigma%2Ff0503%3Flang%3Dfr')")