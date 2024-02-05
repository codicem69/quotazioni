from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrdecorator import public_method

class Main(TableScriptToHtml):
    #pdf_service = 'wk'
    maintable = 'quotazioni.quotazione'
    #Non indicheremo una row_table ma solo una maintable perché stamperemo i record della selezione corrente
    #virtual_columns = '$note_ag,$bank_dt'
    #css_requires='grid'
    #pdf_service = "wk"

    def main(self):
      self.schedaCliente()

    def schedaCliente(self):
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=5,left=4,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='grey')

        layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))
        layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))
        layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))

        dati_cliente = layout.row(height=30, lbl_height=4, lbl_class='smallCaption')
        self.datiCliente(dati_cliente)
        for r in range (5):
            layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))
        #qui verifichiamo quanti <br ci sono nel record body al fine di impostare l'altezza della cella contenente il body
        dati_cert2 = layout.row(height=190,lbl_height=2, lbl_class='smallCaption')
        self.datiBody3(dati_cert2)
        self.paperpage = self.getNewPage()
        layout = self.paperpage.layout(
                            um='mm',top=5,left=4,right=4, bottom=3,
                            border_width=0,
                            font_family='Helvetica',
                            font_size='9pt',
                            lbl_height=4,lbl_class='caption',
                            border_color='grey')
        dati_cert = layout.row(height=190,lbl_height=2, lbl_class='smallCaption')

        self.datiBody2(dati_cert)


        body = self.record['body']
        sub_string = "<br"
        count_er=0
        start_index=0
        for i in range(len(body)):
            j = body.find(sub_string,start_index)
            if(j!=-1):
                start_index = j+1
                count_er+=1
        h_body=(count_er*20)

        quotazione_body = layout.row(height=h_body, lbl_height=4, lbl_class='smallCaption')


    def datiCliente(self, row):
        dati_layout = row.cell().layout(name='datiQuotazione', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')

        dati_layout.row().cell(self.field('data'), lbl="Date")
        dati_layout.row().cell(self.field('quot_n'), lbl="Quotation no.")
        cliente_layout = row.cell().layout(name='datiCliente', um='mm', border_color='white', lbl_class='smallCaption',
                                    lbl_height=3, style='line-height:5mm;text-indent:2mm;')
        customer = "<div style='font-size:10pt;padding:1px'><strong>{rag_soc}<br>&nbsp;&nbsp;{indirizzo}<br>&nbsp;&nbsp;{cap}&nbsp;&nbsp;{city}</strong></div>::HTML".format(rag_soc=self.field('@cliente_id.rag_sociale'),indirizzo=self.field('@cliente_id.address'),cap=self.field('@cliente_id.cap'),city=self.field('@cliente_id.city'))

        cliente_layout.row().cell(customer, lbl="Customer")

    def datiBody2(self,row):
        #for r in range (5):
        #    layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))

        col1 = row.cell(width=50).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=50,content_class='cellheader_p2')
        col2 = row.cell(width=35).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col3 = row.cell(width=16).layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col4 = row.cell(width=16).layout(name='col4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col5 = row.cell(width=35).layout(name='col5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col6 = row.cell(width=15).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=15,content_class='cellheader_p2')
        col7 = row.cell(width=25).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=25,content_class='cellheader_p2')

        col1.row(height=13).cell('Tipo di certificato<br>Type of Certificate::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col2.row(height=13).cell('Rilasciato a<br>Issued at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col3.row(height=13).cell('il<br>on::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col4.row(height=13).cell('Valido fino<br>Valid until::HTML', lbl="",font_weight='bold', style='line-height:3mm;',content_class='cellheader_pt')
        col5.row(height=13).cell('Visita annuale a<br>annual survey at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col6.row(height=13).cell('Data visita annuale annual surv. date', lbl="",font_weight='bold')
        col7.row(height=13).cell('Note<br>Notes::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')

    def datiBody3(self,row):
        #for r in range (5):
        #    layout.row(height=10).cell("<div style='font-size:10pt;padding:5px'><strong>Subject: {subject}</strong></div>::HTML".format(subject=self.field('oggetto')))

        col1 = row.cell(width=50).layout(name='col1', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=50,content_class='cellheader_p2')
        col2 = row.cell(width=35).layout(name='col2', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col3 = row.cell(width=16).layout(name='col3', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col4 = row.cell(width=16).layout(name='col4', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=16,content_class='cellheader_p2')
        col5 = row.cell(width=35).layout(name='col5', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=35,content_class='cellheader_p2')
        col6 = row.cell(width=15).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=15,content_class='cellheader_p2')
        col7 = row.cell(width=25).layout(name='col6', um='mm', border_color='black', lbl_class='smallCaption',hasBorderTop=True,hasBorderLeft=True,
                                    vertical_align= 'middle',lbl_height=3, style='line-height:3mm;font-size:8pt;',width=25,content_class='cellheader_p2')

        col1.row(height=13).cell('Tipo di certificato<br>Type of Certificate::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col2.row(height=13).cell('Rilasciato a<br>Issued at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col3.row(height=13).cell('il<br>on::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col4.row(height=13).cell('Valido fino<br>Valid until::HTML', lbl="",font_weight='bold', style='line-height:3mm;',content_class='cellheader_pt')
        col5.row(height=13).cell('Visita annuale a<br>annual survey at::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
        col6.row(height=13).cell('Data visita annuale annual surv. date', lbl="",font_weight='bold')
        col7.row(height=13).cell('Note<br>Notes::HTML', lbl="",font_weight='bold',content_class='cellheader_sp')
