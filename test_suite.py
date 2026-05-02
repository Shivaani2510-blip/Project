import unittest
from core.physics_engine import SolarPhysics
from entities.storage import BatteryBank

class GridSafetyTests(unittest.TestCase):
    def setUp(self):
        self.physics = SolarPhysics()
        self.battery = BatteryBank(500)

    def test_solar_night_efficiency(self):
        """Ensure energy generation is exactly 0 at midnight."""
        res = self.physics.calculate_irradiance(0, 30, 0)
        self.assertEqual(res, 0, "Physics Error: Solar detected at night!")

    def test_battery_overflow(self):
        """Ensure battery logic rejects energy when full."""
        self.battery.current_energy = 500
        waste = self.battery.charge(100)
        self.assertGreater(waste, 0, "Safety Error: Battery overcharged!")

    def test_panel_tilt_impact(self):
        """Verify that a 90-degree tilt reduces vertical irradiance."""
        flat = self.physics.calculate_irradiance(12, 0, 0)
        tilted = self.physics.calculate_irradiance(12, 90, 0)
        self.assertLess(tilted, flat, "Physics Error: Tilt math is inverted.")

if __name__ == "__main__":
    print("\n[V-TEST] STARTING AUTOMATED VALIDATION...")
    unittest.main()



#This is the Quality Assurance (QA) block. It contains "Unit Tests." It runs a series of "hidden" simulations to verify that the physics and math are 100% correct. If the math is wrong, this file will flag it immediately.




