'''
This module is for reading and writing files as needed. 
Since both the input and output files are optional, these functions can be avoided.
The structure file is required however, and currently the only supported format is xyz files.
Data on elements is also imported and searchable. Primary use at this time is for the atomic radius
'''

import os
import pandas as pd
import trimesh

def getInput(filePath):
    '''Reads input file if provided'''
    params = {}
    with open(filePath, encoding = 'utf-8') as f:
        for line in f:
            key, value = line.strip().split('=')
            params[key.strip()] = value.strip()

    return params

def readStrucFile(filePath):
    '''Reads structure file'''
    # Reads XYZ
    if filePath[-3:] == 'xyz':
        return pd.read_csv(filePath, delim_whitespace=True,
                           skiprows=2, names=["Atom", "X", "Y", "Z"]), None
    # Reads PDB
    if filePath[-3:] == 'pdb':
        return readPdb(filePath)

    return f"ERROR: Issue generating file to {filePath}"

def readPdb(filePath):
    '''Reads structure file if a pdb'''
    data = []
    unitCell = None
    symbols = getElementData('AtomicMass')

    with open(filePath, 'r', encoding = 'utf-8') as pdbFile:
        for line in pdbFile:

            if line.startswith('CRYST1'):
                # Extract unit cell parameters from the CRYST1 line
                a = float(line[6:15].strip())
                b = float(line[15:24].strip())
                c = float(line[24:33].strip())
                alpha = float(line[33:40].strip())
                beta = float(line[40:47].strip())
                gamma = float(line[47:54].strip())
                unitCell = {'a': a, 'b': b, 'c': c, 'alpha': alpha, 'beta': beta, 'gamma': gamma}

            elif line.startswith('ATOM') or line.startswith('HETATM'):
                # Parse relevant fields from the PDB format
                atomName = line[12:16].strip()
                element = line[76:78].strip()

                if element not in symbols['Symbol']:
                    element = atomName

                try:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                except ValueError:
                    continue # Skip line if coordinates are invalid
                residueName = line[17:20].strip()
                residueSeq = int(line[22:26].strip())

                data.append([element, x, y, z, residueName, residueSeq])

    df = pd.DataFrame(data, columns=['Atom', 'X', 'Y', 'Z', 'Residue', 'ResidueSeq'])

    return df, unitCell

def readMesh(filePath):
    '''Reads mesh files in format like .obj, .stl, .ply'''
    mesh = trimesh.load(filePath)
    return mesh

def writeOutput(data, filePath, strucType, cellParams=None):
    '''Writes data to output file'''
    try:
        # Writes XYZ
        if filePath[-3:] == 'xyz':
            writeXYZ(data, filePath, strucType)
        # Writes PDB
        elif filePath[-3:] == 'pdb':
            if cellParams != None:
                writePdb(data, filePath, cellParams)
            else:
                writePdb(data, filePath)
    except KeyError:
        print(f"Filetype {filePath[-3:]} not supported\n")

def writePdb(data, filePath, cellParams=None):
    '''Writes a pdb file from results'''
    template = (
        "HETATM{atomNum:5d} {atomType:>2}  {residueName:>3} A{resNum: >4d}"
        "    {x: >8.3f}{y: >8.3f}{z: >8.3f}{occupancy: >6.2f}{tempFactor: >6.2f}\n"
        )

    with open(filePath, 'w', encoding = 'utf-8') as pdbFile:
        atomNum = 1
        resNum = 1
        cell = cellParams

        if cell != None:
            pdbFile.write(cell + '\n')

        for mol in data:
            for atom in mol:
                pdbFile.write(template.format(
                   atomNum = atomNum,
                   atomType = atom[0],
                   residueName = atom[4],
                   resNum = resNum,
                   x = atom[1],
                   y = atom[2],
                   z = atom[3],
                   occupancy = 1.00, # Default value
                   tempFactor = 0.00, # Default value
                ))

                atomNum += 1
            resNum += 1
        pdbFile.write("END\n")

def writeXYZ(data, filePath, strucType):
    '''Writes an xyz file from results'''
    if strucType == 'molecule':
        columns = ['Atom', 'X', 'Y', 'Z']
        df = pd.DataFrame(columns=['Atom', 'X', 'Y', 'Z'])

        for mol in data:
            for atom in mol:
                df = df._append(pd.Series(atom, index=columns),
                                ignore_index = True)

        with open(filePath, 'w', encoding = 'utf-8') as f:
            f.write(str(len(df['Atom'])))
            f.write('\n\n')
            f.write(df.to_string(header=False, index=False))

    else:
        df = pd.DataFrame(data, columns=['Atom', 'X', 'Y', 'X'])
        with open(filePath, 'w', encoding = 'utf-8') as f:
            f.write(str(len(df['Atom'])))
            f.write('\n\n')
            f.write(df.to_string(header=False, index=False))

def getElementData(param):
    '''
    Import Atomic Data
    Database Information
    Mass: g/mol
    Denisty Units: g/mL, Temp Units: Kelvin, Heat Capacity Units: J/(g*K),
    Heat of Vaporization/Fusion Units = kJ/mol
    Molar Volume Units: mL, Thermal Conductivty Units: Watts/(m * K),
    Atomic/Covalent/Van Det Waals Radius Units = pm
    Ionization Energy Units = kJ/mol, Electron Affinity Units = kJ/mol
    Data From: https://github.com/Bluegrams/periodic-table-data
    '''

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'data/ElementData.csv')

    elements = pd.read_csv(filename, delimiter=",", header=0)
    columnsToRemove = ["DiscoveredBy", "Discovery", "AbundanceCrust", "AbundanceUniverse"]
    elements = elements.drop(labels=columnsToRemove, axis = 1)

    return pd.DataFrame(elements, columns=['Symbol', param])
