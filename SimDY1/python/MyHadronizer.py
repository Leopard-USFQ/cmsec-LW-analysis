import FWCore.ParameterSet.Config as cms

from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(5),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        
		pythia8CommonSettings = cms.vstring(
			'Tune:preferLHAPDF = 2',
			'Main:timesAllowErrors = 10000',
			'Check:epTolErr = 0.01',
			'Beams:setProductionScalesFromLHEF = off',
			'SLHA:minMassSM = 1000.',
			'ParticleDecays:limitTau0 = on',
			'ParticleDecays:tau0Max = 10',
			'ParticleDecays:allowPhotonRadiation = on',
		),
        pythia8CUEP8M1Settings = cms.vstring(
			'Tune:pp 14',
			'Tune:ee 7',
			'MultipartonInteractions:pT0Ref=2.4024',
			'MultipartonInteractions:ecmPow=0.25208',
			'MultipartonInteractions:expPow=1.6',
    	),
		pythia8aMCatNLOSettings = cms.vstring(
			'SpaceShower:pTmaxMatch = 1',
			'SpaceShower:pTmaxFudge = 1',
			'SpaceShower:MEcorrections = off',
			'TimeShower:pTmaxMatch = 1',
			'TimeShower:pTmaxFudge = 1',
			'TimeShower:MEcorrections = off',
			'TimeShower:globalRecoil = on',
			'TimeShower:limitPTmaxGlobal = on',
			'TimeShower:nMaxGlobalRecoil = 1',
			'TimeShower:globalRecoilMode = 2',
			'TimeShower:nMaxGlobalBranch = 1',
			'TimeShower:weightGluonToQuark = 1',
		),
        processParameters = cms.vstring(
            'WeakSingleBoson:ffbar2gmZ = on',
            '23:onMode = off',
            '23:onIfAny = 11',
            '23:onIfAny = 13',
            '23:onIfAny = 15',
            '23:mMin = 50.',
        ),
        #JetMatchingParameters = cms.vstring(
            #'JetMatching:setMad = off',
            #'JetMatching:scheme = 1',
            #'JetMatching:merge = on',
            #'JetMatching:jetAlgorithm = 2',
            #'JetMatching:etaJetMax = 999.',
            #'JetMatching:coneRadius = 1.',
            #'JetMatching:slowJetPower = 1',
            #'JetMatching:qCut = 30.', #this is the actual merging scale
            #'JetMatching:doFxFx = on',
            #'JetMatching:qCutME = 10.',#this must match the ptj cut in the lhe generation step
            #'JetMatching:nQmatch = 5', #4 corresponds to 4-flavour scheme (no matching of b-quarks), 5 for 5-flavour scheme
            #'JetMatching:nJetMax = 2', #number of partons in born matrix element for highest multiplicity
            #'TimeShower:mMaxGamma = 4.0',
        #),
        
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'pythia8aMCatNLOSettings',
                                    'processParameters',
                                    #"JetMatchingParameters",
                                    )
    )
)
