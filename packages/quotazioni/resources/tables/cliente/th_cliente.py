#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale')
        r.fieldcell('address')
        r.fieldcell('cap')
        r.fieldcell('city')
        r.fieldcell('email')
        r.fieldcell('tel')
        r.fieldcell('note')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('rag_sociale' )
        fb.field('address' )
        fb.field('cap' )
        fb.field('city' )
        fb.field('email' )
        fb.field('tel' )
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
