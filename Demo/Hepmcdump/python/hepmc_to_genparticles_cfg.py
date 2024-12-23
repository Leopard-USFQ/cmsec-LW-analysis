#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("GEN")

# Setup 'analysis' options
options = VarParsing.VarParsing('analysis')

# Default options:
options.inputFiles = 'file:JJSJ.hepmc'
options.outputFile = 'file:genParticle.root'
options.maxEvents = -1  # -1 means all events

options.parseArguments()

# Standard sequences and services:
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
# import of standard configurations
#process.load('Configuration.StandardSequences.Services_cff')
#process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeV2016Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
#process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Input:
process.source = cms.Source(
    "MCFileSource",  # Use HepMCSource instead of MCFileSource
    fileNames=cms.untracked.vstring(options.inputFiles),
    firstLuminosityBlockForEachRun=cms.untracked.VLuminosityBlockID([cms.LuminosityBlockID(1, 1)])
)

# Number of events to process:
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))

# Logs:
#process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'

# Load the magnetic field and geometry
#process.load("Configuration.StandardSequences.MagneticField_cff")
#process.load("Configuration.Geometry.GeometryIdeal_cff")

# Load the vertex smearing configuration for 13 TeV (2016)
#process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVCollision_cfi')

# Set the vertex smearing source
process.VtxSmeared.src = cms.InputTag("source")  # No change here

# Load the genParticles producer
process.load("PhysicsTools.HepMCCandAlgos.genParticles_cfi")
#process.genParticles.src = cms.InputTag("source")  # Point to the correct HepMC source
genParticles = cms.EDProducer("GenParticleProducer",
                  src = cms.InputTag("source")
)

# Load the Particle Data Table (PDT)
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

# Use default condition tag
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

# Set the Global Tag (you may need to change this depending on your release)
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag.connect = cms.string('sqlite_file:/cvmfs/cms-opendata-conddb.cern.ch/106X_mcRun2_asymptotic_v17.db')
process.GlobalTag.globaltag = '106X_mcRun2_asymptotic_v17'

# Output:
process.output = cms.OutputModule(
    "PoolOutputModule",
    fileName=cms.untracked.string(options.outputFile),
    outputCommands=cms.untracked.vstring('keep *')
)

# Path and EndPath definitions
process.generation_step = cms.Path(process.VtxSmeared + process.genParticles)
process.generation_step = cms.Path(process.genParticles)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(
    process.generation_step,
    process.genfiltersummary_step,
    process.endjob_step,
    process.output_step
)
