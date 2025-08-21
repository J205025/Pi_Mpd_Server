<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl text-center">
        <h1 class="text-5xl font-extrabold text-gray-900 mb-4">Pc Player</h1>
      </div>

      <div v-if="selectedTrack" class="bg-white p-6 rounded-lg shadow-xl mt-8">
        <div class="text-center mb-4">
          <p class="text-gray-600 font-bold">{{ trackTitle }}</p>
          <p class="text-gray-500 text-sm mt-1">
            <span v-if="trackArtist">{{ trackArtist }}</span>
            <span v-if="trackArtist && trackAlbum"> - </span>
            <span v-if="trackAlbum">{{ trackAlbum }}</span>
          </p>
        </div>

        <audio
          ref="audioPlayer"
          :src="`http://127.00.1:8001/music/${selectedTrack}`"
          @loadedmetadata="onLoadedMetadata"
          @timeupdate="onTimeUpdate"
          @ended="onTrackEnded"
          @loadstart="isLoading = true"
          @canplay="handleCanPlay"
          @error="onAudioError"
          @canplaythrough="onCanPlayThrough"
          preload="metadata"
          class="hidden"
        ></audio>

        <div class="mb-6">
          <div class="flex justify-between text-sm text-gray-600 mb-2">
            <span>{{ formatTime(currentTime) }}</span>
            <span>{{ formatTime(duration) }}</span>
          </div>
          <div 
            class="w-full bg-gray-200 rounded-full h-2 cursor-pointer"
            @click="seekTo($event)"
          >
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-100"
              :style="{ width: progressPercentage + '%' }"
            ></div>
          </div>
        </div>

        <div class="flex items-center justify-center space-x-4 mb-6">
          <button
            @click="previousTrack"
            :disabled="pc_playlist_all.length <= 1"
            class="bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed p-3 rounded-full transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M8.445 14.832A1 1 0 0010 14v-2.798l5.445 3.63A1 1 0 0017 14V6a1 1 0 00-1.555-.832L10 8.798V6a1 1 0 00-1.555-.832l-6 4a1 1 0 000 1.664l6 4z"/>
            </svg>
          </button>

          <button
            @click="togglePlayPause"
            :disabled="isLoading"
            class="w-24 h-24 rounded-full bg-blue-500 hover:bg-blue-600 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed text-white transition-colors duration-200 flex items-center justify-center shadow-lg"
          >
            <svg v-if="isLoading" class="w-12 h-12 animate-spin" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4 2a2 2 0 00-2 2v12a2 2 0 002 2h12a2 2 0 002-2V4a2 2 0 00-2-2H4z"/>
            </svg>
            <svg v-else-if="isPlaying" class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd"/>
            </svg>
            <svg v-else class="w-12 h-12" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832L12 10.202V12a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2A1 1 0 0012 8v1.798l-2.445-1.63z" clipRule="evenodd"/>
            </svg>
          </button>

          <button
            @click="nextTrack"
            :disabled="pc_playlist_all.length <= 1"
            class="bg-gray-200 hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed p-3 rounded-full transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z"/>
            </svg>
          </button>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2">
            <button @click="toggleMute" class="text-gray-600 hover:text-gray-800">
              <svg v-if="isMuted || volume === 0" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.293 7.293a1 1 0 011.414 0L15 8.586l1.293-1.293a1 1 0 111.414 1.414L16.414 10l1.293 1.293a1 1 0 01-1.414 1.414L15 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L13.586 10l-1.293-1.293a1 1 0 010-1.414z" clipRule="evenodd"/>
              </svg>
              <svg v-else-if="volume < 0.5" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.146 6.146a.5.5 0 01.708 0l.646.647.646-.647a.5.5 0 11.708.708L13.207 8.5l1.647 1.646a.5.5 0 01-.708.708L12.5 9.207l-.646.647a.5.5 0 11-.708-.708L12.793 7.5l-1.647-1.646a.5.5 0 010-.708z" clipRule="evenodd"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM15.657 6.343a1 1 0 00-1.414 1.414.5.5 0 000 .707l.707.707a1 1 0 101.414-1.414l-.707-.707a.5.5 0 000-.707zm1.414 5.657a1 1 0 01-1.414 0 .5.5 0 000-.707l-.707-.707a1 1 0 111.414-1.414l.707.707a.5.5 0 000 .707z" clipRule="evenodd"/>
              </svg>
            </button>
            <input
              type="range"
              min="0"
              max="1"
              step="0.05"
              v-model="volume"
              @input="updateVolume"
              class="w-20 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
            >
            <span class="text-sm text-gray-600 w-8">{{ Math.round(volume * 100) }}</span>
          </div>

          <div class="flex items-center space-x-2">
            <button
              @click="toggleShuffle"
              :class="[
                'p-2 rounded transition-colors duration-200',
                isShuffleMode ? 'bg-blue-100 text-blue-600' : 'text-gray-600 hover:text-gray-800'
              ]"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732L14.146 12.8l-1.179 4.456a1 1 0 01-1.856-.288L12.382 12H10a1 1 0 110-2h2.382l-.271-4.968A1 1 0 0112 2z" clipRule="evenodd"/>
              </svg>
            </button>

            <button
              @click="toggleRepeat"
              :class="[
                'p-2 rounded transition-colors duration-200',
                repeatMode === 'none' ? 'text-gray-600 hover:text-gray-800' : 'bg-blue-100 text-blue-600'
              ]"
            >
              <svg v-if="repeatMode === 'one'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 12V7H3l4-4 4 4H9v5a1 1 0 01-1 1H5zm10 1v5h2l-4 4-4-4h2V8a1 1 0 011-1h3zm-5-3h2v2h-2V10z"/>
              </svg>
              <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M5 12V7H3l4-4 4 4H9v5a1 1 0 01-1 1H5zm10 1v5h2l-4 4-4-4h2V8a1 1 0 011-1h3z"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="mt-4 text-center text-sm text-gray-500">
          Track {{ currentTrackIndex + 1 }} of {{ pc_playlist_all.length }}
          <span v-if="isShuffleMode" class="ml-2">(Shuffle)</span>
          <span v-if="repeatMode === 'all'" class="ml-2">(Repeat All)</span>
          <span v-if="repeatMode === 'one'" class="ml-2">(Repeat One)</span>
        </div>
      </div>

      <div v-if="pc_playlist_all.length > 0" class="bg-white p-6 rounded-lg shadow-xl mt-12">
        <label for="playlist-select" class="block text-xl font-bold mb-3 text-gray-800">Select a Track:</label>
        <select 
          id="playlist-select" 
          v-model="selectedTrack" 
          @change="onTrackChange"
          class="block w-full p-3 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        >
          <option disabled value="">-- Please choose a track --</option>
          <option v-for="(track, index) in pc_playlist_all" :key="track" :value="track">
            {{ index + 1 }} - {{ getTrackArtist(track) }} - {{ getTrackAlbum(track) }} - {{ getTrackTitle(track) }}
          </option>
        </select>
        
        <div class="mt-4">
            <p class="text-lg font-bold mb-2 text-gray-800">Enter Track Index:</p>
            <div class="flex flex-wrap gap-2 justify-center">
                <button
                    v-for="number in 10"
                    :key="number - 1"
                    @click="handleNumberPress(number - 1)"
                    class="bg-gradient-to-r from-blue-400 to-blue-600 text-white p-4 rounded-lg w-[120px] h-20 flex items-center justify-center text-3xl font-bold
                           hover:from-blue-500 hover:to-blue-700 hover:shadow-lg transition-transform hover:scale-105"
                >
                    {{ number - 1 }}
                </button>
            </div>
            <div class="mt-2 text-center text-gray-600">
                Current Number: <span class="font-bold">{{ currentNumberString }}</span>
            </div>
        </div>
      </div>


      
      <div class="grid md:grid-cols-3 gap-8 mt-12">
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">Feature One</h2>
          <p class="text-gray-700">Explore the first amazing feature we have to offer. It's designed to make your life easier and more productive.</p>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">Feature Two</h2>
          <p class="text-gray-700">Discover how our second feature can help you achieve your goals faster than ever before.</p>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">Feature Three</h2>
          <p class="text-gray-700">Our third feature is revolutionary, providing insights and capabilities you won't find anywhere else.</p>
        </div>
      </div>
    </main>
    
    <footer />

  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';

