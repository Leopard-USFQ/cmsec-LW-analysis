#!/bin/bash

# Print a message to indicate the start of the process
echo "Starting the simulation process..."

# Run each cmsRun command sequentially and check for errors
if cmsDriver.py SimLW/Sim2/python/myHadronizer.py --mc --beamspot Realistic25ns13TeV2016Collision --eventcontent=RAWSIM --datatier=GEN-SIM --conditions 106X_mcRun2_asymptotic_v17 --step=GEN,SIM --python_filename=gensimLW.py --no_exec --number=1000 --fileout=gensimLW.root --customise Configuration/DataProcessing/Utils.addMonitoring --filein file:JJSJ_Addflighttime.lhe --filetype LHE; then
    echo "Successfully completed cmsDriver in gensim step"
else
    echo "Error in cmsDriver in gensim step"
    exit 1
fi

if cmsRun gensimLW.py > ./logs/log_gensim.log 2>&1; then
    echo "Successfully completed gensimLW.py"
else
    echo "Error in gensimLW.py"
    exit 1
fi

if cmsDriver.py step2 --mc --eventcontent=RAWSIM --datatier=GEN-SIM-DIGI-RAW --conditions 106X_mcRun2_asymptotic_v17 --step=DIGI,L1,DIGI2RAW,HLT:@relval2016 --geometry DB:Extended --era Run2_2016 --python_filename=digiHLT.py --no_exec --filein file:gensimLW.root --fileout=digiHLT.root --customise Configuration/DataProcessing/Utils.addMonitoring -n 1000; then
    echo "Successfully completed cmsDriver in HLT step"
else
    echo "Error in cmsDriver in HLT step"
    exit 1
fi

if cmsRun digiHLT.py > ./logs/log_hlt.log 2>&1; then
    echo "Successfully completed digiHLT.py"
else
    echo "Error in digiHLT.py"
    exit 1
fi

if cmsDriver.py --python_filename reco.py --eventcontent AODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier AODSIM --fileout file:reco.root --conditions 106X_mcRun2_asymptotic_v17 --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --filein file:digiHLT.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 1000; then
    echo "Successfully completed cmsDriver in RECO step"s
else
    echo "Error in cmsDriver in RECO step"
    exit 1
fi

if cmsRun reco.py > ./logs/log_reco.log 2>&1; then
    echo "Successfully completed reco.py"
else
    echo "Error in reco.py"
    exit 1
fi

if cmsDriver.py  --python_filename pat.py --eventcontent MINIAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier MINIAODSIM --fileout file:pat.root --conditions 106X_mcRun2_asymptotic_v17 --step PAT --procModifiers run2_miniAOD_UL --geometry DB:Extended --filein file:reco.root --era Run2_2016 --runUnscheduled --no_exec --mc -n 1000; then
    echo "Successfully completed cmsDriver in PAT step"
else
    echo "Error in cmsDriver in PAT step"
    exit 1
fi

if cmsRun pat.py > ./logs/log_pat.log 2>&1; then
    echo "Successfully completed pat.py"
else
    echo "Error in pat.py"
    exit 1
fi

if cmsDriver.py --filein file:pat.root --fileout file:NanoAOD.root --mc --eventcontent NANOAODSIM --datatier NANOAODSIM --conditions 106X_mcRun2_asymptotic_v17 --step NANO --nThreads 4 --geometry DB:Extended --era Run2_2016,run2_nanoAOD_94X2016 --python_filename nanoAOD_cfg.py --no_exec --customise_commands "process.nanoAOD_step *= process.nanoSequenceMC" -n 1000; then
    echo "Successfully completed cmsDriver in PAT step"
else
    echo "Error in cmsDriver in PAT step"
    exit 1
fi

# Run the final step and redirect all output to SimLines.log
if cmsRun nanoAOD_cfg.py > ./logs/log_nano.log 2>&1; then
    echo "Successfully completed nanoAOD_cfg.py. Check SimLines.log for details."
else
    echo "Error in nanoAOD_cfg.py. Check SimLines.log for details."
    exit 1
fi

# Print a message to indicate the end of the process
echo "Simulation process completed successfully."

