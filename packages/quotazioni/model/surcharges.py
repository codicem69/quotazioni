class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('surcharges', pkey='id', name_long='!![en]Surcharges', name_plural='!![en]Surcharges',caption_field='surcharges_id')
        self.sysFields(tbl,counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione.id', relation_name='surcharge_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('surcharges_id',size='22', group='_', name_long='!![en]Surcharges'
                    ).relation('maggiorazioni.id', relation_name='maggiorazioni', mode='foreignkey', onDelete='raise')