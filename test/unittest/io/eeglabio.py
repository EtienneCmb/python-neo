# -*- coding: utf-8 -*-



import unittest
import os, sys, numpy
sys.path.append(os.path.abspath('../../..'))

from neo.io import EegLabIO
from neo.core import *
from numpy import *
from scipy import rand
import pylab

class ElanIOTest(unittest.TestCase):
    
#    def testOpenFile1(self):
#        eeglab = eeglabio.    EegLabIO()
#        seg = eeglab.read_segment( filename = 'datafiles/308_ems_S1_ChS_ICA.set',)
##        print len(seg.get_analogsignals())
#        assert len(seg.get_analogsignals()) == 64
#        
#        for sig in seg.get_analogsignals():
#            #print sig.signal.shape[0]
#            assert sig.signal.shape[0] == 367984
##            pylab.plot(sig.t()[:5000],sig.signal[:5000])
#        
#        #print len (seg.get_events() )
#        assert len (seg.get_events() )==40
#        for ev in seg.get_events():
##            print ev.time
#            pylab.axvline(ev.time)
#        
##        pylab.show()
    
    def testWriteReadSinusAndEvent(self):
        
        seg = Segment()
        sampling_rate = 10000.
        totaltime = 15.
        t = arange(0,totaltime,1./sampling_rate)
        sig = 3.6*sin(2*numpy.pi*t*60.)
        ana = AnalogSignal( signal = sig,
                                        sampling_rate = sampling_rate,
                                        )
        ana.label = 'therese'
        nbchannel = 32
        for i in range(nbchannel) :
            seg._analogsignals += [ ana ]
        
        nbevent = 40
        for i in range(nbevent):
            event = Event(time = rand()*totaltime)
            event.label = '1'
            seg._events += [ event ]
            
        
        io = EegLabIO(filename = 'testNeoEeglabIO.set',)
        io.write_segment(  seg, )
        io = EegLabIO(filename = 'testNeoEeglabIO.set',)
        seg2 = io.read_segment()
        ana2 = seg2.get_analogsignals()[0]
        
        assert len(seg2.get_analogsignals()) == nbchannel
        
        # .1% error due to i2 convertion
        assert mean((ana2.signal - ana.signal)**2)/mean(ana.signal**2) < .001
        
        for i in range(nbevent):
#            print seg._events[i].time
#            print seg2._events[i].time
            assert seg._events[i].time - seg2._events[i].time < 1./sampling_rate



if __name__ == "__main__":
    unittest.main()
