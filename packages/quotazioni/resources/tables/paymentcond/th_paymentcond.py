#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('quotazione_id', width='40em')
        r.fieldcell('paymentcond_id', width='auto')

    def th_order(self):
        return 'paymentcond_id'

    def th_query(self):
        return dict(column='paymentcond_id', op='contains', val='')


class ViewFromPaymCond(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('paymentcond_id', width='auto', edit=True)

    def th_order(self):
        return '_row_count'
    
    def th_options(self):
        return dict(grid_selfDragRows=True)    

class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('paymentcond_id' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
