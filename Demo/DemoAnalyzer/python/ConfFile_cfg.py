import FWCore.ParameterSet.Config as cms
process = cms.Process("Demo")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
process.source = cms.Source("PoolSource",
# replace 'myfile.root' with the source file you want to use
   fileNames = cms.untracked.vstring(
       #'root://eospublic.cern.ch//eos/opendata/cms/Run2015D/SingleElectron/MINIAOD/08Jun2016-v1/10000/001A703B-B52E-E611-BA13-0025905A60B6.root'
       'file:reco.root'
   )
)
# process.load("SimGeneral.MixingModule.mixNoPU_cfi")
# process.load("SimGeneral.MixingModule.trackingTruthProducerSelection_cfi")
# process.trackingParticles.simHitCollections = cms.PSet( )
# process.mix.playback = cms.untracked.bool(True)
# process.mix.digitizers = cms.PSet(
#      mergedtruth = cms.PSet(process.trackingParticles)
# )
# for a in process.aliases: delattr(process, a)
process.printTree = cms.EDAnalyzer("ParticleListDrawer",
  maxEventsToPrint = cms.untracked.int32(10),
  printVertex = cms.untracked.bool(True),
  printOnlyHardInteraction = cms.untracked.bool(True), # Print only status=3 particles. This will not work for Pythia8, which does not have any such particles.
  src = cms.InputTag("genParticles"),
  pdgId = cms.untracked.vint32(556)
)

process.modifyGenParticles = cms.EDProducer('ModifyGenParticles',
                                            src = cms.InputTag('genParticles'))

process.demo = cms.EDAnalyzer('DemoAnalyzer',genpart = cms.InputTag("mix","MergedTrackTruth"))
#process.p = cms.Path(process.mix + process.demo)
#process.p = cms.Path(process.demo + process.printTree + process.modifyGenParticles)# + process.demo)
#process.p = cms.Path(process.modifyGenParticles)
process.p = cms.Path(process.printTree)

# Output module configuration
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('modifiedGenParticles.root'),  # Name of the output file
    outputCommands = cms.untracked.vstring(
        #'drop *',  # Drop all existing branches
        #'keep *_modifyGenParticles_*_*'  # Keep only the modified particles
    )
)

# EndPath to write the output file
process.outpath = cms.EndPath(process.output)

