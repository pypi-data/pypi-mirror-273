import requests

class GetUniProt:
    def __init__(self, pfam: str, choice: str) -> None:
        self.pfam, self.ch, self.dseq = pfam, choice, None
        
    def _req(self) -> requests:
        '''Sends a request to Uniprot'''
        if self.ch == 'Y': ch = ''
        else: ch = 'NOT+'
        request = f'https://rest.uniprot.org/uniprotkb/stream?compressed=false&format=fasta&query=%28{ch}%28xref%3Apfam-{self.pfam}%29+AND+%28reviewed%3Atrue%29%29'
        return requests.get(request)

    def _get_dseq(self) -> None:
        '''Generates a UniProt sequences dictionary'''
        dseq = {}
        r = self._req()
        for line in r.iter_lines():
            line = line.decode('utf-8')
            if line[0] == '>':
                id = line.split('|')[1]
                dseq[id] = ''
                continue
            dseq[id] = dseq[id] + line.rstrip()
        self.dseq = dseq
    
    def get_seqs(self, ids: list) -> str:
        idseq = ''
        if self.dseq == None: self._get_dseq()
        for id in ids: idseq += f">{id}\n{self.dseq[id]}\n"
        return idseq
        
    def get_ids(self) -> str:
        if self.dseq == None: self._get_dseq()
        return '\n'.join(self.dseq.keys())