# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('corrispondenza', pkey='id', name_long='!![en]Correspondence', name_plural='!![en]Correspondence',caption_field='description')
        self.sysFields(tbl)
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation id'
                    ).relation('quotazione.id', relation_name='corrisp', mode='foreignkey', onDelete='cascade')
        tbl.column('tipo', size='20', name_long='!![en]Type',values='email ricevuta,email inviata,telefonata,nota interna,richiesta cliente,risposta fornitore,altro')
        tbl.column('data_comunicazione', dtype='DH', name_long='!![en]Communication date')
        tbl.column('oggetto', name_long='!![en]Subject')
        tbl.column('mittente', name_long='!![en]Sender')
        tbl.column('destinatario', name_long='!![en]Recipient')
        tbl.column('description', name_short='!![en]Description')
        tbl.column('stato', size='15', name_long='!![en]Status', values='DRAFT,SENT,RECEIVED,READ,ARCHIVED')
