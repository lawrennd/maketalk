#!/usr/bin/env python3

import os
import argparse

import lynguine.util.talk as nt
import lynguine.util.yaml as ny

import lamd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        type=str,
                        help="The filename where dependencies are being searched")

    args = parser.parse_args()

    basename = os.path.basename(args.filename)
    base = os.path.splitext(basename)[0]
    
    dirname = os.path.dirname(lamd.__file__)
    make_dir = os.path.join(dirname, "makefiles")
    includes_dir = os.path.join(dirname, "includes")
    script_dir = os.path.join(dirname, "scripts")


    os.system('git pull')
    os.system('make all')
    
    f = open('makefile', 'w+')
    f.write(f"BASE={base}\n")
    f.write(f"MAKEFILESDIR={make_dir}\n")
    f.write(f"INCLUDESDIR={includes_dir}\n")
    f.write(f"SCRIPTDIR={script_dir}\n")
    
    f.write(f"include $(MAKEFILESDIR)/make-cv-flags.mk\n")
    f.write(f"include $(MAKEFILESDIR)/make-cv.mk\n")
    f.close()
    for field in ["snippetsdir", "bibdir"]:
        try:
            answer = nt.talk_field(field, f"{base}.md", user_file=["_lamd.yml", "_config.yml"])
        except ny.FileFormatError:
            iface = lamd.config.interface.Interface.from_file(user_file=["_lamd.yml", "_config.yml"], directory=".")
            if field in iface:
                answer = iface[field]
            else:
                answer = ''
    
        # Hacky way to make sure snippets are pulled down
        os.system(f"CURDIR=`pwd`;cd {answer}; git pull; cd $CURDIR")

    os.system('git pull')
    os.system(f"make all")

if __name__ == "__main__":
    sys.exit(main())
