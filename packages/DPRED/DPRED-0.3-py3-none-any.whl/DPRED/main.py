import argparse
import time

import get_pdb_data as pdbdata
import hmm
import validation

def PDBobj(pfam: str, l: list, res: int, mut: int, iden: int): return pdbdata.GetPDB(pfam, l, res, mut, iden)

def DPRED(pdbobj: object, pfam: str, k: int, l: int, bid: int, n: str, mtm: bool, msa: bool, pdb: bool, chunks: bool, sets: bool, db: bool) -> None:
    start = time.time()
    hmm.HMM(pdbobj, pfam, mtm, pdb).hmm(n, msa) # generates a HMM model for domain prediction
    validation.KCrossVal(pdbobj, pfam, k, db).validation(bid, l, chunks, sets, n) # validate the model through a K-fold CV
    print('Finished!')
    lap = time.time()-start
    h, rem = divmod(lap, 3600)
    m, s = divmod(rem, 60)
    print(f'Total execution time = {int(round(h))}:{int(round(m))}:{int(round(s))}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DPRED', description='Domain prediction and validation using HMM.')
    
    # mandatory
    parser.add_argument('--pfam', type=str, required=True, help='Pfam ID for domain prediction')
    parser.add_argument('-k', type=int, required=True, help='Number of folds for cross-validation')
    parser.add_argument('-l', type=str, required=True, help='Domain length range (upper incl.)')
    
    # domain name
    parser.add_argument('-n', type=str, help='Domain name (default is "domain")', default='domain')
    
    # pdb parameters
    parser.add_argument('--res', type=int, help="Max pdb structure's resolution (default = 3)", default=3)
    parser.add_argument('--mut', type=int, help='Mutation count per pdb structure (default = 0)', default=0)
    parser.add_argument('--iden', type=int, help='% sequence identity used for grouping pdb entities (default = 50)', default=50)
    
    # blast parameters
    parser.add_argument('--bid', type=int, help='% sequence identity used for positives blast selection (default = 95)', default=95)
    
    # folders and files maintanance
    parser.add_argument('--mtm', action='store_true', help='Maintain msa folder', default=False)
    parser.add_argument('--msa', action='store_true', help='Maintain msa file', default=False)
    parser.add_argument('--pdb', action='store_true', help='Maintain pdb structures folder', default=False)
    parser.add_argument('--chunks', action='store_true', help='Maintain chunks folder', default=False)
    parser.add_argument('--sets',action='store_true', help='Maintain sets folder', default=False)
    parser.add_argument('--db', action='store_true', help='Maintain blast db folder', default=False)
    
    args = parser.parse_args()
    if args.pfam is None or args.k is None or args.l is None: parser.error("USAGE: --pfam <PFAM> -k <k-fold> -l <A:B domain length range")
    
    l = args.l.split(':')
    pdbobj = PDBobj(args.pfam, l, args.res, args.mut, args.iden)
    DPRED(pdbobj, args.pfam, args.k, int(l[0]), args.bid, args.n, args.mtm, args.msa, args.pdb, args.chunks, args.sets, args.db)