import argparse
import os
import sys

from controler.execute_turing_machine import ExecuteTM
from controler.visualize_turing_machine import VisualizeTM, PrintTM, is_template

tm_executor, visual_executor, args = None, None, None


def run_tape(tape):
    tm_executor.execute_TM(tape)

    out_dir = args.out if args.out else './target'
    result = visual_executor.write_file(out_dir)

    print('Written result to ', result)

    if not args.silent:
        visual_executor.visualize()


def start_interactive_mode():
    def read_input():
        return input("Enter the tape characters (or 'quit()' to exit): ")

    print("Usage:")
    print("Type the characters of each tape. Missing tapes are assumed to be empty. You may either type 'tape1 tape2' "
          "for single character tapes or use the multi character input formats 't,a,p,e,1;t,a,p,e,2' or "
          "'tape:{'i','i'}: tape:{'i','i'}'")

    tape = read_input()
    while tape != 'quit()':
        run_tape(tape)
        tape = read_input()


def run():
    global tm_executor
    global visual_executor

    tm_executor = ExecuteTM.parse_file(args.program)
    visual_executor = VisualizeTM.create(args.template)

    tm_executor.add_observer(visual_executor)

    if args.verbose:
        tm_executor.add_observer(PrintTM())

    if args.viewer:
        visual_executor.set_viewer(args.viewer)

    if args.tape:
        run_tape(args.tape)
    else:
        start_interactive_mode()


def validate_arguments():
    if not os.path.isfile(args.program):
        sys.stderr.write('Program \'{}\' does not exist.'.format(args.program))
        return False

    if not is_template(args.template):
        sys.stderr.write('Cannot find template \'{}\'.'.format(args.template))
        return False

    return True


def get_args():
    global args

    arg_parser = argparse.ArgumentParser(description='Visualizes Turing Machines')
    arg_parser.add_argument('program', help='The path to the turing program')
    arg_parser.add_argument('--tape', help='Path to the tape file. If empty the program starts in interacitve mode')
    arg_parser.add_argument('--out', default='./target', help='The path to the output directory')

    arg_parser.add_argument('--template', default='latex', help='The name or path of the document template.')

    arg_parser.add_argument('--verbose', action='store_true',
                            help='Prints the iterations of the turing machine if active.')
    arg_parser.add_argument('--viewer', help='Opens the output with the given viewer name')
    arg_parser.add_argument('-s', '--silent', action='store_true', help='Does not open the generated file if set.')

    args = arg_parser.parse_args()
    return validate_arguments()


def main():
    try:
        if get_args():
            run()
            return 0
        else:
            return 1

    except Exception as err:
        sys.stderr.write('ERROR: {}'.format(err))
        return 1


if __name__ == '__main__':
    sys.exit(main())
