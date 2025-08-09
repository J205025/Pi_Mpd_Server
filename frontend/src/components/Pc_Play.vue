<template>
  <div>
    <Header />
    <main>
      <h2>PC Play</h2>
      <p>This is the PC player.</p>

      <section class="player-controls">
        <h3>Player Controls</h3>
        <div class="current-song">
          <p><strong>Current Song:</strong> {{ currentSongTitle }}</p>
          <p><strong>Status:</strong> {{ isPlaying ? 'Playing' : 'Paused' }}</p>
        </div>

        <div class="buttons">
          <button @click="previousSongLocal">Previous</button>
          <button @click="togglePlayPauseLocal">{{ isPlaying ? 'Pause' : 'Play' }}</button>
          <button @click="stopPlaybackLocal">Stop</button>
          <button @click="nextSongLocal">Next</button>
        </div>

        <div class="volume-control">
          <label for="volume">Volume:</label>
          <input type="range" id="volume" min="0" max="100" v-model="volume" @input="setVolumeLocal" />
          <span>{{ volume }}%</span>
        </div>
      </section>

      <section class="playlist">
        <h3>My Personal Playlist</h3>
        <button @click="savePersonalPlaylist">Save My Playlist</button>
        <ul>
          <li v-for="(song, index) in playlist" :key="index" :class="{ 'is-playing': index === currentSongIndex }">
            {{ song }}
            <button @click="playSong(index)">Play</button>
          </li>
        </ul>
      </section>

      <section class="master-playlist">
        <h3>Available Songs</h3>
        <ul>
          <li v-for="(song, index) in masterPlaylist" :key="index">
            {{ song }}
            <button @click="addSongToPersonalPlaylist(song)">Add to My Playlist</button>
          </li>
        </ul>
      </section>

      <audio ref="audioElement" @ended="nextSongLocal"></audio>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject } from 'vue';
import Header from './Header.vue';

const playlist = ref<string[]>([]); // User's personal playlist
const masterPlaylist = ref<string[]>([]); // All available songs
const audioElement = ref<HTMLAudioElement | null>(null);
const currentSongIndex = ref(-1);
const isPlaying = ref(false);
const volume = ref(50); // Initial volume

// Inject the setGlobalError function
const setGlobalError = inject('setGlobalError') as (message: string) => void;

const currentSongTitle = computed(() => {
  if (currentSongIndex.value !== -1 && playlist.value.length > currentSongIndex.value) {
    return playlist.value[currentSongIndex.value];
  }
  return 'No song playing';
});

const getAuthHeaders = () => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  const token = localStorage.getItem('access_token');
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
};

const fetchPlaylist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_playlist', {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch personal playlist');
    }
    const data = await response.json();
    playlist.value = data;
  } catch (err: any) {
    setGlobalError(err.message);
  }
};

const fetchMasterPlaylist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/master_playlist', {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch master playlist');
    }
    const data = await response.json();
    masterPlaylist.value = data;
  } catch (err: any) {
    setGlobalError(err.message);
  }
};

const playSong = (index: number) => {
  if (audioElement.value && playlist.value[index]) {
    audioElement.value.src = `http://127.0.0.1:8001/music/${playlist.value[index]}`;
    audioElement.value.play();
    currentSongIndex.value = index;
    isPlaying.value = true;
  }
};

const togglePlayPauseLocal = () => {
  if (audioElement.value) {
    if (isPlaying.value) {
      audioElement.value.pause();
    } else {
      audioElement.value.play();
    }
    isPlaying.value = !isPlaying.value;
  }
};

const stopPlaybackLocal = () => {
  if (audioElement.value) {
    audioElement.value.pause();
    audioElement.value.currentTime = 0;
    isPlaying.value = false;
    currentSongIndex.value = -1; // Reset current song
  }
};

const nextSongLocal = () => {
  if (playlist.value.length > 0) {
    const nextIndex = (currentSongIndex.value + 1) % playlist.value.length;
    playSong(nextIndex);
  }
};

const previousSongLocal = () => {
  if (playlist.value.length > 0) {
    const prevIndex = (currentSongIndex.value - 1 + playlist.value.length) % playlist.value.length;
    playSong(prevIndex);
  }
};

const setVolumeLocal = () => {
  if (audioElement.value) {
    audioElement.value.volume = volume.value / 100;
  }
};

const addSongToPersonalPlaylist = (song: string) => {
  if (!playlist.value.includes(song)) {
    playlist.value.push(song);
  }
};

const savePersonalPlaylist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_playlist', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(playlist.value),
    });
    if (!response.ok) {
      throw new Error('Failed to save personal playlist');
    }
    alert('Playlist saved successfully!');
  } catch (err: any) {
    setGlobalError(err.message);
  }
};

onMounted(() => {
  fetchPlaylist();
  fetchMasterPlaylist();
  if (audioElement.value) {
    audioElement.value.volume = volume.value / 100; // Set initial volume
  }
});
</script>

<style scoped>
main {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.player-controls, .playlist, .master-playlist {
  margin-top: 2rem;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.player-controls h3, .playlist h3, .master-playlist h3 {
  text-align: center;
  margin-bottom: 1rem;
  color: #333;
}

.current-song {
  text-align: center;
  margin-bottom: 1rem;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.buttons button {
  padding: 0.8rem 1.5rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.buttons button:hover {
  background-color: #369f75;
}

.volume-control {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.play-modes {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.playlist ul, .master-playlist ul {
  list-style: none;
  padding: 0;
}

.playlist li, .master-playlist li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.playlist li:last-child, .master-playlist li:last-child {
  border-bottom: none;
}

.playlist li button, .master-playlist li button {
  padding: 0.3rem 0.8rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.playlist li button:hover, .master-playlist li button:hover {
  background-color: #0056b3;
}

.playlist li.is-playing {
  font-weight: bold;
  color: #42b983;
}

/* Removed .error style */
</style>
