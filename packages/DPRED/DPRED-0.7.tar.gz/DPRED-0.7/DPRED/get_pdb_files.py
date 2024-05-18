from Bio.PDB import PDBList, PDBParser, PDBIO, Select
import logging
import os

from . import remove

logging.getLogger("Bio").setLevel(logging.ERROR)

class ChainSelector(Select):
    '''A chain selector for Bio.PDB'''
    def __init__(self, target_chain: str) -> None:
        self.target_chain = target_chain
    
    def accept_chain(self, chain: str) -> bool:
        return chain.get_id() == self.target_chain

class PDBChainDownloader:
    '''A tool for downloading PDB atoms belonging to a certain chain'''
    def __init__(self, pdbobj) -> None:
        self.pdbids, self.outdir = pdbobj.get_ids().splitlines(), 'input_pdb/'

    def _rename_file(self, chain: str, i: int) -> None:
        '''Turns the .env extension into .pdb and includes the chain'''
        filename = os.listdir(self.outdir)[i]
        if filename.endswith(".ent"):
            new_filename = filename.split(".")[0] + "_" + chain + ".pdb"
            os.rename(os.path.join(self.outdir, filename), os.path.join(self.outdir, new_filename))

    def _filter_atoms_by_chain(self, pdb_file: str, pdb_id: str, target_chain: str) -> None:
        '''Filters the PDB files using the chain selector'''
        parser = PDBParser(QUIET=True)
        structure = parser.get_structure(pdb_id, pdb_file)
        io = PDBIO()
        io.set_structure(structure)
        io.save(pdb_file, select=ChainSelector(target_chain))
        #parser, io = None, None # closing the objects
        
    def download_filtered_pdbs(self) -> None:
        '''Downloads the chain-filtered PDB files'''
        try:
            pdblist = PDBList(verbose=False)
            i = 0
            for pdbid in self.pdbids:
                chain = pdbid[4]
                pdblist.retrieve_pdb_file(pdbid[:4], pdir=self.outdir, file_format='pdb', overwrite=True) 
                self._rename_file(chain, i)    
                pdbfile = os.path.join(self.outdir, f"pdb{pdbid[:4]}_{chain}.pdb")
                self._filter_atoms_by_chain(pdbfile, pdbid[:4], chain)
                i += 1
            remove.Remove('obsolete').remove()
        except Exception as e:
            remove.Remove('msa').remove()
            remove.Remove('input_pdb').remove()
            remove.Remove('obsolete').remove()
            raise RuntimeError(e)

if __name__ == '__main__':
    pdb = PDBChainDownloader('PF00014')
    pdb.download_filtered_pdbs()