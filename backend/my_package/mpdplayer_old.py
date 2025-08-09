import mpd
from mpd import ConnectionError, CommandError

class MPDController:
    """
    A class to control the Music Player Daemon (MPD) using python-mpd2.
    """

    def __init__(self, host='localhost', port=6600, timeout=30):
        """
        Initializes the MPDController with connection details.

        Args:
            host (str): The hostname or IP address of the MPD server.
            port (int): The port number of the MPD server.
            timeout (int): Network timeout in seconds for MPD commands.
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.client = mpd.MPDClient()
        self.client.timeout = self.timeout
        self.is_connected = False

    def connect(self):
        """
        Connects to the MPD server.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        if self.is_connected:
            print("Already connected to MPD.")
            return True
        try:
            self.client.connect(self.host, self.port)
            self.is_connected = True
            print(f"Successfully connected to MPD at {self.host}:{self.port}")
            return True
        except ConnectionError as e:
            print(f"Connection Error: Could not connect to MPD at {self.host}:{self.port} - {e}")
            self.is_connected = False
            return False
        except Exception as e:
            print(f"An unexpected error occurred during connection: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """
        Disconnects from the MPD server.
        """
        if self.is_connected:
            try:
                self.client.close()      # Send the 'close' command to MPD
                self.client.disconnect() # Disconnect the socket
                self.is_connected = False
                print("Disconnected from MPD.")
            except ConnectionError:
                print("Already disconnected or connection lost.")
                self.is_connected = False # Ensure state is updated
            except Exception as e:
                print(f"An error occurred during disconnection: {e}")
                self.is_connected = False
        else:
            print("Not connected to MPD.")

    def _execute_command(self, command_func, *args, **kwargs):
        """
        Helper method to execute MPD commands and handle common errors.

        Args:
            command_func (callable): The MPDClient method to call.
            *args: Positional arguments for the command_func.
            **kwargs: Keyword arguments for the command_func.

        Returns:
            Any: The result of the command, or None if an error occurred.
        """
        if not self.is_connected:
            print("Error: Not connected to MPD. Please connect first.")
            return None
        try:
            return command_func(*args, **kwargs)
        except CommandError as e:
            print(f"MPD Command Error: {e}")
            return None
        except ConnectionError as e:
            print(f"Connection lost while executing command: {e}. Attempting to reconnect...")
            self.is_connected = False # Mark as disconnected
            if self.connect(): # Try to reconnect
                return self._execute_command(command_func, *args, **kwargs) # Retry command
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def get_status(self):
        """
        Gets the current status of the MPD server.

        Returns:
            dict: A dictionary containing the MPD status, or None on error.
        """
        status = self._execute_command(self.client.status)
        if status:
            print("\n--- MPD Status ---")
            for key, value in status.items():
                print(f"  {key}: {value}")
            return status
        return None

    def play(self, song_pos=None):
        """
        Starts playing the current playlist, or a specific song by position.

        Args:
            song_pos (int, optional): The position of the song to play (0-indexed).
                                      If None, plays the current song or starts from the beginning.
        """
        if song_pos is not None:
            print(f"Playing song at position: {song_pos}")
            self._execute_command(self.client.play, song_pos)
        else:
            print("Playing current song.")
            self._execute_command(self.client.play)

    def pause(self):
        """Pauses playback."""
        print("Pausing playback.")
        self._execute_command(self.client.pause, 1)

    def resume(self):
        """Resumes playback."""
        print("Resuming playback.")
        self._execute_command(self.client.pause, 0)

    def stop(self):
        """Stops playback."""
        print("Stopping playback.")
        self._execute_command(self.client.stop)

    def next_song(self):
        """Plays the next song in the playlist."""
        print("Playing next song.")
        self._execute_command(self.client.next)

    def previous_song(self):
        """Plays the previous song in the playlist."""
        print("Playing previous song.")
        self._execute_command(self.client.previous)

    def get_play_modes(self):
        """
        Gets the current state of repeat, random, single, and consume modes.

        Returns:
            dict: A dictionary with boolean values for each mode, or None on error.
        """
        status = self.get_status()
        if status:
            modes = {
                'repeat': status.get('repeat', '0') == '1',
                'random': status.get('random', '0') == '1',
                'single': status.get('single', '0') == '1',
                'consume': status.get('consume', '0') == '1'
            }
            print("\n--- Current Play Modes ---")
            for mode, state in modes.items():
                print(f"  {mode.capitalize()}: {state}")
            return modes
        return None

    def set_repeat(self, enable: bool):
        """Sets the repeat mode."""
        action = "enabling" if enable else "disabling"
        print(f"{action.capitalize()} repeat mode.")
        self._execute_command(self.client.repeat, 1 if enable else 0)

    def set_random(self, enable: bool):
        """Sets the random (shuffle) mode."""
        action = "enabling" if enable else "disabling"
        print(f"{action.capitalize()} random (shuffle) mode.")
        self._execute_command(self.client.random, 1 if enable else 0)

    def set_single(self, enable: bool):
        """Sets the single song mode."""
        action = "enabling" if enable else "disabling"
        print(f"{action.capitalize()} single song mode.")
        self._execute_command(self.client.single, 1 if enable else 0)

    def set_consume(self, enable: bool):
        """Sets the consume mode (removes played songs from playlist)."""
        action = "enabling" if enable else "disabling"
        print(f"{action.capitalize()} consume mode.")
        self._execute_command(self.client.consume, 1 if enable else 0)

    def get_volume(self):
        """
        Gets the current volume level.

        Returns:
            int: The current volume (0-100), or None on error.
        """
        status = self.get_status()
        if status and 'volume' in status:
            volume = int(status['volume'])
            print(f"Current volume: {volume}")
            return volume
        return None

    def set_volume(self, volume: int):
        """
        Sets the volume level.

        Args:
            volume (int): The desired volume level (0-100).
        """
        if 0 <= volume <= 100:
            print(f"Setting volume to: {volume}")
            self._execute_command(self.client.setvol, volume)
        else:
            print("Volume must be between 0 and 100.")

    def add_to_playlist(self, uri: str):
        """
        Adds a song (URI) to the current playlist.

        Args:
            uri (str): The URI of the song to add (e.g., 'path/to/song.mp3', 'http://stream.url').
        """
        print(f"Adding '{uri}' to playlist.")
        self._execute_command(self.client.add, uri)


    def clear_playlist(self):
        """Clears the current playlist."""
        print("Clearing current playlist.")
        self._execute_command(self.client.clear)
    
    def save_playlist(self,filename: str):
        """Save the current playlist."""
        print("Saving current playlist.")
        self._execute_command(self.client.save(filename))

    def get_playlist(self):
        """Get the current playlist."""
        print("Getting current playlist.")
        playlist= self._execute_command(self.client.playlist())   
        return playlist
    def get_current_song(self):
        """
        Gets information about the currently playing song.

        Returns:
            dict: A dictionary containing song details, or None if no song is playing or on error.
        """
        current_song = self._execute_command(self.client.currentsong)
        if current_song:
            print("\n--- Current Song ---")
            for key, value in current_song.items():
                print(f"  {key}: {value}")
            return current_song
        print("No song currently playing.")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    # Create an instance of the MPDController
    # Replace 'localhost' and 6600 with your MPD server's IP/hostname and port if different
    mpd_ctrl = MPDController(host='localhost', port=6600)

    # 1. Connect to MPD
    if mpd_ctrl.connect():
        # 2. Get current status
        mpd_ctrl.get_status()

        # 3. Get current play modes
        mpd_ctrl.get_play_modes()

        # 4. Set some play modes
        mpd_ctrl.set_repeat(True)
        mpd_ctrl.set_random(False) # Ensure random is off for sequence
        mpd_ctrl.set_single(False)
        mpd_ctrl.set_consume(False)
        mpd_ctrl.get_play_modes()

        # 5. Clear current playlist and add some dummy songs (replace with actual paths/URIs)
        mpd_ctrl.clear_playlist()
        # You'll need to have some music files accessible by your MPD server
        # For example, if MPD's music_directory is '/var/lib/mpd/music'
        # and you have 'song1.mp3' and 'song2.mp3' inside it.
        # If you don't have actual songs, these commands will likely fail unless MPD can find them.
        # For demonstration, you might need to add actual paths or stream URIs.
        # mpd_ctrl.add_to_playlist("Music/song1.mp3") # Example path relative to MPD's music_directory
        # mpd_ctrl.add_to_playlist("Music/song2.mp3")
        # mpd_ctrl.add_to_playlist("http://icecast.radiofrance.fr/fip-midfi.mp3") # Example internet radio stream

        # Let's assume some songs are already in the playlist for playback tests
        print("\nAssuming playlist has songs for playback tests...")

        # 6. Play
        mpd_ctrl.play()

        # 7. Get current song info
        mpd_ctrl.get_current_song()

        # 8. Pause and Resume
        import time
        time.sleep(5) # Play for 5 seconds
        mpd_ctrl.pause()
        time.sleep(2) # Pause for 2 seconds
        mpd_ctrl.resume()
        time.sleep(3) # Resume for 3 seconds

        # 9. Next and Previous
        mpd_ctrl.next_song()
        time.sleep(3)
        mpd_ctrl.previous_song()
        time.sleep(3)

        # 10. Get and Set Volume
        mpd_ctrl.get_volume()
        mpd_ctrl.set_volume(70)
        mpd_ctrl.get_volume()

        # 11. Stop playback
        mpd_ctrl.stop()

        # 12. Disconnect
        mpd_ctrl.disconnect()
    else:
        print("Failed to connect to MPD. Please ensure MPD is running and accessible.")
