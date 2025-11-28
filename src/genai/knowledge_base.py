"""
Energy Efficiency Knowledge Base
Curated information for RAG chatbot recommendations
"""

ENERGY_EFFICIENCY_KNOWLEDGE = [
    {
        "topic": "HVAC Optimization",
        "content": """
        HVAC systems account for 40-50% of building energy consumption. Key optimization strategies:

        1. Temperature Setpoints: Maintain 22-24°C in summer, 20-22°C in winter
        2. Scheduling: Reduce HVAC during non-occupied hours (can save 20-30%)
        3. Regular Maintenance: Clean filters monthly, inspect systems quarterly
        4. Zoning: Implement zone-based controls to avoid cooling/heating unused areas
        5. Variable Speed Drives: Can reduce HVAC energy use by 25-40%

        Expected savings: 15-30% energy reduction
        Payback period: 1-3 years for controls, 3-7 years for equipment upgrades
        """,
        "category": "hvac",
        "priority": "high"
    },
    {
        "topic": "Lighting Efficiency",
        "content": """
        Lighting accounts for 15-25% of commercial building energy use. Strategies:

        1. LED Conversion: Replace fluorescent/incandescent with LEDs (60-80% savings)
        2. Occupancy Sensors: Automatic shutoff in unoccupied spaces (20-30% savings)
        3. Daylight Harvesting: Dim artificial lights when natural light is sufficient
        4. Task Lighting: Focus light where needed, reduce ambient lighting
        5. Light Color: Use 4000K-5000K for offices, 2700K-3000K for common areas

        Expected savings: 30-50% lighting energy reduction
        Payback period: 2-5 years
        """,
        "category": "lighting",
        "priority": "high"
    },
    {
        "topic": "Building Envelope",
        "content": """
        Building envelope improvements reduce heating/cooling loads:

        1. Insulation: Add to walls, roof, and foundation (20-30% HVAC savings)
        2. Air Sealing: Seal leaks around doors, windows, penetrations
        3. Window Upgrades: Install double/triple pane, low-E coating windows
        4. Cool Roofs: Reflective roofing reduces cooling loads by 10-15%
        5. Shading: External shading devices reduce solar heat gain

        Expected savings: 15-25% overall energy reduction
        Payback period: 5-15 years depending on climate
        """,
        "category": "envelope",
        "priority": "medium"
    },
    {
        "topic": "Renewable Energy",
        "content": """
        On-site renewable energy reduces grid dependency and emissions:

        1. Solar PV: Panels on roof or parking structures (offset 30-70% of electricity)
        2. Solar Thermal: For hot water heating in facilities with high demand
        3. Geothermal: Ground-source heat pumps (50-70% heating/cooling savings)
        4. Wind: Small turbines for windy locations
        5. Combined Heat and Power (CHP): Generate electricity and use waste heat

        Expected savings: 25-100% energy cost reduction
        Payback period: 7-15 years for solar, 10-20 years for geothermal
        Carbon reduction: 30-100% depending on system size
        """,
        "category": "renewables",
        "priority": "medium"
    },
    {
        "topic": "Energy Monitoring",
        "content": """
        Real-time energy monitoring enables data-driven decisions:

        1. Sub-metering: Monitor by zone, equipment, or end-use
        2. Building Management Systems (BMS): Centralized control and monitoring
        3. Energy Dashboards: Visual displays for staff awareness
        4. Anomaly Detection: AI-powered alerts for unusual consumption
        5. Benchmarking: Compare performance to similar buildings

        Expected savings: 5-15% through improved awareness and quick issue detection
        Payback period: 1-3 years
        """,
        "category": "monitoring",
        "priority": "high"
    },
    {
        "topic": "Plug Loads and Equipment",
        "content": """
        Office equipment and plug loads account for 20-30% of energy use:

        1. Energy Star Equipment: Choose certified computers, monitors, appliances
        2. Power Management: Enable sleep modes on computers and displays
        3. Smart Power Strips: Eliminate phantom loads (5-10% savings)
        4. Equipment Scheduling: Automatic shutoff during non-business hours
        5. Right-sizing: Don't oversize equipment for actual needs

        Expected savings: 15-25% plug load reduction
        Payback period: 1-3 years
        """,
        "category": "equipment",
        "priority": "medium"
    },
    {
        "topic": "Behavioral and Operational",
        "content": """
        Low-cost behavioral changes can deliver quick wins:

        1. Occupant Training: Educate staff on energy-saving practices
        2. Thermostat Management: Avoid extreme setpoints, use programmable controls
        3. Equipment Shutdown: Turn off lights, computers when not in use
        4. Dress Code: Allow seasonal dress codes to reduce HVAC demand
        5. Energy Champions: Designate energy-conscious team members

        Expected savings: 5-15% energy reduction
        Cost: Minimal, mostly time investment
        Payback: Immediate
        """,
        "category": "behavioral",
        "priority": "high"
    },
    {
        "topic": "Water Heating",
        "content": """
        Water heating strategies for buildings with significant hot water demand:

        1. Heat Pump Water Heaters: 2-3x more efficient than electric resistance
        2. Solar Thermal: Pre-heat water before conventional heating
        3. Point-of-Use Heaters: Reduce distribution losses
        4. Insulation: Insulate tanks and pipes to reduce standby losses
        5. Low-Flow Fixtures: Reduce hot water demand

        Expected savings: 20-40% water heating energy
        Payback period: 3-7 years
        """,
        "category": "water_heating",
        "priority": "low"
    },
    {
        "topic": "Data Centers and IT",
        "content": """
        For buildings with data centers or server rooms:

        1. Virtualization: Reduce number of physical servers (20-40% savings)
        2. Hot/Cold Aisle Containment: Improve cooling efficiency
        3. Raise Temperature Setpoints: Modern equipment tolerates 24-27°C
        4. Free Cooling: Use outside air when temperature permits
        5. Energy-Efficient Servers: Choose ENERGY STAR certified equipment

        Expected savings: 25-40% data center energy reduction
        Payback period: 2-5 years
        """,
        "category": "data_center",
        "priority": "medium"
    },
    {
        "topic": "Quick Wins - Low/No Cost",
        "content": """
        Immediate actions with minimal investment:

        1. Adjust thermostat setpoints by 1-2°C
        2. Turn off lights in unoccupied areas
        3. Close blinds to reduce solar heat gain in summer
        4. Fix air leaks around doors and windows
        5. Clean HVAC filters regularly
        6. Disable screensavers, enable computer sleep mode
        7. Unplug unused equipment
        8. Schedule HVAC to match occupancy

        Expected savings: 5-10% immediate energy reduction
        Cost: Under $500
        Payback: Less than 3 months
        """,
        "category": "quick_wins",
        "priority": "high"
    }
]

def get_knowledge_by_category(category: str):
    """Get knowledge base entries by category"""
    return [k for k in ENERGY_EFFICIENCY_KNOWLEDGE if k["category"] == category]

def get_knowledge_by_priority(priority: str):
    """Get knowledge base entries by priority"""
    return [k for k in ENERGY_EFFICIENCY_KNOWLEDGE if k["priority"] == priority]

def get_all_topics():
    """Get list of all available topics"""
    return [k["topic"] for k in ENERGY_EFFICIENCY_KNOWLEDGE]

def search_knowledge(query: str):
    """Simple keyword search in knowledge base"""
    query_lower = query.lower()
    results = []

    for item in ENERGY_EFFICIENCY_KNOWLEDGE:
        if (query_lower in item["topic"].lower() or
            query_lower in item["content"].lower() or
            query_lower in item["category"].lower()):
            results.append(item)

    return results
