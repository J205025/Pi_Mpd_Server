<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl text-center">
        <h1 class="text-5xl font-extrabold text-gray-900 mb-4">Pc Player</h1>
      </div>

      <div v-if="pc_playlist_all.length > 0" class="bg-white p-6 rounded-lg shadow-xl mt-12">
        <label for="playlist-select" class="block text-xl font-bold mb-3 text-gray-800">Select a Track:</label>
        <select 
          id="playlist-select" 
          v-model="selectedTrack" 
          class="block w-full p-3 text-gray-700 bg-gray-50 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500"
        >
          <option disabled value="">-- Please choose a track --</option>
          <option v-for="track in pc_playlist_all" :key="track" :value="track">
            {{ formatTrackName(track) }}
          </option>
        </select>
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
import { ref, onMounted } from 'vue';

const pc_playlist_all = ref([]);
const selectedTrack = ref('');

onMounted(async () => {
  try {
    const { data: playlist, pending, error } = await useFetch('/api/pc_get_playlist_all');

    if (playlist.value) {
        pc_playlist_all.value = playlist.value;
        
        // LOGS FOR DEBUGGING
        console.log('Playlist data received:', pc_playlist_all.value);
        console.log('Is it an array?', Array.isArray(pc_playlist_all.value));
        console.log('Playlist length:', pc_playlist_all.value.length);

    } else {
        console.log('Fetch was successful but returned no data.');
        if (error.value) {
          console.error('An error occurred during fetch:', error.value);
        }
    }
  } catch (err) {
    console.error('Error fetching playlist:', err);
  }
});

const formatTrackName = (fullPath) => {
  if (!fullPath) return '';
  return fullPath.split('/').pop().replace('.mp3', '');
};
</script>

<style scoped>
/* Page-specific styles can remain here */
</style>

,
  routeRules: {
    // This rule proxies all requests starting with '/api/'
    // to your FastAPI backend at http://127.0.0.1:8001
    '/api/**': {
      proxy: 'http://127.0.0.1:8001/api/**'
    }
  }