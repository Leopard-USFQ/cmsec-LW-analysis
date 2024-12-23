import FWCore.ParameterSet.Config as cms



process = cms.Process("GEN")

process.load('PhysicsTools.HepMCCandAlgos.genParticles_cfi')
#process.load("PhysicsTools.HepMCCandAlgos.genParticleCandidatesFast_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")


# Read the HepMC file
process.source = cms.Source("MCFileSource",
                            fileNames = cms.untracked.vstring('file:JJSJ.hepmc'),
                            firstLuminosityBlockForEachRun = cms.untracked.VLuminosityBlockID([cms.LuminosityBlockID(1, 1)]))

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

# Convert HepMC to GenParticleCandidate using FastGenParticleCandidateProducer
process.genParticleCandidates = cms.EDProducer("GenParticleProducer",
                                               src = cms.InputTag("source"))
#process.genParticleCandidates = cms.EDProducer("FastGenParticleCandidateProducer",
                                               #src = cms.InputTag("source"))

# Define output module
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('genParticlesOutput.root'),
                               outputCommands = cms.untracked.vstring('keep *_genParticleCandidates_*_*'))

process.outpath = cms.EndPath(process.out)

process.p = cms.Path(process.genParticleCandidates)