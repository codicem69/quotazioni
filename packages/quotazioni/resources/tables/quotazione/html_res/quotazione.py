from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag


class Main(TableScriptToHtml):
    #pdf_service = 'wk'
    maintable = 'quotazioni.quotazione'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    #virtual_columns = '$note_ag,$bank_dt'
    css_requires='grid'
    #pdf_service = "wk"
    page_header_height = 0
    page_footer_height = 0
    doc_header_height = 35
    doc_footer_height = 30
    grid_header_height = 5
    grid_row_height = 5

    def defineCustomStyles(self):
        self.body.style(""".cell_label{
                            font-size 8pt;
                            text-align:left;
                            color:gray;
                            text-indent:0.5mm;
                            width:auto;
                            font-weight: normal;
                            #line-height:auto;
                            line-height:3mm;
                            height:3mm;}
                           
                            .footer_content{   
                            text-align:right;
                            margin:2mm;
                            }
                            """)

    def docHeader(self, header):
        layout = header.layout(name='doc_header', margin='1mm', border_width=0)
        
        row = layout.row()
        left_cell = row.cell(width=105)
        #center_cell = row.cell()
        right_cell = row.cell(width=80)
       # self.quotazione()

        self.testataLeft(left_cell)
        self.testataRight(right_cell)    
        
        layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Oggetto: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))

        #layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'>{descr_costo}</div>::HTML".format(descr_costo=self.field('descr_costo')))
        
        #layout.row(height=15)
     
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
  
    def datiQuot(self,row):
        dati_layout = row.cell().layout(name='datiQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')

        dati_layout.row().cell(self.field('data'), lbl="Date", font_size='10pt')
        dati_layout.row().cell(self.field('quot_n'), lbl="Quotation no.", font_size='10pt')

    def datiCliente(self, row):
        
        cliente_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')
        customer = "<div style='font-size:10pt;padding:1px'><strong>{rag_soc}<br>&nbsp;{indirizzo}<br>&nbsp;{cap}&nbsp;{city}</strong></div>::HTML".format(rag_soc=self.field('@cliente_id.rag_sociale'),indirizzo=self.field('@cliente_id.address'),cap=self.field('@cliente_id.cap'),city=self.field('@cliente_id.city'))

        cliente_layout.row().cell(customer, lbl="Customer")

    def gridData(self):
        result = Bag()
        tbl_quotazione = self.db.table('quotazioni.quotazione')
        dati_quotazione = tbl_quotazione.record(self.record['id']).output('dict')
        quot_id = tbl_quotazione.record(self.record['id']).output('record')
        quotazione_id = dati_quotazione['id']
        
        first_description = self.db.table('quotazioni.description').query(columns='$description,$amount',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        extracost = self.db.table('quotazioni.extracost').query(columns='$extra_description as description,$extra_amount as amount',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        serv_incl = self.db.table('quotazioni.services_incl').query(columns='@servicesincl_id.description as description',
                                                                    where='quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        surcharges = self.db.table('quotazioni.surcharges').query(columns='@surcharges_id.description as description',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        serv_excl = self.db.table('quotazioni.services_excl').query(columns='@servicesexcl_id.description as description',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        specific_cond = self.db.table('quotazioni.specific_cond').query(columns='$description',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        working_times = self.db.table('quotazioni.times_work').query(columns='@worktimes_id.description as description',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        note = self.db.table('quotazioni.note').query(columns='$description,$amount',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        payment_cond = self.db.table('quotazioni.paymentcond').query(columns='@paymentcond_id.description as description',
                                                                    where='$quotazione_id=:p_id',
                                                                    p_id=self.record['id']).fetch()
        
        righe = []
        #con il ciclo for andiamo a inserire nella descrizione e  importo della first_description i tag strong per avere la scritta bold
        for r in range(len(first_description)):
            if first_description[r]['amount'] is None:
                amount = ''
            else:
                amount = first_description[r]['amount']
            update = {'description':'<strong>'+ str(first_description[r]['description'])+'</strong>::HTML','amount':'<strong>'+ amount +'</strong>::HTML'}
            first_description = [{**d,**update} for d in first_description]
        righe = righe + first_description
        righe = righe + extracost
        if serv_incl:
            righe.append(dict(description='<strong>La tariffa sopra esposta si intende comprensiva di:</strong>'+"::HTML", amount=''))
        righe = righe + serv_incl
        if specific_cond:
            righe.append(dict(description='<strong>Condizioni specifiche:</strong>'+"::HTML", amount=''))
        righe = righe + specific_cond
        if serv_excl:
            righe.append(dict(description='<strong>Servizi esclusi:</strong>'+"::HTML", amount=''))
        righe = righe + serv_excl
        if surcharges:
            righe.append(dict(description='<strong>Eventuali maggiorazioni:</strong>'+"::HTML", amount=''))
        righe = righe + surcharges
        if working_times:
            righe.append(dict(description='<strong><br></strong></br>'+"::HTML", amount=''))
        righe = righe + working_times    
        righe = righe + note
        if payment_cond:
            righe.append(dict(description='<strong>Condizioni di pagamento:</strong>'+"::HTML", amount=''))
        righe = righe + payment_cond
    
        return righe
        
   #def calcRowHeight(self):
   #    #Determina l'altezza di ogni singola riga con approssimazione partendo dal valore di riferimento grid_row_height
   #    descr_descrizione_offset = 80
   #    #Stabilisco un offset in termini di numero di caratteri oltre il quale stabilirò di andare a capo.
   #    #Attenzione che in questo caso ho una dimensione in num. di caratteri, mentre la larghezza della colonna è definita
   #    #in mm, e non avendo utti i caratteri la stessa dimensione si tratterà quindi di individuare la migliore approssimazione
   #    n_rows_nome_descr = len(self.rowField('description'))//descr_descrizione_offset + 1
   #    n_rows_nome_tariffa = len(self.rowField('amount'))//80 + 1
   #    #In caso di valori in relazione, è necessario utilizzare "_" nel metodo rowField per recuperare correttamente i valori
   #    #A tal proposito si consiglia comunque sempre di utilizzare le aliasColumns
   #    n_rows = max(n_rows_nome_descr,n_rows_nome_tariffa )#, n_rows_nome_provincia)
   #    height = (self.grid_row_height * n_rows)
   #    return height
    
    def gridStruct(self,struct):
        r = struct.view().rows()
       
        r.cell('description', name='Descrizione', content_class="breakword")
        r.cell('amount', mm_width=40, name=' ',content_class="breakword")

    def gridLayout(self, grid):
                return grid.layout(name='rowsL',um='mm',border_color='gray',
                                   top=1,bottom=1,left=1,right=1,
                                   border_width=0,lbl_class='caption',
                                   style='line-height:5mm;text-align:left;font-size:7.5pt;')
    
    def docFooter(self, footer, lastPage=None):
        layout = footer.layout('footer',top=0,left=0.1,border_width=0,
                           lbl_class='caption', 
                           content_class = 'footer_content')
        quotazione_firma = layout.row(height=40, lbl_height=4, lbl_class='smallCaption')
        self.quotazioneFirma(quotazione_firma)

    def quotazioneFirma(self,row):
        dati_layout = row.cell().layout(name='firmaQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:4mm;text-indent:0mm;')
        dati_layout.row().cell()
        dati_layout.row().cell()
        dati_layout = row.cell().layout(name='firmaQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:4mm;text-indent:0mm;')
        dati_layout.row(height=5).cell(self.field('@agency_id.agency_name')+"::HTML", lbl="")
        timbro=self.record['@agency_id.agency_stamp']
        #timbro=self.page.externalUrl(stamp)
        dati_layout.row().cell("""<img src="%s" width="100" height="100">::HTML""" %timbro,lbl='')
