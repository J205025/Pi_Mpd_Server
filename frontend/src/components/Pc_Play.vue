<template>
 <Header />
      <section>
        <h3>Player Controls</h3>
        <div>
          <p><strong>Current Song:</strong> {{ pc_Currenttitle }}</p>
          <p><strong>Status:</strong> {{ pc_Playing? 'Playing' : 'Paused' }}</p>
        </div>

        <div>
          <button @click="pc_Prev">Previous</button>
          <button @click="pc_Playpause">{{ pc_Playing? 'Pause' : 'Play' }}</button>
          <button @click="pc_Stop">Stop</button>
          <button @click="pc_Next">Next</button>
        </div>

        <div>
          <label for="volume">Volume:</label>
          <input type="range" id="volume" min="0" max="100" v-model="pc_Volume" @input="set_pc_Volume" />
          <span>{{ pc_Volume }}%</span>
        </div>
      </section>

      <div>
        <section>
          <h3>My Personal Playlist</h3>
          <button @click="savePersonalPlaylist">Save My Playlist</button>
          <ul>
            <li v-for="(song, index) in pc_playlist" :key="index" :class="{ 'is-playing': index === pc_Index }">
              {{ song }}
              <button @click="pc_Playindex(index)">Play</button>
            </li>
          </ul>
        </section>

        <section>
          <h3>Available Songs</h3>
          <ul>
            <li v-for="(song, index) in masterPlaylist" :key="index">
              {{ song }}
              <button @click="pc_Addsong(song)">Add to My Playlist</button>
            </li>
          </ul>
        </section>
      </div>

      <audio ref="audioElement" @ended="pc_Next"></audio>

<div style="display:none" ><audio id="radioPc"> <source src="https://stream.live.vc.bbcmedia.co.uk/bbc_world_service" type="audio/mpeg">    你的瀏覽器不支援 audio tag！ </audio></div>

</template>

<script setup lang="ts">
import { ref, onMounted, computed, inject } from 'vue';
import Header from './Header.vue';
const audioElement = ref<HTMLAudioElement | null>(null);
const pc_playlist = ref<string[]>([]); // User's personal playlist
const masterPlaylist = ref<string[]>([]); // All available songs
const pc_Index = ref(-1);
const pc_Playing= ref(false);
const pc_Playmode = ref(0);
const pc_RadioNo = ref(0);
const pc_Mute= ref(false);
const pc_Playrate = ref(1);
const pc_Sleeptime= ref(0);
const pc_Albumstring= ref("");
const pc_Volume = ref(50); // Initial pc_Volume

// Inject the setGlobalError function
const setGlobalError = inject('setGlobalError') as (message: string) => void;

const pc_Currenttitle = computed(() => {
  if (pc_Index.value !== -1 && pc_playlist.value.length > pc_Index.value) {
    return pc_playlist.value[pc_Index.value];
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

const fetch_pc_Playlist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_playlist', {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch personal playlist');
    }
    const data = await response.json();
    pc_playlist.value = data;
  } catch (err: any) {
    setGlobalError(err.message);
  }
};

const fetch_MasterPlaylist = async () => {
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

const pc_Playindex = (index: number) => {
  if (audioElement.value && pc_playlist.value[index]) {
    audioElement.value.src = `http://127.0.0.1:8001/music/${pc_playlist.value[index]}`;
    audioElement.value.play();
    pc_Index.value = index;
    pc_Playing.value = true;
  }
};

const pc_Playpause = () => {
  if (audioElement.value) {
    if (pc_Playing.value) {
      audioElement.value.pause();
    } else {
      audioElement.value.play();
    }
    pc_Playing.value = !pc_Playing.value;
  }
};

const pc_Stop = () => {
  if (audioElement.value) {
    audioElement.value.pause();
    audioElement.value.currentTime = 0;
    pc_Playing.value = false;
    pc_Index.value = -1; // Reset current song
  }
};

const pc_Next = () => {
  if (pc_playlist.value.length > 0) {
    const nextIndex = (pc_Index.value + 1) % pc_playlist.value.length;
    pc_Playindex(nextIndex);
  }
};

const pc_Prev = () => {
  if (pc_playlist.value.length > 0) {
    const prevIndex = (pc_Index.value - 1 + pc_playlist.value.length) % pc_playlist.value.length;
    pc_Playindex(prevIndex);
  }
};

const set_pc_Volume = () => {
  if (audioElement.value) {
    audioElement.value.volume = pc_Volume.value / 100;
  }
};

const pc_Addsong = (song: string) => {
  if (!pc_playlist.value.includes(song)) {
    pc_playlist.value.push(song);
  }
};

const savePersonalPlaylist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_playlist', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(pc_playlist.value),
    });
    if (!response.ok) {
      throw new Error('Failed to save personal playlist');
    }
    alert('Playlist saved successfully!');
  } catch (err: any) {
    setGlobalError(err.message);
  }
};

const pc_Playradio= () => {

};


const set_pc_Playmode= () => {

};

onMounted(() => {
  fetch_pc_Playlist();
  fetch_MasterPlaylist();
  if (audioElement.value) {
    audioElement.value.volume = pc_Volume.value / 100; // Set initial volume
  }
});

</script>


