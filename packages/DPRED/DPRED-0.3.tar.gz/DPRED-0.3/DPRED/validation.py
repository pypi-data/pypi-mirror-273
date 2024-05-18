import subprocess
import random
import os
import time

import blast
import remove
import get_uniprot_data as updata
import performance as pf

class KCrossVal:
    
    def __init__(self, pdbobj: object, pfam: str, k: int, db: bool) -> None:
        self.k = k
        # UniProt data
        start = time.time()
        self.posobj = updata.GetUniProt(pfam, 'Y')
        self.negobj = updata.GetUniProt(pfam, 'N')
        print('Collecting the positives...')
        self.posobj._get_dseq()
        lap1 = time.time()-start
        h, rem = divmod(lap1, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        print('Collecting the negatives...')
        self.negobj._get_dseq() # 200 s
        lap2 = time.time()-lap1
        h, rem = divmod(lap2, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        self.posids = self.posobj.get_ids().splitlines()
        self.negids = self.negobj.get_ids().splitlines()
        # PDB data
        self.pdbfasta = pdbobj.get_fasta()
        # blast correction
        print('Performing a positives blast search...')
        lap3 = time.time()-lap2
        h, rem = divmod(lap3, 3600)
        m, s = divmod(rem, 60)
        self.outblast = blast.Blast(self.pdbfasta, self.posobj.get_seqs(self.posids)).blastp()
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        if db is False: remove.Remove(os.path.join(os.getcwd(), 'dbdir')).remove() # remove dbdir
        
    def _removefromdb(self, bid: int, l: int) -> None:
        '''Removes the ids from a reference .ids according to some parameters'''
        try:            
            for line in self.outblast.splitlines():
                if line[0] == '#': continue
                fields = line.split()
                if float(fields[2]) > bid and float(fields[3]) > l:
                    if fields[0] in self.posids: self.posids.remove(fields[0])
            
        except Exception as e: raise e
    
    def _chunks(self, chunks_dir: str) -> None:
        os.makedirs(chunks_dir)
        for ids, name in ((self.posids, 'pos'), (self.negids, 'neg')):
            # data ids shuffle
            random.shuffle(ids)
            # splitting into k folds
            size = len(ids)//self.k 
            folds = (ids[i*size:(i+1)*size] for i in range(self.k))
            # retrieving and saving the sequences
            for i, fold in enumerate(folds, start=1):
                path = os.path.join(chunks_dir, f'{name}{i}.txt')
                if name == 'pos':
                    with open(path, 'w') as f: f.write(self.posobj.get_seqs(fold))
                else:
                    with open(path, 'w') as f: f.write(self.negobj.get_seqs(fold))

    def _hmmsearch(self, sets_dir: str, chunks: bool, n: str) -> None:
        
        name = ('neg', 'pos')
        ref = (set(self.negids), set(self.posids))
        
        chunks_dir = os.path.join(os.getcwd(), "chunks")
        if not os.path.exists(chunks_dir): self._chunks(chunks_dir)
        
        os.makedirs(sets_dir) 
        
        for i in range(1, self.k+1):
            setfile = os.path.join(sets_dir, f'set{i}.txt')
            results = {'neg': [], 'pos': []}
            for j in range(2):
            
                hmmsearch = ["hmmsearch", "-Z", "1", "--domZ", "1", "--max", "--noali", "--tblout", "search.out", f"{n}.hmm", os.path.join(chunks_dir, f"{name[j]}{i}.txt")]
                subprocess.run(hmmsearch, check=True, capture_output=True, text=True)
                
                with open('search.out') as f:
                    for line in f:
                        if line.startswith('#'): continue
                        fields = line.split()
                        results[name[j]].append((fields[0], fields[7], str(j)))
                missing = ref[j] - {result[0] for result in results[name[j]]}
                for id in missing: results[name[j]].append((id, '10', str(j)))
                with open(setfile, 'a') as f: f.write('\n'.join(['\t'.join(el) for el in results[name[j]]])+'\n')
        
        remove.Remove(os.path.join(os.getcwd(), 'search.out')).remove() # remove search.out
        if chunks is False: remove.Remove(chunks_dir).remove() # remove chunks
            
    def validation(self, bid: int, l: int, chunks: bool, sets: bool, n: str) -> None:
        
        print(f'Performing a {self.k}-fold cross-validation...')
        start = time.time()
        self._removefromdb(bid, l)
        
        sets_dir = os.path.join(os.getcwd(), "sets")
        if not os.path.exists(sets_dir): self._hmmsearch(sets_dir, chunks, n)
        
        res = []
        for i in range(1, self.k+1):
            test = os.path.join(sets_dir, f'set{i}.txt')
            trains = [os.path.join(sets_dir, f'set{j}.txt') for j in range(1, self.k+1) if j != i]
            max_acc, max_mcc = 0, 0
            
            # finding the best ths for the training sets
            best_ths = []
            max_acc, max_mcc = 0, 0
            for train in trains:
                with open(train) as tr:
                    perf = pf.Performance(tr.read())
                    for exp in range(15):
                        th = 10**(-exp)
                        perf.get_cm(th)
                        acc = perf.get_accuracy()
                        mcc = perf.get_mcc()
                        if acc > max_acc:
                            if mcc > max_mcc:
                                max_acc, max_mcc = acc, mcc
                                best_th = th
                        else: break
                best_ths.append(best_th)
                                            
            # applying the lowest th to the test set
            with open(test) as te: best = pf.Performance(te.read())
            th = min(best_ths)
            best.get_cm(th)
            res.append((th, (best.tn, best.fp, best.fn, best.tp, best.tot, best.get_precision(), 
                             best.get_recall(), best.get_fpr(), best.get_fscore(), 
                             best.get_accuracy(), best.get_mcc())))
        
        if sets is False: remove.Remove(sets_dir).remove() # remove sets
        
        max_acc, max_mcc = 0, 0
        for el in res:
            if el[1][1] > max_acc:
                if el[1][2] > max_mcc:
                    th = el[0]
                    tn, fp, fn, tp, tot = el[1][0], el[1][1], el[1][2], el[1][3], el[1][4]
                    p, r, fpr, f = el[1][5], el[1][6], el[1][7], el[1][8]
                    acc, mcc = el[1][9], el[1][10] 
        
        lap = time.time()-start
        h, rem = divmod(lap, 3600)
        m, s = divmod(rem, 60)
        print(f'Done. Time = {int(round(h))}:{int(round(m))}:{int(round(s))}')
        
        content = f'''#########################################################
    \t\t    VALIDATION TABLE
    \nA {self.k}-fold cross-validation was performed.
    \nOptimal threshold = {th}
    \nConfusion matrix:
    TN = {tn}, FP = {fp}
    FN = {fn}, TP = {tp}
    Total = {tot}
    \nMetrics:
    Accuracy = {acc*100} %
    Precision = {p}
    Recall = {r}
    F-score = {f}
    True positive rate = {r}
    False positive rate = {fpr}
    Matthews correlation coefficient = {mcc}
    \n#########################################################
    '''
        with open(f'{n}_validation.txt', 'w') as f: f.write(content)