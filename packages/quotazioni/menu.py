# encoding: utf-8
class Menu(object):
    def config(self,root,**kwargs):
        root.thpage(u"!![en]Quotations", table="quotazioni.quotazione", multipage="True", tags="")
        root.thpage(u"!![en]Customer", table="quotazioni.cliente", multipage="True", tags="")
