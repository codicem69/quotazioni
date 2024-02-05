# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('quotazione_ricevuta', pkey='id', name_long='!![en]Quotation received', name_plural='!![en]Quotations received',caption_field='description')
        self.sysFields(tbl)
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation id'
                    ).relation('quotazione.id', relation_name='quot_ricevuta', mode='foreignkey', onDelete='cascade')
        tbl.column('description', name_short='!![en]Description')