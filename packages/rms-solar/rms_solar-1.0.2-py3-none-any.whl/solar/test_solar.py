################################################################################
# solar/unittester.py
################################################################################

import numpy as np
import unittest
import solar

NAMES = ['STIS_Rieke', 'stis', 'RIEKE', 'Kurucz', 'Colina']
UNITS = list(solar.UNIT_DICT.keys())
XUNITS = list(solar.XUNIT_DICT.keys())

# Testing every possible combination of units doesn't seem strictly necessary,
# but it doesn't take too long.
class Test_Solar(unittest.TestCase):

  def runTest(self):

    for unit in UNITS:
      for xunit in XUNITS:
        model0 = solar.flux_density(NAMES[0], units=unit, xunits=xunit,
                                    sun_range=1., solar_f=False)
        for name in NAMES[1:]:
            model1 = solar.flux_density(name, units=unit, xunits=xunit,
                                        sun_range=1., solar_f=False)
            model0a = model0.subsample(model1.x)
            model1a = model1.subsample(model0a.x)

            model0a = model0a.trim()
            model1a = model1a.trim()

            (min0, max0) = model0a.domain()
            (min1, max1) = model1a.domain()

            test_min = max(min0, min1)
            test_max = min(max0, max1)

            self.assertTrue(test_min < test_max)

            model0a = model0a.clip(test_min, test_max)
            model1a = model1a.clip(test_min, test_max)

            diffs = 2 * np.abs(model1a.y - model0a.y) / (model0a.y + model1a.y)
            median_diff = np.median(diffs)

            self.assertTrue(median_diff < 0.02)

    for name in NAMES:
        model0 = solar.flux_density(name, sun_range=1., solar_f=False)
        saved = model0.y.copy()
        model1 = solar.flux_density(name, sun_range=9., solar_f=False) * 81.
        model2 = solar.flux_density(name, sun_range=1., solar_f=True) * np.pi

        self.assertTrue(np.abs((model1.y - model0.y)/model0.y).max() < 1.e-15)
        self.assertTrue(np.abs((model2.y - model0.y)/model0.y).max() < 1.e-15)

        model0 = solar.flux_density(name, units='W/m^2/um')
        model1 = solar.flux_density(name, units='W/m^2/nm') * 1.e3
        model2 = solar.flux_density(name, units='W/m^2/A')  * 1.e4

        with self.assertRaises(ValueError):
          solar.flux_density(name, units='Fred')
        with self.assertRaises(ValueError):
          solar.flux_density(name, xunits='Fred')

        self.assertTrue(np.abs((model1.y - model0.y)/model0.y).max() < 1.e-15)
        self.assertTrue(np.abs((model2.y - model0.y)/model0.y).max() < 1.e-15)

        model1 = solar.flux_density(name, units='erg/s/cm^2/um') * 1.e-7 * 1.e4
        self.assertTrue(np.abs((model1.y - model0.y)/model0.y).max() < 1.e-15)

        model0 = solar.flux_density(name, units='W/m^2/Hz')
        model1 = solar.flux_density(name, units='erg/s/cm^2/Hz') * 1.e-7 * 1.e4
        model2 = solar.flux_density(name, units='Jy') / 1.e26
        model3 = solar.flux_density(name, units='uJy') / 1.e32

        self.assertTrue(np.abs((model1.y - model0.y)/model0.y).max() < 1.e-15)
        self.assertTrue(np.abs((model2.y - model0.y)/model0.y).max() < 1.e-15)
        self.assertTrue(np.abs((model3.y - model0.y)/model0.y).max() < 1.e-15)

    with self.assertRaises(ValueError):
      solar.flux_density('Fred')

    # Need tests for:
    #   bandpass_flux_density
    #   mean_flux_density
    #   bandpass_f
    #   mean_f

########################################

if __name__ == '__main__':  # pragma: no cover
    unittest.main(verbosity=2)

################################################################################
