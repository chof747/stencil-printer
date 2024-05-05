#!/
import os
import getopt
import sys
import subprocess
import ezdxf
from typing import List, Tuple
from dotenv import load_dotenv

load_dotenv()

APP = os.environ.get("OPENSCAD_APP")
scad_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "openscad")

def read_parameters(argv):
    """
    Reads command line arguments and returns them as a dictionary.
    """
    params = {
        "board_thickness": 1.6,
        "stencil_height": 0.3,
        "tolerance": 0.1,
        "front_paste": None,
        "board_outline": None,
        "output_filepath": None,
    }

    short_options = "hf:b:o:"
    long_options = ["help", "frontpaste=", "boardoutline=", "output=", "board_thickness=", "stencil_height=", "tolerance="]

    try:
        opts, args = getopt.getopt(argv, short_options, long_options)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_usage()
            sys.exit()
        elif opt in ("-f", "--frontpaste"):
            params["front_paste"] = arg
        elif opt in ("-b", "--boardoutline"):
            params["board_outline"] = arg
        elif opt in ("-o", "--output"):
            params["output_filepath"] = arg
        elif opt == "--board_thickness":
            params["board_thickness"] = float(arg)
        elif opt == "--stencil_height":
            params["stencil_height"] = float(arg)
        elif opt == "--tolerance":
            params["tolerance"] = float(arg)

    return params

def validate_parameters(params):
    """
    Validates mandatory parameters and the existence of the output directory.
    """
    if not params["front_paste"] or not params["output_filepath"]:
        print("Error: Both the frontpaste and the output filepath are required.")
        print_usage()
        sys.exit(2)
    
    if not os.path.isdir(os.path.dirname(params["output_filepath"])):
        print("Error: The directory for the output filepath does not exist.")
        sys.exit(2)

def print_usage():
    print("Usage: script.py -f <frontpaste>  -b <boardoutline -o <output> [--board_thickness=] [--stencil_height=] [--tolerance=]")
    print("  -f, --frontpaste       Input filepath")
    print("  -b, --boardoutline       Input filepath")
    print("  -o, --output           Output filepath (directory must exist)")
    print("      --board_thickness  Board thickness (default 1.6)")
    print("      --stencil_height   Stencil height (default 0.3)")
    print("      --tolerance        Tolerance (default 0.1)")


def get_max_dimensions(dxf_file):
    doc = ezdxf.readfile(dxf_file)
    msp = doc.modelspace()

    max_x = max(entity.dxf.end[0] for entity in msp if entity.dxftype() == 'LINE')
    max_y = max(entity.dxf.end[1] for entity in msp if entity.dxftype() == 'LINE')

    return max_x, max_y

def runOpenScad(arguments: List[str]) -> Tuple[bool,str,str]:
    """ Combine the application path and parameters into a single command """

    command = [APP] + arguments

    # Run the command
    try:
        # For Python 3.5 and newer, use run() for simplicity
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Access the output and error
        return (True, 
                result.stdout.decode('utf8') if result.stdout else '',
                result.stderr.decode('utf8') if result.stderr else '')
        
    except subprocess.CalledProcessError as e:
        print(f"Error running the command: {e}")
        print(f"Error: {e.stderr}")
        return (True, 
                e.stdout.decode('utf8') if e.stdout else '',
                e.stderr.decode('utf8') if e.stderr else '')

    return True

def main(argv):
    params = read_parameters(argv)
    validate_parameters(params)

    standard_args = [
      "--quiet", "--export-format", "binstl"
    ]

    geometry_args = [
        f"-D stencil_height={params['stencil_height']}",
        f"-D board_thickness={params['board_thickness']}",
        f"-D tolerance={params['tolerance']}"           
    ]

    bl = chr(92)

    stencil_args = [
        f'''-D front_paste="{params['front_paste']}"''',
        os.path.join(scad_path, "stencil.scad"),
        '-o',
        f'''{os.path.join(params['output_filepath'],'stencil.stl')}'''

    ]

    frame_args = [
        f'''-D board_outline="{params['board_outline']}"''',
        os.path.join(scad_path, "frame.scad"),
        '-o',
        f'''{os.path.join(params['output_filepath'],'frame.stl')}'''
    ]

    x,y = get_max_dimensions(params['board_outline'])
    print(f"max_x = {x}, max_y = {y}")

    board_outline_args = [
        f"-D board_x={x}",
        f"-D board_y={y}"
    ]

    #stencil run    
    print("creating stencil ...", end=None)
    runOpenScad(standard_args + geometry_args + stencil_args)
    print(" done")
    #frame run
    print("creating frame ...", end=None)
    runOpenScad(standard_args + geometry_args + frame_args + board_outline_args)
    print(" done")
        

if __name__ == "__main__":
    main(sys.argv[1:])



