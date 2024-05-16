import os
from tabulate import tabulate
import sys
from pathlib import Path
from wtao import obtain_wtao_path


def fireworks():
    # try:
    from wtao.lxq.fireworks_explosion import open_app as open_fireworks
    cur_path = obtain_wtao_path()
    open_fireworks(ui=os.path.join(cur_path, "resources/fireworks/main.ui"),
                    icon=os.path.join(cur_path, "resources/fireworks/icon.png"),
                    snow=os.path.join(cur_path, "resources/fireworks/snow.gif"),
                    emoji=os.path.join(cur_path, "resources/fireworks/paitou.gif"),
                    fireworks=os.path.join(cur_path, "resources/fireworks/fireworks"))
    # except:
    #     print("package err")


