import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
	comEnergy = cms.double(13000.0),
	crossSection = cms.untracked.double(1.333),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(1),
	PythiaParameters = cms.PSet(
	        pythia8CommonSettingsBlock,
		pythia8CUEP8M1SettingsBlock,
		processParameters = cms.vstring(
            		'JetMatching:setMad = off',
            		'JetMatching:scheme = 1',
            		'JetMatching:merge = on',
            		'JetMatching:jetAlgorithm = 2',
            		'JetMatching:etaJetMax = 5.',
            		'JetMatching:coneRadius = 1.',
            		'JetMatching:slowJetPower = 1',
            		'JetMatching:qCut = 19.', #this is the actual merging scale
            		'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            		'JetMatching:nJetMax = 4', #number of partons in born matrix element for highest multiplicity
            		'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
            		'TimeShower:mMaxGamma = 4.0',
        	),
		processMyparameters = cms.vstring(
            		'WeakSingleBoson:ffbar2gmZ = on',
            		'23:onMode = off',
            		'23:onIfAny = 11',
            		'23:onIfAny = 13',
            		'23:onIfAny = 15',
            		'23:mMin = 50.',
        	),
		parameterSets = cms.vstring('pythia8CommonSettings',
		                            'pythia8CUEP8M1Settings',
		                            'processParameters',
					    'processMyparameters',)
	)
)

ProductionFilterSequence = cms.Sequence(generator)
