# encoding: utf-8
from datetime import datetime

class Table(object):

    def config_db(self, pkg):
        tbl = pkg.table('quotazione_servizio', pkey='id', name_long='!![en]Economic service', name_plural='!![en]Economic services',
            caption_field='description')
        self.sysFields(tbl)

        tbl.column('quotazione_id', size='22', group='_', name_long='!![en]Quotation').relation(
            'quotazione.id', relation_name='servizi_economici', mode='foreignkey', onDelete='cascade')

        # Riferimento alla versione e alla riga da cui è stata
        # inizializzata la voce. Sono riferimenti tecnici interni.
        tbl.column('source_version_id',size='22',group='_',name_long='!![en]Source version').relation(
            'quotazione_versione.id',relation_name='servizi_economici_origine',mode='foreignkey')

        tbl.column('source_table', name_long='!![en]Source table')
        tbl.column('source_id', size='22', name_long='!![en]Source record')

        # Dati della voce economica
        tbl.column('description', name_long='!![en]Description')
        tbl.column('um', name_long='!![en]Unit of measure')
        tbl.column('tipo_prezzo', name_long='!![en]Price type', values='FORFAIT,UNITARIO', validate_notnull=True)

        # Prezzi unitari
        tbl.column('price_cliente',name_long='!![en]Customer unit price',size='12,2',dtype='N',format='#,###.00')
        tbl.column('cost_fornitore',name_long='!![en]Supplier unit cost',size='12,2',dtype='N',format='#,###.00')

        tbl.column('note', name_long='!![en]Notes')

        # Totali e margini

        tbl.formulaColumn('margine',
            """CASE
                 WHEN $cost_fornitore IS NULL THEN NULL
                 ELSE $price_cliente - $cost_fornitore
               END""",
            dtype='N'
        )

        tbl.formulaColumn('margine_percentuale',
            """CASE
                 WHEN $cost_fornitore IS NULL
                      OR $price_cliente IS NULL
                      OR $price_cliente = 0
                 THEN NULL
                 ELSE (($price_cliente - $cost_fornitore) / $price_cliente) * 100
               END""",
            dtype='N'
        )
        tbl.formulaColumn('totale_cliente_forfait',
            """CASE
                 WHEN $tipo_prezzo = 'FORFAIT'
                 THEN $price_cliente
                 ELSE NULL
               END""",
            dtype='N')

        tbl.formulaColumn('totale_fornitore_forfait',
            """CASE
                 WHEN $tipo_prezzo = 'FORFAIT'
                 THEN $cost_fornitore
                 ELSE NULL
               END""",
            dtype='N')

        tbl.formulaColumn('margine_forfait',
            """CASE
                 WHEN $tipo_prezzo = 'FORFAIT'
                 THEN $margine
                 ELSE NULL
               END""",
            dtype='N')

    def trigger_onUpdated(self, record, old_record=None):
        if not old_record:
            return

        tbl_storico = self.db.table('quotazioni.quotazione_servizio_storico')

        campi_da_controllare = [
            'tipo_prezzo',
            'price_cliente',
            'cost_fornitore'
        ]

        for campo in campi_da_controllare:
            valore_precedente = old_record.get(campo)
            valore_nuovo = record.get(campo)

            if valore_precedente != valore_nuovo:
                if valore_precedente in (None, ''):
                    continue
                tbl_storico.insert({
                    'quotazione_servizio_id': record['id'],
                    'campo': campo,
                    'valore_precedente': str(valore_precedente) if valore_precedente is not None else None,
                    'valore_nuovo': str(valore_nuovo) if valore_nuovo is not None else None,
                    'data_modifica': datetime.now(),
                    'utente_modifica': self.db.currentEnv.get('user'),
                    'origine': 'manuale'
                }) 