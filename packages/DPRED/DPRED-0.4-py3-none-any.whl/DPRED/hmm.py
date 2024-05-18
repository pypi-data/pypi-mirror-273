import os
import subprocess
import time

import msa
import remove

class HMM:
    def __init__(self, pdbobj: object, pfam: str, mtm: bool, pdb: bool) -> None:
        self.msa = 'msa'
        if not os.path.exists(self.msa): msa.MSA(pdbobj, pfam, mtm, pdb).write_msa()
        
    def hmm(self, name: str, msa: bool) -> None:
        start = time.time()
        print('Generating the HMM...')
        subprocess.run(["hmmbuild", f"{name}.hmm", self.msa], stdout=subprocess.DEVNULL)
        lap = time.time()-start
        h, rem = divmod(lap, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        if msa is False: remove.Remove(self.msa).remove()