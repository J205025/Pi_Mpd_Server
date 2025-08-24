<template>
  <nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex justify-between items-center">
      <NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="text-white text-2xl font-bold">
        My Media Player
      </NuxtLink>
      
      <div class="hidden md:flex items-center space-x-6">
        <!--NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="text-gray-300 hover:text-white transition duration-300">Home</NuxtLink-->
        <NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="text-gray-300 hover:text-white transition duration-300">電腦播放</NuxtLink>
        <NuxtLink :to="isLoggedIn ? '/piplayer' : '/'" class="text-gray-300 hover:text-white transition duration-300">音響播放</NuxtLink>
        <NuxtLink :to="isLoggedIn ? '/playlist' : '/'" class="text-gray-300 hover:text-white transition duration-300">歌單編輯</NuxtLink>
        <div class="flex-grow"></div>

        <template v-if="isLoggedIn">
          <span class="text-gray-300">Hi, {{ currentUser.toUpperCase() }}</span>
          <button @click="handleLogout" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Logout
          </button>
        </template>
      </div>
      
      <button @click="toggleMobileMenu" class="md:hidden text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
        </svg>
      </button>
    </div>
    
    <div :class="{ 'hidden': !isMobileMenuOpen }" class="md:hidden mt-4">
      <!--NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">Home</NuxtLink-->
      <NuxtLink :to="isLoggedIn ? '/pcplayer' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">電腦播放</NuxtLink>
      <NuxtLink :to="isLoggedIn ? '/piplayer' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">音響播放</NuxtLink>
      <NuxtLink :to="isLoggedIn ? '/playlist' : '/'" class="block text-gray-300 hover:text-white py-2 px-4">歌單編輯</NuxtLink>      
      <template v-if="isLoggedIn">
        <span class="block text-gray-300 py-2 px-4">Welcome, {{ currentUser.toUpperCase() }}</span>
        <button @click="handleLogout" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          Logout
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// Get runtime config
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Mobile menu state
const isMobileMenuOpen = ref(false);

// Authentication state
const isLoggedIn = ref(false);
const currentUser = ref('');

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

// Check authentication status
const checkAuthStatus = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      isLoggedIn.value = false;
      return;
    }

    const response = await fetch(`${apiBase}/users/me/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      }
    });

    if (response.ok) {
      const userData = await response.json();
      isLoggedIn.value = true;
      currentUser.value = userData.username;
    } else {
      localStorage.removeItem('authToken');
      isLoggedIn.value = false;
      currentUser.value = '';
    }
  } catch (error) {
    console.error('Auth check error:', error);
    isLoggedIn.value = false;
    currentUser.value = '';
  }
};

// Handle logout
const handleLogout = () => {
  localStorage.removeItem('authToken');
  isLoggedIn.value = false;
  currentUser.value = '';
  // Use Nuxt's navigateTo for proper SPA navigation
  navigateTo('/');
};

// Check auth status when component mounts
onMounted(() => {
  checkAuthStatus();
});
</script>