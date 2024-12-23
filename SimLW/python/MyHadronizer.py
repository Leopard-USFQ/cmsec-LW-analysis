import FWCore.ParameterSet.Config as cms

#from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
   maxEventsToPrint = cms.untracked.int32(5),
   pythiaPylistVerbosity = cms.untracked.int32(1),
   filterEfficiency = cms.untracked.double(1.0),
   pythiaHepMCVerbosity = cms.untracked.bool(True),
   comEnergy = cms.double(13000.0),
   UseExternalGenerators = cms.untracked.bool(True),

   PythiaParameters = cms.PSet(
        pythia8CommonSettings = cms.vstring(
	      'Tune:preferLHAPDF = 2',
	      'Main:timesAllowErrors = 10000',
	      'Check:epTolErr = 0.01',
	      'Beams:setProductionScalesFromLHEF = off',
	      'SLHA:keepSM = on',
	      'SLHA:minMassSM = 1000.',
	      'ParticleDecays:limitTau0 = on',
	      'ParticleDecays:tau0Max = 10',
	      'ParticleDecays:allowPhotonRadiation = on',
	    ),
        #pythia8CP5SettingsBlock,
        pythia8CP5Settings = cms.vstring(
	    	'Tune:pp 14',
		'Tune:ee 7',
		'MultipartonInteractions:ecmPow=0.03344',
		'MultipartonInteractions:bProfile=2',
		'MultipartonInteractions:pT0Ref=1.41',
		'MultipartonInteractions:coreRadius=0.7634',
		'MultipartonInteractions:coreFraction=0.63',
		'ColourReconnection:range=5.176',
		'SigmaTotal:zeroAXB=off',
		'SpaceShower:alphaSorder=2',
		'SpaceShower:alphaSvalue=0.118',
		'SigmaProcess:alphaSvalue=0.118',
		'SigmaProcess:alphaSorder=2',
		'MultipartonInteractions:alphaSvalue=0.118',
		'MultipartonInteractions:alphaSorder=2',
		'TimeShower:alphaSorder=2',
		'TimeShower:alphaSvalue=0.118',
		'SigmaTotal:mode = 0',
		'SigmaTotal:sigmaEl = 21.89',
		'SigmaTotal:sigmaTot = 100.309',
		'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118',
		),
        
        processParameters = cms.vstring(
            'WeakSingleBoson:ffbar2gmZ = on',
	    '23:oneChannel= 1   0.03453449    0        13       -13',
	    '23:addChannel= 1   0.03453449    0        11       -11',
	    '23:addChannel= 1   0.03445616    0        15       -15',
            '23:mMin = 50.',
            ),
        JetMatchingParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 5.',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 20.', #this is the actual merging scale
            'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            'JetMatching:nJetMax = 4', #number of partons in born matrix element for highest multiplicity
            'JetMatching:doShowerKt = off', #off for MLM matching, turn on for shower-kT matching
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    'JetMatchingParameters'
                                    )
        )
)
