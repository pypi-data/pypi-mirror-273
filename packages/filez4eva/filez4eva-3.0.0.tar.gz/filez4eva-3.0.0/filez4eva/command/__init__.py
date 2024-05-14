from wizlib.command import WizCommand
from wizlib.stream_handler import StreamHandler
from wizlib.config_handler import ConfigHandler
from wizlib.ui_handler import UIHandler


class Filez4EvaCommand(WizCommand):

    default = 'scan'
    handlers = [StreamHandler, ConfigHandler, UIHandler]
