# Import required functions
from setuptools import setup, find_packages
# from bacGWAStatLearn import  _program
_program = "bacGWAStatLearn"
# Call setup function
setup(
    author="Paul Phillips",
    description="A machine learning approach for conducting genome wide association studies (GWAS) on bacteria",
    name="bacGWAStatLearn",
    packages=find_packages(include=["bacGWAStatLearn", "bacGWAStatLearn.*", "bacGWAStatLearn.Snakefile"]),
    version="0.1.3",
    package_data={'bacGWAStatLearn': ['Snakefile']},
    install_requires=['pandas', 'scipy', 'statsmodels','numpy==1.23.5', 'scikit-learn', 'xgboost', 'matplotlib', 'joblib', 'snakemake', 'Boruta', 'shap', 'seaborn','plotnine'],
    # py_modules=['Snakefile', 'ClassIndexing.py'],
    url="https://github.com/PaulDanPhillips/bacGWAStatLearn",
    license="MIT",
    entry_points="""
    [console_scripts]
    {program} = bacGWAStatLearn.main:main
    """.format(program=_program),
    include_package_data=True,
)