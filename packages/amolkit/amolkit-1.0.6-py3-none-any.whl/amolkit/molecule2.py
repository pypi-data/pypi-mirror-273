import os
import sys
from os.path import join as opj
from operator import sub
from collections import OrderedDict
from amolkit import getEleInfo as gei 
from amolkit.stringmanip import updateAtomNames 
from amolkit import misc
from amolkit.atom import Atom 

def crdreadfmt(crdtype='extended'):
    if crdtype[0:3].lower() == 'ext':
        #fortran_format = '(2I10,2X,A8,2X,A8,3F20.10,2X,A8,2X,A8,F20.10)'
        indexdict={'srlno':[0,10],'resid':[10,20],'resn':[22,30],'aname':[32,40],
            'x':[40,60],'y':[60,80],'z':[80,100],'segn':[102,110],'segid':[112,120],'tfac':[120,140]}
    else:    
        #fortran_format = '(2I5,1X,A4,1X,A4,3F10.5,1X,A4,1X,A4,F10.5)'
        indexdict={'srlno':[0,5],'resid':[5,10],'resn':[11,15],'aname':[16,20],
            'x':[20,30],'y':[30,40],'z':[40,50],'segn':[51,55],'segid':[56,60],'tfac':[60,70]}
    return indexdict    
        
def pdbreadfmt(pdbtype='charmm'):
    indexdict={'srlno':[6,11],'aname':[12,16],'resn':[17,21],'chain':[22],'resid':[22,26],
                    'x':[30,38],'y':[38,46],'z':[46,54],'occu':[54,60],'tfac':[60,66],'segn':[72,76],'ele':[76,78],'charge':[78,80]}
    return indexdict

def crdwrtfmt(cd): 
    return "{:>10}{:>10}  {:<8}  {:<8}{:>20.10f}{:>20.10f}{:>20.10f}  {:<8}  {:<8}{:>20.10f}".format(cd["srlno"],
            cd["resid"],cd["resn"],cd["aname"],cd["coord"][0],cd["coord"][1],cd["coord"][2],cd["segn"],cd["resid"],0.0)

def pdbwrtfmt(pd):
    return "{:6s}{:5d} {:^4s}{:4s}  {:4d}    {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:4s}".format('ATOM',
            pd["srlno"],pd["aname"],pd["resn"],pd["resid"],pd["coord"][0],pd["coord"][1],pd["coord"][2],pd["occu"],pd["tfac"],pd["segn"])

def xyzwrtfmt(xd):
    return "%s %15.10f %15.10f %15.10f"%(xd["aname"],xd["coord"][0],xd["coord"][1],xd["coord"][2])

