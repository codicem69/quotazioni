# encoding: utf-8

class Table(object):

    def config_db(self, pkg):
        tbl = pkg.table('quotazione_servizio_storico',pkey='id',name_long='!![en]Economic service history',name_plural='!![en]Economic service history',
            caption_field='campo')
        self.sysFields(tbl)

        tbl.column('quotazione_servizio_id',size='22',group='_',name_long='!![en]Economic service').relation(
            'quotazione_servizio.id',relation_name='storico_economico',mode='foreignkey',onDelete='cascade')
        tbl.column('campo',name_long='!![en]Modified field',values='price_cliente:Customer price,cost_fornitore:Supplier cost')
        tbl.column('valore_precedente',name_long='!![en]Previous value',size='12,2',dtype='N',format='#,###.00')
        tbl.column('valore_nuovo',name_long='!![en]New value',size='12,2',dtype='N',format='#,###.00')
        tbl.column('data_modifica',name_long='!![en]Modification date',dtype='DH')
        tbl.column('utente_modifica',name_long='!![en]Modified by')
        tbl.column('origine', name_long='!![en]Update origin', values='manuale:Manuale,email:Email,altro:Altro')
        tbl.column('motivo', name_long='!![en]Reason')