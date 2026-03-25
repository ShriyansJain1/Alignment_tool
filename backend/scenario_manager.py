SCENARIOS = {}

def save_scenario(name, df):
    SCENARIOS[name] = df

def get_scenarios():
    return list(SCENARIOS.keys())

def get_scenario(name):
    return SCENARIOS.get(name)