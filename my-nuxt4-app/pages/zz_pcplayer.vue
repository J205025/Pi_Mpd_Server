<template>
 <Header />
      <section>
        <h3>Player Controls</h3>

    <div id="player-container">
        <h1>MP3 Player with Synced Lyrics</h1>
        <audio id="audioPlayer" controls>
            <source src="song.mp3" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    </div>

    <div id="lyrics-container">
        <p id="current-lyric">Loading lyrics...</p>
    </div>




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
            <li v-for="(song, index) in pc_playlist_all" :key="index">
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

const audioElement = ref<HTMLAudioElement | null>(null);
const pc_playlist = ref<string[]>([]); // User's personal playlist
const pc_playlist_all = ref<string[]>([]); // All available songs
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

const fetch_pc_playlist = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_get_playlist', {
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

const fetch_pc_playlist_all = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8001/pc_get_playlist_all', {
      headers: getAuthHeaders(),
    });
    if (!response.ok) {
      throw new Error('Failed to fetch master playlist');
    }
    const data = await response.json();
    pc_playlist_all.value = data;
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


        const audioPlayer = document.getElementById('audioPlayer');
        const currentLyricDisplay = document.getElementById('current-lyric');
        let lyrics = []; // To store parsed LRC data

        // Function to parse LRC content
        async function loadLRC(url) {
            try {
                const response = await fetch(url);
                const lrcText = await response.text();
                const lines = lrcText.split('\n');
                let parsedLyrics = [];

                lines.forEach(line => {
                    // Regular expression to match timestamps like [mm:ss.xx]
                    const match = line.match(/\[(\d{2}):(\d{2})\.(\d{2,3})\](.*)/);
                    if (match) {
                        const minutes = parseInt(match[1], 10);
                        const seconds = parseInt(match[2], 10);
                        const milliseconds = parseInt(match[3], 10);
                        const time = (minutes * 60) + seconds + (milliseconds / (match[3].length === 2 ? 100 : 1000)); // Handle 2 or 3 digit milliseconds
                        const text = match[4].trim();
                        if (text) { // Only add if there's actual text
                            parsedLyrics.push({ time: time, text: text });
                        }
                    }
                });
                // Sort lyrics by time to ensure correct order
                parsedLyrics.sort((a, b) => a.time - b.time);
                return parsedLyrics;
            } catch (error) {
                console.error('Error loading or parsing LRC file:', error);
                return [];
            }
        }

        // Function to update the displayed lyric
        function updateLyric() {
            const currentTime = audioPlayer.currentTime;
            let foundLyric = false;

            for (let i = 0; i < lyrics.length; i++) {
                if (currentTime >= lyrics[i].time) {
                    // Check if there's a next lyric and if current time is before it
                    if (i + 1 < lyrics.length && currentTime < lyrics[i + 1].time) {
                        currentLyricDisplay.textContent = lyrics[i].text;
                        foundLyric = true;
                        break;
                    } else if (i + 1 === lyrics.length) { // Last lyric
                        currentLyricDisplay.textContent = lyrics[i].text;
                        foundLyric = true;
                        break;
                    }
                }
            }

            if (!foundLyric) {
                currentLyricDisplay.textContent = ""; // Clear if no lyric is active
            }
        }

        // Event listener for time updates
        audioPlayer.addEventListener('timeupdate', updateLyric);

        // Load lyrics when the page loads
        document.addEventListener('DOMContentLoaded', async () => {
            lyrics = await loadLRC('song.lrc');
            if (lyrics.length > 0) {
                currentLyricDisplay.textContent = "Play the audio to see lyrics.";
            } else {
                currentLyricDisplay.textContent = "No lyrics found or an error occurred.";
            }
        });

        // Optional: Reset lyric display when audio ends
        audioPlayer.addEventListener('ended', () => {
            currentLyricDisplay.textContent = "Song ended.";
        });


onMounted(() => {
  fetch_pc_playlist();
  fetch_pc_playlist_all();
  if (audioElement.value) {
    audioElement.value.volume = pc_Volume.value / 100; // Set initial volume
  }
});

</script>


