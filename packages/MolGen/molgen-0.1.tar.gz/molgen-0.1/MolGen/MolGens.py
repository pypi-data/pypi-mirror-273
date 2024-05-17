from __future__ import absolute_import, division, print_function
from math import ceil
import pytraj as pt
import nglview as ngl
import mdtraj
import pyemma.coordinates
import pyemma.coordinates.data
import nglview #
import os
import sys
import shutil
import numpy as np
import tqdm
import importlib
from Bio import PDB
from subprocess import call
import logging
from Bio.PDB import PDBParser
import pickle
import warnings
import io
from scipy.spatial import distance
import barnaba as bb
import pandas as pd
import itertools
from . import definitions
from . import nucleic
from . import calc_mats as ff
from scipy.stats import skew, kurtosis

# Suppress specific warnings or all warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', '.*Disordered.*')

class MolGen(object):

    def __init__(self, topology=None, 
                topology_select=None,
                cryst_pdb_list = False,
                file_names = None, 
                structure_names = None, 
                align=False, 
                chunk_size=None):
        """ generates and visualizes conformational ensembles for ensemble docking
        
        Parameters
        ------------
        trajectory: str 
            a path to the trajectory file (.xtc, .dcd, etc.)
        topology: str
            a path to the trajectory file (.pdb)
        topology_select: str | list, default = None
            a select string that indicates what part of the topology is relevant for featurization
            or an array of atom indices of interest (as required by mdtraj)
        cryst_pdb_list: boolean, default = False
            is your input a list of crystal structure files??
        file_names: list, default = None
            if your input is the list of PDB files, provide the list here
        structure_names: list, default = None
            if your input is the list of PDB files, provide their names here
        align: boolean, default = False
            specify if you wish to align the given trajectory before analyzing
        chunk_size: int, default = 1000
            specify the chunk size of trajectory that is loaded into memory at once
            (decrease this number when having memory issues)
        """
        
        
        #if topology is not None and file_names is not None:
        #    print("topology and file_names can not be provided at the same time!")
        #    exit(-1)


        # perform the alignment if specified
        self.ref = topology
        self.full_ref = topology
        self.refrestraint = topology_select
        self._selection_indices = None
        self.chunk_size = chunk_size

        self.mdtrajref = mdtraj.load(self.ref).topology
        self.crystal_flag = cryst_pdb_list
        self.pdb_files = file_names
        self.structure_names = structure_names
        if structure_names is None: self.structure_names = file_names
        self.pdb_list = None
        self.mdtraj_list = []
        self.mdtraj = []
        
        
        if topology is not None:
            # load topology and save to xtc file
            self.pdb_files = file_names
            
        '''
        if align or cryst_pdb_list:
            traj_new = trajectory[:trajectory.rfind(".")]+"-aligned.xtc"
            self.align_trajectory(traj_new)
            self.traj = traj_new
            self.traj_name = traj_new
            self.full_traj_name = traj_new
        '''
        if align and cryst_pdb_list:
            self.align_pdb_files()

        #if self.crystal_flag and self.refrestraint is None:
        if self.refrestraint is None: 
            self.pdb_list = []
            self.mdtraj = []
            self.mdtraj_list = []
            for elem in tqdm.tqdm(self.pdb_files, "Loading files (might take a while)"):
                print("Loading ", elem)
                elem_frame = mdtraj.load(elem)
                elem_frame_dst = elem[:-4]+"_tmp.xtc"
                elem_frame.save(elem_frame_dst)
                self.mdtraj.append(elem_frame)
                self.mdtraj_list.append(elem_frame_dst)
                pyemma_frame = pyemma.coordinates.source(elem_frame_dst, top=elem, chunksize=self.chunk_size)
                self.pdb_list.append(pyemma_frame)

        # load a restrained trajectory based on a selection/list/None
        if isinstance(self.refrestraint, str):
            tmp_top = mdtraj.load(self.ref).topology
            self._selection_indices = tmp_top.select(topology_select)
            self.select_atoms_trajectory(self._selection_indices)
        '''
        elif isinstance(self.refrestraint, list):
            self._selection_indices = self.refrestraint
            self.select_atoms_trajectory(self._selection_indices)

        '''
        self.featurizers = []
        self.featurizer_names =[]
        self.data = None
        self.dimRed = None
        self.cluster = None 
        self.chosen_feat_index = -1
        self.dimred_data = None
        self.dimred_featcorr = None

    @property
    def ref(self):
        return self._ref

    @ref.setter
    def ref(self, r):
        valid_ext =[".pdb"]
        if not r: raise Exception("Topology reference can not be empty")
        if not isinstance(r, str): raise Exception("Topology reference must be a string")
        if not r[r.rfind('.'):] in valid_ext: raise Exception("Topology reference must be with a correct extension")
        if not os.path.exists(r): Exception("Topology reference does not exist.")
        self._ref = r
    
    @property
    def refrestraint(self):
        return self._refrestraint

    @refrestraint.setter
    def refrestraint(self, r):
        if not r: 
            self._refrestraint = r
            return
        if not (isinstance(r, str) or isinstance(r, list)): 
            raise Exception("Topology restraint must be a string")
        self._refrestraint = r

    def align_pdb_files(self):

        parser = PDB.PDBParser(QUIET = True)
        # first structure as reference structure
        ref_structure = parser.get_structure("tmp_ref", self.pdb_files[0])
        ref_atoms = [] # only align C- alpha
        # Iterate of all chains in the model in order to find all residues
        for ref_chain in ref_structure[0]:
            # Iterate of all residues in each model in order to find proper atoms
            for ref_res in ref_chain:
                ref_atoms.append(ref_res['CA'])

        for elem in tqdm.tqdm(self.pdb_files, "Aligning pdb files (might take a while)"):
            sample_structure = parser.get_structure("tmp_sample", elem)
            sample_model = sample_structure[0]
            sample_atoms = [] # only Calpha
            for sample_chain in sample_model:
                for sample_res in sample_chain:
                    sample_atoms.append(sample_res['CA'])
            # Now we initiate the superimposer:
            super_imposer = PDB.Superimposer()
            super_imposer.set_atoms(ref_atoms, sample_atoms)
            super_imposer.apply(sample_model.get_atoms())
            # Save the aligned version of 1UBQ.pdb
            io = PDB.PDBIO()
            io.set_structure(sample_structure) 
            io.save(elem[:-4]+"_algn.pdb")
        
        self.pdb_files = [ f[:-4]+"_algn.pdb" for f in self.pdb_files]
    
    def analyze_pdb_files(self):
        protein_residues = {'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLU', 'GLN', 'GLY', 'HIS', 'ILE', 'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL'}
        rna_residues = {'A', 'C', 'G', 'U'}
        parser = PDBParser(QUIET=True)
        results = {}
        protein_list = []
        rna_list = []

        for pdb_file in self.pdb_files:
            try:
                structure = parser.get_structure('PDB_ID', pdb_file)
                has_protein_residues = False
                has_rna_residues = False

                for model in structure:
                    for chain in model:
                        for residue in chain:
                            res_id = residue.get_resname().strip()
                            if res_id in protein_residues:
                                has_protein_residues = True
                            elif res_id in rna_residues:
                                has_rna_residues = True

                if has_protein_residues:
                    protein_list.append(pdb_file)

                if has_rna_residues:
                    rna_list.append(pdb_file)

            except Exception as e:
                logging.error(f"Error processing {pdb_file}: {e}")

        results['all_proteins'] = protein_list
        logging.info(f"results['all_proteins'] {results['all_proteins']}")
        results['all_rna'] = rna_list
        logging.info(f"results['all_rna'] {results['all_rna']}")
        return results

    def select_atoms_pdb_list(self, selected_atoms):

        self.pdb_list = []
        old_files = self.pdb_files
        self.pdb_files = []
        self.mdtraj_list = []
        self.mdtraj = []
        for elem in tqdm.tqdm(old_files, "Loading PDB files with atom selection"):
            elem_frame = mdtraj.load(elem, atom_indices= selected_atoms)
            elem_frame_dst = elem[:-4]+"_tmp.xtc"
            elem_frame.save(elem_frame_dst)
            pyemma_frame = pyemma.coordinates.source(elem_frame_dst, top=elem_frame)
            self.mdtraj.append(elem_frame)
            self.mdtraj_list.append(elem_frame_dst)
            self.pdb_list.append(pyemma_frame)
            elem_frame_dst = elem[:-4]+"_tmp.pdb"
            elem_frame.save(elem_frame_dst)
            self.pdb_files.append(elem_frame_dst)
    
    def select_atoms_trajectory(self, selected_atoms):
        
        if self.crystal_flag:
            self.select_atoms_pdb_list(selected_atoms)
        tmp_traj = mdtraj.iterload(self.traj, top=self.ref, atom_indices=selected_atoms)
         # see trajectory length
        tmp_pe = pyemma.coordinates.source(self.traj, top=self.ref, chunksize=self.chunk_size)
        traj_len = tmp_pe.trajectory_length(0)
        file_names = []
        n_iter = ceil(traj_len/self.chunk_size)
        saved_ref=False
        tmp_dir ="./tmp_files"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        else:
            shutil.rmtree(tmp_dir)
            os.makedirs(tmp_dir)
        i=0
        # save chunks
        for chunk in tqdm.tqdm(tmp_traj, desc = "Making the selection... "):

            if not saved_ref:
                tmp_pdb_name = self.traj[:self.traj.rfind(".")]+"-molgen-selected.pdb"
                chunk[0].save(tmp_pdb_name)
                self.ref = tmp_pdb_name
                self.mdtrajref = mdtraj.load(tmp_pdb_name).topology
                self.ref = tmp_pdb_name
                saved_ref=True
            # save a temporary chunk
            file_name = os.path.join(tmp_dir, "molgen-tmp_chunk"+str(i)+".xtc")
            chunk.save(file_name)
            file_names.append(file_name)
            i+=1 
        
        tmp_name = self.traj[:self.traj.rfind(".")]+"-molgen-selected.xtc"
        
        if os.path.exists(tmp_name):
            os.remove(tmp_name)

        ret_val = call(["mdconvert -o {} {}".format(tmp_name, " ".join(file_names))] , shell=True)
        if not ret_val == 0:
            raise(Exception("Error making selection."))

        self.traj = tmp_name
        self.traj_name = tmp_name

        for i in tqdm.tqdm(range(len(file_names)), desc="Cleaning files..."):
            elem = file_names[i]
            os.remove(elem)

        if len(os.listdir(tmp_dir))==0:
            os.rmdir(tmp_dir)
    
    #--------------------FEATURIZATION--------------------------#
    def reset_featurizers(self):
        self.featurizer_names = []
        self.featurizers = []

    def add_featurizer(self, feats: dict):
        """
        Adds another featurization type to the list of featurizers
        
        Parameters
        ------------
        feats: dict object with entries {"add_feature_func_name": params, ...}
                "add_feature_func_name" should be an add function of pyemma.coordinates.featurizer.MDFeaturizer
                params should be parameters of the given function
        """
        if self.crystal_flag:
            pyemma_feat = []
            for elem in tqdm.tqdm(self.pdb_files, "Adding featurizers per PDB file.."):
                name = ""
                tmp_top = pyemma.coordinates.featurizer(elem)
                for key, params in feats.items():
                    name+=key[len("add_"):]
                    name+="&"
                    func =  getattr(tmp_top, key)
                    func(**params)
                name = name[:-1]
                pyemma_feat.append(tmp_top)
            self.featurizer_names.append(name)
            self.featurizers.append(pyemma_feat)
        else:
            pyemma_feat = pyemma.coordinates.featurizer(self.mdtrajref) 
            name = ""
            for key, params in feats.items():
                name+=key[len("add_"):]
                name+="&"
                func =  getattr(pyemma_feat, key)
                func(**params)
            name = name[:-1]
            self.featurizer_names.append(name)
            self.featurizers.append(pyemma_feat)

    def add_pyemma_featurizer(self, pyemma_feat: pyemma.coordinates.data.MDFeaturizer, name: str):
        """
        Adds another featurization type to the list of featurizers
        
        Parameters
        ------------
        feat: pyEmma featurizer
        name: name for the featurizer
        """
        self.featurizer_names.append(name)
        self.featurizers.append(pyemma_feat)

    def init_featurizers_default(self):
        """
        Adds default featurizers type to the list of featurizers
        
        Parameters
        ------------
        type: type of function for adding to inital default featurizer

        """

        # only called if initialization
        if not len(self.featurizers) == 0:
            return

        if not self.crystal_flag:
            default_feat1 = {
                "add_residue_mindist": {"scheme":'closest-heavy'}
            }
            default_feat2 = {
                "add_backbone_torsions": {"cossin":True, "periodic":False}

            }
            default_feat3 = {
                "add_backbone_torsions": {"cossin":True, "periodic":False},
                "add_residue_mindist": {"scheme":'closest-heavy'}

            }
            default_feats = [default_feat1, default_feat2, default_feat3]

        else:
            
            n_residues = min(mdtraj.load(file).top.n_residues for file in self.pdb_files)
            all_resi = [i for i in range(n_residues)]
            default_feat1 = {
                "add_residue_COM": {"residue_indices":all_resi ,"scheme":'all'}
            }
            default_feats = [default_feat1]

        for feat_dict in default_feats:
            self.add_featurizer(feat_dict)

    def apply_featurizations(self):
        self.data = []
        for f in self.featurizers:
            if not self.crystal_flag:
                prefix_to_remove = '/lab/hou/vchaudhari/molgens/pdb_data/accepted/'
                self.mdtraj_list = [path.replace(prefix_to_remove, '') for path in self.mdtraj_list]
                self.data += pyemma.coordinates.source(self.mdtraj, features=f, chunksize=self.chunk_size)
            else:
                per_pdb_data = None
                prefix_to_remove = '/lab/hou/vchaudhari/molgens/pdb_data/accepted/'
                self.mdtraj_list = [path.replace(prefix_to_remove, '') for path in self.mdtraj_list]
                for i, elem in tqdm.tqdm(enumerate(self.mdtraj), "Applying featurization per PDB file"):
                    tmp_name = self.pdb_files[i][:-4]+".xtc"
                    elem.save(tmp_name)
                    data = pyemma.coordinates.load(tmp_name, features=f[i])
                    if per_pdb_data is None: 
                        per_pdb_data = data
                    elif per_pdb_data.shape[1] == data.shape[1]:
                        per_pdb_data = np.vstack((per_pdb_data, data)) 
                self.data.append((0, per_pdb_data))

    def clean(self):
        if self.crystal_flag == True:
            # free this space
            self.mdtraj_list = None
            self.pdb_list = None

    def describe_featurizers(self):
        res = ""
        if not self.crystal_flag:
            for i, f in enumerate(self.featurizers):
                res += "Featurizer no. "+str(i)+":\n "
                res += self.featurizer_names[i] + "\n"
                desc_tmp = f.describe()
                res += str(desc_tmp[:10]) +"..." + str(desc_tmp[-10:]) +"\n "
        else:
            for i, f in enumerate(self.featurizers):
                res += "Featurizer no. (residues may differ from file to file) "+str(i)+":\n "
                res += self.featurizer_names[i] + "\n"
                desc_tmp = f[i].describe()
                res += str(desc_tmp[:10]) +"..." + str(desc_tmp[-10:]) +"\n "
        return res

