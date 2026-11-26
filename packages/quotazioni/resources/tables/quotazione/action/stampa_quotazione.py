from __future__ import print_function
from gnr.web.batch.btcaction import BaseResourceAction
from datetime import datetime
from gnr.web.batch.btcprint import BaseResourcePrint

tags = 'system'
caption = 'Stampa Quotazioni PDF'
tags = 'admin,user'
description = 'Genera il PDF delle quotazioni selezionate'

class Main(BaseResourceAction):
    batch_prefix = 'print_quot'
    batch_title = 'Stampa Quotazioni'
    batch_steps = 'main'

    def step_main(self):
        pkeys = self.get_selection_pkeys()
        if not pkeys:
            return

        html_pages = []

        for quot_id in self.btc.thermo_wrapper(pkeys, message="Preparazione stampa..."):
            data = self.getQuotazioneData(str(quot_id))
            html_content = self.buildQuotazioneHtml(data)
            html_pages.append(html_content)

        # Unisci le pagine con interruzione di pagina CSS
        full_html = '<div style="page-break-after: always;"></div>'.join(html_pages)
        self.html_res = full_html

    def result_handler(self):
        html_content = getattr(self, 'html_res', None)
        if not html_content:
            return "Nessun dato da stampare", dict()

        # Passare html_res nell'action 'clientprint' forza il browser ad aprire il dialogo di stampa
        return "Stampa in corso", dict(html_res=html_content, action='clientprint')

    def messaggio_termometro(self, record, curr, tot, **kwargs):
        quot_n = record.get('quot_n') or 'N.D.'
        return f"Generazione PDF Quotazione {quot_n} ({curr}/{tot})"

    def getQuotazioneData(self, record_id):
        tbl_quot = self.db.table('quotazioni.quotazione')
        quot_record = tbl_quot.record(record_id).output('record')
        quot_dict = tbl_quot.record(record_id).output('dict')

        return {
            'record': quot_record,
            'quotazione': quot_dict,
            'first_description': self.db.table('quotazioni.description').query(
                columns='$description,$um,$amount',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'extracost': self.db.table('quotazioni.extracost').query(
                columns='$extra_description as description,$extra_um as um,$extra_amount as amount',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'serv_incl': self.db.table('quotazioni.services_incl').query(
                columns='@servicesincl_id.description as description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'surcharges': self.db.table('quotazioni.surcharges').query(
                columns='@surcharges_id.description as description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'serv_excl': self.db.table('quotazioni.services_excl').query(
                columns='@servicesexcl_id.description as description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'specific_cond': self.db.table('quotazioni.specific_cond').query(
                columns='$description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'working_times': self.db.table('quotazioni.times_work').query(
                columns='@worktimes_id.description as description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'note': self.db.table('quotazioni.note').query(
                columns='$description,$um,$amount',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch(),
            'payment_cond': self.db.table('quotazioni.paymentcond').query(
                columns='@paymentcond_id.description as description',
                where='$quotazione_id=:p_id', p_id=record_id
            ).fetch()
        }

    def getOutputDocName(self, quotazione):
        quot_n = quotazione.get('quot_n')
        if quot_n:
            return f"Quotation_{quot_n.replace('/', '_')}.pdf"
        return "Quotation.pdf"

    def buildQuotazioneHtml(self, data):
        css = self.getCssStyles()
        body = self.getBodyHtml(data)
        return f"""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <style>{css}</style>
                </head>
                <body>
                    {body}
                </body>
                </html>"""

    def getCssStyles(self):
        return """
            @page {
                size: A4;
                margin: 15mm;
            }
            body {
                font-family: Helvetica, Arial, sans-serif;
                font-size: 10pt;
                line-height: 1.4;
                color: #222;
                margin: 0;
                padding: 0;
            }
        """

    def getBodyHtml(self, data):
        rec = data['record']
        html = []

        # 1. TESTATA
        cliente_rag = rec.get('@cliente_id.rag_sociale') or ''
        cliente_add = rec.get('@cliente_id.address') or ''
        cliente_cap = rec.get('@cliente_id.cap') or ''
        cliente_city = rec.get('@cliente_id.city') or ''

        html.append(f"""
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
            <tr>
                <td style="vertical-align: top; width: 50%;">
                    <span style="font-size: 8pt; color: #666; text-transform: uppercase; font-weight: bold;">Date</span><br>
                    <strong>{rec.get('data') or ''}</strong><br><br>
                    <span style="font-size: 8pt; color: #666; text-transform: uppercase; font-weight: bold;">Quotation no.</span><br>
                    <strong>{rec.get('quot_n') or ''}</strong>
                </td>
                <td style="vertical-align: top; width: 50%;">
                    <span style="font-size: 8pt; color: #666; text-transform: uppercase; font-weight: bold;">Customer</span><br>
                    <strong>{cliente_rag}</strong><br>
                    {cliente_add}<br>
                    {cliente_cap} {cliente_city}
                </td>
            </tr>
        </table>
        """)

        # 2. OGGETTO
        if rec.get('oggetto'):
            html.append(f'<div style="font-size: 11pt; font-weight: bold; margin: 15px 0 10px 0; padding-bottom: 5px; border-bottom: 1px solid #ccc;">Oggetto: {rec["oggetto"]}</div>')

        # 3. TESTO INTRODUTTIVO
        if rec.get('body_in'):
            html.append(f'<div style="font-size: 10pt; margin-bottom: 15px; white-space: pre-wrap; word-wrap: break-word;">{rec["body_in"]}</div>')

        # 4. TABELLA PREZZI PRINCIPALI
        if data['first_description']:
            html.append("""
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; table-layout: fixed;">
                <thead>
                    <tr style="border-bottom: 2px solid #ccc;">
                        <th style="width: 65%; text-align: left; font-size: 8pt; color: #666; padding: 6px 4px;">Descrizione</th>
                        <th style="width: 15%; text-align: center; font-size: 8pt; color: #666; padding: 6px 4px;">U.M.</th>
                        <th style="width: 20%; text-align: right; font-size: 8pt; color: #666; padding: 6px 4px;">Importo</th>
                    </tr>
                </thead>
                <tbody>
            """)
            for item in data['first_description']:
                val = item.get('amount')
                amt_str = f"€ {val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if val is not None else ''
                html.append(f"""
                <tr style="border-bottom: 1px solid #eee; page-break-inside: avoid;">
                    <td style="padding: 6px 4px; vertical-align: top; text-align: left; word-wrap: break-word; white-space: normal;">
                        <strong>{item.get('description', '')}</strong>
                    </td>
                    <td style="padding: 6px 4px; vertical-align: top; text-align: center;">{item.get('um') or ''}</td>
                    <td style="padding: 6px 4px; vertical-align: top; text-align: right;"><strong>{amt_str}</strong></td>
                </tr>
                """)
            html.append('</tbody></table>')

        # 5. EXTRACOST (Sistemata la chiusura </tbody> che mancava nel tuo codice)
        if data['extracost']:
            html.append('<table style="width: 100%; border-collapse: collapse; margin-bottom: 15px; table-layout: fixed;"><tbody>')
            for item in data['extracost']:
                val_ex = item.get('amount')
                amt_ex_str = f"€ {val_ex:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if val_ex is not None else ''
                html.append(f"""
                <tr style="border-bottom: 1px solid #eee; page-break-inside: avoid;">
                    <td style="width: 65%; padding: 6px 4px; vertical-align: top; text-align: left; word-wrap: break-word; white-space: normal;">{item.get('description', '')}</td>
                    <td style="width: 15%; padding: 6px 4px; vertical-align: top; text-align: center;">{item.get('um') or ''}</td>
                    <td style="width: 20%; padding: 6px 4px; vertical-align: top; text-align: right;"><strong>{amt_ex_str}</strong></td>
                </tr>
                """)
            html.append('</tbody></table>')

        # 6. SEZIONI CONDIZIONI E SERVIZI
        def render_sezione(titolo, lista_voci):
            if not lista_voci:
                return ''
            out = f'<div style="margin-top: 12px; page-break-inside: avoid;"><div style="font-weight: bold; font-size: 10pt; color: #333; margin-bottom: 4px;">{titolo}</div>'
            for voce in lista_voci:
                desc = voce.get('description', '')
                if desc:
                    out += f'<div style="font-size: 9.5pt; padding-left: 10px; margin-bottom: 2px; word-wrap: break-word;">• {desc}</div>'
            out += '</div>'
            return out

        html.append(render_sezione('La tariffa sopra esposta si intende comprensiva di:', data['serv_incl']))
        html.append(render_sezione('Condizioni specifiche:', data['specific_cond']))
        html.append(render_sezione('Servizi esclusi:', data['serv_excl']))
        html.append(render_sezione('Eventuali maggiorazioni:', data['surcharges']))

        if data['working_times']:
            html.append('<div style="margin-top: 12px; page-break-inside: avoid;">')
            for voce in data['working_times']:
                desc = voce.get('description', '')
                if desc:
                    html.append(f'<div style="font-size: 9.5pt; padding-left: 10px; margin-bottom: 2px;">• {desc}</div>')
            html.append('</div>')

        # 7. NOTE CON IMPORTO
        if data['note']:
            html.append('<table style="width: 100%; border-collapse: collapse; margin-top: 12px; margin-bottom: 15px; table-layout: fixed;"><tbody>')
            for item in data['note']:
                val_note = item.get('amount')
                amt_note = f"€ {val_note:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') if val_note is not None else ''
                html.append(f"""
                <tr style="border-bottom: 1px solid #eee; page-break-inside: avoid;">
                    <td style="width: 65%; padding: 6px 4px; vertical-align: top; text-align: left; word-wrap: break-word;">{item.get('description', '')}</td>
                    <td style="width: 15%; padding: 6px 4px; vertical-align: top; text-align: center;">{item.get('um') or ''}</td>
                    <td style="width: 20%; padding: 6px 4px; vertical-align: top; text-align: right;">{amt_note}</td>
                </tr>
                """)
            html.append('</tbody></table>')

        html.append(render_sezione('Condizioni di pagamento:', data['payment_cond']))

        # 8. FIRMA E TIMBRO
        agency_name = rec.get('@agency_id.agency_name') or ''
        agency_stamp = rec.get('@agency_id.agency_stamp') or ''
        stamp_img = f'<img src="{agency_stamp}" style="max-width: 140px; max-height: 140px; margin-top: 5px;">' if agency_stamp else ''

        html.append(f"""
        <div style="margin-top: 30px; width: 100%; page-break-inside: avoid;">
            <div style="float: right; width: 220px; text-align: center;">
                <div><strong>{agency_name}</strong></div>
                <div>{stamp_img}</div>
            </div>
            <div style="clear: both;"></div>
        </div>
        """)

        return "".join(html)
