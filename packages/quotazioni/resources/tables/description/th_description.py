#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('quotazione_id',width='40em')
        r.fieldcell('description', width='auto')
        r.fieldcell('amount',width='20em')

    def th_order(self):
        return 'quotazione_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewFromDescription(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('_row_count', counter=True, name='N.',width='3em')
        r.fieldcell('quotazione_id')
        r.fieldcell('description',width='50em',edit=dict(editor=True,validate_len=':125'))
        r.fieldcell('amount',edit=True)

    def th_order(self):
        return '_row_count'
    
    def th_options(self):
        return dict(grid_selfDragRows=True)
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('quotazione_id' )
        fb.field('description' )
        fb.field('amount' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
