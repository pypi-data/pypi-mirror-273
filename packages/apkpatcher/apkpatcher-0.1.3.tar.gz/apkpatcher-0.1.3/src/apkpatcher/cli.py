
import argparse
import logging
from apkpatcher import *

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--apk', help='Specify the apk you want to patch')
    parser.add_argument('-g', '--gadget', help='Specify the frida-gadget file \
                        file.so or file with no architecture specified will be \
                        autocomplete with file_<arch>.so')
    parser.add_argument('-s', '--sdktools', help='Path of the sdktools')
    parser.add_argument('-b', '--version_buildtools', help='version for buildtools')
    parser.add_argument('-r', '--arch', choices=[Patcher.ARCH_ARM, Patcher.ARCH_ARM64,
                                                 Patcher.ARCH_X86, Patcher.ARCH_X64],
                                                 help='architecture targeted')
    parser.add_argument('-v', '--verbosity', help='Verbosity level (0 to 3). Default is 3')

    parser.add_argument('-e', '--enable-user-certificates', help='Add some configs in apk to accept user certificates',
                        action='store_true')
    parser.add_argument('-c', '--custom-certificate', help='Install a custom network certificate inside the apk')

    parser.add_argument('-o', '--output-file', help='Specify the output file (patched)')

    parser.add_argument('-p', '--pause', help='pause before repackage the apk',
            action="store_true")
    parser.add_argument('--plugin', help='execute load plugin (a python file with as argument the folder before the packaging)')
    parser.add_argument('-V', '--version', help='version of apkpatcher', action='store_true')

    args = parser.parse_args()

    if args.version:
        print(f"version {conf.VERSION}")
        return 0

    if len(sys.argv) == 1 or not (args.apk and \
                                  args.sdktools and \
                                  args.version_buildtools):
        print("apkpatcher -a <apk> -s <sdktools> -b <version> [options]")
        parser.print_help()
        return 1

    if args.verbosity:
        if args.verbosity == 3:
            logging.basicConfig(level=logging.DEBUG)
        if args.verbosity == 2:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.INFO)

    patcher = Patcher(args.apk, args.sdktools, args.version_buildtools)
    if args.custom_certificate:
        patcher.add_network_certificate(args.custom_certificate)
    if args.arch:
        patcher.set_arch(args.arch)
    patcher.pause(args.pause)
    if args.plugin:
        patcher.set_plugin(args.plugin)
    if args.output_file:
        patcher.patching(args.gadget,
                output_file=args.output_file,
                user_certificate=args.enable_user_certificates)
    else:
        patcher.patching(args.gadget,
                user_certificate=args.enable_user_certificates)

