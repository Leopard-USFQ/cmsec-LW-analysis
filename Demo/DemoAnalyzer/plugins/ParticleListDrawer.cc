#include <memory>
#include <string>
#include <iostream>
#include <sstream>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "SimGeneral/HepPDTRecord/interface/ParticleDataTable.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Candidate/interface/CandidateFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Common/interface/Ref.h"

/**
   \class   ParticleListDrawer ParticleListDrawer.h "PhysicsTools/HepMCCandAlgos/plugins/ParticleListDrawer.h"

   \brief   Module to analyze the particle listing as provided by common event generators

   Module to analyze the particle listing as provided by common event generators equivalent
   to PYLIST(1) (from pythia). It is expected to run on vectors of  reo::GenParticles. For
   an example of use have a look to:

   PhysicsTools/HepMCCandAlgos/test/testParticleTreeDrawer.py

   Caveats:
   Status 3 particles can have daughters both with status 2 and 3. In pythia this is not
   the same mother-daughter. The relations are correct but special care has to be taken
   when looking at mother-daughter relation which involve status 2 and 3 particles.
*/


using namespace std;
using namespace reco;
using namespace edm;

class ParticleListDrawer : public edm::EDAnalyzer {
  public:
    explicit ParticleListDrawer(const edm::ParameterSet & );
    ~ParticleListDrawer() override {};
    void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) override;

  private:
    std::string getParticleName( int id ) const;

    edm::InputTag src_;
    edm::EDGetTokenT<reco::CandidateView> srcToken_;
    edm::ESHandle<ParticleDataTable> pdt_;
    int maxEventsToPrint_; // Must be signed, because -1 is used for no limit
    unsigned int nEventAnalyzed_;
    bool printOnlyHardInteraction_;
    bool printVertex_;
    bool printFlags_;
    bool useMessageLogger_;
    //bool accept( const reco::Candidate & ) const;
    bool hasValidDaughters( const reco::Candidate & ) const;
};

ParticleListDrawer::ParticleListDrawer(const edm::ParameterSet & pset) :
  src_(pset.getParameter<InputTag>("src")),
  srcToken_(consumes<reco::CandidateView>(src_)),
  maxEventsToPrint_ (pset.getUntrackedParameter<int>("maxEventsToPrint",1)),
  nEventAnalyzed_(0),
  printOnlyHardInteraction_(pset.getUntrackedParameter<bool>("printOnlyHardInteraction", false)),
  printVertex_(pset.getUntrackedParameter<bool>("printVertex", false)),
  printFlags_(pset.getUntrackedParameter<bool>("printFlags", false)),
  useMessageLogger_(pset.getUntrackedParameter<bool>("useMessageLogger", false)) {
}

/*bool ParticleListDrawer::accept( const reco::Candidate & c ) const {
  if ( status_.empty() ) return true;
  return find( status_.begin(), status_.end(), c.status() ) != status_.end();
}*/

bool ParticleListDrawer::hasValidDaughters( const reco::Candidate & c ) const {
  size_t ndau = c.numberOfDaughters();
  for( size_t i = 0; i < ndau; ++ i )
      return true;
  return false;
}

std::string ParticleListDrawer::getParticleName(int id) const
{
  const ParticleData * pd = pdt_->particle( id );
  if (!pd) {
    std::ostringstream ss;
    ss << "P" << id;
    return ss.str();
  } else
    return pd->name();
}

