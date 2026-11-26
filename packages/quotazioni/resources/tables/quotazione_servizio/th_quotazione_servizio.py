#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('quotazione_id')
        r.fieldcell('source_version_id')
        r.fieldcell('source_table')
        r.fieldcell('source_id')
        r.fieldcell('description')
        r.fieldcell('um')
        r.fieldcell('tipo_prezzo')
        r.fieldcell('price_cliente')
        r.fieldcell('cost_fornitore')
        r.fieldcell('note')

    def th_order(self):
        return 'quotazione_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')

class ViewDashboard(BaseComponent):

    def th_struct(self, struct):
        r = struct.view().rows()
        r.fieldcell('description', name='!![en]Service',width='auto', font_weight='bold')
        r.fieldcell('um', name='!!U.M.', font_weight='bold')
        r.fieldcell('tipo_prezzo')
        r.fieldcell('price_cliente', name='!![en]Customer price', font_weight='bold', color='green')
        r.fieldcell('cost_fornitore', name='!![en]Supplier cost')
        r.fieldcell('margine', name='!![en]Margin')
        r.fieldcell('margine_percentuale', name='!![en]Margin %')
        r.fieldcell('totale_cliente_forfait',name='!![en]Customer forfait total',
            totalize=True, dtype='N', format='#,###.00')
        r.fieldcell('totale_fornitore_forfait',name='!![en]Supplier forfait total',
                    totalize=True, dtype='N', format='#,###.00')
        r.fieldcell('margine_forfait', name='!![en]Forfait margin',
                    totalize=True, dtype='N', format='#,###.00')
    
    def th_order(self):
        return 'description'

    def th_query(self):
        return dict(column='description', op='contains', val='')
    
class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=1, border_spacing='4px',colswidth='auto',fld_width='100%')
        fb.field('quotazione_id' )
        fb.field('source_version_id' )
        fb.field('source_table' )
        fb.field('source_id' )
        fb.field('description' )
        fb.field('um' )
        fb.field('tipo_prezzo' )
        fb.field('price_cliente' )
        fb.field('cost_fornitore' )
        fb.field('note' )


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