class Molecule():
    def __init__(self):
        #self.atomindex_byId=OrderedDict()
        #self.atomname_byIdx=OrderedDict()
        #self.atomserial_byIdx=OrderedDict()
        #self.atomresn_byIdx=OrderedDict()
        #self.atomresn_byId=OrderedDict()
        #self.atomresid_byIdx=OrderedDict()
        #self.atomresid_byId=OrderedDict()
        #self.atomcoord_byIdx=OrderedDict()
        #self.atomcoord_byId=OrderedDict()
        #self.atomchain_byIdx=OrderedDict()
        #self.atomchain_byId=OrderedDict()
        #self.atomoccu_byIdx=OrderedDict()
        #self.atomoccu_byId=OrderedDict()
        #self.atomtfac_byIdx=OrderedDict()
        #self.atomtfac_byId=OrderedDict()
        #self.atomsegn_byIdx=OrderedDict()
        #self.atomsegn_byId=OrderedDict()
        #self.atomele_byIdx=OrderedDict() 
        #self.atomele_byId=OrderedDict() 
        #self.atomcharge_byIdx=OrderedDict()
        #self.atomcharge_byId=OrderedDict()
        #self.atommass_byIdx=OrderedDict()
        #self.atommass_byId=OrderedDict()
        self.atoms=[]
        self.bondindices=[]
        self.energy=None
        self.natoms=None
        self.nmoltoms=None
        self.totalcharge=None

    def AddAtom(self,atom):
        self.atoms.append(atom)

    def GetAtoms(self):
        return self.atoms

    def readmol2(self,filename,istart=None,resid=None,bio=True):
        molblock = open(filename,"r").readlines()
        foundatm=False
        foundbnd=False
        if not istart: istart = 0
        ind=0
        for line in molblock:
            field = line.split()
            if len(field) !=0:
                if "@<TRIPOS>" in field[0].strip() and field[0].strip("@<TRIPOS>") not in ["MOLECULE","ATOM","BOND"]: break
            if len(field) != 0 and not foundatm:
                if field[0] == "@<TRIPOS>ATOM":
                    foundatm=True
                    foundbnd=False
                    continue
            elif len(field) != 0 and not foundbnd:
                if field[0] == "@<TRIPOS>BOND":
                    foundbnd = True
                    foundatm = False
                    continue
            if foundatm and len(field) >= 4:
                try:
                    ind += 1
                    srlno = int(istart) + ind
                    name = field[1]
                    x = round(float(field[2]),7) 
                    y = round(float(field[3]),7) 
                    z = round(float(field[4]),7) 
                    symbol = field[5].split(".")[0]
                    try:
                        charge = float(field[-1])
                    except (ValueError,IndexError):
                        charge = None
                    atom = Atom(index=ind,serial=srlno,name=name,x=x,y=y,z=z,symbol=symbol,charge=charge) 
                    self.AddAtom(atom)
                except (IndexError,ValueError):
                    # Reset the index back to previous value, because of error in atom line
                    ind = ind - 1
                    foundatm = False
                continue

            if foundbnd and len(field) == 4:
                self.bondindices.append([int(field[1]),int(field[2])])
                continue
        

        allnames = list(map(lambda x:x.upper(), self.atomname_byIdx.values())) 
        #if len(allnames) ==  len(list(set(allnames))):
        #    self.atomindex_byId = {v: k for k, v in self.atomname_byIdx.items()}

        self.nmolatoms = len(self.atoms)
        onlyatoms = [a.name for a in self.atoms if a.name[0:2].upper() != "LP" and a.name[0] != "D"]
        self.natoms = len(onlyatoms)
        self.totalcharge = int(round(sum(self.atomcharge_byIdx.values())))

    def readpdb(self,filename,istart=None,resid=None,bio=True):
        '''
        Parses the lines of a file object, if lines starts with ATOM or HETATM. 
        The names and the coordinates are extracted according to the PDB format.
        Providing user option for istart i.e. starting serial num and resid because these two may require adjustment.
        '''

        indexdict=pdbreadfmt('charmm')

        molblock = open(filename,"r").readlines()

        ind = 0
        for line in molblock:
            if line.startswith('ATOM') or line.startswith('HETATM'):
                ind += 1
                srlno = int(line[indexdict['srlno'][0]:indexdict['srlno'][1]].strip()) if not istart  else int(istart) + ind
                aname = line[indexdict['aname'][0]:indexdict['aname'][1]].strip()
                resn = line[indexdict['resn'][0]:indexdict['resn'][1]].strip()
                chain = line[indexdict['chain'][0]].strip()
                resid = int(resid)  if resid else int(line[indexdict['resid'][0]:indexdict['resid'][1]].strip())
                x=round(float(line[indexdict['x'][0]:indexdict['x'][1]].strip()),7)
                y=round(float(line[indexdict['y'][0]:indexdict['y'][1]].strip()),7)
                z=round(float(line[indexdict['z'][0]:indexdict['z'][1]].strip()),7)
                occu = float(line[indexdict['occu'][0]:indexdict['occu'][1]].strip())
                tfac = float(line[indexdict['tfac'][0]:indexdict['tfac'][1]].strip())
                segn = line[indexdict['segn'][0]:indexdict['segn'][1]].strip()
                ele = line[indexdict['ele'][0]:indexdict['ele'][1]].strip()
                ele = ele if ele else None
                charge = line[indexdict['charge'][0]:indexdict['charge'][1]].strip()
                charge = float(charge) if charge else None
                atom = Atom(index=ind,serial=srlno,name=name,resn=resn,resid=resid,segn=segn,occu=occu,tfac=tfac,x=x,y=y,z=z,symbol=symbol,charge=charge,chain=chain) 
                self.AddAtom(atom)

        # For single residue with all names different, populate the atomindex_byId
        allnames = list(map(lambda x:x.upper(), self.atomname_byIdx.values())) 
        #if len(allnames) ==  len(list(set(allnames))):
        #    self.atomindex_byId = {v: k for k, v in self.atomname_byIdx.items()}

        self.nmolatoms=len(self.atomname_byIdx)
        onlyatoms = [a for a in self.atomname_byIdx.values() if a[0:2].upper() != "LP" and a[0] != "D"]
        self.natoms = len(onlyatoms)

    def readcrd(self,filename,istart=None,resid=None,bio=True):
        molblock = open(filename,"r").readlines()
        ind = 0
        crdtype = 'standard'
        for line in molblock:
            field = line.split()
            if field[0] == '*' or len(field) == 0:
                continue  
            if len(field) <= 2:
                self.nmolatoms = int(field[0])
                if field[-1].upper() == 'EXT': crdtype = 'extended'
                indexdict = crdreadfmt(crdtype)
                continue

            if len(field) >= 10 and field[0] != "*":
                ind += 1
                if istart == None:
                    srlno = int(field[0].strip())
                    self.atomserial_byIdx[ind] = srlno 
                else:
                    srlno = int(istart) + ind
                    self.atomserial_byIdx[ind] = srlno
                if resid:
                    self.atomresid_byIdx[ind] = int(resid)
                else:
                    resid = int(line[indexdict['resid'][0]:indexdict['resid'][1]].strip())
                    self.atomresid_byIdx[ind] = resid 
                resn = line[indexdict['resn'][0]:indexdict['resn'][1]].strip()
                self.atomresn_byIdx[ind] = resn 
                aname = line[indexdict['aname'][0]:indexdict['aname'][1]].strip()
                self.atomname_byIdx[ind] = aname 
                self.atomele_byIdx[ind] = gei.atomsymbol_by_atomname(aname,bio)
                x=round(float(line[indexdict['x'][0]:indexdict['x'][1]].strip()),7)
                y=round(float(line[indexdict['y'][0]:indexdict['y'][1]].strip()),7)
                z=round(float(line[indexdict['z'][0]:indexdict['z'][1]].strip()),7)
                self.atomcoord_byIdx[ind] = [x,y,z]
                segn = line[indexdict['segn'][0]:indexdict['segn'][1]].strip()
                self.atomsegn_byIdx[ind] = segn 
                tfac = float(line[indexdict['tfac'][0]:indexdict['tfac'][1]].strip())
                self.atomtfac_byIdx[ind] = tfac

        # sanity check
        if self.nmolatoms != ind:
            raise ValueError("Found %d coordinates in %r but should be %d coordinates." % (self.nmolatoms, filename, ind))

        allnames = list(map(lambda x:x.upper(), self.atomname_byIdx.values())) 
        if len(allnames) ==  len(list(set(allnames))):
            self.atomindex_byId = {v: k for k, v in self.atomname_byIdx.items()}

        onlyatoms = [a for a in self.atomname_byIdx.values() if a[0:2].upper() != "LP" and a[0] != "D"]
        self.natoms = len(onlyatoms)

    def readxyz(self,filename,istart=None,resid=None,bio=True):
        if not istart: istart = 0
        ind = 0
        molblock = open(filename,"r").readlines()
        for i,line in enumerate(molblock):
            field = line.split()
            if i == 0: self.nmolatoms = int(field[0]) 
            if i == 1: continue # Second line is comment
            if len(field) >= 4:
                ind += 1
                srlno = int(istart) + ind
                self.atomserial_byIdx[ind] = srlno
                self.atomname_byIdx[ind] = field[0]
                self.atomcoord_byIdx[ind] = list(map(lambda x:round(float(x),7), field[1:4]))
                self.atomele_byIdx[ind] = gei.atomsymbol_by_atomname(field[0],bio)

        # sanity check
        if self.nmolatoms != ind:
            raise ValueError("Found %d coordinates in %r but should be %d coordinates." % (self.nmolatoms, filename, ind))

        allnames = list(map(lambda x:x.upper(), self.atomname_byIdx.values())) 
        if len(allnames) ==  len(list(set(allnames))):
            self.atomindex_byId = {v: k for k, v in self.atomname_byIdx.items()}

        onlyatoms = [a for a in self.atomname_byIdx.values() if a[0:2].upper() != "LP" and a[0] != "D"]
        self.natoms = len(onlyatoms)
 
    @staticmethod
    def generateBonds(elementnames=[],coordinates=[]):
        """
        Expects list of names and coordinates of same length 
        """
        import numpy as np
        from amolkit import getEleInfo as gei 
    
        if elementnames and coordinates and len(elementnames) != len(coordinates):
            raise IndexError("names list and coordinate list don't match")
         
        coordinates = np.array(coordinates,dtype ='float32')
    
        delta = [None]*3
        for i in range(3):
           coord = coordinates[:,i]
           delta[i] = coord - coord.reshape((len(coord),1))
    
        dist = delta[0]**2 + delta[1]**2 + delta[2]**2 + 10. * np.identity(len(coordinates))
    
        radius = []
        for el in elementnames:
            radius.append(gei.covrad_by_atomsymbol(el)) 
        radius = np.array(radius, dtype='float32')
    
        radcov = (radius + radius.reshape((len(radius),1)))*2
        bonded = np.array(np.where(dist - radcov<0.)).transpose()
        distmat = np.sqrt(dist[bonded[:,0],bonded[:,1]])
        
        # amolkit indices for molecules starts from 1
        bondindices=[]
        for b in bonded:
            bondindices.append(list(map(lambda x:x+1,b)))
    
        bondinfo={}
        bondinfo["radcov"]         = radcov
        bondinfo["pybondindices"]  = bonded
        bondinfo["distmat"]        = distmat
        bondinfo["bondindices"]    = bondindices
        return bondinfo 

    def genBonds(self):
        self.bondindices=self.generateBonds(list(self.atomele_byIdx.values()),list(self.atomcoord_byIdx.values()))["bondindices"]

    def autoupdateAtomNames(self):
        atomnames=updateAtomNames(list(self.atomname_byIdx.values()))
        for i in range(len(atomnames)):
            ind = i + 1
            self.atomname_byIdx[ind] = atomnames[i]

    def updateAtomNamesWith(self,atomnames):
        if not isinstance(atomnames,list) or len(atomnames) != len(list(self.atomname_byIdx.values())):
            raise IndexError ("Length of atomnames not same as molecule atoms.")
        for i in range(len(atomnames)):
            ind = i + 1
            self.atomname_byIdx[ind] = atomnames[i]

    def readMolecule(self,filename,istart=None,resid=None,bio=True):
        filestatus = misc.FileStatus(filename) 
        extension = misc.getExtension(filename)
        if not filestatus:
            raise RuntimeError ("Error reading file")
        if extension not in ["xyz","mol2","pdb","crd"]: 
            raise RuntimeError ("Cant read this file format")
        if extension == "pdb":  self.readpdb(filename,istart,resid,bio)
        if extension == "crd":  self.readcrd(filename,istart,resid,bio)
        if extension == "mol2": self.readmol2(filename,istart,resid,bio)
        if extension == "xyz":  self.readxyz(filename,istart,resid,bio)

