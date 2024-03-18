# #------------- GOAT | T.M.W.H.N.L -------------
# #------------- PLUTO | O.O.T.S.S -------------
import sounddevice as sd  # Import the sounddevice library for recording audio
import numpy as np  # Import the numpy library for numerical operations
import wave  # Import the wave library for working with WAV audio files
import pygame  # Import the pygame library for playing audio
import tkinter as tk  # Import the tkinter library for creating GUIs
from tkinter import ttk  # Import ttk from tkinter for themed widgets
from tkinter import messagebox  # Import messagebox from tkinter for displaying message boxes

# Define global variables for duration entry, file name entry, status label, and recording flag
duration_entry = None
file_name_entry = None
status_label = None
recording = None

# Function to record audio
def record_audio():
    global recording
    
    try:
        duration = int(duration_entry.get())  # Get the duration entered by the user
        if duration <= 0:  # Check if duration is valid
            raise ValueError
        file_name = file_name_entry.get()  # Get the file name entered by the user
        if not file_name:  # Check if file name is provided
            raise ValueError
        
        status_label.config(text="Recording...")  # Update status label to indicate recording
        
        # Set audio parameters
        fs = 44100  # Sample rate
        seconds = duration  # Duration of recording

        # Start recording
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
    except ValueError:  # Handle invalid input errors
        messagebox.showerror("Error", "Invalid duration or file name.")  # Show error message in case of invalid input

# Function to stop recording
def stop_recording():
    global recording
    
    if recording is not None:
        sd.stop()  # Stop recording
        file_name = file_name_entry.get()  # Get the file name entered by the user
        
        # Save recording to file
        if file_name:
            wavefile = wave.open(file_name, 'wb')
            wavefile.setnchannels(1)
            wavefile.setsampwidth(2)
            wavefile.setframerate(44100)
            wavefile.writeframes(recording.tobytes())
            wavefile.close()
            
            status_label.config(text="Finished recording.")  # Update status label to indicate finished recording
            messagebox.showinfo("Info", "Recording finished.")  # Show message box with recording completion message
        else:
            messagebox.showerror("Error", "File name not provided.")  # Show error message if file name is not provided
        recording = None
    else:
        messagebox.showinfo("Info", "No recording in progress.")  # Show info message if no recording is in progress

# Function to play recorded audio
def play_audio():
    try:
        file_name = file_name_entry.get()  # Get the file name entered by the user
        if not file_name:  # Check if file name is provided
            raise ValueError
        
        pygame.init()  # Initialize pygame
        pygame.mixer.music.load(file_name)  # Load audio file
        pygame.mixer.music.play()  # Play audio
    except Exception as e:  # Handle errors
        messagebox.showerror("Error", str(e))  # Show error message in case of any exception

# Function to restart recording
def restart_recording():
    file_name_entry.delete(0, tk.END)  # Clear file name entry
    duration_entry.delete(0, tk.END)  # Clear duration entry
    status_label.config(text="")  # Clear status label

# Main function
def main():
    global duration_entry, file_name_entry, status_label
    
    root = tk.Tk()  # Create main application window
    root.title("Audio Recorder")  # Set window title

    # Create and configure the main frame
    main_frame = ttk.Frame(root, padding="20")
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # File name entry
    file_name_label = ttk.Label(main_frame, text="File name:")  # Create label for file name entry
    file_name_label.grid(row=0, column=0, sticky=tk.W)  # Place label in main frame
    file_name_entry = ttk.Entry(main_frame, width=30)  # Create entry field for file name
    file_name_entry.grid(row=0, column=1, sticky=tk.W)  # Place entry field in main frame

    # Duration entry
    duration_label = ttk.Label(main_frame, text="Duration (seconds):")  # Create label for duration entry
    duration_label.grid(row=1, column=0, sticky=tk.W)  # Place label in main frame
    duration_entry = ttk.Entry(main_frame, width=10)  # Create entry field for duration
    duration_entry.grid(row=1, column=1, sticky=tk.W)  # Place entry field in main frame

    # Record button
    record_button = ttk.Button(main_frame, text="Record", command=record_audio)  # Create record button
    record_button.grid(row=2, column=0, columnspan=2, pady=10)  # Place button in main frame
    
    # Stop recording button
    stop_button = ttk.Button(main_frame, text="Stop Recording", command=stop_recording)  # Create stop recording button
    stop_button.grid(row=3, column=0, columnspan=2, pady=10)  # Place button in main frame
    
    # Status label
    status_label = ttk.Label(main_frame, text="")  # Create status label
    status_label.grid(row=4, column=0, columnspan=2)  # Place status label in main frame

    # Play button
    play_button = ttk.Button(main_frame, text="Play", command=play_audio)  # Create play button
    play_button.grid(row=5, column=0, columnspan=2, pady=10)  # Place button in main frame
    
    # Restart button
    restart_button = ttk.Button(main_frame, text="Restart", command=restart_recording)  # Create restart button
    restart_button.grid(row=6, column=0, columnspan=2, pady=10)  # Place button in main frame

    root.mainloop()  # Run the main event loop

if __name__ == "__main__":
    main()  # Call the main function if script is executed directly
