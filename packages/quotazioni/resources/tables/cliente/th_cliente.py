#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('rag_sociale',width='40em')
        r.fieldcell('address',width='30em')
        r.fieldcell('cap',width='10em')
        r.fieldcell('city',width='10em')
        r.fieldcell('email',width='10em')
        r.fieldcell('tel',width='10em')
        r.fieldcell('note',width='auto')

    def th_order(self):
        return 'rag_sociale'

    def th_query(self):
        return dict(column='full_cliente', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px',fld_width='50em')
        fb.field('rag_sociale' )
        fb.field('address' )
        fb.field('cap' )
        fb.field('city' )
        fb.field('email' )
        fb.field('tel' )
        fb.field('note', tag='simpleTextArea' , colspan=2, width='99%')


    def th_options(self):
        #return dict(dialog_height='400px', dialog_width='600px' )
        return dict(dialog_windowRatio = 1 )
        