#def genMolFromAtomNames(atomnames:list,atomcoords:list,updatenames=False,**kwargs):
def genMol(atomnames:list,atomcoords:list,updatenames=False,**kwargs):
    if not isinstance(atomnames,list) and not isinstance(atomcoords,list):
        raise ValueError ("Provide list of atomnames and list of coords")
    if len(atomnames) != len(atomcoords):
        raise IndexError ("Length of atomnames and coords are not same.")
    
    resname = "RESN"; resid = 1; segname = "SEGN"
    if 'resname' in kwargs:
       resname = kwargs["resname"] 
    if 'resid' in kwargs:
       resid = kwargs["resid"]
    if 'segname' in kwargs:
       segname = kwargs["segname"]

    mol = Molecule()
    mol.nmolatoms = len(atomnames) 
    
    for i in range(len(atomnames)): 
        ind = i + 1
        name = atomnames[i]
        x,y,z = atomcoords[i] 
        atom = Atom(index=ind,serial=ind,name=atomnames[i],resn=resname,resid=resid,segn=segname,x=x,y=y,z=z) 
        atom.GetSymbol()
        self.AddAtom(atom)
    if updatenames:
        for i in range(len(atomnames)): 

    return mol

#def genMolFromAtomicNumber(atomicnumbers:list,atomcoords:list,updatenames=False,**kwargs):
#    if not isinstance(atomnumbers,list) and not isinstance(atomcoords,list):
#        raise ValueError ("Provide list of atomnames and list of coords")
#    if len(atomnumbers) != len(atomcoords):
#        raise IndexError ("Length of atomnames and coords are not same.")
#    
#    resname = "RESN"; resid = 1; segname = "SEGN"
#    if 'resname' in kwargs:
#       resname = kwargs["resname"] 
#    if 'resid' in kwargs:
#       resid = kwargs["resid"]
#    if 'segname' in kwargs:
#       segname = kwargs["segname"]
#
#    mol = Molecule()
#    mol.nmolatoms = len(atomicnumbers) 
#    
#    for i in range(len(atomicnumbers)): 
#        ind = i + 1
#        name = atomnames[i]
#        x,y,z = atomcoords[i] 
#        atom = Atom(index=ind,serial=ind,name=name,resn=resname,resid=resid,segn=segname,x=x,y=y,z=z) 
#        atom.GetSymbol()
#        self.AddAtom(atom)
#    return mol

