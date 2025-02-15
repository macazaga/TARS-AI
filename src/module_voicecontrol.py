"""
module_voicecontrol.py

Voice Control Module for TARS-AI Application.

This module handles voice command processing for robot movement control,
mapping natural language commands to servo control functions.
"""

from module_servoctl import (
    height_neutral_to_up,
    torso_neutral_to_forwards,
    torso_bump,
    torso_return,
    turn_right,
    turn_left,
    neutral_to_down,
    down_to_up,
    portMainPlus,
    portMainMinus,
    starMainPlus,
    starMainMinus,
    portForarmPlus,
    portForarmMinus,
    starForarmPlus,
    starForarmMinus,
    portHandPlus,
    portHandMinus,
    starHandPlus,
    starHandMinus
)

def step_forward():
    """Sequence of movements to step forward"""
    height_neutral_to_up()
    torso_neutral_to_forwards()
    torso_bump()
    torso_return()

def sit():
    """Sequence for sitting down"""
    neutral_to_down()
    torso_neutral_to_forwards()
    down_to_up()

def stand():
    """Sequence for standing up"""
    torso_return()

# Movement command mappings
MOVEMENT_COMMANDS = {
    # Basic movement
    "move forward": {
        "function": step_forward,
        "response": "Moving forward.",
        "aliases": ["walk forward", "step forward", "go forward"]
    },
    "turn right": {
        "function": turn_right,
        "response": "Turning right.",
        "aliases": ["rotate right", "go right"]
    },
    "turn left": {
        "function": turn_left,
        "response": "Turning left.",
        "aliases": ["rotate left", "go left"]
    },
    
    # Pose commands
    "stand up": {
        "function": stand,
        "response": "Standing up.",
        "aliases": ["get up", "rise"]
    },
    "sit down": {
        "function": sit,
        "response": "Sitting down.",
        "aliases": ["lower", "crouch"]
    },

    # Arm control - Port side
    "port arm up": {
        "function": portMainPlus,
        "response": "Raising port arm.",
        "aliases": ["raise left arm", "left arm up"]
    },
    "port arm down": {
        "function": portMainMinus,
        "response": "Lowering port arm.",
        "aliases": ["lower left arm", "left arm down"]
    },
    "port forearm up": {
        "function": portForarmPlus,
        "response": "Raising port forearm.",
        "aliases": ["bend left arm up"]
    },
    "port forearm down": {
        "function": portForarmMinus,
        "response": "Lowering port forearm.",
        "aliases": ["bend left arm down"]
    },
    "port hand up": {
        "function": portHandPlus,
        "response": "Raising port hand.",
        "aliases": ["left hand up"]
    },
    "port hand down": {
        "function": portHandMinus,
        "response": "Lowering port hand.",
        "aliases": ["left hand down"]
    },

    # Arm control - Starboard side
    "starboard arm up": {
        "function": starMainPlus,
        "response": "Raising starboard arm.",
        "aliases": ["raise right arm", "right arm up"]
    },
    "starboard arm down": {
        "function": starMainMinus,
        "response": "Lowering starboard arm.",
        "aliases": ["lower right arm", "right arm down"]
    },
    "starboard forearm up": {
        "function": starForarmPlus,
        "response": "Raising starboard forearm.",
        "aliases": ["bend right arm up"]
    },
    "starboard forearm down": {
        "function": starForarmMinus,
        "response": "Lowering starboard forearm.",
        "aliases": ["bend right arm down"]
    },
    "starboard hand up": {
        "function": starHandPlus,
        "response": "Raising starboard hand.",
        "aliases": ["right hand up"]
    },
    "starboard hand down": {
        "function": starHandMinus,
        "response": "Lowering starboard hand.",
        "aliases": ["right hand down"]
    }
}

def process_movement_command(command: str) -> tuple[bool, str]:
    """
    Process a movement command and execute the corresponding function.
    
    Parameters:
    - command (str): The voice command to process
    
    Returns:
    - tuple[bool, str]: Success status and response message
    """
    # Convert command to lowercase for matching
    command = command.lower().strip()
    
    # Check direct commands and aliases
    for cmd, details in MOVEMENT_COMMANDS.items():
        if command == cmd or command in details["aliases"]:
            try:
                details["function"]()
                return True, details["response"]
            except Exception as e:
                return False, f"Error executing movement: {str(e)}"
    
    return False, "Command not recognized."