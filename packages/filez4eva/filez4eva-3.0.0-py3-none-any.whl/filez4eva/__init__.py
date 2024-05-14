from wizlib.app import WizApp

from filez4eva.command import Filez4EvaCommand


class Filez4EvaApp(WizApp):

    base_command = Filez4EvaCommand
    name = 'filez4eva'
