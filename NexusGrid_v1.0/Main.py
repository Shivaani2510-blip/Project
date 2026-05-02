import time
import os
from datetime import datetime

# Import all your custom modules from the folders
from core.controller import GridMaster
from core.physics_engine import SolarPhysics
from core.environment import WeatherEngine
from entities.buildings import House, Hospital, Factory
from entities.storage import BatteryBank
from utils.diagnostics import DataLogger
from utils.config_manager import ConfigManager
from utils.validator import InputValidator

def setup_workspace():
    """Ensures the directory structure exists before running."""
    folders = ['data', 'data/simulation_logs']
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)

def print_welcome_banner():
    print("="*60)
    print("      NEXUS-GRID v2.0: GLOBAL SUSTAINABILITY SUITE")
    print("          Aligned with UN SDGs 7, 11, and 13")
    print("="*60)

def main():
    # 1. Workspace and Config Setup
    setup_workspace()
    print_welcome_banner()
    
    config_tool = ConfigManager()
    settings = config_tool.initialize_config()
    print(f"[SYSTEM] Loaded Configuration for: {settings['city_name']}")

    # 2. Validation Layer (Safety Check)
    try:
        InputValidator.validate_inputs(10, settings['battery_capacity'])
    except ValueError as e:
        print(f"[CRITICAL ERROR] {e}")
        return

    # 3. Component Initialization
    battery = BatteryBank(settings['battery_capacity'])
    solar_phys = SolarPhysics()
    weather_sim = WeatherEngine()
    logger = DataLogger()
    
    # Initialize the "Brain"
    master_grid = GridMaster(battery, solar_phys, weather_sim)

    # 4. Populate the City (SDG 11)
    print("[SYSTEM] Connecting infrastructure to Smart Grid...")
    master_grid.add_building(Hospital())
    master_grid.add_building(Factory())
    for i in range(15): # Adding 15 Residential Houses
        master_grid.add_building(House(i))

    # 5. Execute 24-Hour Simulation Loop
    print(f"\n{'HOUR':<5} | {'GEN (kW)':<10} | {'BATT SOC':<10} | {'EVENT'}")
    print("-" * 60)

    for hour in range(24):
        # The Dispatcher decides energy flow
        results = master_grid.process_hour(hour, settings['panel_tilt'])
        
        # Log the hour's data for the CSV export
        logger.add_entry(hour, results['gen'], battery.current_energy)
        
        # Live Display
        battery_pct = (battery.current_energy / battery.max_cap) * 100
        event_msg = results['reports'][0] if results['reports'] else "Normal"
        
        print(f"{hour:02d}:00 | {results['gen']:<10.2f} | {battery_pct:<9.1f}% | {event_msg}")
        
        time.sleep(0.1) # Simulate real-time calculation

    # 6. Shutdown and Export
    print("-" * 60)
    logger.export_csv()
    
    # Final Sustainability Audit
    print("\n[AUDIT] Generating Final Sustainability Report...")
    print(f"Total CO2 Prevented: {master_grid.total_co2_saved:.2f} kg")
    print(f"Simulation saved to: data/simulation_logs/")
    print("="*60)

if __name__ == "__main__":
    main()



#This is the Orchestrator. It starts the "Clock" (the 24-hour loop). It calls the Weather engine, sends that data to the Controller, and updates the display. It’s like the conductor of an orchestra, making sure every other file plays its part at the right time.




