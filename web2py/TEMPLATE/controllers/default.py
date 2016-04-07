# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations
import sys,os
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#requires login
def index():
    from gluon.dal import DAL, Field
    from gluon.validators import *
    module_path=os.path.abspath(os.path.dirname(__file__))
    dbpath = module_path +'/../databases'
    db_name = "storage.sqlite"
    db = DAL("sqlite://"+ db_name ,folder=dbpath, auto_import=True)
    table = db.tables[0]#name of last new table
    x = getattr(db, table)#get the TABLE with the corresponding name !Bugs if name of table equals one other attribute of DAL (like debug)!
    rows = db(x).select()
    form=SQLFORM(x)
    records=SQLFORM.grid(x)
    return dict(form=form, records=records)


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()