################################################################################################################
    def rna_dump_rvec(self,filename,topology=None,cutoff=2.4):
        """
        Calculate relative position of pair of nucleobases within ellipsoidal cutoff

        Parameters
        ----------
        reference : string
            Filename of structure, any format accepted by MDtraj can be used.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        cutoff :  float, optional
            Cutoff for eRMSD calculation.
            This cutoff value roughly correspond to considering pair of bases whose distance is within an ellipsoidal cutoff with axis x=y=2.4*5 = 12 Angstrom and z=2.4*3=7.2 Angstrom. Larger values of cutoff can be useful when analyzing unstructured/flexible molecules.
        Returns
        -------
        rmat :
            Numpy array with dimension (m,n,n,3). *m* is the number of structures in target, *n* is the number of nucleotides. As an example, the position of base 10 in the reference system of base 9 in the fourth frame is given by v = rmat[3,8,9], where v is a 3-dimensional vector
        seq :
            List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX

        """

        if(topology==None):
            traj = mdtraj.load(filename)
        else:
            traj = mdtraj.load(filename,top=topology)

        warn = "# Loading %s \n" % filename
        sys.stderr.write(warn)
        return  self.rna_dump_rvec_traj(traj,cutoff=cutoff)

    def rna_dump_rvec_traj(self,traj,cutoff=2.4):

        top = traj.topology
        nn = nucleic.Nucleic(top)
        rvecs = []
        for i in range(traj.n_frames):
            coords_lcs = traj.xyz[i,nn.indeces_lcs]
            rvecs.append(ff.calc_rmat(coords_lcs,cutoff))

        return np.asarray(rvecs), nn.rna_seq

    ###############################################

    def rna_dump_gvec(self,filename,topology=None,cutoff=2.4):

        """
        Calculate relative position of pair of nucleobases within ellipsoidal cutoff

        Parameters
        ----------
        reference : string
            Filename of structure, any format accepted by MDtraj can be used.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        cutoff :  float, optional
            Cutoff for eRMSD calculation.
            This cutoff value roughly correspond to considering pair of bases whose distance is within an ellipsoidal cutoff with axis x=y=2.4*5 = 12 Angstrom and z=2.4*3=7.2 Angstrom. Larger values of cutoff can be useful when analyzing unstructured/flexible molecules.
        Returns
        -------
        gmat :
            Numpy array with dimension (m,n,n,4). *m* is the number of structures in target, *n* is the number of nucleotides. As an example, the position of base 10 in the reference system of base 9 in the fourth frame is given by v = rmat[3,8,9], where v is a 4-dimensional vector
        seq :
            List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX


        """

        if(topology==None):
            traj = mdtraj.load(filename)
        else:
            traj = mdtraj.load(filename,top=topology)

        warn = "# Loading %s \n" % filename
        sys.stderr.write(warn)
        return self.rna_dump_gvec_traj(traj,cutoff=cutoff)

    def rna_dump_gvec_traj(self,traj,cutoff=2.4):

        top = traj.topology
        nn = nucleic.Nucleic(top)
        gvecs = []
        for i in range(traj.n_frames):
            coords_lcs = traj.xyz[i,nn.indeces_lcs]
            gvecs.append(ff.calc_gmat(coords_lcs,cutoff))
        return np.asarray(gvecs), nn.rna_seq

    #################################################

    def rna_rmsd(self,reference,target,topology=None,out=None,heavy_atom=False):

        """
        Calculate rmsd after optimal alignment between reference and target structures. Superposition and RMSD calculations are performed using all heavy atoms.
        If the sequence of reference and target is different, only backbone/sugar heavy atoms are used.

        Parameters
        ----------
        reference : string
            Filename of reference structure, any format accepted by MDtraj can be used.
        target : string
            Filename of target structure. If a trajectory is provided, a topology file must be specified.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        out :  string, optional
            If a string is specified, superimposed PDB structures are written to disk with the specified prefix.
        heavy_atom :   bool, optional
            If True, all heavy atoms are used for superposition. Default is False

        Returns
        -------
        array :
            RMSD distance (in nm) numpy array with dimension *m*,  the number of structures in target.

        """

        ref = mdtraj.load(reference)
        warn =  "# Loaded reference %s \n" % reference

        if(topology==None):
            traj = mdtraj.load(target)
        else:
            traj = mdtraj.load(target,top=topology)
        warn += "# Loaded target %s \n" % target

        return self.ran_rmsd_traj(ref,traj,out=out,heavy_atom=heavy_atom)


    def rna_rmsd_traj(self,reference,traj,out=None,heavy_atom=False):

        top_traj = traj.topology
        # initialize nucleic class
        nn_traj = nucleic.Nucleic(top_traj)

        top_ref = reference.topology
        # initialize nucleic class
        nn_ref = nucleic.Nucleic(top_ref)

        assert(len(nn_traj.ok_residues)==len(nn_ref.ok_residues))
        # check that sequence is identical when using heavy atoms
        if(nn_traj.rna_seq_id!=nn_ref.rna_seq_id and heavy_atom==True):
            sys.stderr.write("# Sequences are not identical, cannot superimpose using all heavy atoms. ")
            sys.exit(1)

        # loop over residues and find common heavy atoms
        idx_ref = []
        idx_target = []

        for ii in range(len(nn_ref.ok_residues)):

            res1 = nn_ref.ok_residues[ii]
            res2 = nn_traj.ok_residues[ii]

            resname1 = nn_ref.rna_seq_id[ii]
            resname2 = nn_traj.rna_seq_id[ii]

            # if heavy_atom is true, use all atoms
            if(heavy_atom):

                name2 = [at.name for at in res2.atoms if  at.name in definitions.nt_atoms[resname2]]
                for at in res1.atoms:
                    if at.name in definitions.nt_atoms[resname1]:
                        if(at.name in name2):
                            idx_ref.append(at.index)
                            idx_target.append(((res2.atom(at.name)).index))
            # else, use bb only
            else:
                name2 = [at.name for at in res2.atoms if  at.name in definitions.bb_atoms]
                for at in res1.atoms:
                    if at.name in definitions.bb_atoms:
                        if(at.name in name2):
                            idx_ref.append(at.index)
                            idx_target.append(((res2.atom(at.name)).index))
        print("# found ",len(idx_ref), "atoms in common")

        if(len(idx_ref)<3):
            warn =  "# Only  %d atoms in common. abort.\n" % len(idx_ref)
            sys.stderr.write(warn)
            sys.exit(1)

        traj.superpose(reference,atom_indices=idx_target, ref_atom_indices=idx_ref)
        if(out!=None): traj.save(out)

        rmsd = np.sqrt(3*np.mean((traj.xyz[:, idx_target, :] - reference.xyz[0,idx_ref, :])**2, axis=(1,2)))
        return self.rna_rmsd

    ########################################################

    def rna_backbone_angles(self,filename,topology=None,residues=None,angles=None):

        """
        Calculate backbone ([alpha,beta,gamma,delta,espilon,zeta]) and glycosydic (chi) torsion angles.

        Parameters
        ----------
        reference : string
            Filename of structure, any format accepted by MDtraj can be used.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        residues :  list, optional
            If a list of residues is specified, only the selected residues will be calculated. Otherwise, the calculation is performed for all residues.
            The residue naming convention is RESNAME_RESNUMBER_CHAININDEX
        angles : list, optional
            If a list of angles is specified, only the selected angles will be calculated.
            Otherwise, the calculation is performed for all torsion angles.
        Returns
        -------
        array :
            Torsion angles in radians. A Numpy array with dimension (m,n,q) is returned. *m* is the number of structures in target, *n* is the number of residues, and q is the number of requested angles (7 by default).
        seq :
            List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX

        """

        if(topology==None):
            traj = mdtraj.load(filename)
        else:
            traj = mdtraj.load(filename,top=topology)
        warn = "# Loading %s \n" % filename
        sys.stderr.write(warn)
        return self.rna_backbone_angles_traj(traj,residues=residues,angles=angles)

    def rna_backbone_angles_traj(self,traj,residues=None,angles=None):

        top = traj.topology
        # initialize nucleic class
        nn = nucleic.Nucleic(top)
        all_idx,rr =  nn.get_bb_torsion_idx(residues)

        if(angles==None):
            idx_angles = np.arange(all_idx.shape[1])
        else:

            idx_angles = []
            for i in range(len(angles)):
                if(angles[i] in definitions.bb_angles):
                    idx_angles.append(definitions.bb_angles.index(angles[i]))
                else:
                    msg = "# Fatal error. requested angle \"%s\" not available.\n" % angles[i]
                    msg += "# Choose from: %s \n" % definitions.bb_angles
                    sys.stderr.write(msg)
                    sys.exit(1)


        idxs = (all_idx[:,idx_angles,:]).reshape(-1,4)
        missing = np.where(np.sum(idxs,axis=1)==0)

        torsions = mdtraj.compute_dihedrals(traj,idxs,opt=True)

        # set to NaN where atoms are missing
        torsions[:,np.where(np.sum(idxs,axis=1)==0)[0]] = np.nan

        torsions = torsions.reshape((traj.n_frames,all_idx.shape[0],len(idx_angles)))

        return torsions, rr
    ########################################################

    def rna_sugar_angles(self,filename,topology=None,residues=None,angles=None):

        """
        Calculate sugar [nu1,nu2,nu3,nu4,nu5] torsion angles.

        Parameters
        ----------
        reference : string
            Filename of structure, any format accepted by MDtraj can be used.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        residues :  list, optional
            If a list of residues is specified, only the selected residues will be calculated. Otherwise, the calculation is performed for all residues.
            The residue naming convention is RESNAME_RESNUMBER_CHAININDEX
        angles : list, optional
            If a list of angles is specified, only the selected angles will be calculated.
            Otherwise, the calculation is performed for all torsion angles.

        Returns
        -------
        array :
            Torsion angles in radians. A Numpy array with dimension (m,n,q) is returned. *m* is the number of structures in target, *n* is the number of residues, and q is the number of requested angles (5 by default).
        seq :
            List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX

        """

        if(topology==None):
            traj = mdtraj.load(filename)
        else:
            traj = mdtraj.load(filename,top=topology)
        warn = "# Loading %s \n" % filename
        sys.stderr.write(warn)
        return self.rna_sugar_angles_traj(traj,residues=residues,angles=angles)

    def rna_sugar_angles_traj(self,traj,residues=None,angles=None):

        top = traj.topology
        # initialize nucleic class
        nn = nucleic.Nucleic(top)
        all_idx,rr =  nn.get_sugar_torsion_idx(residues)
        if(angles==None):
            idx_angles = np.arange(all_idx.shape[1])
        else:
            # find indeces corresponding to angles
            idx_angles = []
            for i in range(len(angles)):
                if(angles[i] in definitions.sugar_angles):
                    idx_angles.append(definitions.sugar_angles.index(angles[i]))
                else:
                    msg = "# Fatal error. requested angle \"%s\" not available.\n" % angles[i]
                    msg += "# Choose from: %s \n" % (definitions.sugar_angles)
                    sys.stderr.write(msg)
                    sys.exit(1)

        idxs = (all_idx[:,idx_angles,:]).reshape(-1,4)
        missing = np.where(np.sum(idxs,axis=1)==0)

        torsions = mdtraj.compute_dihedrals(traj,idxs,opt=True)
        # set to NaN where atoms are missing
        torsions[:,missing[0]] = np.nan
        torsions = torsions.reshape((traj.n_frames,all_idx.shape[0],len(idx_angles)))

        return torsions, rr

    #############################################################

    def rna_pucker_angles(self,filename,topology=None,residues=None,altona=False):

        """
        Calculate sugar pucker pseudorotation  torsion angles: phase and amplitude

        Parameters
        ----------
        reference : string
            Filename of structure, any format accepted by MDtraj can be used.
        topology : string, optional
            Topology filename. Must be specified if target is a trajectory.
        residues :  list, optional
            If a list of residues is specified, only the selected residues will be calculated. Otherwise, the calculation is performed for all residues.
            The residue naming convention is RESNAME_RESNUMBER_CHAININDEX
        Returns
        -------
        array :
            Phase and amplitude. A Numpy array with dimension (m,n,2) is returned. *m* is the number of structures in target, *n* is the number of residues.
        seq :
            List of residue names. Each residue is identified with the string RESNAME_RESNUMBER_CHAININDEX

        """

        if(topology==None):
            traj = mdtraj.load(filename)
        else:
            traj = mdtraj.load(filename,top=topology)
        warn = "# Loading %s \n" % filename
        sys.stderr.write(warn)
        if(altona):
            return self.rna_pucker_altona_traj(traj,residues=residues)
        else:
            return self.rna_pucker_rao_traj(traj,residues=residues)

    def rna_pucker_altona_traj(self,traj,residues=None):

        torsions,rr = self.rna_sugar_angles_traj(traj,residues=residues)
        x1 = torsions[:,:,4] +  torsions[:,:,1] -  torsions[:,:,3] -   torsions[:,:,0]
        x2 = 3.0776835*torsions[:,:,2]
        phase = np.arctan2(x1,x2)
        phase[np.where(phase<0.0)] += 2.0*np.pi
        tm = torsions[:,:,2]/np.cos(phase)
        angles = np.dstack((phase,tm))
        return angles, rr

    def rna_pucker_rao_traj(self,traj,residues=None):

        torsions,rr = self.rna_sugar_angles_traj(traj,residues=residues)

        period = 4.*np.pi/5
        A = (2./5.)*(torsions[:,:,0]+np.cos(period)*torsions[:,:,1] + np.cos(2.*period)*torsions[:,:,2] + \
                    np.cos(3.*period)*torsions[:,:,3] + np.cos(4.*period)*torsions[:,:,4])
        B = -(2./5.)*(np.sin(period)*torsions[:,:,1] + np.sin(2.*period)*torsions[:,:,2] + \
                    np.sin(3.*period)*torsions[:,:,3] + np.sin(4.*period)*torsions[:,:,4])

        phase = np.arctan2(B,A) - 0.5*period
        phase[np.where(phase<0.0)] += 2.0*np.pi
        tm = np.sqrt(A*A + B*B)
        angles = np.dstack((phase,tm))
        return angles, rr
