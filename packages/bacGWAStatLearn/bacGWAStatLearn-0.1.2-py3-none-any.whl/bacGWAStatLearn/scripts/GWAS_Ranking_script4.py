import pandas as pd
from bacGWAStatLearn.TreeTune.ClassTuning import Tuning
from bacGWAStatLearn.FeatureSelect.ClassFeatureSelection import FeatSelection
import os
import pickle
from joblib import Parallel, delayed
from optparse import OptionParser

usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--predictor",  dest="lsbsr_boruta", help="lsbsr matrix [REQUIRED]", type="string")
parser.add_option("-r", "--response",  dest="abx", help="response vector [REQUIRED]", type="string")
parser.add_option("-s", "--simulation",  dest="sim", help="simulation identifier [REQUIRED]", type="string")
parser.add_option("-n", "--NumIter",  dest="NumIter", default=100, help="Number of times to iterate Permutation or Feature Importance", type="int")
parser.add_option("-k", "--PermImpInternal",  dest="InterIter", default=10, help="Number of internal Permutation Importances to conduct", type="int")
parser.add_option("-t", "--PermImpscore",  dest="score", default='balanced_accuracy', help="scoring function for permutation importance", type="string")
parser.add_option("-o", "--output", dest="outdir", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")
parser.add_option("-m", "--model", dest="model", default='RF', help="model to optimize (RF or XGB) [REQUIRED]", type="string")
parser.add_option("-c", "--class", dest="resp", default='binary', help="if the response is binary or multiclass [REQUIRED]", type="string")

options, args = parser.parse_args()

parentDIR = os.getcwd()
numCores = -1
print(os.cpu_count(), numCores)
TuneObj = Tuning()
X, Y, n_splits, class_weight =TuneObj.XY_index(X=options.lsbsr_boruta, Y=options.abx, BacGWASim=False)
print((X.shape))
print((Y.shape))
print((Y.value_counts()))

# %% Read optimized model parameters
with open('TuningOUT_'+ str(options.model)+'/RFOptimal_Tuning2_'+options.sim+'.pickle', 'rb') as filehandle:
    RFoptimal=pickle.load(filehandle)


if not os.path.isdir('FinalFeatures_'+str(options.model)):
    os.makedirs("FinalFeatures_"+str(options.model))
os.chdir("FinalFeatures_"+str(options.model))
NewNASPobj = FeatSelection(repeat=options.NumIter)

FI = Parallel(n_jobs=numCores,  backend="loky", prefer='processes' )(delayed(NewNASPobj.FeatImp)(RFoptimal, X, Y, rand=i,) for i in range(NewNASPobj.repeat))
FI = pd.concat(FI)
FI=FI.reset_index().groupby('index', as_index=True).mean().sort_values(0,ascending=False)
FI.index.rename('variant', inplace=True)
FI.to_csv('FeatureImportance_Ranked_'+options.sim+'.out', sep='\t')

# SHAPdata =  Parallel(n_jobs=numCores, backend='loky', prefer='processes' )(delayed(NewNASPobj.SHAPscores)(RFoptimal, X, Y,rand=i,)for i in range(NewNASPobj.repeat))
# SHAPster = pd.concat(SHAPdata).groupby('variant', as_index=False).mean().sort_values('mean', key=abs, ascending=False).reset_index(drop=True)
# SHAPster.to_csv('SHAPster_Ranked_'+options.sim+'.out', sep='\t')


PI = Parallel(n_jobs=numCores, backend="loky", prefer='processes' )(delayed(NewNASPobj.PermImp)(RFoptimal, X, Y,options.InterIter, scorer=options.score, rand=i, ) for i in range(NewNASPobj.repeat))
PI = pd.concat(PI)
PI=PI.reset_index().groupby('index', as_index=True).mean().sort_values(0,ascending=False)
PI.index.rename('variant', inplace=True)
PI.to_csv('PermutationImportance_Ranked_'+options.sim+'.out', sep='\t')
