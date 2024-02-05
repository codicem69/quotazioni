# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('quotazione', pkey='id', name_long='!![en]Quotation', name_plural='!![Quotations]',caption_field='full_quot')
        self.sysFields(tbl,counter=True)

        tbl.column('data', dtype='D', name_long='!![en]Date', name_short='!![en]Date')
        tbl.column('quot_n', name_short='!![en]Quot.no.')
        tbl.column('oggetto', name_short='!![en]Subject')
        tbl.column('cliente_id',size='22', group='_', name_long='!![en]Customer'
                    ).relation('cliente.id', relation_name='cliente_quot', mode='foreignkey', onDelete='raise')
        tbl.column('htmlbag_quot', dtype='X', name_long='!![en]Html quotation doc') 
        tbl.formulaColumn('full_quot',"""$data || coalesce(' - '|| $quot_n, '') || coalesce(' - '|| $oggetto,'')""" )
        tbl.aliasColumn('cliente_br', '@cliente_id.cliente_br')
        tbl.aliasColumn('cliente', '@cliente_id.full_cliente')
        tbl.formulaColumn('servincl_int',"""CASE WHEN @servincl_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='La tariffa sopra esposta si intende comprensiva di:<br>')
        tbl.formulaColumn('servexcl_int',"""CASE WHEN @serviexcl_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='ESCLUSIONI:<br>')
        tbl.formulaColumn('spec_cond_int',"""CASE WHEN @specific_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='Condizioni specifiche:<br>')
        tbl.formulaColumn('surcharges_int',"""CASE WHEN @surcharge_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='Eventuali maggiorazioni:<br>')

    def defaultValues(self):
        return dict(agency_id=self.db.currentEnv.get('current_agency_id'),data = self.db.workdate)
    
    def counter_quot_n(self,record=None):
        #2021/000001
        tbl_agency = self.db.table('agz.agency')
        codice = tbl_agency.readColumns(columns='$code', where = '$id =:ag_id', ag_id=record['agency_id'])
        return dict(format='$K$YYYY/$NNNN', code=codice, period='YYYY', date_field='data', showOnLoad=True, date_tolerant=True, recycle=True)    
    
    @public_method
    def getHTMLDoc(self,quot_id=None,record_template=None,**kwargs):
        testo=TableTemplateToHtml(table=self,record_template=record_template).contentFromTemplate(record=quot_id)
        return testo