from amolkit import getEleInfo as gei 
#class PsfAtom:
#    def __init__(self, atom_name, atom_index, atom_type, atom_charge, atom_mass, atom_resname, atom_resid, atom_segn, atom_qlp):
#        self.name = atom_name
#        self.index = atom_index
#        self.type = atom_type
#        self.charge = atom_charge
#        self.mass = atom_mass
#        self.resname = atom_resname
#        self.resid = atom_resid
#        self.segn = atom_segn
#        self.qlp = atom_qlp
#        self.alpha = None
#        self.thole = None
#
#class Psf:
#    def __init__(self):
#        self.atoms = {}
#        self.bond_indices = []
#        self.lpbond_indices = []
#        self.drudebond_indices = []
#        self.angle_indices = []
#        self.dihedral_indices = []
#        self.improper_indices = []
#        self.donor_indices = []
#        self.acceptor_indices = []
#        self.cmap_indices = []
#        self.lpics = []
#        self.anisotropies = []
#        self.drudebonds = []
#        self.groups = []
#
#    def add_atom(self, atom_name, atom_index, atom_type, atom_charge, atom_mass, atom_resname, atom_resid, atom_segn, atom_qlp, atom_alpha=None, atom_thole=None):
#        atom = PsfAtom(atom_name, atom_index, atom_type, atom_charge, atom_mass, atom_resname, atom_resid, atom_segn, atom_qlp)
#        atom.alpha = atom_alpha
#        atom.thole = atom_thole
#        self.atoms[atom_index] = atom
#
#    def add_bond(self, atom_a, atom_b):
#        self.bond_indices.append([atom_a, atom_b])

class Atom():
    def __init__(self,index,name=None,serial=None,atype=None,dtype=None,symbol=None,mass=None,charge=None,
                 Z=None,x=None,y=None,z=None,resn=None,resid=None,segn=None,chain=None,
                 alpha=None,thole=None,occu=None,tfac=None,penalty=None,comment=None):
        self.index   = index
        self.name    = name 
        self.serial  = serial 
        self.atype   = atype 
        self.dtype   = dtype 
        self.symbol  = symbol 
        self.Z       = Z 
        self.mass    = mass 
        self.charge  = charge 
        self.alpha   = alpha
        self.thole   = thole
        self.resn    = resn 
        self.resid   = resid 
        self.chain   = chain 
        self.segn    = segn 
        self.x       = x 
        self.y       = y 
        self.z       = z 
        self.occu    = occu 
        self.tfac    = tfac 
        self.penalty = penalty
        self.comment = comment

    def GetName(self):
        return self.name

    def GetSymbol(self,bio=True):
        self.symbol = gei.atomsymbol_by_atomname(self.name,bio)
        return self.symbol

    def GetSymbolbyAtomicNumber(self): 
        self.symbol = gei.atomsymbol_by_atomicnumber(self.Z) #atomicnumber) 
        return self.symbol

    def GetAtomicNumber(self,bio=True):
        self.Z = gei.atomicnumber_by_atomname(self.name,bio)
        return self.Z

    def GetAtomicMass(self,bio=True):
        self.mass = gei.atomicmass_by_atomname(self.name,bio)
        return self.mass

    def GetCovRad(self,bio=True):
        self.radius = gei.covrad_by_atomname(self.name,bio)
        return self.radius

    def GetCoordinate(self):
        self.coord = [self.x,self.y,self.z]
        return self.coord

class ElementProp():
   def __init__(self, Z, radius, max_bonds, r, g, b):
      self.Z = Z
      self.radius = radius
      self.max_bonds = max_bonds
      self.color = np.array([r,g,b], dtype='float32')
   def __str__(self):
      format_string = ' '.join(['{:4d}','{:9f}','{:4d}','{:9f}'*3])
      return format_string.format(self.Z, self.radius, self.max_bonds, *self.color)

class AssignElementProp(ElementProp):
   def __init__(self): 
      self.PSE = {}
      self.ATSYM = {}
      for atsym in ei.AtomOrder:
         self.PSE[atsym.upper()] = ElementProp(ei.AtomicNumber[atsym],ei.CovalentRadius[atsym],ei.BondOrder[atsym],*ei.AtomColor[atsym])
         self.ATSYM[ei.AtomicNumber[atsym]] = atsym
