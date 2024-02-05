class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('services', pkey='id', name_long='!![en]Services', name_plural='!![en]Services',caption_field='description', 
                              lookup=True)
        self.sysFields(tbl)
        tbl.column('description', name_short='!![en]Description')