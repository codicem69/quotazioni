# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('description', pkey='id', name_long='!![en]Description', name_plural='!![en]Description',caption_field='description')
        self.sysFields(tbl, counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation id'
                    ).relation('quotazione.id', relation_name='description_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('description', name_short='!![en]First description')
        tbl.column('amount', name_short='!![en]Amount')