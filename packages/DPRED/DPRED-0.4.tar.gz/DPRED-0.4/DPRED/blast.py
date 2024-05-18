import subprocess
import os

class Blast:
    def __init__(self, pdbfasta: str, upfasta: str) -> None:
        self.dbdir = 'dbdir'    
        self.pdbfasta, self.upfasta = pdbfasta, upfasta
        self.dbpath, self.querypath = os.path.join(self.dbdir, 'db.blast'), os.path.join(self.dbdir, 'query.blast') 
        
    def _makeblastdb(self) -> None:
        '''Makes a blast database out of a .fasta file'''
        try: 
            if not os.path.exists(self.dbdir): os.makedirs(self.dbdir)
            with open(self.dbpath, 'w') as f: f.write(self.pdbfasta) 
            subprocess.run(["makeblastdb", "-in", self.dbpath, "-dbtype", "prot"], stdout=subprocess.DEVNULL)
        except Exception as e: raise e

    def blastp(self) -> None:
        '''Runs a blastp search against a blast database'''
        try:
            if not os.path.exists(self.dbdir): self._makeblastdb()
            with open(self.querypath, 'w') as f: f.write(self.upfasta)
            return subprocess.run(["blastp", "-query", self.querypath, "-db", self.dbpath, "-outfmt", "7"], capture_output=True, text=True).stdout
        except Exception as e: raise e