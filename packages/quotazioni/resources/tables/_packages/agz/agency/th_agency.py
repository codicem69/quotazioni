#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method
import re,os

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('code', width='3em')
        r.fieldcell('agency_name')
        r.fieldcell('description')
        r.fieldcell('address')
        r.fieldcell('tel', width='6em')
        r.fieldcell('fax', width='6em')
        r.fieldcell('email')
        r.fieldcell('web')
        r.fieldcell('vat')
        r.fieldcell('cf')
        r.fieldcell('sdi')
        r.fieldcell('virtual_stamp')
        r.fieldcell('emailpec_account_id')
        r.fieldcell('port')

    def th_order(self):
        return 'agency_name'

    def th_query(self):
        return dict(column='agency_name', op='contains', val='')

class Form(BaseComponent):

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.DatiAgenzia(bc.borderContainer(region='top',datapath='.record',height='450px', splitter=True))
        self.agency_att(bc.contentPane(region='center',height='100%', splitter=True))

    def DatiAgenzia(self,bc):
        center = bc.roundedGroup(region='center', title='Agency details').div(margin='10px',margin_right='20px')
        fb = center.formbuilder(cols=2, border_spacing='4px',fld_width='30em')
        fb.field('code', placeholder='Max 2 letters' )
        fb.field('agency_name' )
        fb.field('description' )
        fb.field('address' )
        fb.field('tel' )
        fb.field('fax' )
        fb.field('email' )
        fb.field('web' )
        fb.field('vat', placeholder='e.g. IT017.......' )
        fb.field('cf' )
        fb.field('sdi' ,placeholder='!![en] insert 7 characters')
        fb.br()

        fb.simpleTextArea(lbl='!![en]Bank details',value='^.bank_details',editor=True, height='150px', width='150px' )
        fb.simpleTextArea(lbl='Virtual stamp',value='^.virtual_stamp',editor=True, height='150px', width='150px' )
        fb.field('emailpec_account_id', hasDownArrow=True )
        fb.field('htmltemplate_id', hasDownArrow=True)
        fb.field('port' ,colspan=2)
        fb.br()
        right = bc.roundedGroup(region='right',title='!![en]Agency stamp',width='200px')

        right.img(src='^.agency_stamp', edit=True, crop_width='100px', crop_height='100px', border='2px dotted silver',margin_left='5px',
                        placeholder=True,upload_folder='*') #upload_folder='site:image', upload_filename='=.id', width='100px', height='100px')

    def agency_att(self,pane):
        #fb = bc.formbuilder(cols=1, border_spacing='4px',margin='4px',region='bottom', height='100%')
        #fb.div('ciao')
        pane.attachmentGrid(viewResource='View')  

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )

