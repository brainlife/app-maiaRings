#
# This file is the main python script for this app
#
# you can run this script(main) without any parameter to test how this App will run outside brainlife
# you will need to copy config.json.brainlife-sample to config.json before running `main` as `main`
# will read all parameters from config.json
#
# Author: Dan Bullock


# set up environment
#this code ensures that we can acesess the OCT_scripts repo
#Repo is located here:  https://github.com/DanNBullock/OCT_scripts
import subprocess
import os
import json
#get top directory path of the current git repository, under the presumption that 
#the notebook was launched from within the repo directory
gitRepoPath=subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('ascii').strip()

#establish path to the OCT_scripts
OCT_scriptsDirPath=os.path.join(gitRepoPath,'OCT_scripts')   

#change to the wma_tools path, load the function set, then change back to the top directory
os.chdir(OCT_scriptsDirPath)
import groupMAIA
os.chdir(gitRepoPath)

# load inputs from config.json
with open('config.json') as config_json:
	config = json.load(config_json)

#extrct microperimetry file path from config.json    
currentFile = str(config['microperimetry'])


import pandas as pd
import matplotlib.pyplot as plt

#make the output directory
if not os.path.exists('output'):
    os.makedirs('output')

#do the polar coordinate table conversion
convertedMAIAtable=loadAndConvertMAIA_polar(currentFile)
#compute the ring means and save to csv
ringMeanTable=ringMeanDev(convertedMAIAtable)
ringMeanTable.to_csv('output/ringMeanTable.csv')
#do the radar plot and save to file
radarOut=MAIAradarPlot(convertedMAIAtable)
radarOut.savefig('output/radarPlot.png')
#do the scatter plot and save to file
scatterOut=MAIAscatterPlot(convertedMAIAtable)
scatterOut.savefig('output/scatterPlot.png')