#def genMol(atomlist:list,atomcoords:list,updatenames=False,**kwargs):
#    if not isinstance(atomnumbers,list) and not isinstance(atomcoords,list):
#        raise ValueError ("Provide list of atomnames and list of coords")
#    if len(atomlist) != len(atomcoords):
#        raise IndexError ("Length of atomnames and coords are not same.")
#    atnumber=False
#    for at in atomlist:
#        if str(at).isnumber(): atnumber=True
#    if atnumber:
#        genMolFromAtomicNumber(atomlist,atomcoords,updatenames=updatenames,**kwargs)
#    else:
#        genMolFromAtomName(atomlist,atomcoords,updatenames=updatenames,**kwargs)
#
    
def coordline(molecule,pyindex,serialnum=None,resid=None):
    '''
    For index = ind in molinstance, this function assigns variables required 
    for writing coordinate line in crd/pdb/xyz/mol2
    Arguments:
        molinstance: instance of Molecule class with preloaded molecule information
        pyindex: Index for which information is required; Starts with 0 not 1. 
        istart: In case the molecule in molinstance is not the first molecule, 
        then serial number of first atom can be provided.
        resid: User defined resid
    Returns:
        cpvar:: Dictionary containing all possible information extracted from molinstance[ind]
    '''
    i = pyindex # Python index
    cpvar={}
    if serialnum:
        cpvar["srlno"] = serialnum 
    else:    
        cpvar["srlno"] = molecule.atoms[i].serial #erial_byIdx[ind] 

    cpvar["aname"] = molecule.atoms[i].name #_byIdx[ind] 

    if molecule.atoms[i].resn: #_byIdx and ind in molecule.atomresn_byIdx.keys():
        cpvar["resn"] = molecule.atoms[i].resn #_byIdx[ind] 
    else:    
        cpvar["resn"] = "RESN" 

    if molecule.atoms[i].chain: #_byIdx and ind in molecule.atomchain_byIdx.keys():
        cpvar["chain"] = molecule.atoms[i].chain #_byIdx[ind] 
    else:    
        cpvar["chain"] = "" 

    if resid:
        cpvar["resid"] = resid 
    elif molecule.atoms[i].resid: #_byIdx and ind in molecule.atomresid_byIdx.keys():
        cpvar["resid"] = molecule.atoms[i].resid #_byIdx[ind] 
    else:    
        cpvar["resid"] = 1 

    cpvar["coord"] = [molecule.atoms[i].x,molecule.atoms[i].y,molecule.atoms[i].z] #coord #_byIdx[ind] 

    if molecule.atoms[i].occu: #_byIdx and ind in molecule.atomoccu_byIdx.keys():
        cpvar["occu"] = molecule.atoms[i].occu #_byIdx[ind] 
    else:    
        cpvar["occu"] = 0.0  

    if molecule.atoms[i].tfac: #_byIdx and ind in molecule.atomtfac_byIdx.keys():
        cpvar["tfac"] = molecule.atoms[i].tfac #_byIdx[ind] 
    else:    
        cpvar["tfac"] = 0.0  

    if molecule.atoms[i].segn: #_byIdx and ind in molecule.atomsegn_byIdx.keys():
        cpvar["segn"] = molecule.atoms[i].segn #_byIdx[ind] 
    else:    
        cpvar["segn"] = "SEGN" 

    if molecule.atoms[i].symbol: #ele_byIdx and ind in molecule.atomele_byIdx.keys():
        cpvar["ele"] = molecule.atoms[i].symbol #ele_byIdx[ind] 
    else:    
        cpvar["ele"] = "" 

    if molecule.atoms[i].charge: #_byIdx and ind in molecule.atomcharge_byIdx.keys():
        cpvar["charge"] = molecule.atoms[i].charge #_byIdx[ind] 
    else:    
        cpvar["charge"] = 0.0 
    return cpvar 
 
