import FWCore.ParameterSet.Config as cms

process = cms.Process("HEPMC2EDM")

# Input source
process.source = cms.Source("HepMCProduct",
    fileNames = cms.untracked.vstring('file:JJSJ.hepmc')  # Replace with your HepMC file path
)

# Define the conversion module
process.hepmcToEdm = cms.EDProducer("HepMCProduct",
    src = cms.InputTag("source"),
)

# Output configuration
process.output = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('file:output_file.root'),  # Replace with your desired EDM output file path
    outputCommands = cms.untracked.vstring('keep *')
)

# Define the process path
process.path = cms.Path(process.hepmcToEdm)

# Define the end path
process.endpath = cms.EndPath(process.output)

# Define the schedule
process.schedule = cms.Schedule(
    process.path,
    process.endpath
)