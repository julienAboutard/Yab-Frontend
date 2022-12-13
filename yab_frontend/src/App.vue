<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <v-toolbar dark color="#162130" style="height:10vh;">
      <v-toolbar-title class="white--text">
        <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
      </v-toolbar-title>
      <v-toolbar-items>
        <RouterLink to="/apprenants">Apprenants</RouterLink> |&nbsp;
        <RouterLink to="/briefs">Briefs</RouterLink>
      </v-toolbar-items>
      <v-spacer></v-spacer>
    </v-toolbar>
  </v-app>


  <!-- <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />
      <nav>
        <RouterLink to="/apprenants">Apprenants</RouterLink> |&nbsp;
        <RouterLink to="/briefs">Briefs</RouterLink>
      </nav>
  </header> -->

  <RouterView />
</template>

<style>
  .v-application__wrap {
    min-height: 0vh !important;
  }
</style>