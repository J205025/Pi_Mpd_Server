<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">
    
    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-2 rounded-lg shadow-xl flex justify-between items-center relative">
        <div class="absolute left-1/2 -translate-x-1/2">
            <h1 class="text-4xl font-extrabold text-gray-900">音響播放-歌單編輯(Pi Player)</h1>
        </div>
        <div class="ml-6 p-2 border border-gray-300 rounded-lg text-sm bg-gray-50 shadow-inner">
          <div class="grid grid-cols-2 gap-x-4">
            <div class="font-bold">MPD Status:</div>
            <div class="text-right">
              <span 
                :class="{
                  'text-green-500': isMpdNormal, 
                  'text-red-500': !isMpdNormal
                }" 
                class="font-semibold"
              >
                {{ isMpdNormal ? 'Normal' : 'Abnormal' }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Add to Playlist Section -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-12">
        <h2 class="text-2xl font-bold text-gray-800">建立歌單:</h2>
        <div class="flex flex-col sm:flex-row gap-4 mt-4">
          <input 
            type="text"
            v-model="uriToAdd"
            placeholder="Enter song URI"
            class="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            @click="pi_addSongToPlaylist"
            :disabled="isLoading || !currentSelectedPlaylist"
            class="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition duration-300"
          >
            加入路徑
          </button>
        </div>
        <div class="flex flex-col sm:flex-row gap-4 mt-4">
          <input 
            type="text"
            v-model="folderName"
            placeholder="Enter folder name (e.g., 國語)"
            class="flex-grow p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button 
            @click="pi_addFolderToPlaylist"
            :disabled="isLoading || !currentSelectedPlaylist"
            class="bg-blue-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition duration-300"
          >
            加入資料夾
          </button>
        </div>
        <div v-if="!currentSelectedPlaylist" class="mt-2 text-sm text-red-500">Please select a playlist below first.</div>

        <div v-if="errorMessage" class="mt-4 text-red-600 bg-red-100 p-3 rounded-lg">
          {{ errorMessage }}
        </div>
      </div>

      <!-- Playlist List Section -->
      <div class="bg-white p-6 rounded-lg shadow-xl mt-6">
        <h2 class="text-2xl font-bold mb-4 text-gray-800">MPD 歌單:(點歌單名字可編輯曲目)</h2>
        <button @click="promptForNewPlaylist" class="bg-green-500 text-white py-2 px-4 rounded-lg hover:bg-green-600 transition duration-300 mb-4">
          新增歌單
        </button>
        <div v-if="playlistsList.length > 0">
          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="playlist in sortedPlaylists" :key="playlist.playlist"
                class="flex items-center text-gray-700 p-2 border-b border-gray-200 last:border-b-0">
              <span class="cursor-pointer hover:text-blue-600 font-medium" 
                    @click="pi_getPlaylistSongs(playlist.playlist)" 
                    :class="{ 
                      'bg-blue-200': playlist.playlist === currentSelectedPlaylist,
                      'text-red-600': playlist.playlist === '我的最愛',
                      'text-green-600': playlist.playlist === '定期播放'
                    }">
                {{ playlist.playlist }}
              </span>
              <div class="flex ml-auto">
                <button @click="promptRenamePlaylist(playlist.playlist)" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">
                  更名
                </button>
                <button @click="pi_deletePlaylist(playlist.playlist)" class="bg-red-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-red-600 transition duration-300 mr-2">
                  刪除
                </button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else class="text-gray-600 p-4 text-center">
          No playlists saved yet.
        </div>

        <div v-if="selectedPlaylistSongs.length > 0" class="mt-6">
          <h3 class="text-xl font-semibold text-gray-800 mb-3">歌單-{{ currentSelectedPlaylist }}:</h3>
          
          <div class="mb-4">
            <button 
              @click="editModeForPlaylist = !editModeForPlaylist; selectedSongsInEditMode = []"
              class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700 transition duration-300 mr-2"
            >
              {{ editModeForPlaylist ? '離開編輯' : '編輯' }}
            </button>
             <button 
              v-if="editModeForPlaylist"
              @click="pi_deleteSelectedSongsFromPlaylist"
              :disabled="selectedSongsInEditMode.length === 0"
              class="bg-red-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-700 disabled:bg-gray-400 transition duration-300"
            >
              刪除選取歌曲
            </button>
            <button 
              @click="pi_clearPlaylist"
              class="bg-orange-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-orange-600 transition duration-300 ml-2"
            >
              清空歌單
            </button>
          </div>

          <ul class="list-disc list-inside bg-gray-50 p-4 rounded-lg max-h-96 overflow-y-auto">
            <li v-for="(song, index) in selectedPlaylistSongs" :key="index" 
                class="text-gray-700 p-1 truncate"
                :class="{ 'bg-red-300 cursor-pointer': editModeForPlaylist && selectedSongsInEditMode.includes(song), 'cursor-pointer': editModeForPlaylist && !selectedSongsInEditMode.includes(song), 'cursor-default': !editModeForPlaylist }"
                @click="editModeForPlaylist ? toggleSongSelectionInEditMode(song) : null">
              {{ song }}
            </li>
          </ul>
        </div>
      </div>

      <!-- Dialogs -->
      <div v-if="showNewPlaylistDialog" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <h3 class="text-xl font-bold mb-4">Enter New Playlist Name</h3>
          <input 
            type="text"
            v-model="newPlaylistName"
            placeholder="My New MPD Playlist"
            class="w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div class="flex justify-end gap-4">
            <button @click="showNewPlaylistDialog = false" class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
            <button @click="pi_createNewPlaylist" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Create</button>
          </div>
        </div>
      </div>

      <div v-if="showRenameDialog" class="fixed inset-0 bg-gray-800 bg-opacity-50 flex items-center justify-center">
        <div class="bg-white p-6 rounded-lg shadow-xl">
          <h3 class="text-xl font-bold mb-4">Rename Playlist: "{{ playlistToRename }}"</h3>
          <input 
            type="text"
            v-model="newPlaylistNameInput"
            placeholder="Enter new playlist name"
            class="w-full p-3 border border-gray-300 rounded-lg mb-4"
          />
          <div class="flex justify-end gap-4">
            <button @click="showRenameDialog = false" class="bg-gray-300 text-gray-800 font-bold py-2 px-4 rounded-lg">Cancel</button>
            <button @click="pi_confirmRename" class="bg-blue-600 text-white font-bold py-2 px-4 rounded-lg">Rename</button>
          </div>
        </div>
      </div>

    <div class="grid md:grid-cols-4 gap-6 mt-6">

    <div class="bg-white p-6 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-2 text-gray-800">自動產生歌單-類型:</h2>
    <div class="grid grid-cols-3 gap-4">
    <button @click="autoSavePiPlaylist('國語')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">國語</button>
    <button @click="autoSavePiPlaylist('台語')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">台語</button>
    <button @click="autoSavePiPlaylist('日語')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">日語</button>
    <button @click="autoSavePiPlaylist('英語')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">英語</button>
    <button @click="autoSavePiPlaylist('古典')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">古典</button>
    <button @click="autoSavePiPlaylist('英語')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">英語</button>
    <button @click="autoSavePiPlaylist('輕音樂')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">輕音樂</button>
    <button @click="autoSavePiPlaylist('有聲書')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">有聲書</button>
    <button @click="autoSavePiPlaylist('播客')" class="bg-green-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-green-600 transition duration-300">播客</button>
    </div>

    </div>
    <div class="bg-white p-6 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-2 text-gray-800">自動產生歌單-歌手:</h2>
    <div class="grid grid-cols-3 gap-4">
    <button @click="autoSavePiPlaylist('國語/張學友')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友</button>
    <button @click="autoSavePiPlaylist('國語/張學友-演唱會')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友-演唱會</button>
    <button @click="autoSavePiPlaylist('國語/張學友-精選輯')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友-精選輯</button>
    <button @click="autoSavePiPlaylist('國語/劉德華')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">劉德華</button>
    <button @click="autoSavePiPlaylist('國語/孫燕姿')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">孫燕姿</button>
    <button @click="autoSavePiPlaylist('國語/弦子')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">弦子</button>
    <button @click="autoSavePiPlaylist('國語/原子邦妮')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">原子邦妮</button>
    <button @click="autoSavePiPlaylist('英語/Lady_Gaga')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">Lady Gaga</button>
    <button @click="autoSavePiPlaylist('台語/鄭進一')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">鄭進一</button>
    <button @click="autoSavePiPlaylist('英語/Regine')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">Regine</button>
    <button @click="autoSavePiPlaylist('英語/Bryan_Adams')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">Bryan Adams</button>
    <button @click="autoSavePiPlaylist('國語/萬芳')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">萬芳</button>
    <button @click="autoSavePiPlaylist('日語/AKB48')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">AKB48</button>
    <button @click="autoSavePiPlaylist('台語/黃乙玲')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">黃乙玲</button>
    <button @click="autoSavePiPlaylist('台語/秀蘭瑪雅')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">秀蘭瑪雅</button>
    <button @click="autoSavePiPlaylist('台語蘇宥蓉')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">蘇宥蓉</button>
    <button @click="autoSavePiPlaylist('台語/玖壹壹')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">玖壹壹</button>
    <button @click="autoSavePiPlaylist('國語/張韶涵')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張韶涵</button>
    <button @click="autoSavePiPlaylist('國語/張韶涵')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張韶涵</button>
    <button @click="autoSavePiPlaylist('國語/張惠妺')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張惠妹</button>
    <button @click="autoSavePiPlaylist('國語/任賢齊')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">任賢齊</button>
    <button @click="autoSavePiPlaylist('國語/鄭中基')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">鄭中基</button>
    <button @click="autoSavePiPlaylist('國語/蔡健雅')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">蔡健雅</button>
    <button @click="autoSavePiPlaylist('國語/伍佰')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">伍佰</button>
    <button @click="autoSavePiPlaylist('國語/張靚穎')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張靚穎</button>
    <button @click="autoSavePiPlaylist('國語/梁靜茹')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">梁靜茹</button>
    <button @click="autoSavePiPlaylist('國語/蘇打綠')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">蘇打綠</button>
    <button @click="autoSavePiPlaylist('國語/高慧君')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">高慧君</button>
    <button @click="autoSavePiPlaylist('國語/張棟樑')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張棟樑</button>
    <button @click="autoSavePiPlaylist('國語/郁可唯')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">郁可唯</button>
    <button @click="autoSavePiPlaylist('國語/楊丞琳')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">楊丞琳</button>
    <button @click="autoSavePiPlaylist('國語/王心凌')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">王心凌</button>
    <button @click="autoSavePiPlaylist('國語/王傑')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">王傑</button>
    </div>

    </div>
    <div class="bg-white p-6 rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-2 text-gray-800">自動產生歌單-專輯:</h2>
    <div class="grid grid-cols-3 gap-4">
    <button @click="autoSavePiPlaylist('國語/張學友/天下第一流')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友 天下第一流</button>
    <button @click="autoSavePiPlaylist('國語/張學友/吻別')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友 吻別</button>
    <button @click="autoSavePiPlaylist('國語/張學友-演唱會/2003音樂之旅Live演唱會')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張學友2003音樂之旅演唱會</button>
    <button @click="autoSavePiPlaylist('國語/張惠妺/你在看我嗎')" class="bg-blue-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-blue-600 transition duration-300">張惠妹 你在看我嗎</button>
    <button @click="autoSavePiPlaylist('播客/BBC')" class="bg-purple-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-purple-600 transition duration-300">BBC</button>
    <button @click="autoSavePiPlaylist('播客/Daily')" class="bg-purple-500 text-white py-1 px-3 rounded-lg text-sm hover:bg-purple-600 transition duration-300">Daily</button>
    </div>

    </div>

        <div class="bg-white p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-bold mb-2 text-gray-800">下載最新播客:</h2>
          <div class="grid grid-cols-3 gap-4">
          <button @click="autoDownloadPodcast()" class="bg-purple-600 text-white py-4 px-4 rounded-lg text-m hover:bg-purple-700 transition duration-300">下載播客</button>
          </div>
        </div>

      </div>
    </main>

    <footer />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

