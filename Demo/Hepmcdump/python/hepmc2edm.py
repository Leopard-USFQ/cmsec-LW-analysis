#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

# Usage: cmsRun OPTIONS
#   or   ./hepmc2edm.py OPTIONS
#
# Description: converts an HEP2MC2 ascii file into an EDM file.
#
# OPTIONS:
#   inputFiles=INPUT_FILE  specifies the input file using CMSSW standard format for the path (file:, /store...).
#                          Add one option per file to read. (default: file:sample.hepmc2).
#   outputFile=OUTPUT_FILE specifies the output file using CMSSW standard format for the path. 
#                          (default: file:sampl.root)
#   maxEvents=MAX_EVENTS   Maximum number of events to process. (default: -1)

process = cms.Process("GEN")

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

#default options:
options.inputFiles= 'file:JJSJ.hepmc'
options.outputFile = 'file:hepmc_file.root'
options.maxEvents = -1 # -1 means all events

options.parseArguments()

# Standard sequences and services:
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.load("GeneratorInterface.Core.hepmcConverter_cfi")
#process.load('GeneratorInterface.Core.generator_cfi')

# Input:
process.source = cms.Source(
    "MCFileSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    firstEvent = cms.untracked.uint32(1),
    firstRun = cms.untracked.uint32(1),
    input = cms.untracked.int32(options.maxEvents),
    firstLuminosityBlockForEachRun = cms.untracked.VLuminosityBlockID([cms.LuminosityBlockID(1, 1)]),
    type = cms.untracked.string("HepMCProduct")
)

# Number of events to process:
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.maxEvents))

# Load the necessary module to process HepMCProduct
#process.load("GeneratorInterface.Core.genParticles_cfi")
# Use GenParticleProducer to convert HepMC input
process.genParticles = cms.EDProducer(
    "GenParticleProducer",
    saveBarCodes = cms.untracked.bool(True),
    src = cms.InputTag("source"),
    abortOnUnknownPDGCode = cms.untracked.bool(False)
)
# Logs:
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'

# Vertex smearing:
process.load("IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeV2016Collision_cfi")

# Producer of generator objects  is "source" instead of usual "generator":
process.VtxSmeared.src = cms.InputTag("genParticles")
process.genParticles.src = cms.InputTag("source",)

# Use default condition tag:
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

#Output:
process.output = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string (options.outputFile),
    outputCommands = cms.untracked.vstring('keep *')
    )

# Path and EndPath definitions
process.generation_step = cms.Path(process.genParticles * process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step           = cms.EndPath(process.endOfProcess)
process.output_step           = cms.EndPath(process.output)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,
                                process.genfiltersummary_step,
                                process.endjob_step,
                                process.output_step)