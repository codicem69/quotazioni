# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('times_work', pkey='id', name_long='!![en]Working times', name_plural='!![en]Working times',caption_field='worktimes_id')
        self.sysFields(tbl,counter='quotazione_id')
        tbl.column('quotazione_id',size='22', group='_', name_long='!![en]Quotation'
                    ).relation('quotazione.id', relation_name='times_quot', mode='foreignkey', onDelete='cascade')
        tbl.column('worktimes_id',size='22', group='_', name_long='!![en]Working times'
                    ).relation('working_times.id', relation_name='work_times', mode='foreignkey', onDelete='raise')
        