#include <iostream>
#include <fstream>
#include "HepMC/GenEvent.h"
#include "HepMC/IO_GenEvent.h"

int main() {
    std::string input_file = "v2JJSJ.hepmc";
    std::string output_file = "Modifiedv2.hepmc";

    HepMC::IO_GenEvent input_stream(input_file, std::ios::in);
    HepMC::IO_GenEvent output_stream(output_file, std::ios::out);

    HepMC::GenEvent* event = nullptr;

    bool flag = false;

    while ((event = input_stream.read_next_event())) {
        // Iterate over all vertices in the event
        for (auto vertex = event->vertices_begin(); vertex != event->vertices_end(); ++vertex) {
            HepMC::GenVertex* vtx = *vertex;

            // Iterate over outgoing particles from the vertex
            for (auto particle = vtx->particles_out_const_begin(); particle != vtx->particles_out_const_end(); ++particle) {
                HepMC::GenParticle* p = *particle;

                if (p->pdg_id() == 556 and !flag) {
                    HepMC::FourVector position = vtx->position();
                    position.set(position.x()*-1, position.y()*-1, position.z()*-1, position.t());
                    vtx->set_position(position);
                    HepMC::GenVertex* daughter_vtx = p->end_vertex(); //get daughter vertex id
                    flag =true;
                }
                while (vtx->id() != 0 and flag)
                {
                    auto daughter = vtx->particles_out_const_begin();
                    p = *daughter;

                    HepMC::FourVector position = vtx->position();
                    position.set(position.x()*-1, position.y()*-1, position.z()*-1, position.t());
                    vtx->set_position(position);
                    vtx = p->end_vertex(); //get daughter vertex id
                }                
                
            }
        }

        // Write the modified event to the output file
        output_stream.write_event(event);

        // Clean up the event
        delete event;
    }

    std::cout << "Processing complete. Modified file saved as " << output_file << std::endl;

    return 0;
}