const pc_playlist_all = ref([]);
const selectedTrack = ref('');
const loading = ref(false);
const error = ref(null);

// Audio player state
const audioPlayer = ref(null);
const isPlaying = ref(false);
const isLoading = ref(false);
const currentTime = ref(0);
const duration = ref(0);
const volume = ref(0.7);
const isMuted = ref(false);
const previousVolume = ref(0.7);
const autoPlayOnLoad = ref(false); // Flag to autoplay track from dropdown

// Play modes
const isShuffleMode = ref(false);
const repeatMode = ref('none'); // 'none', 'all', 'one'

// State for button-based number input
const currentNumberString = ref('');
let inputTimer = null;
const INPUT_TIMEOUT = 4000; // 4 seconds

// Computed properties
const currentTrackIndex = computed(() => {
  return pc_playlist_all.value.findIndex(track => track === selectedTrack.value);
});

const progressPercentage = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 : 0;
});

// New functions for parsing track metadata for the select dropdown
const getTrackTitle = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.pop().replace(/\.(mp3|MP3|flac|FLAC)$/, '');
};

const getTrackAlbum = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.length > 2 ? parts[parts.length - 2] : '';
};

const getTrackArtist = (fullPath) => {
  if (!fullPath) return '';
  const parts = fullPath.split('/');
  return parts.length > 2 ? parts[parts.length - 3] : '';
};


