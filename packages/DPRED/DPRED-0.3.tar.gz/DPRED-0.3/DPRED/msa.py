import os
import subprocess
from collections import Counter
import time

import get_pdb_files as pdbfiles
import remove

class MSA:
    def __init__(self, pdbobj: object, pfam: str, mtm, pdb) -> None: 
        self.msadir = os.path.join(os.getcwd(), "mTM_result")
        self.pdbdir = os.path.join(os.getcwd(), "input_pdb")
        self.pdbobj, self.pfam, self.mtm, self.pdb = pdbobj, pfam, mtm, pdb
        self.ids = []
        
    def _download_pdb(self) -> None: 
        print('Downloading PDB structures...')
        start = time.time()
        pdbfiles.PDBChainDownloader(self.pdbobj).download_filtered_pdbs()
        lap = time.time()-start
        h, rem = divmod(lap, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
    
    def _msa(self) -> None:
        if not os.path.exists(self.pdbdir): self._download_pdb()    
        with open('pdblst', 'w') as f: f.write(self.pdbobj.get_lst())
        start = time.time()
        print('Performing multiple structural alignment...')
        subprocess.run(["./mTM-align/src/mTM-align", "-i", "pdblst"], stdout=subprocess.DEVNULL)
        lap = time.time()-start
        h, rem = divmod(lap, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        if self.pdb is False: remove.Remove(self.pdbdir).remove() # remove input_pdb
        if self.mtm is False: remove.Remove('pdblst').remove() # remove pdblst
        
    def _parse_msa(self) -> str:
        msa, i = '', 0
        if not os.path.exists(self.msadir): self._msa()
        res_file = os.path.join(self.msadir, "result.fasta")
        with open(res_file) as res:
            for line in res:
                if line[0] == '>':
                    i += 1
                    self.ids.append(line)
                    continue
                if i==1: 
                    msa += line.rstrip()
                else:
                    i -= 1
                    msa += '\n' + line.rstrip()
        if self.mtm is False: remove.Remove(self.msadir).remove() # remove mTM_result
        return msa
    
    def _find_start(self, msa: str) -> int:
        occ = {} # a dict of first-ch occurrencies
        for i, line in enumerate(msa.splitlines()):
            for ch in line:
                if ch == '-': continue
                else: occ[i] = line.index(ch)
                break
        return Counter(occ.values()).most_common()[0][0]
    
    def _find_end(self, msa: str) -> int:
        occ = {}
        for i, line in enumerate(msa.splitlines()):
            line = ''.join(reversed(line))
            for ch in line:
                if ch == '-': continue
                else: occ[i] = line.index(ch)
                break
        return len(line) - Counter(occ.values()).most_common()[0][0]
        
    def _clear_msa(self) -> str:
        msa = self._parse_msa()
        start = self._find_start(msa)
        end = self._find_end(msa)
        clean_msa = ''
        for i, line in enumerate(msa.splitlines()): clean_msa += self.ids[i] + line[int(start):int(end)] + '\n'
        return clean_msa
    
    def write_msa(self) -> None:
        with open('msa', 'w') as f: f.write(self._clear_msa())
        
if __name__ == '__main__':
    obj = MSA('PF00014')
    obj._msa()