#######################################################################################################################
    def collect_features(self,filenames, results_folder):

        for pdbfile in filenames:
            pdbname = os.path.basename(pdbfile)[:-4]

            if not os.path.exists(results_folder):
                os.makedirs(results_folder)

            tmpdir = './tmp'
            if not os.path.exists(tmpdir):
                os.makedirs(tmpdir)

            source_file = pdbfile
            if pdbfile.endswith('.PDB'):
                destination_file = './tmp/'+os.path.basename(pdbfile)[:-4]  + '.pdb'
                shutil.copy(source_file, destination_file)
                source_file = destination_file

            ### generate gvec and rvec
            gvec,seq = self.rna_dump_gvec(source_file)  # 1, L, L, 4
            rvec,seq = self.rna_dump_rvec(source_file)  # 1, L, L, 3

            ### generate backbone_angles
            angles,res = self.rna_backbone_angles(source_file)
            # print angles
            header = "#_Residue " + "".join(["%10s " % ('bb_'+aa) for aa in definitions.bb_angles])
            #print(header)
            for j in range(angles.shape[1]):
                stri = "%10s" % res[j]
                for k in range(angles.shape[2]):
                    stri += "%10.3f " % angles[0,j,k]
                #print(stri)
                header += "\n"+stri
            # Use StringIO to turn the string into a file-like object
            data = io.StringIO(header)
            backbone_angles_df = pd.read_csv(data, delimiter='\s+')
            backbone_angles_df


            ### generate pucker_angles
            angles,res = self.rna_pucker_angles(source_file)
            # print angles
            header = "#_Residue " + "".join(["%10s " % aa for aa in ['pucker_Phase', 'pucker_amplitude']])
            #print(header)
            for j in range(angles.shape[1]):
                stri = "%10s" % res[j]
                for k in range(angles.shape[2]):
                    stri += "%10.3f " % angles[0,j,k]
                #print(stri)
                header += "\n"+stri
            # Use StringIO to turn the string into a file-like object
            data = io.StringIO(header)
            pucker_angles_df = pd.read_csv(data, delimiter='\s+')
            pucker_angles_df


            ### generate sugar_angles
            angles,res = self.rna_sugar_angles(source_file)
            # print angles
            header = "#_Residue " + "".join(["%10s " % aa for aa in ['sugar_nu1','sugar_nu2','sugar_nu3','sugar_nu4','sugar_nu5']])
            #print(header)
            for j in range(angles.shape[1]):
                stri = "%10s" % res[j]
                for k in range(angles.shape[2]):
                    stri += "%10.3f " % angles[0,j,k]
                #print(stri)
                header += "\n"+stri
            # Use StringIO to turn the string into a file-like object
            data = io.StringIO(header)
            sugar_angles_df = pd.read_csv(data, delimiter='\s+')
            sugar_angles_df

            merged_df = pd.merge(backbone_angles_df, pucker_angles_df, on='#_Residue')
            merged_df = pd.merge(merged_df, sugar_angles_df, on='#_Residue')

            results = {}
            results['motifname'] = pdbname
            results['motifseq'] = seq
            results['angle_features'] = merged_df
            results['rvec_features'] = rvec
            results['gvec_features'] = gvec


            filename = results_folder+'/'+pdbname+'.pkl'

            # Open a file for writing in binary mode
            with open(filename, 'wb') as file:
                # Dump the dictionary into the file
                pickle.dump(results, file)

            print(f"Dictionary has been saved to {filename}")

            # clean file
            checkfile = './tmp/'+os.path.basename(pdbfile)[:-4]  + '.pdb'
            if os.path.exists(checkfile):
                os.remove(checkfile)

    def get_angle_statistics_table(self, filenames, labels, feature_path='/lab/hou/vchaudhari/molgens/Cosmos_feat'):
        total_data = []

        # Define calculate_angle_statistics function outside the loop
        def calculate_angle_statistics(torsion_angles):
            mean_angles = np.mean(torsion_angles, axis=0)
            median_angles = np.median(torsion_angles, axis=0)
            std_angles = np.std(torsion_angles, axis=0)
            range_angles = np.ptp(torsion_angles, axis=0)  # peak-to-peak range
            skewness_angles = skew(torsion_angles, axis=0)
            kurtosis_angles = kurtosis(torsion_angles, axis=0)
            return (mean_angles, median_angles, std_angles, range_angles, skewness_angles, kurtosis_angles)

        for pdbfile in filenames:
            for label in labels:
                feature_file = os.path.join(feature_path, os.path.basename(pdbfile)[:-4] + '.pkl')

                # Load the dictionary back from the pickle file
                with open(feature_file, 'rb') as file:
                    pdb_features = pickle.load(file)

                pdb_features_impute = pdb_features['angle_features'].fillna(0)
                torsion_angles = pdb_features_impute.drop('#_Residue', axis=1).to_numpy()

                pdb_name = pdb_features['motifname']
                pdb_seq = pdb_features['motifseq']
                sequence = ''.join([item[0] for item in pdb_features['motifseq']])

                statistics = calculate_angle_statistics(torsion_angles)
                mean_angles, median_angles, std_angles, range_angles, skewness_angles, kurtosis_angles = statistics

                # Create dataframes for each statistical measure
                mean_angles_pd = pd.DataFrame([mean_angles], columns=[i+'_mean' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                                                                                        'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                                                                                        'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])
                mean_angles_pd = pd.DataFrame([mean_angles],columns = [ i+'_mean' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                median_angles_pd = pd.DataFrame([median_angles],columns = [ i+'_median' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                std_angles_pd = pd.DataFrame([std_angles],columns = [ i+'_std' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                range_angles_pd = pd.DataFrame([range_angles],columns = [ i+'_range' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                skewness_angles_pd = pd.DataFrame([skewness_angles],columns = [ i+'_skewness' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                kurtosis_angles_pd = pd.DataFrame([kurtosis_angles],columns = [ i+'_kurtosis' for i in ['bb_alpha', 'bb_beta', 'bb_gamma', 'bb_delta', 'bb_eps',
                    'bb_zeta', 'bb_chi', 'pucker_Phase', 'pucker_amplitude', 'sugar_nu1',
                    'sugar_nu2', 'sugar_nu3', 'sugar_nu4', 'sugar_nu5']])

                # Combine all dataframes into one
                combined_df = pd.concat([mean_angles_pd, median_angles_pd, std_angles_pd, range_angles_pd, skewness_angles_pd, kurtosis_angles_pd], axis=1)

                # Add label and sequence information
                combined_df['Label'] = label
                combined_df.insert(0, 'Motifseq', [sequence])
                combined_df.insert(0, 'Motifname', [pdb_name])

                # Append the combined dataframe to total_data
                total_data.append(combined_df)

        #combined_df = pd.concat(total_data, ignore_index=True)
        #combined_df.to_csv(labels+'.csv', index=False)
        return total_data
#######################################################################################################################
    def check_pdb_data(filenames, generated_pdb_data):
        def extract_pdb_names(filenames):
            pdb_names = []
            for file_path in filenames:
                parts = file_path.split('/')
                file_name = parts[-1]
                pdb_name = file_name.split('.')[0]
                pdb_names.append(pdb_name)
            return pdb_names

        pdb_names = extract_pdb_names(filenames)

        data = pd.read_csv(generated_pdb_data)
        motif_list = data["Motifname"].tolist()

        missing_columns_dict = {}

        for pdb in pdb_names:
            if pdb not in motif_list:
                missing_columns_dict[pdb] = []
            elif pdb in motif_list:
                pdb_data = data[data['Motifname'] == pdb]
                if pdb_data.isnull().values.any():
                    columns_with_null = pdb_data.columns[pdb_data.isnull().any()].tolist()
                    missing_columns_dict[pdb] = columns_with_null

        return missing_columns_dict
    
    def feature_update(self,filenames, generated_pdb_data, save_path):
        def extract_pdb_names(filenames):
            pdb_names = []
            for file_path in filenames:
                parts = file_path.split('/')
                file_name = parts[-1]
                pdb_name = file_name.split('.')[0]
                pdb_names.append(pdb_name)
            return pdb_names

        missing_column_dict = self.check_pdb_data(filenames, generated_pdb_data)

        matched_pdbs = [pdb for pdb in extract_pdb_names(filenames) if pdb in missing_column_dict]

        self.collect_features(matched_pdbs, '/lab/hou/vchaudhari/molgens/Cosmos_feat')

        new_data = self.get_angle_statistics_table(filenames, labels, feature_path='/lab/hou/vchaudhari/molgens/Cosmos_feat')

        data = pd.read_csv(generated_pdb_data)

        for pdb, missing_columns in missing_column_dict.items():
            if pdb in new_data and pdb in data['Motifname'].tolist():
                pdb_data = data[data['Motifname'] == pdb]
                for col in missing_columns:
                    if col in new_data.columns:
                        new_value = new_data.loc[pdb, col]
                        data.loc[data['Motifname'] == pdb, col] = new_value

        data.to_csv(save_path, index=False)

        return matched_pdbs, new_data

####################################################################################################################### 
js_script = """
var x = document.nglview.stage.getRepresentationsByName("selection");
var stickRepr = x['list'][0];
var rules = JSON.stringify(stickRepr.repr.selection.selection.rules);
console.log("Hello");
console.log(rules);
var command = "selection = '" + rules + "'";
IPython.notebook.kernel.execute(command);
IPython.notebook.kernel.execute("selection = json.loads(selection)");
"""

def get_selstring(selection):
    chains = []
    residues = []
    for elem in selection:
        for rule in elem['rules']:
            for key, value in rule.items():
                if key == "chainname": chains.append(value)
                if key == "resno": residues.append(value)

    sel_string = ""
    for residue in residues:
        sel_string+= "residue=="+str(residue) + " or "
    sel_string = sel_string[:-len(" or ")]
    return sel_string

def select_residues_nglview(top_loc):
    nglwidget = nglview.show_structure_file(top_loc)
    nglwidget.clear_representations()
    nglwidget.add_cartoon(colorScheme="residueindex")
    nglwidget.add_ball_and_stick(color="red", selection="0", name="selection")
    nglwidget.gui_style = 'ngl'
    nglwidget._execute_js_code("document.nglview = this;")
    nglwidget._execute_js_code(
    """
        var stickSel = ""
        var x = this.stage.getRepresentationsByName("selection")
        var stickRepr = x['list'][0]

        var f1 = function (pickingProxy) {
        if (stickRepr.repr.selection.selection.rules[0] && stickRepr.repr.selection.selection.rules[0].keyword == 20) {
         stickSel = ""
        }
        if (pickingProxy && pickingProxy.ctrlKey && (pickingProxy.atom || pickingProxy.bond)){
            console.log("CTRL")
            console.log(pickingProxy)
            var atom = pickingProxy.atom || pickingProxy.closestBondAtom;
            var residue = atom.residue
            var curSel = String(residue.resno)+':'+residue.chainname+' or '

            console.log(curSel)

            var isSel = stickSel.search(curSel)
            if (isSel == -1) {
                // Append to selection
                stickSel += curSel
            }
            console.log(stickSel);
            stickRepr.setSelection(stickSel)

        }

        if (pickingProxy && pickingProxy.shiftKey && (pickingProxy.atom || pickingProxy.bond)){
            console.log("SHIFT")
            console.log(pickingProxy)
            var atom = pickingProxy.atom || pickingProxy.closestBondAtom;
            var residue = atom.residue
            var curSel = String(residue.resno)+':'+residue.chainname+' or '
            console.log(curSel)
            console.log(stickSel)
            var isSel = stickSel.search(curSel)
            if (isSel != -1)  {
                // Remove from selection
                stickSel = stickSel.replace(curSel, "")
            }
            console.log(stickSel);
            if(stickSel.length == 0) {
                stickRepr.setSelection("none")
            }
            else{
            stickRepr.setSelection(stickSel)
            }
        }

        }
        this.stage.signals.hovered.add(f1)
    """
    )
    return nglwidget
