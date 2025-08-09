<template>
  <nav class="bg-gray-800 p-4 text-white">
    <div class="container mx-auto flex justify-between items-center">
      <div class="text-lg font-bold">My App</div>
      <div class="space-x-4">
        <a href="#/" class="hover:text-gray-300">PC Play</a>
        <a href="#/pi" class="hover:text-gray-300">Pi Play</a>

        <template v-if="!isLoggedIn">
          <a href="#/login" class="hover:text-gray-300">Login</a>
          <a href="#/register" class="hover:text-gray-300">Register</a>
        </template>
        <template v-else>
          <button @click="handleLogout" class="hover:text-gray-300">Logout</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';

const isLoggedIn = ref(false);

const checkLoginStatus = () => {
  isLoggedIn.value = !!localStorage.getItem('access_token');
};

watchEffect(() => {
  checkLoginStatus();
});

const handleLogout = () => {
  localStorage.removeItem('access_token');
  isLoggedIn.value = false;
  window.location.hash = '/login';
};
</script>

<style scoped>
/* No specific scoped styles needed if using Tailwind CSS */
</style>
