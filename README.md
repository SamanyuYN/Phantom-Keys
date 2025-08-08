# Phantom Keys

A virtual MIDI pi1. Run the program:
python phantom_keys.py
that uses hand tracking to play D-scale chords through finger gestures captured via webcam.

## Features
- Real-time hand tracking using MediaPipe
- D-scale chord generation using MIDI
- Finger gesture recognition for different chord combinations
- Visual feedback of detected hand gestures

## Requirements
- Python 3.11 (3.11.8 recommended)
- Webcam
- MIDI-compatible sound output (your system's audio should work by default)

## Installation

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # For Windows PowerShell
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Activate the virtual environment (if not already activated):
```bash
.\venv\Scripts\Activate.ps1  # For Windows PowerShell
```

2. Run the program:
```bash
python air_piano.py
```

3. Position your hand in front of the webcam.
4. Use different finger combinations to play different notes and chords:
   - Thumb only: D4
   - Index only: E4
   - Middle only: F#4
   - Ring only: G4
   - Pinky only: A4
   - All fingers (5): D major chord (D4-F#4-A4)
   - First three fingers: D4-E4-F#4
   - Last three fingers: F#4-G4-A4

5. Press 'q' to quit the program.

## How it Works
- The program uses MediaPipe for accurate hand tracking and finger detection
- Hand gestures are converted into binary finger states (up/down)
- Each finger combination maps to specific notes or chords in the D scale
- MIDI messages are sent through Pygame to produce the sound
- Real-time visual feedback shows detected fingers on the webcam feed

## Troubleshooting
- If you don't hear any sound, check your system's MIDI output settings
- Make sure you have adequate lighting for hand detection
- Keep your hand within the camera frame
- Perform clear finger movements for better detection
