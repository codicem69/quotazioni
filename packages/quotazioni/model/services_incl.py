# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('services_incl', pkey='id', name_long='!![en]Services included', name_plural='!![en]Services included',caption_field='servicesincl_id')
        self.sysFields(tbl,counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione.id', relation_name='servincl_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('servicesincl_id',size='22', group='_', name_long='!![en]services included'
                    ).relation('services.id', relation_name='serv_incl', mode='foreignkey', onDelete='raise')
        
    