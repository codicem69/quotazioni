# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('cliente', pkey='id', name_long='!![en]Customer', name_plural='!![en]Customers',caption_field='full_cliente')
        self.sysFields(tbl)

        tbl.column('rag_sociale', name_short='!![en]Company name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('cap', name_short='!![en]CAP')
        tbl.column('city', name_short='!![en]City place')
        tbl.column('email', name_short='Email')
        tbl.column('tel', name_short='Tel.')
        tbl.column('note', name_short='Note')
        tbl.formulaColumn('full_cliente',"""$rag_sociale || coalesce(' - '|| $address, '') || coalesce(' - '|| $cap,'') || coalesce(' - '|| $city,'')""" )
        