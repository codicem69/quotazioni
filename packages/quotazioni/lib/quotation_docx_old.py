# quotation_docx.py

from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
from datetime import datetime
import re
import base64
import tempfile
from html import unescape
from docxtpl import RichText

class QuotationDocxBuilder(object):

    def __init__(self, db, site):

        self.db = db
        self.site = site

        self.tbl_quot = self.db.table('quotazioni.quotazione_versione')


    # ---------------------------------------------------------
    # Converte una relazione Genropy in lista per docxtpl
    # ---------------------------------------------------------
    def bag_rows(self, bag, relation, mapping):

        result = []

        rows = bag.getItem(relation)

        if not rows:
            return result


        for node in rows:

            row = node.value

            item = {}


            for key, field in mapping.items():

                if row:
                    item[key] = row.getItem(field) or ''
                else:
                    item[key] = ''


            result.append(item)


        return result

    def html_to_text(self, value):

        if not value:
            return ''
    
        # converte entità html (&agrave; &nbsp; ecc.)
        value = unescape(value)
    
        # elimina tabulazioni inserite dall'editor HTML
        value = value.replace('\t', '')
    
        # div e br diventano ritorni riga
        value = re.sub(
            r'<\s*br\s*/?>',
            '\n',
            value,
            flags=re.I
        )
    
        value = re.sub(
            r'</\s*div\s*>',
            '\n',
            value,
            flags=re.I
        )
    
        value = re.sub(
            r'<\s*div[^>]*>',
            '',
            value,
            flags=re.I
        )
    
        # elimina eventuali altri tag HTML
        value = re.sub(
            r'<[^>]+>',
            '',
            value
        )
    
        # elimina spazi vuoti non normali
        value = value.replace('\xa0', ' ')
    
        # elimina spazi a inizio/fine riga
        value = '\n'.join(
            line.strip()
            for line in value.split('\n')
        )
    
        # elimina righe vuote consecutive
        value = re.sub(
            r'\n\s*\n\s*\n+',
            '\n\n',
            value
        )
    
        return value.strip()
    
    def clean_text(self, value):

        if not value:
            return ''

        value = value.replace('\r\n', '\n')

        # elimina righe vuote consecutive
        value = re.sub(
            r'\n\s*\n\s*\n+',
            '\n\n',
            value
        )

        return value.strip()

    def rows_to_text(self, rows, bullet=False):
        """Converte una lista di righe in un testo con ritorni a capo."""
        if not rows:
            return ''

        result = []
        for row in rows:
            description = row.get('description', '')
            if description:
                if bullet:
                    result.append(f'• {description}')
                else:
                    result.append(description)

        return '\n'.join(result)

    def rows_to_richtext(self, rows, bullet=False):
        rt = RichText()

        if not rows:
            return rt

        first = True
        for row in rows:
            text = row.get('description', '')
            if not text:
                continue

            if not first:
                rt.add('\n')

            if bullet:
                rt.add('• ')

            rt.add(text)
            first = False

        return rt

    # ---------------------------------------------------------
    # Costruzione del context per Word
    # ---------------------------------------------------------
    def build_context(self, rec):

        ctx = {}


        # campi principali

        main_fields = [
            'data',
            'quot_n',
            'oggetto',
            'body_in',
            'note',
            'servincl_int',
            'servexcl_int',
            'spec_cond_int',
            'surcharges_int',
            'workingtimes_int',
            'agent_sign',
            'agent_name'
        ]


        for field in main_fields:

            value = rec.getItem(field) or ''

            if field == 'body_in':
                value = self.html_to_text(value)

            ctx[field] = value


        ctx['agency_logo'] = ''
        ctx['stamp'] = ''

        # -------------------------------------------------
        # Cliente
        # -------------------------------------------------

        ctx['customer_rag_sociale'] = (
            rec.getItem('@cliente_id.rag_sociale') or ''
        )

        ctx['customer_address'] = (
            rec.getItem('@cliente_id.address') or ''
        )

        ctx['customer_cap'] = (
            rec.getItem('@cliente_id.cap') or ''
        )

        ctx['customer_city'] = (
            rec.getItem('@cliente_id.city') or ''
        )



        # -------------------------------------------------
        # Agency
        # -------------------------------------------------

        ctx['agency_name'] = (
            rec.getItem('@agency_id.agency_name') or ''
        )

        ctx['agency_address'] = (
            rec.getItem('@agency_id.address') or ''
        )

        ctx['agency_tel'] = (
            rec.getItem('@agency_id.tel') or ''
        )

        ctx['agency_fax'] = (
            rec.getItem('@agency_id.fax') or ''
        )

        ctx['agency_email'] = (
            rec.getItem('@agency_id.email') or ''
        )

        ctx['agency_web'] = (
            rec.getItem('@agency_id.web') or ''
        )

        ctx['agency_vat'] = (
            rec.getItem('@agency_id.vat') or ''
        )

        ctx['agency_cf'] = (
            rec.getItem('@agency_id.cf') or ''
        )

        ctx['data'] = (
                    rec.getItem('data').strftime("%d/%m/%Y") or ''
                )

        ctx['quot_n'] = (
                    rec.getItem('quot_n') or ''
                )

        # -------------------------------------------------
        # Tabelle
        # -------------------------------------------------
        
        ctx['description_quot'] = self.bag_rows(
            rec,
            '@description_quot',
            {
                'description': 'description',
                'um': 'um',
                'amount': 'amount'
            }
        )
        
        ctx['quotazione_extra'] = self.bag_rows(
            rec,
            '@quotazione_extra',
            {
                'description': 'extra_description',
                'um': 'extra_um',
                'amount': 'extra_amount'
            }
        )
        
        ctx['note_quot'] = self.bag_rows(
            rec,
            '@note_quot',
            {
                'description': 'description',
                'um': 'um',
                'amount': 'amount'
            }
        )
        
        # ---------- Servizi inclusi ----------
        rows = self.bag_rows(
            rec,
            '@servincl_quot',
            {
                'description': '@servicesincl_id.description'
            }
        )
        
        ctx['servincl_text'] = self.rows_to_text(rows, bullet=True)
        
        # ---------- Servizi esclusi ----------
        rows = self.bag_rows(
            rec,
            '@serviexcl_quot',
            {
                'description': '@servicesexcl_id.description'
            }
        )
        
        ctx['serviexcl_text'] = self.rows_to_text(rows, bullet=True)
        
        # ---------- Condizioni specifiche ----------
        rows = self.bag_rows(
            rec,
            '@specific_quot',
            {
                'description': 'description'
            }
        )
        
        ctx['specific_text'] = self.rows_to_text(rows)
        
        # ---------- Maggiorazioni ----------
        rows = self.bag_rows(
            rec,
            '@surcharge_quot',
            {
                'description': '@surcharges_id.description'
            }
        )
        
        ctx['surcharge_text'] = self.rows_to_text(rows, bullet=True)
        
        # ---------- Orari ----------
        rows = self.bag_rows(
            rec,
            '@times_quot',
            {
                'description': '@worktimes_id.description'
            }
        )
        
        ctx['times_text'] = self.rows_to_text(rows, bullet=True)
        
        # ---------- Pagamenti ----------
        rows = self.bag_rows(
            rec,
            '@paym_quot',
            {
                'description': '@paymentcond_id.description'
            }
        )
        
        ctx['paym_text'] = self.rows_to_text(rows, bullet=True)
        
        return ctx

    def base64_image(self, image_data):
    
        if not image_data:
            return None

        if ',' in image_data:
            header, encoded = image_data.split(',', 1)
        else:
            encoded = image_data


        image_bytes = base64.b64decode(encoded)


        tmp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix='.png'
        )

        tmp.write(image_bytes)
        tmp.close()


        return tmp.name

    # ---------------------------------------------------------
    # Generazione documento
    # ---------------------------------------------------------

    def build(self, record_id):

        rec = self.tbl_quot.record(record_id).output('bag')
        
        context = self.build_context(rec)


        template_node = self.site.storageNode(
            'home:stampe_template',
            'quotation_template.docx'
        )

        template_path = template_node.internal_path

        doc = DocxTemplate(template_path)


        # -------------------------------------------------
        # valori iniziali immagini
        # -------------------------------------------------

        context['agency_logo'] = ''
        context['stamp'] = ''
        context['show_signature'] = False


        # -------------------------------------------------
        # LOGO AGENZIA
        # -------------------------------------------------

        logo = rec['@quotazione_id.@agency_id'].getItem(
            'agency_logo'
        )

        logo_file = self.base64_image(
            logo
        )


        if logo_file:

            context['agency_logo'] = InlineImage(
                doc,
                logo_file,
                width=Mm(75)
            )


        # -------------------------------------------------
        # FIRMA / TIMBRO AGENZIA
        # -------------------------------------------------

        firma = rec.getItem(
            'firma'
        )


        if firma:

            context['show_signature'] = True


            stamp = rec['@quotazione_id.@agency_id'].getItem(
                'agency_stamp'
            )


            stamp_file = self.base64_image(
                stamp
            )


            if stamp_file:

                context['stamp'] = InlineImage(
                    doc,
                    stamp_file,
                    width=Mm(30)
            )


        # -------------------------------------------------
        # Render documento
        # -------------------------------------------------
        
        doc.render(context)

        quot_n = rec['@quotazione_id'].getItem(
                    'quot_n'
                ).replace('/', '_')
        vers_n = rec.getItem(
                    'version'
                ).replace('/', '_')
        
        filename = 'quotation_%s_%s.docx' % (quot_n,vers_n)

        #filename = 'quotation_%s_%s.docx' % (quot_n, datetime.now().strftime(
        #            '%Y%m%d_%H%M%S'))

        output = self.site.storageNode(
            'home:stampe_template',
            filename)

        doc.save(output.internal_path)

        return output
