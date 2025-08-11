<template>
  <div>
    <main>
      <div>
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div>
            <label for="username">Username:</label>
            <input type="text" id="username" v-model="username" required :disabled="loading" />
          </div>
          <div>
            <label for="password">Password:</label>
            <input type="password" id="password" v-model="password" required :disabled="loading" />
          </div>
          <button type="submit" :disabled="loading">
            <span v-if="loading">Logging in...</span>
            <span v-else>Login</span>
          </button>
        </form>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import Navbar from './Navbar.vue';
import Footer from './Footer.vue';

const username = ref('');
const password = ref('');
const loading = ref(false); // New loading ref

const setGlobalError = inject('setGlobalError') as (message: string) => void;

const handleLogin = async () => {
  loading.value = true; // Set loading to true
  try {
    const response = await fetch('http://127.0.0.1:8001/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: username.value,
        password: password.value,
      }).toString(),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Login failed');
    }

    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    console.log('Login successful!', data);
    window.location.hash = '/piplay';
  } catch (err: any) {
    setGlobalError(err.message);
  } finally {
    loading.value = false; // Set loading to false
  }
};
</script>



