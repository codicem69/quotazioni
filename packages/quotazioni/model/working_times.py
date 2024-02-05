class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('working_times', pkey='id', name_long='!![en]Working times', name_plural='!![en]Working times',caption_field='description', 
                              lookup=True)
        self.sysFields(tbl)
        tbl.column('description', name_short='!![en]Description')