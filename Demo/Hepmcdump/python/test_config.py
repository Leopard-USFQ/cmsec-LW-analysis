import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.source = cms.Source("MCFileSource",
                            fileNames = cms.untracked.vstring('file:JJSJ.hepmc'),
                            firstLuminosityBlockForEachRun = cms.untracked.VLuminosityBlockID([cms.LuminosityBlockID(1, 1)]))

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('testOutput.root'),
                               outputCommands = cms.untracked.vstring('drop *'))

process.outpath = cms.EndPath(process.out)
