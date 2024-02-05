# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('extracost', pkey='id', name_long='!![en]Extra costs', name_plural='!![en]Extra costs',caption_field='id')
        self.sysFields(tbl, counter='quotazione_id')

        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation id'
                    ).relation('quotazione.id', relation_name='quotazione_extra', mode='foreignkey', onDelete='cascade')
        tbl.column('extra_description', name_short='!![en]Description')
        tbl.column('extra_amount', name_short='!![en]Amount')


        