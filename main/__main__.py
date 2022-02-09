from cpaste_editor import run
from cpaste_editor.themes import _on_package_delete as themes_unload
import argparse
from os import system


parser = argparse.ArgumentParser(description="Run cpaste game engine, or do some actions with it")
parser.add_argument("-d", "--delete", action="store_true", help="Delete cpaste engine modules", default=None)
args = parser.parse_args()

if args.delete:
    print("unloading cpaste-api")
    pass
    print("unloading cpaste-core")
    pass
    print("unloading cpoaste-editor")
    themes_unload()
    print("unloading cpaste")
    pass
    print("deleting cpaste-api")
    system("pip uninstall -y cpaste-api")
    print("deleting cpaste-core")
    system("pip uninstall -y cpaste-core")
    print("deleting cpaste-editor")
    system("pip uninstall -y cpaste-editor")
    print("deleting cpaste")
    system("pip uninstall -y cpaste")
else:
    run()
