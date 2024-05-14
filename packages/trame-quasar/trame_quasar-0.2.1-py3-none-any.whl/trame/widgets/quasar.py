from trame_quasar.widgets.quasar import *

def initialize(server):
    from trame_quasar.module import quasar

    server.enable_module(quasar)
