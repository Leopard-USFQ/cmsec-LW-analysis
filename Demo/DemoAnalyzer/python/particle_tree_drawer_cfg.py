import FWCore.ParameterSet.Config as cms

# Define the process
process = cms.Process("DRAW")

#process.MessageLogger.cerr.FwkReport.reportEvery = 1

# Load the necessary module for genParticles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

#Load the ParticleTreeDrawer analyzer
process.printTree = cms.EDAnalyzer("ParticleTreeDrawer",
                                   src = cms.InputTag("genParticles"),  # Input tag for the particles to analyze
                                   printP4 = cms.untracked.bool(True),  # Option to print the 4-momentum
                                   printPtEtaPhi = cms.untracked.bool(False),  # Option to print pt, eta, phi
                                   printVertex = cms.untracked.bool(False),  # Option to print vertex information
                                   printStatus = cms.untracked.bool(True),  # Option to print status flags
                                   printIndex = cms.untracked.bool(False),  # Option to print particle index
                                   status = cms.untracked.vint32( ),  # Include 44 to explore what is happening
                                   )

# process.printDecay = cms.EDAnalyzer("ParticleDecayDrawer",
#     src = cms.InputTag("genParticles"),
#     printP4 = cms.untracked.bool(False),
#     printPtEtaPhi = cms.untracked.bool(False),
#     printVertex = cms.untracked.bool(True),
#     status = cms.untracked.vint32( ),
#   )

# process.printTree = cms.EDAnalyzer("ParticleListDrawer",
#   maxEventsToPrint = cms.untracked.int32(10),
#   printVertex = cms.untracked.bool(True),
#   printOnlyHardInteraction = cms.untracked.bool(False), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
#   src = cms.InputTag("genParticles"),
#   pdgId = cms.untracked.vint32(556)
# )

# Define the input source
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring('file:gensimLW_acausal.root')
                            )

# Define the maximum number of events to process
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)  # Number of events to process
)

# Define the path for execution
process.p = cms.Path(process.printTree)
#process.p = cms.Path(process.printDecay)

# End the process with the output module (if needed)
process.schedule = cms.Schedule(process.p)