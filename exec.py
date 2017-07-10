import argparse



'''
TODO debug commands
'''
parser = argparse.ArgumentParser(description='Visualizes Turing Machines')
parser.add_argument('--turing_program', help='the path to the turing program')
parser.add_argument('--tape', help='the path to the tape to run')
parser.add_argument('--out_dir', help='the path to the tape to run')

parser.add_argument('--interactive', help='the path to the turing program')
parser.add_argument('--template', help='the path to the turing program')
parser.add_argument('--tape_item_limit', help='the path to the turing program')
parser.add_argument('--verbose', help='the path to the turing program')

file_to_tm = '/home/martin_jutzi/Temp/divisiontest7.txt'
tm_executor = ExecuteTM._parse_file(file_to_tm)

template_path = '/home/martin_jutzi/PycharmProjects/TikzTuringSimulator/templates/latex'
tape_item_limit = 12
viewer = ''

visual_executor = VisualizeTM.create(template_path)
visual_executor.set_tape_item_limit(tape_item_limit)
# visual_executor.set_viewer(viewer)

tm_executor.add_observer(PrintTM())
tm_executor.add_observer(visual_executor)

# 0', '0', '1', '1', '1
tape_str = '00111'
tm_executor.execute_TM(tape_str)

output_dir = '/home/martin_jutzi/Temp'
visual_executor.write_file(output_dir)
