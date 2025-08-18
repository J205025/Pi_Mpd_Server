<template>
  <nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex justify-between items-center">
      <a href="#" class="text-white text-2xl font-bold">
        My Media Player
      </a>
      
      <div class="hidden md:flex space-x-6">
        <a href="/" class="text-gray-300 hover:text-white transition duration-300">Home</a>
        <a href="/pcplayer" class="text-gray-300 hover:text-white transition duration-300">PC Player</a>
        <a href="/pcplayer_ver1" class="text-gray-300 hover:text-white transition duration-300">PC Player_ver1</a>
        <a href="/piplayer" class="text-gray-300 hover:text-white transition duration-300">Pi Player</a>

        
        <!-- Show user info and logout when logged in -->
        <template v-if="isLoggedIn">
          <span class="text-gray-300">Welcome, {{ currentUser }}</span>
          <button @click="handleLogout" class="text-gray-300 hover:text-white transition duration-300">
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
      <a href="/" class="block text-gray-300 hover:text-white py-2 px-4">Home</a>
      <a href="/pcplayer" class="block text-gray-300 hover:text-white py-2 px-4">PC Player</a>
      <a href="/pcplayer_ver1" class="block text-gray-300 hover:text-white py-2 px-4">PC Player_ver1</a>
      <a href="/piplayer" class="block text-gray-300 hover:text-white py-2 px-4">Pi Player</a>
      <a href="#" class="block text-gray-300 hover:text-white py-2 px-4">Contact</a>
      
      <template v-if="isLoggedIn">
        <span class="block text-gray-300 py-2 px-4">Welcome, {{ currentUser }}</span>
        <button @click="handleLogout" class="block text-gray-300 hover:text-white py-2 px-4 text-left w-full">
          Logout
        </button>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Login from '~/pages/login.vue';

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
    // Check if we have a token
    const token = window.authToken;
    if (!token) {
      isLoggedIn.value = false;
      return;
    }

    // Verify token with backend
    const response = await fetch('http://127.0.0.1:8001/users/me/', {
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
      // Token is invalid, clear it
      delete window.authToken;
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
  // Clear the stored token
  delete window.authToken;
  
  // Update local state
  isLoggedIn.value = false;
  currentUser.value = '';
  
  // Redirect to home page
  window.location.href = '/';
};

// Check auth status when component mounts
onMounted(() => {
  checkAuthStatus();
});
</script>

<style scoped>
/* You can add component-specific styles here */
</style>