const folderName = ref('');
const uriToAdd = ref('');
const isLoading = ref(false);
const errorMessage = ref('');
const showNewPlaylistDialog = ref(false);
const newPlaylistName = ref('');
const showRenameDialog = ref(false);
const playlistToRename = ref('');
const newPlaylistNameInput = ref('');
const playlistsList = ref([]);
const selectedPlaylistSongs = ref([]);
const currentSelectedPlaylist = ref('');
const selectedSongsInEditMode = ref([]);
const editModeForPlaylist = ref(false);

const mpdStatus = ref({});
let pollInterval;

const isMpdNormal = computed(() => {
  return mpdStatus.value && Object.keys(mpdStatus.value).length > 0 && mpdStatus.value.state !== undefined;
});

const sortedPlaylists = computed(() => {
  const playlists = [...playlistsList.value];
  const favoriteName = '我的最愛';
  const regularPlayName = '定期播放';

  let favoritePlaylist = null;
  let regularPlaylist = null;
  const otherPlaylists = [];

  // Separate special playlists and collect others
  playlists.forEach(p => {
    if (p.playlist === favoriteName) {
      favoritePlaylist = p;
    } else if (p.playlist === regularPlayName) {
      regularPlaylist = p;
    } else {
      otherPlaylists.push(p);
    }
  });

  const result = [];
  if (favoritePlaylist) {
    result.push(favoritePlaylist);
  }
  if (regularPlaylist) {
    result.push(regularPlaylist);
  }
  result.push(...otherPlaylists);
  
  return result;
});