def writecrd(molecule,fileout=None,nolpd=False,comment=None):
    ocrdfile = open(fileout,"w")
    if comment:
        ocrdfile.write("* %s\n"%(comment))
    else:
        ocrdfile.write("* Generated by amolkit\n")
    ocrdfile.write("* \n")
    if not nolpd:
        ocrdfile.write("%10i  EXT\n" %(molecule.nmolatoms))
        for i in range(molecule.nmolatoms):
            #ind=i+1
            cdict = coordline(molecule,i)
            ocrdfile.write(crdwrtfmt(cdict)+"\n")
        ocrdfile.close()
    else:
        serialnum = 0
        ocrdfile.write("%10i  EXT\n" %(molecule.natoms))
        for i in range(molecule.nmolatoms):
            #ind=i+1
            checkatm = molecule.atoms[i].name #_byIdx[ind]
            if checkatm[0:1] == "D" or checkatm[0:2] == "LP":
                serialnum = serialnum
            else:    
                serialnum = serialnum + 1
            cdict = coordline(molecule,i,serialnum=serialnum)
            ocrdfile.write(crdwrtfmt(cdict)+"\n")
        ocrdfile.close()
    prntscr = " ".join((str(fileout),"created"))
    print(prntscr) 

def writepdb(molecule,fileout=None,nolpd=False,comment=None):
    opdbfile = open(fileout,"w")
    if comment:
        opdbfile.write("REMARK   %s\n"%(comment))
    else:
        opdbfile.write("REMARK   1 Generated by amolkit\n")
    if not nolpd:
        for i in range(molecule.nmolatoms):
            #ind=i+1
            cdict = coordline(molecule,i)
            opdbfile.write(pdbwrtfmt(cdict)+"\n")
    else:
        serialnum = 0
        for i in range(molecule.nmolatoms):
            #ind=i+1
            checkatm = molecule.atoms[i].name #_byIdx[ind]
            #checkatm = molecule.atomname_byIdx[ind]
            if checkatm[0:1] == "D" or checkatm[0:2] == "LP":
                serialnum = serialnum
            else:    
                serialnum = serialnum + 1
            pdict = coordline(molecule,i,serialnum=serialnum)
            opdbfile.write(pdbwrtfmt(pdict)+"\n")
    opdbfile.write("TER\n")
    opdbfile.write("END\n")
    opdbfile.close()
    prntscr = " ".join((str(fileout),"created"))
    print(prntscr) 

