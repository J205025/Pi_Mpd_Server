<template>
  <nav class="bg-gray-800 p-4 shadow-lg">
    <div class="container mx-auto flex justify-between items-center">
      <a href="#" class="text-white text-2xl font-bold">
        My Media Player
      </a>
      
      <div class="hidden md:flex space-x-6">
        <a href="/" class="text-gray-300 hover:text-white transition duration-300">Home</a>
        <a href="/pcplayer" class="text-gray-300 hover:text-white transition duration-300">PC Player</a>
        <a href="/piplayer" class="text-gray-300 hover:text-white transition duration-300">Pi Player</a>
        <a href="#" class="text-gray-300 hover:text-white transition duration-300">Contact</a>
      </div>
      
      <button @click="toggleMobileMenu" class="md:hidden text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" />
        </svg>
      </button>
    </div>
    
    <div :class="{ 'hidden': !isMobileMenuOpen }" class="md:hidden mt-4">
      <a href="/" class="block text-gray-300 hover:text-white py-2 px-4">Home</a>
      <a href="/pcplayer" class="block text-gray-300 hover:text-white py-2 px-4">Pc Player</a>
      <a href="/piplayer" class="block text-gray-300 hover:text-white py-2 px-4">Pi Player</a>
      <a href="#" class="block text-gray-300 hover:text-white py-2 px-4">Contact</a>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

// This state and function are now encapsulated within the Nav component
const isMobileMenuOpen = ref(false);

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};
</script>

<style scoped>
/* You can add component-specific styles here */
</style>