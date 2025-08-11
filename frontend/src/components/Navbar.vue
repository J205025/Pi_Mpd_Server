<template>
<nav class="navbar">
<ul>
  <li><a class="active" href="#home">Home</a></li>
  <li><a href="#pcplay">Pc Player</a></li>
  <li><a href="#piplay">Pi_Player</a></li>
  <li><a href="#about">About</a></li>
</ul>
</nav>
</template>

<script setup lang="ts">
</script>

<style scoped>
/* Basic reset for consistent styling */
body {
  margin: 0;
  font-family: sans-serif;
}

/* Navbar container */
.navbar {
  background-color: #333; /* Dark background */
  padding: 10px 20px; /* Spacing inside the navbar */
}

/* List of links */
.nav-links {
  list-style: none; /* Remove bullet points */
  margin: 0;
  padding: 0;
  display: flex; /* Use flexbox for horizontal layout */
  justify-content: flex-end; /* Align links to the right */
}

/* Individual list items */
.nav-links li {
  margin-left: 20px; /* Spacing between links */
}

/* Anchor tags (the links themselves) */
.nav-links a {
  color: white; /* Text color */
  text-decoration: none; /* Remove underline */
  font-size: 18px; /* Font size */
  padding: 5px 10px; /* Padding for click area */
  transition: color 0.3s ease; /* Smooth color transition on hover */
}

/* Hover effect */
.nav-links a:hover {
  color: #ddd; /* Lighter color on hover */
}
</style>
