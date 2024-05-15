# bacGWAStatLearn
* a bacterial genome wide association approach through utilizing machine learning practices.
## installation
```bash
pip install bacGWAStatLearn
```
## Use
### Downlaod example from GitHub
```bash
git clone https://github.com/PaulDanPhillips/bacGWAStatLearn.git
```
### **c**hange **d**irectory to example
```bash
cd bacGWAStatLearn/example
```
### Run the example data
```bash
bacGWAStatLearn --config Sim1.yaml --cores 4
```
## Running your own data:
### Data organization
* The data needs to be split into two files: 1 containing all of the genetic features and 2 the response phenotype ensureing that the indexes on the feature matrix align with the reponse vector.
#### Configure.yaml file:

* You will edit the Sim1.yaml file from the example directory.
1. **Predictor**
    * The absolute or relative path to your genetic feature matrix will take the place of """bacGWAStatLearn/example/BalancedArbitrayPredictor_Sim1.txt"""
2. **Response**
    * The absolute or relative path to your response phenotype vector will take the place of """bacGWAStatLearn/example/BalancedArbitrary_Response_1.txt"""
3. ***chi2Correct**
    * The user need to decie if they want to the chi2 prefilter step to be corrected via false-discovery-rate or not (only True or False)
4. **FDRchi2Thresh**
    * The user needs to decide what the FDR chi2 threshold is for removing genetic features based on this chi2 test is. 

