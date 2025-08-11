<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import Pc_Play from './components/Pc_Play.vue'
import Pi_Play from './components/Pi_Play.vue'
import Login from './components/Login.vue'
import Register from './components/Register.vue'
import Navbar from './components/Navbar.vue'

// Global error message ref
const globalError = ref('');

interface RouteComponents {
  [key: string]: any;
}

const routes: RouteComponents = {
  '/pcplay': Pc_Play,
  '/piplay': Pi_Play,
  '/login': Login,
  '/register': Register
}

const currentPath = ref(window.location.hash)

const isAuthenticated = () => {
  return !!localStorage.getItem('access_token');
};

watch(currentPath, (newPath) => {
  const pathKey = newPath.slice(1) || '/';
  const publicRoutes = ['/login', '/register'];

  if (!publicRoutes.includes(pathKey) && !isAuthenticated()) {
    window.location.hash = '/login';
  }
}, { immediate: true });

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentComponent = computed(() => {
  const pathKey = currentPath.value.slice(1) || '/'
  return routes[pathKey] || Pc_Play
})
</script>

<template>
  <div id="app-container">
    <Navbar />
    <div v-if="globalError" class="global-error">{{ globalError }}</div>
    <main>
      <component :is="currentComponent" />
    </main>
  </div>
</template>

<style scoped>
/* Remove nav styles as they are now in Navbar.vue */

.global-error {
  background-color: #ffdddd;
  color: #d8000c;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #d8000c;
  border-radius: 5px;
  text-align: center;
}
</style>
