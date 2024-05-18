import numpy as np

class Performance():
    def __init__(self, data: str) -> None:
        self.data = data
        self.tp, self.tn, self.fp, self.fn, self.tot = None, None, None, None, None
    
    def _get_data(self) -> list:
        '''Reading the information and assign for each one of the identifier the associated e-value'''
        preds = []
        for line in self.data.rstrip().splitlines():
            v = line.split()
            v[1] = float(v[1])
            v[2] = int(v[2])
            preds.append(v)
        return preds

    def get_cm(self, th: float) -> None:
        cm = np.zeros((2, 2))
        for pred in self._get_data():
            p = 0
            r = pred[2]
            if pred[1] <= th: p = 1
            cm[p][r] += 1
        self.tp = cm[1][1]
        self.tn = cm[0][0]
        self.fp = cm[0][1]
        self.fn = cm[1][0]
        self.tot = np.sum(cm)
            
    def get_accuracy(self) -> float: return float(self.tn + self.tp)/self.tot

    def get_precision(self) -> float: return self.tp/(self.tp+self.fp)
    
    def get_recall(self) -> float: return self.tp/(self.tp+self.fn)
    
    def get_fpr(self) -> float: return self.fp/(self.fp+self.tn)
    
    def get_fscore(self) -> float:
        p = self.get_precision()
        r = self.get_recall()
        return 2*p*r/(p+r)

    def get_mcc(self) -> float:
        mcc = self.tp*self.tn - self.fp*self.fn
        d = np.sqrt((self.tp+self.fn)*(self.tp+self.fp)*(self.tn+self.fp)*(self.tn+self.fn))
        return mcc/d