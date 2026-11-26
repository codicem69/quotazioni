
from __future__ import print_function

from gnr.web.batch.btcaction import BaseResourceAction


caption = 'Inizializza servizi economici'
tags = 'admin,user'
description = 'Inizializza la situazione economica dalla versione ufficiale'


class Main(BaseResourceAction):

    batch_prefix = 'ise'
    batch_title = 'Inizializzazione servizi economici'
    batch_delay = 0.5
    batch_steps = 'main'
    batch_cancellable = True

    def step_main(self):
        # Tabelle
        tbl_quotazione = self.db.table('quotazioni.quotazione')
        tbl_versione = self.db.table('quotazioni.quotazione_versione')
        tbl_servizio = self.db.table('quotazioni.quotazione_servizio')
    
        # Recupero della quotazione selezionata
        batch_parameters = self.batch_parameters or {}
        extra_parameters = batch_parameters.get('extra_parameters')
        
        quotazione_ids = extra_parameters.getItem('quotazione_ids') if extra_parameters else None
        
        if not quotazione_ids:
            quotazione_ids = self.get_selection_pkeys()
        
        if isinstance(quotazione_ids, str):
            quotazione_ids = [quotazione_ids]
        
        if len(quotazione_ids) != 1:
            raise Exception('Selezionare una sola quotazione.')
        
        quotazione_id = quotazione_ids[0]
    
        # Recupero della versione scelta nei parametri
        versione_id = self.batch_parameters.get('versione_id')
    
        if not versione_id:
            raise Exception('Selezionare una versione ufficiale.')
    
        # Verifico che la versione appartenga alla quotazione selezionata
        versioni = tbl_versione.query(
            where='$id=:versione_id AND $quotazione_id=:quotazione_id',
            versione_id=versione_id,
            quotazione_id=quotazione_id
        ).fetchAsDict('pkey')
    
        if not versioni:
            raise Exception(
                'La versione selezionata non appartiene alla quotazione.'
            )
    
        # Controllo che non siano già stati inizializzati servizi economici
        servizi_esistenti = tbl_servizio.query(
            where='$quotazione_id=:quotazione_id',
            quotazione_id=quotazione_id
        ).fetchAsDict('pkey')
    
        if servizi_esistenti:
            raise Exception(
                'Esistono già servizi economici per questa quotazione. '
                'Inizializzazione annullata.'
            )
    
        # Definizione delle tabelle sorgenti e dei relativi campi
        sorgenti = [
            {
                'table': 'quotazioni.description',
                'description_field': 'description',
                'um_field': 'um',
                'amount_field': 'amount'
            },
            {
                'table': 'quotazioni.extracost',
                'description_field': 'extra_description',
                'um_field': 'extra_um',
                'amount_field': 'extra_amount'
            },
            {
                'table': 'quotazioni.note',
                'description_field': 'description',
                'um_field': 'um',
                'amount_field': 'amount'
            }
        ]
    
        # Raccolgo tutte le righe da importare
        righe_da_importare = []
    
        for sorgente in sorgenti:
            tbl_sorgente = self.db.table(sorgente['table'])
    
            records = tbl_sorgente.query(
                where='$quotvers_id=:versione_id AND $%s > 0'
                      % sorgente['amount_field'],
                versione_id=versione_id
            ).fetchAsDict('pkey')
    
            # fetchAsDict restituisce:
            # {pkey: Bag, pkey: Bag, ...}
            for source_id, source_record in records.items():
            
                description = source_record[
                    sorgente['description_field']
                ]
                um = source_record[sorgente['um_field']]
                amount = source_record[sorgente['amount_field']]
    
                if amount is None or amount <= 0:
                    continue
                
                righe_da_importare.append({
                    'source_id': source_id,
                    'source_table': sorgente['table'],
                    'description': description,
                    'um': um,
                    'price_cliente': amount
                })
    
        # Nessuna riga da importare
        if not righe_da_importare:
            raise Exception(
                'La versione selezionata non contiene righe con importi '
                'maggiori di zero.'
            )
    
        # Importazione con termometro
        maximum = len(righe_da_importare)
    
        iteratore = self.btc.thermo_wrapper(
            righe_da_importare,
            message=self.messaggio_termometro,
            maximum=maximum
        )
    
        for record in iteratore:
        
            new_record = {
                'quotazione_id': quotazione_id,
                'source_version_id': versione_id,
                'source_table': record['source_table'],
                'source_id': record['source_id'],
                'description': record['description'],
                'um': record['um'],
                'price_cliente': record['price_cliente'],
                'cost_fornitore': None
            }
    
            tbl_servizio.insert(new_record)
    
        # Commit
        self.db.commit()

    def messaggio_termometro(self, record, curr, tot, **kwargs):
        return 'Importazione servizi economici %i/%i' % (curr, tot)

    def table_script_parameters_pane(self, pane, extra_parameters=None,
                                 record_count=None, **kwargs):

        call_kwargs = getattr(self, '_call_kwargs', {}) or {}
        
        extra_parameters = call_kwargs.get('extra_parameters')
        quotazione_ids = extra_parameters.getItem('quotazione_ids') if extra_parameters else None

        if isinstance(quotazione_ids, str):
            quotazione_ids = [quotazione_ids]

        if isinstance(quotazione_ids, str):
            quotazione_ids = [quotazione_ids]

        if not quotazione_ids:
            selection_name = call_kwargs.get('selectionName')
            selected_rowidx = call_kwargs.get('selectedRowidx')
            selection_filter_cb = call_kwargs.get('selectionFilterCb')
            table_name = call_kwargs.get('table')

            selection = self.getUserSelection(
                selectionName=selection_name,
                selectedRowidx=selected_rowidx,
                filterCb=selection_filter_cb,
                table=self.db.table(table_name)
            )
            quotazione_ids = selection.output('pkeylist') if selection else []

        if len(quotazione_ids) != 1:
            raise Exception('Selezionare una sola quotazione.')

        quotazione_id = quotazione_ids[0]

        fb = pane.formbuilder(cols=1, border_spacing='3px')

        fb.dbSelect(
        value='^.versione_id',
        table='quotazioni.quotazione_versione',
        lbl='Versione ufficiale',
        condition='$quotazione_id=:quotazione_id',
        condition_quotazione_id=quotazione_id,
        hasDownArrow=True
        )
