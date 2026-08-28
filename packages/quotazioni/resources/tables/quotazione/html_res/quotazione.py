from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from decimal import Decimal


class Main(TableScriptToHtml):
    #pdf_service = 'wk'
    maintable = 'quotazioni.quotazione'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    #virtual_columns = '$note_ag,$bank_dt'
    css_requires='grid'
    #pdf_service = "wk"
    page_header_height = 0
    page_footer_height = 0
    doc_header_height = 0
    doc_footer_height = 35
    grid_header_height = 0
    grid_row_height = 6
    # Questo flag ci servirà per capire se abbiamo già stampato l'header una volta


    # -----------------------------------------------------------------------
    # Larghezza totale della colonna "description" + "um" + "amount" in mm.
    # Adatta questo valore alla somma reale delle tue colonne (es: 105+10+20).
    # Viene usato dall'helper _full_row per simulare il colspan.
    # -----------------------------------------------------------------------
    FULL_ROW_WIDTH_MM = 180   # description (~105mm) + um (10mm) + amount (20mm)

    def defineCustomStyles(self):
            self.body.style("""
                /* Rende la tabella fluida ed evita che le righe si sormontino */
                .grid_table {
                    table-layout: auto !important;
                    height: auto !important;
                }

                .grid_row, tr {
                    height: auto !important;
                    page-break-inside: avoid !important;
                }

                td.grid_cell {
                    height: auto !important;
                    vertical-align: top !important;
                    padding-top: 1.5mm !important;
                    padding-bottom: 1.5mm !important;
                    line-height: 1.3 !important;
                }

                .cell_label {
                    font-size: 8pt;
                    color: gray;
                }

                .footer_content {
                    text-align: right;
                }
            """)


    # -----------------------------------------------------------------------
    # Helper: crea una riga che si estende visivamente su tutta la larghezza,
    # simulando un colspan=3. Le celle um e amount vengono lasciate vuote.
    # Parametri:
    #   text  – testo da mostrare (può contenere HTML)
    #   bold  – True per wrappare in <strong> (default True)
    #   is_html – True se text contiene già tag HTML (default False)
    # -----------------------------------------------------------------------
    def _full_row(self, text, bold=True, is_html=False):
            if bold and not is_html:
                inner = "<strong>{}</strong>".format(text)
            elif bold and is_html:
                inner = "<strong>{}</strong>".format(text)
            else:
                inner = text

            html = (
                "<div style='width:{width}mm; overflow:visible; white-space:normal; "
                "font-size:9.5pt;'>{inner}</div>::HTML"
            ).format(width=self.FULL_ROW_WIDTH_MM, inner=inner)

            return dict(description=html, um='', amount='')


    def docHeader(self, header):
            # Wrappiamo l'header in un div con altezza/padding dedicato
            # Quando il CSS nasconde .doc_header, nasconde anche questo spazio!
            layout = header.layout(name='doc_header', margin='0mm', border_width=0, style='height:45mm; overflow:hidden;')

            row = layout.row()
            left_cell = row.cell(width=105)
            right_cell = row.cell(width=80)

            self.testataLeft(left_cell)
            self.testataRight(right_cell)

            # Spazio/Oggetto
            if self.field('oggetto'):
                layout.row().cell(
                    "<div style='font-size:10pt; padding-top:5mm;'><strong>Oggetto: {}</strong></div>::HTML".format(
                        self.field('oggetto') or ''
                    )
                )


    def pageHeader(self, builder):
            pass

    def testataLeft(self, c):
        layout = c.layout('dati_quotazione',
                    lbl_class='cell_label',
                    border_width=0)
        dati_quot = layout.row(height=30, lbl_height=4, lbl_class='smallCaption')
        self.datiQuot(dati_quot)

    def testataRight(self, c):
        layout = c.layout('dati_cliente',
                    lbl_class='cell_label',
                    border_width=0)
        dati_cliente = layout.row(height=30, lbl_height=4, lbl_class='smallCaption')
        self.datiCliente(dati_cliente)
  
    def datiQuot(self, row):
        dati_layout = row.cell().layout(name='datiQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')

        dati_layout.row().cell(self.field('data'), lbl="Date", font_size='10pt')
        dati_layout.row().cell(self.field('quot_n'), lbl="Quotation no.", font_size='10pt')

    def datiCliente(self, row):
        cliente_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')
        customer = (
            "<div style='font-size:10pt;padding:1px'>"
            "<strong>{rag_soc}<br>&nbsp;{indirizzo}<br>&nbsp;{cap}&nbsp;{city}</strong>"
            "</div>::HTML"
        ).format(
            rag_soc=self.field('@cliente_id.rag_sociale'),
            indirizzo=self.field('@cliente_id.address'),
            cap=self.field('@cliente_id.cap'),
            city=self.field('@cliente_id.city')
        )
        cliente_layout.row().cell(customer, lbl="Customer")

    def gridData(self):
            result = Bag()
            tbl_quotazione = self.db.table('quotazioni.quotazione')
            dati_quotazione = tbl_quotazione.record(self.record['id']).output('dict')
            quot_id = tbl_quotazione.record(self.record['id']).output('record')
            quotazione_id = dati_quotazione['id']

            first_description = self.db.table('quotazioni.description').query(
                columns='$description,$um,$amount',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            extracost = self.db.table('quotazioni.extracost').query(
                columns='$extra_description as description,$extra_um as um,$extra_amount as amount',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            serv_incl = self.db.table('quotazioni.services_incl').query(
                columns='@servicesincl_id.description as description',
                where='quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            surcharges = self.db.table('quotazioni.surcharges').query(
                columns='@surcharges_id.description as description',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            serv_excl = self.db.table('quotazioni.services_excl').query(
                columns='@servicesexcl_id.description as description',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            specific_cond = self.db.table('quotazioni.specific_cond').query(
                columns='$description',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            working_times = self.db.table('quotazioni.times_work').query(
                columns='@worktimes_id.description as description',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            note = self.db.table('quotazioni.note').query(
                columns='$description,$um,$amount',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            payment_cond = self.db.table('quotazioni.paymentcond').query(
                columns='@paymentcond_id.description as description',
                where='$quotazione_id=:p_id',
                p_id=self.record['id']
            ).fetch()

            righe = []

            # =========================================================================
            # 1. TESTATA DOCUMENTO (SOLO PRIMA PAGINA)
            # =========================================================================
            cliente_rag = self.field('@cliente_id.rag_sociale') or ''
            cliente_add = self.field('@cliente_id.address') or ''
            cliente_cap = self.field('@cliente_id.cap') or ''
            cliente_city = self.field('@cliente_id.city') or ''
            quot_data = self.field('data') or ''
            quot_num = self.field('quot_n') or ''
            oggetto_txt = self.field('oggetto') or ''

            testata_html = """
                    <div style="width:100%; margin-bottom: 5mm; font-family: Arial, sans-serif;">
                        <table style="width:100%; border-collapse:collapse; border:none;">
                            <tr>
                                <td style="width:50%; vertical-align:top; font-size:9pt; line-height:1.4;">
                                    <span style="color:gray; font-size:8pt;">Date</span><br>
                                    <strong>{}</strong><br><br>
                                    <span style="color:gray; font-size:8pt;">Quotation no.</span><br>
                                    <strong>{}</strong>
                                </td>
                                <td style="width:50%; vertical-align:top; font-size:9.5pt; line-height:1.4;">
                                    <span style="color:gray; font-size:8pt;">Customer</span><br>
                                    <strong>{}</strong><br>
                                    {}<br>
                                    {} {}
                                </td>
                            </tr>
                        </table>
                        <div style="margin-top:4mm; font-size:10pt;">
                            <strong>Oggetto: {}</strong>
                        </div>
                    </div>
                    """.format(quot_data, quot_num, cliente_rag, cliente_add, cliente_cap, cliente_city, oggetto_txt)

            righe.append(dict(
                description=testata_html + "::HTML",
                um='',
                amount=''
            ))


            # =========================================================================
            # CORPO DEL TESTO (body_in) - INSERITO IN UN'UNICA RIGA CON <br>
            # =========================================================================
            body_txt = self.field('body_in') or ''
            if body_txt:
                # Sostituiamo gli a capo con <br>
                body_formatted = body_txt.replace('\n', '<br>')
                html_body = "<div style='font-size:9.5pt; line-height:1.4; margin-bottom:3mm;'>{}</div>::HTML".format(body_formatted)
                righe.append(dict(
                    description=html_body,
                    um='',
                    amount=''
                ))


            # =========================================================================
            # 2. PREZZI E TARIFFE BASE
            # =========================================================================
            for item in first_description:
                val = item['amount']
                amount_str = '' if val is None else "{:.2f}".format(val).replace('.', ',')
                righe.append(dict(
                    description="<strong>{}</strong>::HTML".format(item['description']),
                    um=item.get('um') or '',
                    amount="<strong>{}</strong>::HTML".format(amount_str),
                    _class='riga-fluida'
                ))

            # Stacco di spaziatura
            righe.append(dict(
                description='<div style="height:3mm; line-height:3mm;"></div>::HTML',
                um='',
                amount='',
                _class='riga-fluida'
            ))

            # =========================================================================
            # 3. EXTRACOST (OGNI VOCE È UNA RIGA DEDICATA)
            # =========================================================================
            if extracost:
                for item in extracost:
                    val_ex = item.get('amount')
                    amount_ex_str = '' if val_ex is None else "{:.2f} €".format(val_ex).replace('.', ',')
                    righe.append(dict(
                        description="<div style='font-size:9.5pt;'>{}</div>::HTML".format(item['description']),
                        um=item.get('um') or '',
                        amount="<div style='font-size:9.5pt; font-weight:bold;'>{}</div>::HTML".format(amount_ex_str),
                        _class='riga-fluida'
                    ))

            # =========================================================================
            # 4. HELPER E SEZIONI TESTUALI "ATOMIZZATE"
            # =========================================================================
            def _aggiungi_sezione_atomica(titolo, lista_voci):
                # 1. Aggiungiamo il Titolo
                html_titolo = (
                    "<div style='margin-top:10px; font-weight:bold; font-size:10pt; "
                    "font-family:Arial, sans-serif; page-break-after:avoid;'>{}</div>::HTML"
                ).format(titolo)
                righe.append(dict(description=html_titolo, um='', amount='', _class='riga-fluida'))

                # 2. Aggiungiamo ogni singola voce come RIGA AUTONOMA
                for voce in lista_voci:
                    html_voce = (
                        "<div style='font-size:9.5pt; margin-top:2px; "
                        "font-family:Arial, sans-serif;'>{}</div>::HTML"
                    ).format(voce['description'])
                    righe.append(dict(description=html_voce, um='', amount='', _class='riga-fluida'))

            # APPLICAZIONE SEZIONI
            if serv_incl:
                _aggiungi_sezione_atomica('La tariffa sopra esposta si intende comprensiva di:', serv_incl)

            if specific_cond:
                _aggiungi_sezione_atomica('Condizioni specifiche:', specific_cond)

            if serv_excl:
                _aggiungi_sezione_atomica('Servizi esclusi:', serv_excl)

            if surcharges:
                _aggiungi_sezione_atomica('Eventuali maggiorazioni:', surcharges)

            if working_times:
                for voce in working_times:
                    html_wt = "<div style='font-size:9.5pt; margin-top:6px; font-family:Arial, sans-serif;'>{}</div>::HTML".format(voce['description'])
                    righe.append(dict(description=html_wt, um='', amount='', _class='riga-fluida'))

            if note:
                for item in note:
                    val_note = item.get('amount')
                    amount_note = '' if val_note is None else "{:.2f}".format(val_note).replace('.', ',')
                    righe.append(dict(
                        description="<div style='margin-top:6px; font-size:9.5pt;'>{}</div>::HTML".format(item['description']),
                        um=item.get('um') or '',
                        amount="<div style='margin-top:6px; font-size:9.5pt; text-align:right;'>{}</div>::HTML".format(amount_note),
                        _class='riga-fluida'
                    ))

            if payment_cond:
                _aggiungi_sezione_atomica('Condizioni di pagamento:', payment_cond)

            return righe





    def calcRowHeight(self):
            # Determina l'altezza di ogni singola riga con approssimazione
            descr_descrizione_offset = 80
            n_rows_nome_descr = len(self.rowField('description')) // descr_descrizione_offset + 1
            n_rows_nome_tariffa = len(self.rowField('amount')) // 80 + 1
            n_rows = max(n_rows_nome_descr, n_rows_nome_tariffa)
            height = self.grid_row_height * n_rows
            return height



    #def calcRowHeight(self):
    #    # 1. SOLUZIONE DEFINTIVA SPAZI ENORMI:
    #    # Controlliamo se la riga corrente appartiene ai blocchi di testo o extracost fluidi.
    #    # Usiamo self.rowField('_class') per intercettare la classe assegnata nel gridData.
    #    if self.rowField('_class') == 'riga-fluida':
    #        return 0  # Restituendo 0, Genropy non impone altezze fisse e WeasyPrint stringe tutto al millimetro
    #
    #    # 2. IL TUO CODICE ORIGINALE DI CALCOLO
    #    # Determina l'altezza di ogni singola riga con approssimazione per i prezzi standard
    #    descr_descrizione_offset = 80
    #    n_rows_nome_descr = len(self.rowField('description')) // descr_descrizione_offset + 1
    #    n_rows_nome_tariffa = len(self.rowField('amount')) // 80 + 1
    #    n_rows = max(n_rows_nome_descr, n_rows_nome_tariffa)
    #    height = self.grid_row_height * n_rows
    #    return height

    def gridStruct(self, struct):
            r = struct.view().rows()
            r.cell('description', name='Descrizione', width='100%', content_class="breakword")
            r.cell('um', name=' ', mm_width=12)
            r.cell('amount', mm_width=25, name=' ', content_class='aligned_right', dtype='N', format='#,###.00')


    #def gridStruct(self, struct):
    #        r = struct.view().rows()
    #        # Impostiamo la colonna description in modo che occupi tutto lo spazio residuo
    #        r.cell('description', name='Descrizione', content_class="breakword")
    #        r.cell('um', name=' ', mm_width=12)
    #        r.cell('amount', mm_width=25, name=' ', content_class='aligned_right', dtype='N', format='#,###.00')

    def gridLayout(self, grid):
            return grid.layout(
                name='rowsL',
                um='mm',
                border_color='white',
                top=0,
                bottom=0,
                left=0,
                right=0,
                border_width=0,
                lbl_class='caption',
                style='line-height:5mm; font-size:9.5pt;'
            )



    #def gridLayout(self, grid):
    #    return grid.layout(name='rowsL', um='mm', border_color='gray',
    #                       top=1, bottom=1, left=1, right=20,
    #                       border_width=0, lbl_class='caption',
    #                       style='line-height:5mm;font-size:9.5pt;')

    def docFooter(self, footer, lastPage=None):
        if not lastPage:
                    return

        layout = footer.layout('footer', top=0, left=0.1, border_width=0,
                           lbl_class='caption',
                           content_class='footer_content', style='font-size:10pt;')
        quotazione_firma = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        self.quotazioneFirma(quotazione_firma)

    def quotazioneFirma(self, row):
        dati_layout = row.cell().layout(name='firmaQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:4mm;text-indent:0mm;')
        dati_layout = row.cell().layout(name='firmaQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:4mm;text-indent:0mm;text-align:center;')
        dati_layout.row(height=5).cell(self.field('@agency_id.agency_name') + "::HTML", lbl="")
        timbro = self.record['@agency_id.agency_stamp']
        dati_layout.row().cell("""<img src="%s" width="120" height="120">::HTML""" % timbro, lbl='')

    def outputDocName(self, ext=''):
        if ext and not ext[0] == '.':
            ext = '.%s' % ext
        if self.getData('record.quot_n'):
            doc_name = 'Quotation_{quot}{ext}'.format(
                quot=self.getData('record.quot_n').replace("/", ""),
                ext=ext
            )
        else:
            doc_name = 'Quotation{ext}'.format(ext=ext)
        return doc_name
