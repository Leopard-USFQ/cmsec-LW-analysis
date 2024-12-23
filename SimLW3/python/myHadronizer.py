import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
   maxEventsToPrint = cms.untracked.int32(0),
   pythiaPylistVerbosity = cms.untracked.int32(1),
   filterEfficiency = cms.untracked.double(1.0),
   pythiaHepMCVerbosity = cms.untracked.bool(True),
   comEnergy = cms.double(13000.0),
   UseExternalGenerators = cms.untracked.bool(True),
   PythiaParameters = cms.PSet(
       processParameters = cms.vstring(
           'Tune:pp 5',
           'PDF:pSet = 5',
       ),
        #pythia8CommonSettingsBlock,
	    #pythia8CUEP8M1SettingsBlock,
        pythiaMyParameters = cms.vstring(
            '556:new = lwe- lwe+ 2 -3 0 200.0 0.0 200.0 200.0 2.70765e-02', 
            '556:isResonance=off', 
            '556:isVisible=off', 
            '556:addChannel= 1 1.0 100 23 11', 
            #'WeakSingleBoson:ffbar2gmZ = on', 
            '23:onMode = off', 
            '23:onIfAny = 11', 
            '23:onIfAny = 13', 
            '23:onIfAny = 15', 
            '23:mMin = 50.'
        ),

	    parameterSets = cms.vstring('pythiaMyParameters',
                                    'processParameters')
                                    #'pythia8CommonSettings',
                                    #'pythia8CUEP8M1Settings')
                        
   )
)