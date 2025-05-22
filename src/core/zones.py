
GAME_GRID = [
    None,
    "Healing",
    None,
    "Savings",
    "Savings",
    None,
    "Gold Bar",
    "Gold Bar",
    "Gold Bar",
    None,
    "Real Estate",
    "Real Estate",
    None,
    "Crypto-Currency",
    "Crypto-Currency",
    "Crypto-Currency",
    "Crypto-Currency",
    None,
]


GAME_STATES = {

    "Healing": {
        "lifespan": 100,
        "strength": 50,
        "property": 0,
        "probability": (0., 0.2),
    },

    "Savings": {
        "lifespan": 10,
        "property": 10,
        "strength": 0,
        "probability": (0.1, 0.),
    },

    "Gold Bar": {
        "lifespan": 20,
        "strength": (-60, -20),
        "property": (10, 100),
        "probability": (0.02, 0.05),
    },

    "Real Estate": {
        "lifespan": 50,
        "strength": (-100, -25),
        "property": (100, 500),
        "probability": (0.01, 0.025),
    },

    "Crypto-Currency": {
        "lifespan": 10,
        "strength": (-50, -10),
        "property": (10, 50),
        "probability": (0.01, 0.025),
    },
}


