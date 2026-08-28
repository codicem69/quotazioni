# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml
from datetime import datetime

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('quotazione_versione', pkey='id', name_long='!![en]Quotation version', name_plural='!![en]Quotation versions',caption_field='quot_no')
        self.sysFields(tbl,counter='quotazione_id')
        
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation').relation('quotazione.id',
            relation_name='quot_vers', mode='foreignkey',onDelete='cascade')
        tbl.column('version', name_long='!![en]Version')
        tbl.column('data', dtype='D', name_long='!![en]Date', name_short='!![en]Date')
        tbl.column('oggetto', name_short='!![en]Subject')
        tbl.column('firma', dtype='B', name_long='!![en]Signature', name_short='!![en]Sign')
        tbl.column('body_in', name_long='!![en]Body first')
        tbl.column('htmlbag_quot', dtype='X', name_long='!![en]Html quotation doc')
        tbl.column('note_vers', name_long='!![en]Note')
        tbl.column('data_invio', dtype='DH', name_long='!![en]Send date')
        tbl.column('accettazione', dtype='B',name_long='Accettazione')
        tbl.column('pathtopdf',name_long='pathtopdf')
        tbl.pyColumn('acceptance',name_long='Acceptance', dtype='T')
        tbl.aliasColumn('cliente_br', '@quotazione_id.@cliente_id.cliente_br')
        tbl.aliasColumn('cliente', '@quotazione_id.@cliente_id.full_cliente')
        tbl.aliasColumn('agencystamp','@quotazione_id.@agency_id.agency_stamp',dtype='P')
        tbl.formulaColumn('stamp',"""CASE WHEN $firma THEN $agencystamp ELSE NULL END""", dtype='P')
        tbl.formulaColumn('agent_sign',"""CASE WHEN $firma THEN @quotazione_id.@agency_id.agency_name ELSE NULL END""")
        tbl.formulaColumn('servincl_int',"""CASE WHEN @servincl_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='La tariffa sopra esposta si intende comprensiva di / The rate listed above includes:<br>')
        tbl.formulaColumn('servexcl_int',"""CASE WHEN @serviexcl_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='ESCLUSIONI / EXCLUSIONS:<br>')
        tbl.formulaColumn('spec_cond_int',"""CASE WHEN @specific_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='Condizioni specifiche / Specific Conditions:<br>')
        tbl.formulaColumn('surcharges_int',"""CASE WHEN @surcharge_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='Eventuali maggiorazioni / Any surcharges:<br>')
        tbl.formulaColumn('workingtimes_int',"""CASE WHEN @times_quot.id IS NOT NULL THEN :testo ELSE '' END""", dtype='T', var_testo='Orari di lavoro / Working times:<br>')
        tbl.formulaColumn('quot_no',"""coalesce(@quotazione_id.quot_n, '') || coalesce(' - '|| $version,'')""" )
        


    def pyColumn_acceptance(self,record,field):
            if record['accettazione']==True:
                accettazione_quot = self.db.application.getPreference('accettazione',pkg='quotazioni')
                quot_id = record['quotazione_id']
                tbl_quotazione = self.db.table('quotazioni.quotazione')
                rec_quot = tbl_quotazione.record(quot_id, ignoreMissing=True).output('bag')
                cliente_id = rec_quot['cliente_id']
                cliente_nome = rec_quot.getItem('@cliente_id.rag_sociale')
                agency_id = rec_quot['@agency_id']
                agency_name = agency_id.getItem('agency_name')
                
                variables = {"${cliente}": cliente_nome,"${agency}":agency_name}
                #con il ciclo for sostituiamo le variabili nel record prelevati dalle preferenze
                for variable_key, variable_value in variables.items():
                    accettazione_quot = accettazione_quot.replace(variable_key, variable_value)                    
            else:
                accettazione_quot = ''
            return accettazione_quot   
    
    def defaultValues(self):
            return dict(data = self.db.workdate)

    def counter_version(self,record=None):
            #01
            return dict(format='$K/$NN',code='V', date_field='data', showOnLoad=True, date_tolerant=True, recycle=True)

    @public_method
    def getHTMLDoc(self,quot_id=None,record_template=None,**kwargs):
       testo=TableTemplateToHtml(table=self,record_template=record_template).contentFromTemplate(record=quot_id)
       return testo