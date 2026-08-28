# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        user=self.db.currentEnv.get('user')
        #if user != 'admin':
        taguser = self.db.currentEnv.get('userTags')
        tag_user=taguser.split(',')

        if 'admin' in tag_user or 'superadmin' in tag_user or '_DEV_' in tag_user:
            quotation = root.branch(u"quotation")
            quotation.packageBranch('Amministrazione sistema',pkg='adm')
            quotation.packageBranch('System',pkg='sys')
            quotation.packageBranch('Email',pkg='email')
            quotation.thpage(u"!!Cliente", table="quotazioni.cliente")
            quotation.thpage(u"!!Quotazione", table="quotazioni.quotazione")
            quotation.thpage(u"!!Quotazione versione", table="quotazioni.quotazione_versione")
            quotation.thpage(u"!!Description", table="quotazioni.description")
            quotation.thpage(u"!!Details", table="quotazioni.extracost")
            quotation.thpage(u"!!Services included", table="quotazioni.services_incl")
            quotation.thpage(u"!!Surcharges", table="quotazioni.surcharges")
            quotation.thpage(u"!!Specific conditions", table="quotazioni.specific_cond")
            quotation.thpage(u"!!Services excluded", table="quotazioni.services_excl")
            quotation.thpage(u"!!Working times ", table="quotazioni.times_work")
            quotation.thpage(u"!!Note", table="quotazioni.note")
            quotation.thpage(u"!!Payment conditions", table="quotazioni.paymentcond")
            quotation.thpage(u"!!Corrispondenza", table="quotazioni.corrispondenza")
            quotation.lookups(u"Lookup tables", lookup_manager="quotazioni")
        else:
            root.thpage(u"!![en]Messages", table="email.message", tags="")
            quotation = root.branch(u"Quotation")
            quotation.thpage(u"!!Cliente", table="quotazioni.cliente")
            quotation.thpage(u"!!Quotazione", table="quotazioni.quotazione")
            quotation.lookups(u"Lookup tables", lookup_manager="quotazioni")
            unlocode = root.branch(u"Unlocode", tags="")
            unlocode.thpage(u"Località", table="unlocode.place", tags="")
            unlocode.thpage(u"Nazione", table="unlocode.nazione", tags="")
            agz = root.branch(u"Agencies", tags="")
            agz.thpage(u"Agencies", table="agz.agency", tags="")
            agz.thpage(u"Staff", table="agz.staff", tags="")
