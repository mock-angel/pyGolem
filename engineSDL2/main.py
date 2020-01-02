# main.py v1.2
# This script starts the Update, Graphics and Event engine which again have the
# same script for every application

# The constant module's import imports data as main_app used by engine to run the game.

# Please Note: All apps subject to be run by Engine wll have the same
# EngineGraphics, UpdateEngine, PycCleanup and main with no variation.
# All apps subject to be run by Engine will be subject to widgets usage
# All apps subject to widgets may or may not be subject to be run by Engine.

import sys
sys.path.insert(0, '../engineSDL2')
import PycCleanup
import Golem
import config

if __name__ == "__main__":
    app = Golem.Application()
    window = app.createNewWindow("PyGolem", window = config.main_app)\
                  .setBackgroundColor(250,100,100,100)
    app.start()
    PycCleanup.clean()
