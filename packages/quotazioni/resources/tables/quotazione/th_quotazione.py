#!/usr/bin/python3
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('data')
        r.fieldcell('quot_n')
        r.fieldcell('oggetto')
        r.fieldcell('cliente_id')

    def th_order(self):
        return 'data'

    def th_query(self):
        return dict(column='full_quot', op='contains', val='')

    def th_options(self):
        return dict(partitioned=True)

class Form(BaseComponent):
    py_requires='gnrcomponents/pagededitor/pagededitor:PagedEditor'

    def th_form(self, form):
        bc = form.center.borderContainer()
        self.datiQuotazione(bc.borderContainer(region='top',datapath='.record',height='150px', splitter=True))
        #self.datiQuotazione(bc.roundedGroupFrame(title='!![en]Quotation',region='top',datapath='.record',height='130px', background='lightgrey', splitter=True))
        tc = bc.tabContainer(region = 'center',margin='2px',selectedPage='^.tabname')
        self.editQuotation(tc.framePane(title='!![EN]Edit Quotation', datapath='#FORM.editPagine'))

    def datiQuotazione(self,bc):
        bc.contentPane(region='center').linkerBox('cliente_id',margin='2px',openIfEmpty=True, validate_notnull=True,
                                                    columns='$ragione_sociale,$address,$cap,$city,$email',
                                                    auxColumns='$tel',
                                                #    clientTemplate=True,
                                                    newRecordOnly=True,formResource='Form',
                                                    dialog_height='500px',dialog_width='800px')
        left = bc.roundedGroup(title='!![en]Quotation datas',region='left',width='50%')
        fb = left.formbuilder(cols=2, border_spacing='4px')
        #fb = pane.div(margin_left='50px',margin_right='80px').formbuilder(cols=4, border_spacing='4px',fld_width='10em')
        
        fb.field('data' )
        fb.field('quot_n', readOnly=True)
        fb.field('oggetto', colspan=2, width='100%', tag='simpleTextArea' )
        #fb.field('cliente_id' )

    def editQuotation(self, frame):
        bar = frame.top.slotBar('10, lett_select,*',height='20px',border_bottom='1px solid silver')
        fb = bar.lett_select.formbuilder(cols=2,datapath='#FORM.record.htmlbag_quot')
        fb.dbselect('^.letterhead_id',table='adm.htmltemplate',lbl='carta intestata',hasDownArrow=True)
        fb.button('Get Html Quotation Doc').dataRpc('#FORM.record.htmlbag_quot.source',self.db.table('quotazioni.quotazione').getHTMLDoc,
                                            quot_id='=#FORM.pkey',
                                            record_template='quotation',
                                            letterhead='.letterhead_id')
        
        frame.pagedEditor(value='^#FORM.record.htmlbag_quot.source',pagedText='^#FORM.record.htmlbag_quot.output',
                          border='1px solid silver',
                          letterhead_id='^#FORM.record.htmlbag_quot.letterhead_id',
                          datasource='#FORM.record',printAction=True)

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px' )
