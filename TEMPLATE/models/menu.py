# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('IINS'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://intraiins.u-bordeaux2.fr/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Chambon Laurent<Laurent.chambon@u-bordeaux.fr>Jourde Tanguy<tanguy.jourde@etu.u-bordeaux.fr>'
response.meta.description = 'a cool new App'
response.meta.keywords = 'manage products'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Admin'), False, URL('admin','default','index'), [])
]



#DEVELOPMENT_MENU = False

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

#if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
def _():
    app = request.application
    ctr = request.controller
    response.menu += [
        (T('Main'), False, URL('default', 'main'))
        ]
_()