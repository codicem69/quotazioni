# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('services_excl', pkey='id', name_long='!![en]Services excluded', name_plural='!![en]Services excluded',caption_field='servicesexcl_id')
        self.sysFields(tbl,counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione.id', relation_name='serviexcl_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('servicesexcl_id',size='22', group='_', name_long='!![en]Services excluded'
                    ).relation('services.id', relation_name='serv_excl', mode='foreignkey', onDelete='raise')
        