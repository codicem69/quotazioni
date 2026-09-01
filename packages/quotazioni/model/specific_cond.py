# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('specific_cond', pkey='id', name_long='!![en]Specific conditions', name_plural='!![en]Specific conditions',caption_field='description')
        self.sysFields(tbl, counter='quotvers_id')
        tbl.column('quotvers_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione_versione.id', relation_name='specific_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('description', name_short='!![en]Description')
        
