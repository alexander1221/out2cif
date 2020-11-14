from sys import argv
from copy import deepcopy
from sys import argv
import os

string2find = "FINAL OPTIMIZED GEOMETRY"
counter = 0

f = argv[argv.index('-o')+1]
t = argv[argv.index('-t')+1]

fi=f[:-4]

a_list=[]

with open (f, "rt") as crystal_out:
  for myline in crystal_out:
    if myline.find(string2find) == 1:
      counter += 1
    if counter >=1:
      a_list.append(myline)
      counter+=1
    if counter == (11+(4*int(t))):
      break           

fobj = open("fog", 'w')         #We create file object to write data into output file

for h in range(0, len(a_list)):
  fobj.write('{}\n'.format(a_list[h])) 

fobj.close()                    #Closes file object

f = open("fog", 'r')            #Open input file in order to read it
b_list = f.readlines()          #Read files line by line and write it in list, where every line is presented as single element of the list
f.close()                       #We need to close f because we do not need it any more (because we have digiyal copy of it) and now it just wastes our memory

def removeComments(in_file, out_file):
  inp = open(in_file, "r")
  out = open(out_file, "w")

  out.write(inp.readline())

  for line in inp:
    if not line.lstrip().startswith("*"):
      out.write(line)

  inp.close()
  out.close()

removeComments("fog", "FOG")

class Cell():
  a = None
  b = None
  c = None
  alpha = None
  beta = None
  gamma = None
  def __init__(self,c=None):
    if c != None:
      self.a = c[0]
      self.b = c[1]
      self.c = c[2]
      self.alpha = c[3]
      self.beta = c[4]
      self.gamma = c[5]
  def __str__(self):
    return '{0:8s}{1:8s}{2:8s}{3:8s}{4:8s}{5:8s}'.format(self.a, self.b, self.c, self.alpha, self.beta, self.gamma)


class Atom():
    id_atom = None
    f_or_t = None
    nz = None
    atom_name = None
    x = None
    y = None
    z = None
    def __init__(self, a=None):
      if a != None:
        atom = filter(lambda x: x != '', a.split())
        self.id_atom = []
        self.f_or_t = []
        self.nz = []
        self.atom_name = []
        self.x = []
        self.y = []
        self.z = []
    def __str__(self):
      return '{0:5d}{1:5s}{2:5d}{3:5s}{4:5s}{5:8d}{6:8.3f}/n'.format(self.id_atom, self.f_or_t, self.nz, self.atom_name, self.x, self.y, self.z)

class Fog():
  volume_cell = None
  primitive_cell = None
  atom = None
  def __init__(self,fogname=None):
    if fogname != None:
      f = open(fogname,'r')
      a = f.readlines()
      f.close()
      i = list(filter(lambda s: s!='\n', a))
      v = i[3]
      c = i[5]
      a = i[8:]
      vol = list(filter(lambda x: x != ' ', v.split()))
      cel = list(filter(lambda x: x != ' ', c.split()))
      at = [i.split(" ") for i in a]
      ato = [' '.join(i).split() for i in at]
      self.volume_cell = vol[7]
      self.primitive_cell = cel
      self.atom = ato
  def __str__(self):
    return self.header+'\n'.join(map(str,self.list_of_atoms))


system=Fog(fogname='FOG')
system_cell=Cell(c=system.primitive_cell)


#in_file = open('atom_str', 'r')
#atomin = in_file.readlines()
#in_file.close()

list_of_str = system.volume_cell
list_of_cell = system.primitive_cell
list_of_atom = system.atom

combination1 =''
for x in list_of_str:
  combination1+=x

combination2 =''
for x in list_of_cell:
  combination2+=x

true_atoms = []

combination3 =''
for x in list_of_atom:
  if x[1]=='T':
    x = " ".join([i.strip() for i in x])
    combination3+=x + '\n'

for x in list_of_atom:
  if x[1]=='T':
    true_atoms.append(x)

for x in true_atoms:
  del x[0]
  del x[1]

c_counter = 0
h_counter = 0
o_counter = 0
br_counter = 0

for x in true_atoms:
  if x[1] == 'C':
    c_counter+=1
    x[0] = 'C' + str(c_counter)
  elif x[1] == 'H':
    h_counter+=1
    x[0] = 'H' + str(h_counter)
  elif x[1] == 'O':
    o_counter+=1
    x[0] = 'O' + str(o_counter)
  elif x[1] == 'BR':
    br_counter+=1
    x[0] = 'BR' + str(br_counter)  

true_atom_table =''
for x in true_atoms:
  x = " ".join([i.strip() for i in x])
  true_atom_table+=x + '\n'

intro = '''#######################################################################''' + '\n' + '#' + '\n' + '#                 Cambridge Crystallographic Data Centre' + '\n' + '#                                CCDC ' + '\n' + '''#######################################################################''' + '\n' + '#' + '\n' + '# If this CIF has been generated from an entry in the Cambridge ' + '\n' + '# Structural Database, then it will include bibliographic, chemical, ' + '\n' + '# crystal, experimental, refinement or atomic coordinate data resulting' + '\n' + '# from the CCDC\'s data processing and validation procedures.' + '\n' + '''#######################################################################'''+ '\n' + '#' + '\n' + ''

data_cryst = 'data_0_Form-I' + '\n' + '_symmetry_cell_setting           monoclinic' + '\n' + '_symmetry_space_group_name_H-M   ' + '\n' + '_symmetry_Int_Tables_number      14' + '\n' + '_space_group_name_Hall           ' + '\n' + 'loop_' + '\n' + '_symmetry_equiv_pos_site_id' + '\n' + '_symmetry_equiv_pos_as_xyz' + '\n' + '1 x,y,z' + '\n' + '2 1/2-x,1/2+y,1/2-z' + '\n' + '3 -x,-y,-z' + '\n' + '4 1/2+x,1/2-y,1/2+z' + '\n' + '_cell_length_a                   ' + system_cell.a + '\n' + '_cell_length_b                   ' + system_cell.b  + '\n' + '_cell_length_c                   ' + system_cell.c  + '\n' + '_cell_angle_alpha                ' + system_cell.alpha  + '\n' + '_cell_angle_beta                 ' + system_cell.beta  + '\n' + '_cell_angle_gamma                ' + system_cell.gamma  + '\n' + '_cell_volume                     ' + system.volume_cell + '\n' + 'loop_'  + '\n' + '_atom_site_label'  + '\n' + '_atom_site_type_symbol'  + '\n' + '_atom_site_fract_x' + '\n' + '_atom_site_fract_y'  + '\n' + '_atom_site_fract_z' + '\n'

f=open(fi+'.cif','w')
f.write(intro)
f.write(data_cryst)
f.write(true_atom_table)
f.write('\n' + '#END')
f.close()

os.remove("fog")
