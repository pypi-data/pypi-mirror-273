import pandas as pd
import numpy as np
from rapidfuzz import fuzz as fz
from joblib import Parallel, delayed

class NameMatch:

    def __init__(self) -> None:
        self.miles_sheet_name = "Miles Names"
        self.icra_sheet_name = "ICRA Names"

    def parallel_fuzzy_match(self,ca, cb, idxa, idxb, metric):
        return [ca[idxa][0],cb[idxb][0],metric(ca[idxa][0],cb[idxb][0])] 

    def run(self,in_path:str, out_path:str) -> bool:
        
        milesSheet = pd.read_excel(in_path, sheet_name=self.miles_sheet_name).dropna()
        icraSheet = pd.read_excel(in_path, sheet_name=self.icra_sheet_name).dropna()
        
        metric = fz.ratio
        thresh = 40
        ca = np.array(icraSheet[["Fund Name"]])
        cb = np.array(milesSheet[["Fund Name"]])

        results = Parallel(n_jobs=-1,verbose=1)(delayed(self.parallel_fuzzy_match)(ca,cb,idx1,idx2,metric) for idx1 in range(len(ca)) for idx2 in range(len(cb)) \
                    if(metric(ca[idx1][0],cb[idx2][0]) > thresh))
        results = pd.DataFrame(results,columns = ["ICRA fund name","Miles fund name","Score"])
        idx = results.groupby(['ICRA fund name'])['Score'].transform(max) == results['Score']
        asd = results[idx]

        writer = pd.ExcelWriter(out_path, engine = 'openpyxl')
        icraSheet.to_excel(writer, sheet_name = 'ICRA')
        milesSheet.to_excel(writer, sheet_name = 'Miles')
        asd.to_excel(writer, sheet_name = 'Result')
        writer.close()        