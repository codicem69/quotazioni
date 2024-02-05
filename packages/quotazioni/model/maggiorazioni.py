class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('maggiorazioni', pkey='id', name_long='!![en]Surcharges', name_plural='!![en]Surcharges',caption_field='description', 
                              lookup=True)
        self.sysFields(tbl)
        tbl.column('description', name_short='!![en]Description')