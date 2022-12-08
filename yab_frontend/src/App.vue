<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
      <nav>
        <RouterLink to="/apprenants">Apprenants</RouterLink> |&nbsp;
        <RouterLink to="/briefs">Briefs</RouterLink>
      </nav>
  </header>

  <RouterView />
</template>
