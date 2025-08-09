<template>
  <div>
    <Header />
    <main>
      <h2>Pi Play</h2>
      <p>This is the Pi player.</p>

      <section class="player-controls">
        <h3>Player Controls</h3>
        <div class="current-song">
          <p><strong>Current Song:</strong> {{ currentSongTitle }}</p>
          <p><strong>Status:</strong> {{ playerStatus.state }}</p>
        </div>

        <div class="buttons">
          <button @click="previousSong">Previous</button>
          <button @click="togglePlayPause">{{ playerStatus.state === 'play' ? 'Pause' : 'Play' }}</button>
          <button @click="stopPlayback">Stop</button>
          <button @click="nextSong">Next</button>
        </div>

        <div class="volume-control">
          <label for="volume">Volume:</label>
          <input type="range" id="volume" min="0" max="100" v-model="playerStatus.volume" @change="setVolume" />
          <span>{{ playerStatus.volume }}%</span>
        </div>

        <div class="play-modes">
          <label>
            <input type="checkbox" v-model="playModes.repeat" @change="setPlayMode('repeat')" /> Repeat
          </label>
          <label>
            <input type="checkbox" v-model="playModes.random" @change="setPlayMode('random')" /> Random
          </label>
          <label>
            <input type="checkbox" v-model="playModes.single" @change="setPlayMode('single')" /> Single
          </label>
        </div>
      </section>

      <section class="playlist">
        <h3>Playlist</h3>
        <ul>
          <li v-for="(song, index) in playlist" :key="index" :class="{ 'is-playing': index === playerStatus.songid }">
            {{ song.title || song.file }}
            <button @click="selectAndPlaySong(index)">Play</button>
          </li>
        </ul>
      </section>

      <p v-if="error" class="error">{{ error }}</p>
    </main>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import Header from './Header.vue';


const playerStatus = ref({
  state: 'unknown',
  volume: 0,
  songid: -1,
  time: '0:0',
});
const playlist = ref<any[]>([]);
const error = ref('');
const playModes = ref({
  repeat: false,
  random: false,
  single: false,
});

const currentSongTitle = computed(() => {
  if (playerStatus.value.songid !== -1 && playlist.value.length > playerStatus.value.songid) {
    const song = playlist.value[playerStatus.value.songid];
    return song.title || song.file;
  }
  return 'No song playing';
});

const fetchStatus = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/status');
    if (!response.ok) {
      throw new Error('Failed to fetch status');
    }
    const data = await response.json();
    playerStatus.value = {
      state: data.state,
      volume: parseInt(data.volume),
      songid: parseInt(data.songid || -1),
      time: data.time,
    };
    playModes.value.repeat = data.repeat === '1';
    playModes.value.random = data.random === '1';
    playModes.value.single = data.single === '1';
  } catch (err: any) {
    error.value = err.message;
  }
};

const fetchPlaylist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pi_playlist');
    if (!response.ok) {
      throw new Error('Failed to fetch playlist');
    }
    const data = await response.json();
    playlist.value = data;
  } catch (err: any) {
    error.value = err.message;
  }
};

const sendCommand = async (endpoint: string, method: string = 'POST', body: any = null) => {
  try {
    const options: RequestInit = { method };
    if (body) {
      options.headers = { 'Content-Type': 'application/json' };
      options.body = JSON.stringify(body);
    }
    const response = await fetch(`http://127.0.0.1:8001/${endpoint}`, options);
    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || `Failed to ${endpoint}`);
    }
    await fetchStatus(); // Refresh status after command
    await fetchPlaylist(); // Refresh playlist after command
  } catch (err: any) {
    error.value = err.message;
  }
};

const togglePlayPause = () => {
  if (playerStatus.value.state === 'play') {
    sendCommand('pause');
  } else {
    sendCommand('play');
  }
};

const stopPlayback = () => sendCommand('stop');
const nextSong = () => sendCommand('next');
const previousSong = () => sendCommand('previous');

const setVolume = () => {
  sendCommand(`volume/${playerStatus.value.volume}`, 'PUT');
};

const setPlayMode = (mode: 'repeat' | 'random' | 'single') => {
  const body: any = {};
  body[mode] = playModes.value[mode];
  sendCommand('play_mode', 'PUT', body);
};

const selectAndPlaySong = (index: number) => {
  sendCommand(`select/${index}`, 'POST');
};

onMounted(() => {
  fetchStatus();
  fetchPlaylist();
  // Optionally, set up an interval to refresh status periodically
  // setInterval(fetchStatus, 5000);
});
</script>

<style scoped>
main {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.player-controls, .playlist {
  margin-top: 2rem;
  padding: 1.5rem;
  border: 1px solid #eee;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.player-controls h3, .playlist h3 {
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

.playlist ul {
  list-style: none;
  padding: 0;
}

.playlist li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.playlist li:last-child {
  border-bottom: none;
}

.playlist li button {
  padding: 0.3rem 0.8rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.playlist li button:hover {
  background-color: #0056b3;
}

.playlist li.is-playing {
  font-weight: bold;
  color: #42b983;
}

.error {
  color: red;
  margin-top: 1rem;
}
</style>
