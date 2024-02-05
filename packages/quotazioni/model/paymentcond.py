# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('paymentcond', pkey='id', name_long='!![en]Payment conditions', name_plural='!![en]Payment conditions',caption_field='paymentcond_id')
        self.sysFields(tbl,counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione.id', relation_name='paym_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('paymentcond_id',size='22', group='_', name_long='!![en]Payment conditions'
                    ).relation('payment_cond.id', relation_name='paym_cond', mode='foreignkey', onDelete='raise')
        