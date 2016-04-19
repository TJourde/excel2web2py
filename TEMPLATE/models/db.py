# -*- coding: utf-8 -*-
import os
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
    db = DAL('sqlite://storage.sqlite')
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
mail.settings.sender = 'chambon@canabis.u-bordeaux2.fr'
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


db.define_table("Produits_chimiques",Field("Nom_francais",type='string',length=30,required=True,ondelete='Cascade',notnull=False,unique=True),Field("Nom_anglais"),Field("Synonyme"),Field("N_CAS"),Field("Formule"),Field("Masse_molaire"),Field("Forme"),Field("Symbole"),Field("Mentions_de_danger"),Field("Conseils_de_prudence"),Field("FDS_piece_jointe"),Field("Hazard_statements"),Field("Precautionary_statements"),Field("MSDS_piece_jointe"),Field("Lien_FDS"),Field("Lien_MSDS"))
db.define_table("Mentions_de_danger",Field("Codes"),Field("Mentions_de_danger"),Field("Hazard_statements"))
db.define_table("Conseils_de_prudence",Field("Codes", "id"),Field("Conseils_de_prudence",type='string'),Field("Precautionary_statements",type='string'))
db.define_table("Link",Field("Sheet"),Field("Colonne"),Field("ColonneT"))
db.define_table("Produits_chimiquesConseils_de_prudence",Field("Produits_chimiques",type="integer"),Field("Conseils_de_prudence",type="integer"),primarykey=["Produits_chimiques","Conseils_de_prudence"])
def getDb():
    from os import path
    module_path=os.path.abspath(os.path.dirname(__file__))
    dbpath = module_path + "/../databases"
    db_name = "storage.sqlite"
    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)
    return db
def getTable(db):
    return db.Produits_chimiques