def writexyz(molecule,fileout=None,nolpd=False,comment=None):
    if fileout == None:
       fileout = "molecule.xyz"
       print ("No output xyzfile name provided. Writing in molecule.xyz") 

    oxyzfile = open(fileout,"w")
    if not nolpd:
        oxyzfile.write("%10i \n" %(molecule.nmolatoms))
        if comment:
            oxyzfile.write("%s\n"%(comment))
        else:
            oxyzfile.write("Generated by amolkit\n")
        for i in range(molecule.nmolatoms):
            #ind=i+1
            xdict = coordline(molecule,i) #ind)
            oxyzfile.write(xyzwrtfmt(xdict)+"\n")
        oxyzfile.close()
    else:
        serialnum = 0
        oxyzfile.write("%10i\n" %(molecule.natoms))
        if comment:
            oxyzfile.write("%s\n"%(comment))
        else:
            oxyzfile.write("Generated by amolkit\n")
        for i in range(molecule.nmolatoms):
            #ind=i+1
            checkatm = molecule.atoms[i].name #_byIdx[ind]
            #checkatm = molecule.atomname_byIdx[ind]
            if checkatm[0:1] == "D" or checkatm[0:2] == "LP":
                serialnum = serialnum
            else:    
                serialnum = serialnum + 1
            xdict = coordline(molecule,i,serialnum=serialnum)
            oxyzfile.write(xyzwrtfmt(xdict)+"\n")
        oxyzfile.close()
    prntscr = " ".join((str(fileout),"created"))
    print(prntscr) 

