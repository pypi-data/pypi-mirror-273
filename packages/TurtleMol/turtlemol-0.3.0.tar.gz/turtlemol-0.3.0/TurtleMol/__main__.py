'''Module contains the main loop'''

import sys
import argparse
from drawMol import drawMolBox, drawMolSphere, drawMolMesh
from readWriteFiles import writeOutput, getInput, readStrucFile
from defaultParams import defaultParams

def parseCommandLine(dparams):
    '''Parses command line for parameters'''
    parser = argparse.ArgumentParser(description='Tile Fill')

    # Command line arguemnnts
    parser.add_argument('-i', '--inputFile', type=str, help="Path to input file")
    parser.add_argument('-struc', '--structureFile', type=str,
                        help='Path to structure file')
    parser.add_argument('-baseStruc', '--baseStrucFile', type=str,
                        help='Path to base structure file', default=dparams['baseStrucFile'])
    parser.add_argument('-s', '--shape', type=str,
                        help="Shape (Box or Cube)", default=dparams['shape'])
    parser.add_argument('-sl', '--sideLength', type=float,
                        help="Dimensions of a cube in Angstroms", default=dparams['sideLength'])
    parser.add_argument('-xl', '--Xlen', type=float,
                        help="X dimension of a box in Angstroms", default=dparams['Xlen'])
    parser.add_argument('-yl', '--Ylen', type=float,
                        help="Y dimension of a box in Angstroms", default=dparams['Ylen'])
    parser.add_argument('-zl', '--Zlen', type=float,
                        help="Z dimension of a box in Angstroms", default=dparams['Zlen'])
    parser.add_argument('-r', '--radius', type=float,
                        help="Radius of a sphere in Angstroms", default=dparams['radius'])
    parser.add_argument('-rand', '--randomizeOrient', type=bool,
                        help="Randomize the orientation or not", default=dparams['randomizeOrient'])
    parser.add_argument('-randFill', '--randFill', type=bool,
                        help="Randomize place molecules when placing a set number",
                        default=dparams['randFill'])
    parser.add_argument('-center', '--center', nargs='+', type=float,
                        help="X, Y, Z coordinates of the center of a sphere",
                        default=dparams['sphereCenter'])
    parser.add_argument('-baseCenter', '--baseStrucCenter', nargs='+', type=float,
                        help="X, Y, Z coordinates of the center of the base structure",
                        default=dparams['baseStrucCenter'])
    parser.add_argument('-n', '--numMolecules', type=int,
                        help="Number of molecules", default=dparams['numMolecules'])
    parser.add_argument('-t', '--tol', type=float,
                        help="Minimum distance between molecules", default=dparams['tol'])
    parser.add_argument('-rho', '--density', type=float,
                        help="Density in g/mL", default=dparams['density'])
    parser.add_argument('-a', '--maxAttempts', type=int,
                        help="Maximum iterations for finite sized systems",
                        default=dparams['maxAttempts'])
    parser.add_argument('-ar', '--atomRadius', type=str,
                        help="What radius type to be used for atoms",
                        default=dparams['atomRadius'])
    parser.add_argument('-out', '--outputFile', type=str,
                        help="Path for output file if desired")
    parser.add_argument('-mesh', '--mesh', type=str,
                        help="Path for mesh file if desired")
    parser.add_argument('-scale', '--meshScale', type=float,
                        help="Uniform scale of mesh", default=dparams['meshScale'])

    return parser.parse_args()

def main():
    '''The main loop'''
    # Init default params
    dparams = defaultParams()

    # Init arguement parser
    args = parseCommandLine(dparams)

    iparams = {}
    if args.inputFile:
        iparams = getInput(args.inputFile)
    else:
        for argName in vars(args):
            iparams[argName] = getattr(args, argName)

    for name in dparams:
        if name not in iparams:
            iparams[name] = dparams[name]

    if not iparams['structureFile']:
        print('Please provide an initial structure')
        sys.exit()

    print(iparams)

    # Get structure
    struc, unitCell = readStrucFile(iparams['structureFile'])
    print(struc)

    if unitCell:
        iparams['unitCell'] = [unitCell['a'], unitCell['b'], unitCell['c']]

    if iparams['baseStrucFile']:
        baseStruc, baseUnitCell = readStrucFile(iparams['baseStrucFile'])
    else:
        baseStruc = None

    if iparams['shape'].lower() == 'box' or iparams['shape'].lower() == 'cube':
        # Generate the new structure

        if unitCell:
            outStruc, strucType, cellParams = drawMolBox(struc, baseStruc, iparams)
        else:
            outStruc, strucType = drawMolBox(struc, baseStruc, iparams)

    elif iparams['shape'].lower() == 'sphere':
        # Generate the new structure

        if unitCell:
            outStruc, strucType, cellParams = drawMolSphere(struc, baseStruc, iparams)
        else:
            outStruc, strucType = drawMolSphere(struc, baseStruc, iparams)

    elif iparams['shape'].lower() == 'mesh' and iparams['mesh'] is not None:
        # Generate the new structure
        outStruc = []

#        if isinstance(iparams['mesh'], str):
#            iparams['mesh'] = [iparams['mesh']]
#
#        for i in iparams['mesh']:

        if unitCell:
            outStrucTemp, strucType, cellParams = drawMolMesh(struc, baseStruc, iparams)
            outStruc.append(outStrucTemp)
        else:
            outStrucTemp, strucType = drawMolMesh(struc, baseStruc, iparams)
            outStruc.append(outStrucTemp)

        
    if iparams['outputFile']:
        if unitCell:
            writeOutput(outStruc, iparams['outputFile'], strucType, cellParams)
        else:
            writeOutput(outStruc, iparams['outputFile'], strucType)

if __name__ == "__main__":
    main()