const fetchMpdStatus = async () => {
  try {
    const response = await $fetch(`${apiBase}/pi_mpd_status`);
    mpdStatus.value = response;
  } catch (error) {
    console.error('Error fetching MPD status:', error);
    mpdStatus.value = {}; // Reset status on error
  }
};

const pi_getPlaylistsList = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const response = await fetch(`${apiBase}/pi_get_playlists_List`);
    if (!response.ok) throw new Error('Failed to fetch playlists');
    playlistsList.value = await response.json();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const pi_getPlaylistSongs = async (playlistName) => {
  isLoading.value = true;
  errorMessage.value = '';
  selectedPlaylistSongs.value = [];
  currentSelectedPlaylist.value = playlistName;
  selectedSongsInEditMode.value = [];
  editModeForPlaylist.value = false;

  try {
    // 1. Clear the queue
    //await $fetch(`${apiBase}/pi_queue_clearsongs`, { method: 'DELETE' });
    // 2. Load playlist to queue
    //await $fetch(`${apiBase}/pi_queue_loadfrom_playlist/${encodeURIComponent(playlistName)}`, { method: 'GET' });
    
    // Original functionality: fetch and display songs
    const response = await fetch(`${apiBase}/pi_playlist_songs/${encodeURIComponent(playlistName)}`);
    if (!response.ok) throw new Error(`Failed to fetch songs for playlist ${playlistName}`);
    selectedPlaylistSongs.value = await response.json();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const promptForNewPlaylist = () => {
  newPlaylistName.value = '';
  showNewPlaylistDialog.value = true;
};

const pi_createNewPlaylist = async () => {
  if (!newPlaylistName.value.trim()) {
    alert('Playlist name cannot be empty.');
    return;
  }
  isLoading.value = true;
  try {
    // This API saves the current queue to a new playlist.
    const response = await fetch(`${apiBase}/pi_queue_saveto_playlist/${encodeURIComponent(newPlaylistName.value)}`, { method: 'GET' });
    if (!response.ok) throw new Error('Failed to create playlist');
    alert('Playlist created successfully (from current queue).');
    showNewPlaylistDialog.value = false;
    await pi_getPlaylistsList();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const pi_deletePlaylist = async (playlistName) => {
  if (!confirm(`Are you sure you want to delete the playlist "${playlistName}"?`)) return;
  isLoading.value = true;
  try {
    const response = await fetch(`${apiBase}/pi_playlist_rmpl/${encodeURIComponent(playlistName)}`, { method: 'DELETE' });
    if (!response.ok) throw new Error('Failed to delete playlist');
    alert(`Playlist "${playlistName}" deleted successfully!`);
    await pi_getPlaylistsList();
    if (currentSelectedPlaylist.value === playlistName) {
      currentSelectedPlaylist.value = '';
      selectedPlaylistSongs.value = [];
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const promptRenamePlaylist = (oldName) => {
  playlistToRename.value = oldName;
  newPlaylistNameInput.value = oldName;
  showRenameDialog.value = true;
};

const pi_confirmRename = async () => {
  if (!newPlaylistNameInput.value.trim() || newPlaylistNameInput.value === playlistToRename.value) {
    alert('New name is invalid or same as old name.');
    return;
  }
  isLoading.value = true;
  try {
    const response = await fetch(`${apiBase}/pi_playlist_renamepl/${encodeURIComponent(playlistToRename.value)}/${encodeURIComponent(newPlaylistNameInput.value)}`, { method: 'PUT' });
    if (!response.ok) throw new Error('Failed to rename playlist');
    alert('Playlist renamed successfully!');
    showRenameDialog.value = false;
    await pi_getPlaylistsList();
    if (currentSelectedPlaylist.value === playlistToRename.value) {
      currentSelectedPlaylist.value = newPlaylistNameInput.value;
    }
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const pi_addSongToPlaylist = async () => {
  if (!uriToAdd.value.trim() || !currentSelectedPlaylist.value) return;
  isLoading.value = true;
  try {
    const response = await fetch(`${apiBase}/pi_playlist_adduri/${encodeURIComponent(currentSelectedPlaylist.value)}/${encodeURIComponent(uriToAdd.value)}`, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to add song');
    uriToAdd.value = '';
    await pi_getPlaylistSongs(currentSelectedPlaylist.value);
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const pi_addFolderToPlaylist = async () => {
  if (!folderName.value.trim() || !currentSelectedPlaylist.value) return;
  isLoading.value = true;
  try {
    const response = await fetch(`${apiBase}/pi_playlist_add_folder/${encodeURIComponent(currentSelectedPlaylist.value)}/${encodeURIComponent(folderName.value)}`, { method: 'POST' });
    if (!response.ok) throw new Error('Failed to add folder');
    folderName.value = '';
    await pi_getPlaylistSongs(currentSelectedPlaylist.value);
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};

const toggleSongSelectionInEditMode = (song) => {
  const index = selectedSongsInEditMode.value.indexOf(song);
  if (index > -1) {
    selectedSongsInEditMode.value.splice(index, 1);
  } else {
    selectedSongsInEditMode.value.push(song);
  }
};

const pi_deleteSelectedSongsFromPlaylist = async () => {
    if (!confirm(`Delete ${selectedSongsInEditMode.value.length} songs?`)) return;
    isLoading.value = true;

    // Get song positions before deleting
    const positionsToDelete = selectedSongsInEditMode.value.map(song => selectedPlaylistSongs.value.indexOf(song));
    // Sort positions in descending order to avoid index shifting issues
    positionsToDelete.sort((a, b) => b - a);

    try {
        for (const pos of positionsToDelete) {
            if (pos === -1) continue;
            const response = await fetch(`${apiBase}/pi_playlist_deletesong/${encodeURIComponent(currentSelectedPlaylist.value)}/${pos}`, {
                method: 'DELETE',
            });
            if (!response.ok) {
                // We stop on first error
                throw new Error(`Failed to delete song at position ${pos}`);
            }
        }
        await pi_getPlaylistSongs(currentSelectedPlaylist.value); // Refresh
        editModeForPlaylist.value = false;
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        isLoading.value = false;
    }
};

const pi_clearPlaylist = async () => {
    if (!confirm(`Are you sure you want to clear all songs from "${currentSelectedPlaylist.value}"?`)) return;
    isLoading.value = true;
    try {
        const response = await fetch(`${apiBase}/pi_playlist_clearsongs/${encodeURIComponent(currentSelectedPlaylist.value)}`, { method: 'DELETE' });
        if (!response.ok) throw new Error('Failed to clear playlist');
        await pi_getPlaylistSongs(currentSelectedPlaylist.value); // Refresh
    } catch (error) {
        errorMessage.value = error.message;
    } finally {
        isLoading.value = false;
    }
}

onMounted(() => {
  pi_getPlaylistsList();
  fetchMpdStatus(); // Fetch initial status
  pollInterval = setInterval(fetchMpdStatus, 3000); // Poll every 3 seconds
});

onBeforeUnmount(() => {
  clearInterval(pollInterval); // Clear interval on component unmount
});

const autoSavePiPlaylist = async (folder) => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    // --- Start of new logic to determine playlistName ---
    let playlistName = folder;
    const lastSlashIndex = folder.lastIndexOf('/');
    
    if (lastSlashIndex !== -1) {
        // If a slash is found, take the substring after the last slash.
        playlistName = folder.substring(lastSlashIndex + 1);
    }
    // --- End of new logic ---

    const folderPath = folder;

    const response = await fetch(`${apiBase}/pi_playlist_add_folder/${encodeURIComponent(playlistName)}/${encodeURIComponent(folderPath)}`, { 
      method: 'POST' 
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(errorData?.detail || `Server responded with status: ${response.status}`);
    }

    alert(`Playlist "${playlistName}" created/updated successfully!`);
    await pi_getPlaylistsList(); // Refresh the playlist list

  } catch (error) {
    console.error(`Failed to auto save playlist for folder ${folder}:`, error);
    errorMessage.value = error.message;
    alert(`Failed to auto save playlist: ${error.message}`);
  } finally {
    isLoading.value = false;
  }
};

const autoDownloadPodcast = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("Authentication token is not available. Please log in.");
    }

    const response = await fetch(`${apiBase}/download_podcast`, {
      method: 'POST',
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
    alert(data.message || 'Podcast download process completed.');

  } catch (error) {
    console.error('Failed to start podcast download:', error);
    errorMessage.value = error.message;
    alert(`Failed to start podcast download: ${error.message}`);
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
