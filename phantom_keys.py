import cv2
import mediapipe as mp
import pygame.midi
import time
from cvzone.HandTrackingModule import HandDetector

class PhantomKeys:
    def __init__(self):
        # Initialize the webcam
        self.cap = cv2.VideoCapture(0)
        
        # Initialize hand detector with high confidence, allowing 2 hands
        self.detector = HandDetector(detectionCon=0.8, maxHands=2)
        
        # Initialize MIDI
        pygame.midi.init()
        self.midi_output = pygame.midi.Output(pygame.midi.get_default_output_id())
        self.midi_output.set_instrument(0)  # Piano instrument
        
        # Define D-scale notes (D4 to D5)
        self.notes = {
            'D4': 62,
            'E4': 64,
            'F#4': 66,
            'G4': 67,
            'A4': 69,
            'B4': 71,
            'C#5': 73,
            'D5': 74
        }
        
        # Track currently playing notes for each hand
        self.active_notes_left = set()
        self.active_notes_right = set()

    def run(self):
        while True:
            # Get frame from webcam
            success, frame = self.cap.read()
            if not success:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Find hands
            hands, frame = self.detector.findHands(frame)
            
            if hands:
                for i, hand in enumerate(hands):
                    fingers = self.detector.fingersUp(hand)
                    
                    # Create binary number from fingers (thumb to pinky)
                    finger_code = sum(digit * (2 ** idx) for idx, digit in enumerate(fingers))
                    
                    # Map finger combinations to notes
                    # For left hand, transpose down an octave
                    if hand['type'] == 'Left':
                        self.play_chord(finger_code, transpose=-12, hand_type='Left')
                    else:
                        self.play_chord(finger_code, transpose=0, hand_type='Right')
                    
                    # Display finger state for each hand
                    pos_y = 30 + (i * 30)  # Offset text position for each hand
                    cv2.putText(frame, f'{hand["type"]} hand: {fingers}', (10, pos_y), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                # Stop all notes when no hand is detected
                self.stop_all_notes()
            
            # Show the frame
            cv2.imshow('Phantom Keys', frame)
            
            # Break loop on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        # Cleanup
        self.cleanup()

    def play_chord(self, finger_code, transpose=0, hand_type='Right'):
        # Define chord mappings based on finger combinations
        chord_mappings = {
            0: [],  # No fingers
            1: ['D4'],  # Thumb only
            2: ['E4'],  # Index only
            3: ['D4', 'E4'],  # Thumb + Index
            4: ['F#4'],  # Middle only
            8: ['G4'],  # Ring only
            16: ['A4'],  # Pinky only
            31: ['D4', 'F#4', 'A4'],  # All fingers (D major chord)
            7: ['D4', 'E4', 'F#4'],  # First three fingers
            28: ['F#4', 'G4', 'A4'],  # Last three fingers
        }
        
        # Get the notes for the current finger combination
        notes_to_play = chord_mappings.get(finger_code, [])
        
        # Use the appropriate active notes set based on hand type
        active_notes = self.active_notes_left if hand_type == 'Left' else self.active_notes_right
        
        # Stop notes that are no longer being played for this hand
        notes_to_stop = active_notes - set(notes_to_play)
        for note in notes_to_stop:
            note_value = self.notes[note] + transpose
            self.midi_output.note_off(note_value)
            active_notes.remove(note)
        
        # Start new notes for this hand
        for note in notes_to_play:
            if note not in active_notes:
                note_value = self.notes[note] + transpose
                self.midi_output.note_on(note_value, 100)
                active_notes.add(note)

    def stop_all_notes(self):
        # Stop notes for left hand
        for note in self.active_notes_left:
            self.midi_output.note_off(self.notes[note] - 12)  # -12 for left hand transposition
        self.active_notes_left.clear()
        
        # Stop notes for right hand
        for note in self.active_notes_right:
            self.midi_output.note_off(self.notes[note])
        self.active_notes_right.clear()

    def cleanup(self):
        self.stop_all_notes()
        self.cap.release()
        cv2.destroyAllWindows()
        pygame.midi.quit()

if __name__ == "__main__":
    phantom = PhantomKeys()
    phantom.run()