// Now Playing display properties (still use computed for reactivity)
const trackTitle = computed(() => getTrackTitle(selectedTrack.value));
const trackAlbum = computed(() => getTrackAlbum(selectedTrack.value));
const trackArtist = computed(() => getTrackArtist(selectedTrack.value));

onMounted(async () => {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await $fetch('http://127.0.0.1:8001/pc_get_allfiles');
    
    console.log('Raw response from API:', response);
    
    if (Array.isArray(response) && response.length > 0) {
      pc_playlist_all.value = response;
      console.log('Playlist data received:', pc_playlist_all.value);
    } else if (Array.isArray(response)) {
      console.log('Fetch was successful, but the playlist is empty.');
      pc_playlist_all.value = [];
    } else {
      console.error('Invalid response format:', response);
      error.value = 'Invalid response format from server';
    }
  } catch (err) {
    console.error('Error fetching playlist:', err);
    error.value = `Failed to fetch playlist: ${err.message || 'Unknown error'}`;
  } finally {
    loading.value = false;
  }
});

// Watch for volume changes
watch(volume, (newVolume) => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = newVolume;
    if (newVolume > 0 && isMuted.value) {
      isMuted.value = false;
    }
  }
});

// Audio player methods
const onTrackChange = () => {
  // When user selects a track from the dropdown, set a flag
  // to play it as soon as it's ready (in handleCanPlay).
  autoPlayOnLoad.value = true;
};

const handleCanPlay = () => {
  isLoading.value = false;
  if (autoPlayOnLoad.value) {
    autoPlayOnLoad.value = false; // Reset the flag
    audioPlayer.value.play().then(() => {
      isPlaying.value = true;
    }).catch(error => {
      console.error('Autoplay was prevented.', error);
      isPlaying.value = false;
    });
  }
};

const togglePlayPause = () => {
  if (!audioPlayer.value) return;
  
  console.log('🎵 Toggle play/pause - Current state:', isPlaying.value);
  console.log('🎵 Audio element readyState:', audioPlayer.value.readyState);
  console.log('🎵 Audio element paused:', audioPlayer.value.paused);
  console.log('🎵 Audio element src:', audioPlayer.value.src);
  console.log('🎵 Audio element volume:', audioPlayer.value.volume);
  console.log('🎵 Audio element muted:', audioPlayer.value.muted);
  
  if (isPlaying.value) {
    audioPlayer.value.pause();
    isPlaying.value = false;
    console.log('🎵 Paused audio');
  } else {
    audioPlayer.value.play().then(() => {
      isPlaying.value = true;
      console.log('🎵 Started playing audio successfully');
    }).catch((error) => {
      console.error('🎵 Error playing audio:', error);
      isPlaying.value = false;
    });
  }
};

const onLoadedMetadata = () => {
  if (audioPlayer.value) {
    duration.value = audioPlayer.value.duration;
    audioPlayer.value.volume = volume.value;
    console.log('🎵 Metadata loaded - Duration:', duration.value);
    console.log('🎵 Audio format supported:', audioPlayer.value.canPlayType('audio/mpeg'));
  }
};

const onTimeUpdate = () => {
  if (audioPlayer.value) {
    currentTime.value = audioPlayer.value.currentTime;
  }
};

const onTrackEnded = () => {
  isPlaying.value = false;
  
  if (repeatMode.value === 'one') {
    // Repeat current track
    audioPlayer.value.currentTime = 0;
    audioPlayer.value.play();
    isPlaying.value = true;
  } else if (repeatMode.value === 'all' || isShuffleMode.value) {
    // Go to next track
    nextTrack();
  } else {
    // Stop at end of playlist
    const nextIndex = currentTrackIndex.value + 1;
    if (nextIndex < pc_playlist_all.value.length) {
      nextTrack();
    }
  }
};