void ParticleListDrawer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  Handle<reco::CandidateView> particles;
  iEvent.getByToken(srcToken_, particles );
  iSetup.getData( pdt_ );

  if(maxEventsToPrint_ < 0 || nEventAnalyzed_ < static_cast<unsigned int>(maxEventsToPrint_)) {
    ostringstream out;
    char buf[256];

    //out << endl<< "[ParticleListDrawer] analysing particle collection " << src_.label() << endl;

    snprintf(buf, sizeof(buf), "idx,ID,Name,Stat,Mo1,Mo2,Da1,Da2,MoPdg,DaPdg,pt,eta,phi,px,py,pz,m,");
    out << buf;
    if (printVertex_) {
      snprintf(buf, sizeof(buf), "vx,vy,vz");
      out << buf;
    }
    out << endl;

    int idx  = -1;
    int iMo1 = -1;
    int iMo2 = -1;
    int iDa1 = -1;
    int iDa2 = -1;
    vector<const reco::Candidate *> cands;
    vector<const Candidate *>::const_iterator found = cands.begin();
    for(CandidateView::const_iterator p = particles->begin();
	      p != particles->end(); ++ p) {
      cands.push_back(&*p);
    }

    for(CandidateView::const_iterator p  = particles->begin();
	p != particles->end();
	p ++) {
      //cout<< p->pdgId()<< "\n";//p->mother()->pdgId();
      //if (printOnlyHardInteraction_ && !(p->pdgId() == 556 || p->pdgId() == -556 || p->pdgId() == 23 || p->pdgId() == -11 || p->pdgId() == 11 )){
        //cout<< p->pdgId()<< " " <<p->mother()->pdgId();
        /*if (p->mother()->pdgId() == 556 || p->mother()->pdgId() == 556)*/ //continue;
      //}
      //if (printOnlyHardInteraction_ && !( p->status()==21 || p->status()==22 || p->status()==23 || p->status()==1 )) continue;
      //if (p->pdgId() == 23 && p->mother()->pdgId() != 556 ) continue;
      if (printOnlyHardInteraction_ && !((p->status()>=21 && p->status()<=24) || p->status()==1)) continue;
      else if(p->status() == 1){
        found = find(cands.begin(), cands.end(), p->mother(0));
        if( found != cands.end()){
          if( !(abs(p->mother()->pdgId()) == 556 || p->mother()->pdgId() == 23) )continue;
        }
        
      }
      // Particle Name
      int id = p->pdgId();
      string particleName = getParticleName(id);

      // Particle Index
      idx =  p - particles->begin();

      // Particles Mothers and Daighters
      iMo1 = -1;
      iMo2 = -1;
      iDa1 = -1;
      iDa2 = -1;
      int nMo = p->numberOfMothers();
      int nDa = p->numberOfDaughters();

      found = find(cands.begin(), cands.end(), p->mother(0));
      if(found != cands.end()) iMo1 = found - cands.begin() ;

      found = find(cands.begin(), cands.end(), p->mother(nMo-1));
      if(found != cands.end()) iMo2 = found - cands.begin() ;

      found = find(cands.begin(), cands.end(), p->daughter(0));
      if(found != cands.end()) iDa1 = found - cands.begin() ;

      found = find(cands.begin(), cands.end(), p->daughter(nDa-1));
      if(found != cands.end()) iDa2 = found - cands.begin() ;

      found = find(cands.begin(), cands.end(), p->mother(0));
      if(found != cands.end()) nMo = p->mother()->pdgId();

      found = find(cands.begin(), cands.end(), p->daughter(0));
      if(found != cands.end()) nDa = p->daughter(0)->pdgId();

      char buf[2400];
      snprintf(buf, sizeof(buf),
	     "%4d,%5d,%10s,%2d,%4d,%4d,%4d,%4d,%4d,%4d,%7.8f,%10.8f,%6.8f,%10.8f,%10.8f,%10.8f,%8.8f,",
             idx,
             p->pdgId(),
             particleName.c_str(),
             p->status(),
             iMo1,iMo2,iDa1,iDa2,nMo,nDa,
             p->pt(),
             p->eta(),
             p->phi(),
             p->px(),
             p->py(),
             p->pz(),
             p->mass()
            );
      out << buf;

      if (printVertex_) {
        snprintf(buf, sizeof(buf), "%10.8f,%10.8f,%10.8f",
                 p->vertex().x(),
                 p->vertex().y(),
                 p->vertex().z());
        out << buf;

      }

      if (printFlags_) {
          const reco::GenParticle *gp = dynamic_cast<const reco::GenParticle *>(&*p);
          if (!gp) throw cms::Exception("Unsupported", "Status flags can be printed only for reco::GenParticle objects\n");
          if (gp->isPromptFinalState()) out << "  PromptFinalState";
          if (gp->isDirectPromptTauDecayProductFinalState()) out << "  DirectPromptTauDecayProductFinalState";
          if (gp->isHardProcess()) out << "  HardProcess";
          if (gp->fromHardProcessFinalState()) out << "  HardProcessFinalState";
          if (gp->fromHardProcessBeforeFSR()) out << "  HardProcessBeforeFSR";
          if (gp->statusFlags().isFirstCopy()) out << "  FirstCopy";
          if (gp->isLastCopy()) out << "  LastCopy";
          if (gp->isLastCopyBeforeFSR()) out << "  LastCopyBeforeFSR";
      }

      out << endl;
      //cout<<p->mother()->pdgId()<<endl;

    }
    /*
    for(CandidateView::const_iterator p  = particles->begin();
        p != particles->end(); p ++) {
          //cout << p->status() << endl;
          if (printOnlyHardInteraction_ && !((p->status()>=21 && p->status()<=24) || p->status()==1)) continue;
          else if(p->status() == 1){
            found = find(cands.begin(), cands.end(), p->mother(0));
            if( found != cands.end()){
              if( !(abs(p->mother()->pdgId()) == 556 || p->mother()->pdgId() == 23) )continue;
            }
            
          }
          cout << p->status() << endl;
          //p->status() = 5;
          cout << p->status() << endl;
          //if ( accept( * p ) ) {
            if ( p->mother() == nullptr ) {
              auto & c = * p;
              cout << getParticleName( c.pdgId() );
              cout << " (" << c.px() << ", " << c.py() << ", " << c.pz() << "; " << c.energy() << ")";
              cout << " [" << c.pt() << ": " << c.eta() << ", " << c.phi() << "]";
              cout << " {" << c.vx() << ", " << c.vy() << ", " << c.vz() << "}";
              cout << "{status: " << c.status() << "}";
              int idx = -1;
              vector<const Candidate *>::const_iterator found = find( cands.begin(), cands.end(), & c );
              if ( found != cands.end() ) {
                idx = found - cands.begin();
                cout << " <idx: " << idx << ">";
              }
              
              cout << endl;

              size_t ndau = c.numberOfDaughters(), validDau = 0;
              for( size_t i = 0; i < ndau; ++ i )
                //if ( accept( * c.daughter( i ) ) )
                  ++ validDau;
              if ( validDau == 0 ) return;

              bool lastLevel = true;
              for( size_t i = 0; i < ndau; ++ i ) {
                if ( hasValidDaughters( * c.daughter( i ) ) ) {
                  lastLevel = false;
                  break;
                }
              }

              if ( lastLevel ) {
                cout << "pre" << "+-> ";
                size_t vd = 0;
                for( size_t i = 0; i < ndau; ++ i ) {
                  const Candidate * d = c.daughter( i );
                  //if ( accept( * d ) ) {
                  cout << getParticleName( d->pdgId() );
                  cout << " (" << c.px() << ", " << c.py() << ", " << c.pz() << "; " << c.energy() << ")";
                  cout << " [" << c.pt() << ": " << c.eta() << ", " << c.phi() << "]";
                  cout << " {" << c.vx() << ", " << c.vy() << ", " << c.vz() << "}";
                  cout << "{status: " << c.status() << "}";
                  
                  int idx = -1;
                  vector<const Candidate *>::const_iterator found = find( cands.begin(), cands.end(), & c );
                  if ( found != cands.end() ) {
                    idx = found - cands.begin();
                    cout << " <idx: " << idx << ">";
                  }
                  
                  if ( vd != validDau - 1 )
                    cout << " ";
                  vd ++;
                  //}
                }
                cout << endl;
                return;
              }
            }//mother null ptr
          //}
    }*/
    nEventAnalyzed_++;

    if (useMessageLogger_)
      LogVerbatim("ParticleListDrawer") << out.str();
    else
      cout << out.str();
  }
}

DEFINE_FWK_MODULE(ParticleListDrawer);

