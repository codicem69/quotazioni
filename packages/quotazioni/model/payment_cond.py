class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('payment_cond', pkey='id', name_long='!![en]Payment conditions', name_plural='!![en]Payment conditions',caption_field='description', 
                              lookup=True)
        self.sysFields(tbl)
        tbl.column('description', name_short='!![en]Description')