const seekTo = (event) => {
  if (!audioPlayer.value || duration.value === 0) return;
  
  const rect = event.currentTarget.getBoundingClientRect();
  const percentage = (event.clientX - rect.left) / rect.width;
  const newTime = percentage * duration.value;
  
  audioPlayer.value.currentTime = newTime;
  currentTime.value = newTime;
};

const previousTrack = () => {
  if (pc_playlist_all.value.length <= 1) return;
  
  let newIndex;
  if (isShuffleMode.value) {
    // Random previous track
    do {
      newIndex = Math.floor(Math.random() * pc_playlist_all.value.length);
    } while (newIndex === currentTrackIndex.value && pc_playlist_all.value.length > 1);
  } else {
    newIndex = currentTrackIndex.value - 1;
    if (newIndex < 0) {
      newIndex = repeatMode.value === 'all' ? pc_playlist_all.value.length - 1 : 0;
    }
  }
  
  selectedTrack.value = pc_playlist_all.value[newIndex];
  setTimeout(() => {
    if (isPlaying.value) {
      autoPlayOnLoad.value = true;
    }
  }, 50);
};

const nextTrack = () => {
  if (pc_playlist_all.value.length <= 1) return;
  
  let newIndex;
  if (isShuffleMode.value) {
    // Random next track
    do {
      newIndex = Math.floor(Math.random() * pc_playlist_all.value.length);
    } while (newIndex === currentTrackIndex.value && pc_playlist_all.value.length > 1);
  } else {
    newIndex = currentTrackIndex.value + 1;
    if (newIndex >= pc_playlist_all.value.length) {
      newIndex = repeatMode.value === 'all' ? 0 : pc_playlist_all.value.length - 1;
    }
  }
  
  selectedTrack.value = pc_playlist_all.value[newIndex];
   setTimeout(() => {
    if (isPlaying.value) {
      autoPlayOnLoad.value = true;
    }
  }, 50);
};

const updateVolume = () => {
  if (audioPlayer.value) {
    audioPlayer.value.volume = volume.value;
  }
};

const toggleMute = () => {
  if (isMuted.value) {
    volume.value = previousVolume.value;
    isMuted.value = false;
  } else {
    previousVolume.value = volume.value;
    volume.value = 0;
    isMuted.value = true;
  }
};

const toggleShuffle = () => {
  isShuffleMode.value = !isShuffleMode.value;
};

const toggleRepeat = () => {
  const modes = ['none', 'all', 'one'];
  const currentIndex = modes.indexOf(repeatMode.value);
  const nextIndex = (currentIndex + 1) % modes.length;
  repeatMode.value = modes[nextIndex];
};

const formatTime = (seconds) => {
  if (isNaN(seconds) || seconds === 0) return '0:00';
  
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
};

const handleNumberPress = (number) => {
    // Clear any existing timer
    clearTimeout(inputTimer);
    
    // Add the new digit
    let newNumberString = currentNumberString.value + String(number);
    
    // Trim the string if it's longer than 4 digits
    if (newNumberString.length > 4) {
        newNumberString = newNumberString.substring(newNumberString.length - 4);
    }
    
    currentNumberString.value = newNumberString;
    
    // Set a new timer to play the track after the timeout
    inputTimer = setTimeout(() => {
        playTrackFromInput();
    }, INPUT_TIMEOUT);
};

const playTrackFromInput = () => {
    // Clear the timer after a track is played
    clearTimeout(inputTimer);
    
    const maxIndex = pc_playlist_all.value.length;
    let index = parseInt(currentNumberString.value, 10);
    
    if (isNaN(index)) {
        alert('Invalid input. Please enter a valid number.');
        currentNumberString.value = '';
        return;
    }

    if (index === 0) {
        alert('Track index cannot be 0. Please enter a number between 1 and ' + maxIndex);
        currentNumberString.value = '';
        return;
    }
    
    if (index > maxIndex) {
        index = index % maxIndex;
        if (index === 0) {
            index = maxIndex;
        }
    }
    
    // Set the selected track and play it
    selectedTrack.value = pc_playlist_all.value[index - 1];
    autoPlayOnLoad.value = true;
    
    // Reset the number string
    currentNumberString.value = '';
};

// Add debugging event handlers
const onAudioError = (event) => {
  console.error('🎵 Audio error:', event);
  console.error('🎵 Audio error code:', audioPlayer.value?.error?.code);
  console.error('🎵 Audio error message:', audioPlayer.value?.error?.message);
  console.error('🎵 Audio src that failed:', audioPlayer.value?.src);
};

const onCanPlayThrough = () => {
  console.log('🎵 Audio can play through - ready for smooth playback');
};
</script>

<style scoped>
/* Custom slider styling */
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>