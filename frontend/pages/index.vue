<template>
  <div class="bg-gray-100 font-sans leading-normal tracking-normal">

    <navbar />

    <main class="container mx-auto mt-10 mb-10 p-6 min-h-screen">
      <div class="bg-white p-8 rounded-lg shadow-xl text-center">
        <h1 class="text-5xl font-extrabold text-gray-900 mb-4">My Media Player Website! 🚀</h1>
        <p class="text-gray-600 text-lg mb-6">
          This is my personal media player station. 
        </p>
        <template v-if="!isLoggedIn">
          <a href="login" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full transition duration-300">
            Login in 
          </a>
        </template>
      </div>

    </main>

    
    <footer />

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const isLoggedIn = ref(false);

onMounted(() => {
  const token = localStorage.getItem('authToken');
  isLoggedIn.value = !!token;
});
</script>

<style scoped>
/* Scoped styles can be added here if needed */
</style>
