#!/bin/bash

# Print a message to indicate the start of the process
echo "Starting the simulation process..."

# Run each cmsRun command sequentially and check for errors
if cmsRun gensimDY.py > log_gensim.log 2>&1; then
    echo "Successfully completed gensimDY.py"
else
    echo "Error in gensimDY.py"
    exit 1
fi

if cmsRun digiHLT.py > log_hlt.log 2>&1; then
    echo "Successfully completed digiHLT.py"
else
    echo "Error in digiHLT.py"
    exit 1
fi

if cmsRun reco.py > log_reco.log 2>&1; then
    echo "Successfully completed reco.py"
else
    echo "Error in reco.py"
    exit 1
fi

if cmsRun pat.py > log_pat.log 2>&1; then
    echo "Successfully completed pat.py"
else
    echo "Error in pat.py"
    exit 1
fi

# Run the final step and redirect all output to SimLines.log
if cmsRun nanoAOD_cfg.py > log_nano.log 2>&1; then
    echo "Successfully completed nanoAOD_cfg.py. Check SimLines.log for details."
else
    echo "Error in nanoAOD_cfg.py. Check SimLines.log for details."
    exit 1
fi

# Print a message to indicate the end of the process
echo "Simulation process completed successfully."

