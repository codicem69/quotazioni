# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        user=self.db.currentEnv.get('user')
        #if user != 'admin':
        taguser = self.db.currentEnv.get('userTags')
        tag_user=taguser.split(',')

        if 'admin' in tag_user or 'superadmin' in tag_user or '_DEV_' in tag_user:
            auto = root.branch(u"auto")
            auto.thpage(u"!!Cliente", table="quotazioni.cliente")
            auto.thpage(u"!!Quotazione", table="quotazioni.quotazione")
            auto.thpage(u"!!Description", table="quotazioni.description")
            auto.thpage(u"!!Details", table="quotazioni.extracost")
            auto.thpage(u"!!Services included", table="quotazioni.services_incl")
            auto.thpage(u"!!Surcharges", table="quotazioni.surcharges")
            auto.thpage(u"!!Specific conditions", table="quotazioni.specific_cond")
            auto.thpage(u"!!Services excluded", table="quotazioni.services_excl")
            auto.thpage(u"!!Working times ", table="quotazioni.times_work")
            auto.thpage(u"!!Note", table="quotazioni.note")
            auto.thpage(u"!!Payment conditions", table="quotazioni.paymentcond")
            auto.thpage(u"!!Quotation received", table="quotazioni.quotazione_ricevuta")
            auto.lookups(u"Lookup tables", lookup_manager="quotazioni")
        else:

            auto = root.branch(u"auto")
            auto.thpage(u"!!Cliente", table="quotazioni.cliente")
            auto.thpage(u"!!Quotazione", table="quotazioni.quotazione")
            auto.lookups(u"Lookup tables", lookup_manager="quotazioni")