class GenMoleculeRDkit():
    import numpy as np
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except ImportError:
        logging.warning('RDKit not found!')


    def __init__(self,topology,resname,resitopfile):
        """
        """
        self.topology = topology()
        self.topology.loadCharmmTopology(resname,resitopfile)

    def genRDMolTop(self):
        self.mol=Chem.RWMol()
        atid={}
        idat={}
        atomicnumber_by_atomname
        for i, aname in topology.atomname_byIdx.items():
            if aname[0]=="D" or aname[0:2] =="LP": continue
            atomicnumber = gei.atomicnumber_by_atomname(aname) 
            atomsymbol = gei.atomsymbol_by_atomname(aname) 
            idx = m.AddAtom(Chem.Atom(atomicnumber))
            atid.update({atomsymbol:idx})
            idat.update({idx:atomsymbol})
        for bond in self.bonds:
            self.mol.AddBond(atid[bond[0]], atid[bond[1]],Chem.BondType.SINGLE)
        try:
            Chem.SanitizeMol(self.mol)
        except ValueError:
            pass
    
        #self.rdmolnrs=idat

    def gen3dRDkit(self):
        AllChem.EmbedMolecule(mol,useExpTorsionAnglePrefs=True,useBasicKnowledge=True)
        AllChem.MMFFOptimizeMolecule(mol)

