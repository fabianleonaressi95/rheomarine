import unittest
import numpy as np
from rheomarine_transport import Grid2D, ParticleClass, stability_timestep, step_advection_diffusion, stokes_settling_velocity

class TransportTests(unittest.TestCase):
    def setUp(self):
        self.grid=Grid2D(20,12,100.0,100.0)
        self.zero=np.zeros((12,20))
    def test_zero_flow_preserves_field(self):
        c=np.arange(240,dtype=float).reshape(12,20)
        out=step_advection_diffusion(c,self.zero,self.zero,0.0,10.0,self.grid).concentration
        np.testing.assert_allclose(out,c,atol=1e-13)
    def test_closed_domain_mass_conservation(self):
        rng=np.random.default_rng(7); c=rng.random((12,20))
        result=step_advection_diffusion(c,np.full_like(c,.02),np.full_like(c,-.01),2.0,100.0,self.grid)
        self.assertAlmostEqual(result.mass_after,result.mass_before,places=9)
        self.assertGreaterEqual(float(result.concentration.min()),0.0)
    def test_diffusion_conserves_mass(self):
        c=np.zeros((12,20)); c[6,10]=1.0
        result=step_advection_diffusion(c,self.zero,self.zero,5.0,100.0,self.grid)
        self.assertAlmostEqual(result.mass_after,result.mass_before,places=10)
        self.assertLess(result.concentration[6,10],1.0)
    def test_source_sink_budget(self):
        c=np.ones((12,20))
        result=step_advection_diffusion(c,self.zero,self.zero,0.0,2.0,self.grid,source=.1,sink_rate=.05)
        np.testing.assert_allclose(result.concentration,(1+.2)*np.exp(-.1))
        self.assertAlmostEqual(result.mass_after,result.mass_before+result.source_mass-result.sink_mass,places=8)
    def test_stability_guard(self):
        u=np.full((12,20),.1); dt=stability_timestep(self.grid,u,self.zero,1.0)
        with self.assertRaises(ValueError):
            step_advection_diffusion(np.ones((12,20)),u,self.zero,1.0,2*dt,self.grid)
    def test_stokes_sign_and_particle_class(self):
        w=stokes_settling_velocity(1e-4,900.0)
        self.assertLess(w,0.0)
        self.assertEqual(ParticleClass("PE-100um",1e-4,900.0,w).class_id,"PE-100um")
        with self.assertRaises(ValueError): ParticleClass("bad",-1,900)
if __name__=="__main__": unittest.main()
