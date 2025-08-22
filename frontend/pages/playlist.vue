<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl text-center">
        <h1 class="text-5xl font-extrabold text-gray-900 mb-4">Playlist Management</h1>
      </div>

      <div class="bg-white p-6 rounded-lg shadow-xl mt-12">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">Generate Playlist from Folder</h2>
        <div class="flex flex-col sm:flex-row gap-4">
          <input 
            type="text"
            v-model="folderName"
            placeholder="Enter folder name (e.g., 國語)"
            class="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            @click="getFiles"
            :disabled="isLoading"
            class="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition duration-300"
          >
            <span v-if="isLoading">Loading...</span>
            <span v-else>Generate Playlist</span>
          </button>
        </div>

        <div v-if="errorMessage" class="mt-4 text-red-600 bg-red-100 p-3 rounded-lg">
          {{ errorMessage }}
        </div>
        
        <div v-if="fileList.length > 0" class="mt-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-3">Generated Files:</h3>
          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="(file, index) in fileList" :key="index" 
                class="text-gray-700 p-1 truncate cursor-pointer"
                :class="{ 'bg-blue-200': selectedFiles.includes(file) }"
                @click="toggleSelection(file)">
              {{ file }}
            </li>
          </ul>
          <div class="mt-4 flex gap-4">
            <button 
              @click="selectAll"
              class="bg-gray-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-700 transition duration-300"
            >
              Select All
            </button>
            <button 
              @click="deselectAll"
              class="bg-gray-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-gray-700 transition duration-300"
            >
              Deselect All
            </button>
            <button 
              @click="promptForPlaylistName"
              :disabled="selectedFiles.length === 0"
              class="bg-green-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition duration-300"
            >
              Save Selected Files to Playlist
            </button>
          </div>
        </div>
      </div>

      <div v-if="showSaveDialog" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <h3 class="text-xl font-bold mb-4">Enter Playlist Name</h3>
          <input 
            type="text"
            v-model="newPlaylistName"
            placeholder="My Awesome Playlist"
            class="w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div class="flex justify-end gap-4">
            <button @click="showSaveDialog = false" class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
            <button @click="savePlaylist" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-3 gap-8 mt-12">
        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">歌曲類型</h2>
          <p class="text-gray-700">國語 台語 英語 古典 有聲書 podcast</p>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">歌手</h2>
          <p class="text-gray-700">張學友 劉德華  BBC CNN</p>
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
import { ref } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const folderName = ref('');
const fileList = ref([]);
const isLoading = ref(false);
const errorMessage = ref('');
const selectedFiles = ref([]);
const showSaveDialog = ref(false);
const newPlaylistName = ref('');

const getFiles = async () => {
  if (!folderName.value.trim()) {
    errorMessage.value = 'Folder name cannot be empty.';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';
  fileList.value = [];
  selectedFiles.value = [];

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }
    
    const response = await fetch(`${apiBase}/pc_gen_fileslist/${encodeURIComponent(folderName.value)}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    const data = await response.json();
    fileList.value = data;

  } catch (error) {
    console.error('Failed to fetch files:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const toggleSelection = (file) => {
  const index = selectedFiles.value.indexOf(file);
  if (index > -1) {
    selectedFiles.value.splice(index, 1);
  } else {
    selectedFiles.value.push(file);
  }
};

const selectAll = () => {
  selectedFiles.value = [...fileList.value];
};

const deselectAll = () => {
  selectedFiles.value = [];
};

const promptForPlaylistName = () => {
  showSaveDialog.value = true;
};

const savePlaylist = async () => {
  if (!newPlaylistName.value.trim()) {
    alert('Playlist name cannot be empty.');
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/pc_save_playlists_tolist/${encodeURIComponent(newPlaylistName.value)}`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ songs: selectedFiles.value })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    alert('Playlist saved successfully!');
    showSaveDialog.value = false;
    newPlaylistName.value = '';
    selectedFiles.value = [];

  } catch (error) {
    console.error('Failed to save playlist:', error);
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

</script>

<style scoped>
.truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>