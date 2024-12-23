//compilate with g++ -v -o MiD ModifieriterativeDaughter.cpp -I/usr/local/include -L/usr/local/lib -lHepMC

#include <iostream>
#include <fstream>
#include <set>
#include "HepMC/GenEvent.h"
#include "HepMC/IO_GenEvent.h"

// Recursive function to iterate over all descendants of a particle
void iterate_descendants(HepMC::GenParticle* particle, std::set<int>& visited, std::set<int>& visvert) {
    if (!particle || visited.count(particle->barcode())) {
        return; // Avoid processing the same particle multiple times
    }

    // Mark this particle as visited
    visited.insert(particle->barcode());


    // Print information about the particle
    std::cout << "Particle ID: " << particle->pdg_id()
              << ", Status: " << particle->status()
              << ", Momentum: (" << particle->momentum().px() << ", "
              << particle->momentum().py() << ", "
              << particle->momentum().pz() << ", "
              << particle->momentum().e() << ") ";
    // Get and modify the production vertex of the particle
    HepMC::GenVertex* production_vertex = particle->production_vertex();
    std::cout << "Vertex ID: " << production_vertex -> barcode() << std::endl;

    if (production_vertex and !visvert.count(production_vertex->barcode())) {
        //Mark Visited vertex 
        visvert.insert(production_vertex->barcode());

        HepMC::FourVector position = production_vertex->position();
        // reverse the position
        position.set(position.x() * -1, position.y() * -1, position.z() * -1, position.t());
        production_vertex->set_position(position);
    }

    // Get the vertex where this particle decays
    HepMC::GenVertex* decay_vertex = particle->end_vertex();
    if (decay_vertex) {
        // Iterate over all particles produced at the decay vertex
        for (auto descendant = decay_vertex->particles_out_const_begin();
             descendant != decay_vertex->particles_out_const_end();
             ++descendant) {
            iterate_descendants(*descendant, visited, visvert);
        }
    }
}

int main() {
    std::string input_file = "v2JJSJ.hepmc";
    std::string output_file = "Modifiedv2.hepmc";

    HepMC::IO_GenEvent input_stream(input_file, std::ios::in);
    HepMC::IO_GenEvent output_stream(output_file, std::ios::out);

    HepMC::GenEvent* event = nullptr;
    int c=0;
    while ((event = input_stream.read_next_event()) and c<1) {
        // Set to track visited particles and avoid infinite loops
        std::set<int> visited;
        // Set to track visited vertices and avoid doible reversing
        std::set<int> visvert;

        // Iterate over all particles in the event
        for (auto particle = event->particles_begin(); particle != event->particles_end(); ++particle) {
            if ((*particle)->pdg_id() == 556) {
                std::cout << "Found particle with PDG ID 556" << std::endl;

                // Start recursive iteration over descendants
                iterate_descendants(*particle, visited, visvert);
            }
        }
        // Write the modified event to the output file
        output_stream.write_event(event);

        // Clean up the event
        delete event;
        c++;
    }

    std::cout << "Processing complete." << std::endl;

    return 0;
}
