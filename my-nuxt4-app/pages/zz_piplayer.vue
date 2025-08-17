<template>


    <Header />
 <main>
            <p><strong>Current Song:</strong> {{ pi_Currentitle }}</p>
            <p><strong>Status:</strong> {{ pi_Status.state }}</p>

            <div>
            <button @click="pi_Prev">Previous</button>
            <button @click="pi_Playpause">{{ pi_Status.state === 'play' ? 'Pause' : 'Play' }}</button>
            <button @click="pi_Stop">Stop</button>
            <button @click="pi_Next">Next</button>
          </div>

          <div>
            <label for="volume">Volume:</label>
            <input type="range" id="volume" min="0" max="100" v-model="pi_Status.volume" @change="set_pi_Volume" />
            <span>{{ pi_Status.volume }}%</span>
          </div>

          <div>
            <label><input type="checkbox" v-model="pi_Playmode.repeat" @change="set_pi_Playmode('repeat')" /> Repeat</label>
            <label><input type="checkbox" v-model="pi_Playmode.random" @change="set_pi_Playmode('random')" /> Random</label>
            <label><input type="checkbox" v-model="pi_Playmode.single" @change="set_pi_Playmode('single')" /> Single</label>
          </div>
   


        <section>
          <h3>Playlist</h3>
          <ul>
            <li v-for="(song, index) in pi_Playlist" :key="index" :class="{ 'is-playing': song.id === pi_Playerstatus.songid }">
              {{ song.title || song.file }}
              <button @click="selectAndPlaySong(song.id)">Play</button>
            </li>
          </ul>
        </section>


      <p v-if="error">{{ error }}</p>
    </main>

</template>



<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import Header from './Header.vue';


const pi_Status = ref({
  state: 'unknown',
  volume: 0,
  songid: -1,
  time: '0:0',
});
const pi_Playlist = ref<any[]>([]);

const pi_Playmode = ref({
  repeat: false,
  random: false,
  single: false,
});
const error = ref('');



const pi_Currentitle = computed(() => {
  if (pi_Status.value.songid !== -1 && pi_Playlist.value.length > 0) {
    const song = pi_Playlist.value.find(s => s.id === pi_Status.value.songid);
    if (song) {
      return song.title || song.file;
    }
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
    pi_Status.value = {
      state: data.state,
      volume: parseInt(data.volume),
      songid: parseInt(data.songid || -1),
      time: data.time,
    };
    pi_Playmode.value.repeat = data.repeat === '1';
    pi_Playmode.value.random = data.random === '1';
    pi_Playmode.value.single = data.single === '1';
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
    pi_Playlist.value = data;
    console.log(pi_Playlist.value)
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

const pi_Playpause = () => {
  if (pi_Status.value.state === 'play') {
    sendCommand('pause');
  } else {
    sendCommand('play');
  }
};

const pi_Stop = () => sendCommand('stop');
const pi_Next = () => sendCommand('next');
const pi_Prev = () => sendCommand('previous');

const set_pi_Volume = () => {
  sendCommand(`volume/${pi_Status.value.volume}`, 'PUT');
};

const set_pi_Playmode = (mode: 'repeat' | 'random' | 'single') => {
  const body: any = {};
  body[mode] = pi_Playmode.value[mode];
  sendCommand('play_mode', 'PUT', body);
};

const selectAndPlaySong = (songId: number) => {
  sendCommand(`select/${songId}`, 'POST');
};

onMounted(() => {
  fetchStatus();
  fetchPlaylist();
  // Optionally, set up an interval to refresh status periodically
  setInterval(fetchStatus, 5000);
  console.log(pi_Playlist.value)
});
</script>


