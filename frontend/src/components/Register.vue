<template>
  <div>
    <main>
      <div>
        <h2>Register</h2>
        <form @submit.prevent="handleRegister">
          <div>
            <label for="reg-username">Username:</label>
            <input type="text" id="reg-username" v-model="username" required :disabled="loading" />
          </div>
          <div>
            <label for="reg-password">Password:</label>
            <input type="password" id="reg-password" v-model="password" required :disabled="loading" />
          </div>
          <div>
            <label for="reg-password-retype">Re-type Password:</label>
            <input type="password" id="reg-password-retype" v-model="passwordRetype" required :disabled="loading" />
          </div>
          <button type="submit" :disabled="loading">
            <span v-if="loading">Registering...</span>
            <span v-else>Register</span>
          </button>
        </form>
        <p v-if="success">{{ success }}</p>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">
import { ref, inject } from 'vue';
import Footer from './Footer.vue';

const username = ref('');
const password = ref('');
const passwordRetype = ref('');
const loading = ref(false); // New loading ref
const success = ref('');

const setGlobalError = inject('setGlobalError') as (message: string) => void;

const handleRegister = async () => {
  if (password.value !== passwordRetype.value) {
    setGlobalError('Passwords do not match');
    return;
  }
  loading.value = true; // Set loading to true
  success.value = '';
  try {
    const response = await fetch('http://127.0.0.1:8001/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || 'Registration failed');
    }

    const data = await response.json();
    success.value = `User ${data.username} registered successfully!`;
    username.value = '';
    password.value = '';
    passwordRetype.value = '';
  } catch (err: any) {
    setGlobalError(err.message);
  } finally {
    loading.value = false; // Set loading to false
  }
};
</script>



