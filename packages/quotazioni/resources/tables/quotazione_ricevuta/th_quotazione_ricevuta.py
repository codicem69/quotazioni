#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('quotazione_id')
        r.fieldcell('description', width='auto')

    def th_order(self):
        return 'quotazione_id'

    def th_query(self):
        return dict(column='description', op='contains', val='')


class Form(BaseComponent):
    py_requires="gnrcomponents/attachmanager/attachmanager:AttachManager"

    def th_form(self, form):
        #pane = form.record
        bc = form.center.borderContainer()
        self.datiQuotReceived(bc.roundedGroupFrame(title='!![en]Quotation received description',region='top',datapath='.record',height='100px', background='lightgrey', splitter=True))
        self.quot_rec_att(bc.contentPane(region='center', title='!![en]Attachments', height='100%'))
        
    def datiQuotReceived(self,pane):    
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('quotazione_id' )
        fb.field('description', width='100em', tag='simpleTextArea')
    
    def quot_rec_att(self,pane):
        pane.attachmentGrid(viewResource='ViewFromQuotRecAtc')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
