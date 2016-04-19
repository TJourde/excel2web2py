# -*- coding: utf-8 -*-
import sys,subprocess
# this file is released under public domain and you can use without limitations
#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#requires login
def main():
    db = getDb()
    table = getTable(db)#in db.py,from script.py
    rows = db(table).select()
    if (len(rows) == 0):
        initData()
    form = forming(table)
    #records=SQLFORM.grid(table,left=db.Conseils_de_prudence.on(db.Conseils_de_prudence.Codes == table.Conseils_de_prudence))
    #records=SQLFORM.smartgrid(table,linked_tables=['Conseils_de_prudence'],editable=True)
    records=SQLFORM.grid(table)
    return dict(form=form, records=records)

def index():
    return response.render()


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
def forming(table):
    form = SQLFORM(table)
    if form.process().accepted:
        response.falsh = 'form accepted'
    elif form.errors:
        response.flash = 'form has errors'
    return form

