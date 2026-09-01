# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('extracost', pkey='id', name_long='!![en]Extra costs', name_plural='!![en]Extra costs',caption_field='id')
        self.sysFields(tbl, counter='quotvers_id')

        tbl.column('quotvers_id',size='22', group='_', name_long='!![en]Quotation id'
                    ).relation('quotazione_versione.id', relation_name='quotazione_extra', mode='foreignkey', onDelete='cascade')
        tbl.column('extra_description', name_short='!![en]Description')
        tbl.column('extra_um', name_short='UM')
        tbl.column('extra_amount', name_short='!![en]Amount', size='10,2',dtype='N', format='#,###.00')


        
