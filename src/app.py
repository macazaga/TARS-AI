"""
app.py

Main entry point for the TARS-AI application.

Initializes modules, loads configuration, and manages key threads for functionality such as:
- Speech-to-text (STT)
- Text-to-speech (TTS)
- Bluetooth control
- AI response generation

Run this script directly to start the application.
"""

# === Standard Libraries ===
import os
import sys
import threading
from datetime import datetime

# === Custom Modules ===
from module_config import load_config
from module_character import CharacterManager
from module_memory import MemoryManager
from module_stt import STTManager
from module_tts import update_tts_settings
from module_btcontroller import *
from module_main import initialize_managers, wake_word_callback, utterance_callback, post_utterance_callback, start_bt_controller_thread
from module_vision import initialize_blip

# === Constants and Globals ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)
sys.path.append(os.getcwd())

CONFIG = load_config()

# === Helper Functions ===
def init_app():
    """
    Performs initial setup for the application
    """
    
    print(f"LOAD: Script running from: {BASE_DIR}")
    #print(f"DEBUG: init_app() called")
    
    # Load the configuration
    CONFIG = load_config()
    if CONFIG['TTS']['ttsoption'] == 'xttsv2':
        update_tts_settings(CONFIG['TTS']['ttsurl'])

# === Main Application Logic ===
if __name__ == "__main__":
    # Perform initial setup
    init_app()

    # Create a shutdown event for global threads
    shutdown_event = threading.Event()

    # Initialize CharacterManager, MemoryManager
    char_manager = CharacterManager(config=CONFIG)
    memory_manager = MemoryManager(config=CONFIG, char_name=char_manager.char_name, char_greeting=char_manager.char_greeting)

    # Initialize STTManager
    stt_manager = STTManager(config=CONFIG, shutdown_event=shutdown_event)
    stt_manager.set_wake_word_callback(wake_word_callback)
    stt_manager.set_utterance_callback(utterance_callback)
    stt_manager.set_post_utterance_callback(post_utterance_callback)

    # Pass managers to main module
    initialize_managers(memory_manager, char_manager, stt_manager)

    # Start necessary threads
    bt_controller_thread = threading.Thread(target=start_bt_controller_thread, name="BTControllerThread", daemon=True)
    bt_controller_thread.start()

    # Initilize BLIP to speed up initial image capture
    if not CONFIG['VISION']['server_hosted']:
        initialize_blip()
    
    try:
        print(f"LOAD: TARS-AI v1.00 running.")
        # Start the STT thread
        stt_manager.start()

        while not shutdown_event.is_set():
            time.sleep(0.1) # Sleep to reduce CPU usage

    except KeyboardInterrupt:
        print(f"INFO: Stopping all threads and shutting down executor...")
        shutdown_event.set()  # Signal global threads to shutdown
        # executor.shutdown(wait=True)

    finally:
        stt_manager.stop()
        bt_controller_thread.join()
        print(f"INFO: All threads and executor stopped gracefully.")