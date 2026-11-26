#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('quotazione_servizio_id')
        r.fieldcell('campo')
        r.fieldcell('valore_precedente')
        r.fieldcell('valore_nuovo')
        r.fieldcell('data_modifica')
        r.fieldcell('utente_modifica')
        r.fieldcell('origine')
        r.fieldcell('motivo')

    def th_order(self):
        return 'quotazione_servizio_id'

    def th_query(self):
        return dict(column='campo', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px',colswidth='auto',fld_width='100%')
        fb.field('quotazione_servizio_id' )
        fb.field('campo' )
        fb.field('valore_precedente' )
        fb.field('valore_nuovo' )
        fb.field('data_modifica' )
        fb.field('utente_modifica' )
        fb.field('origine' )
        fb.field('motivo' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
