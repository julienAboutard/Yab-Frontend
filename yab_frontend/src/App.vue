<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <v-card class="head">
        <v-toolbar color="#b0564f">
          <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="75" height="75" />
          <v-spacer></v-spacer>
          <nav>
            <v-btn class="tool" to="/" icon><v-icon>mdi-home</v-icon></v-btn> 
            <v-btn class="tool" to="/apprenants" icon><v-icon>mdi-account-multiple</v-icon></v-btn>
            <v-btn class="tool" to="/briefs" icon><v-icon>mdi-file-multiple</v-icon></v-btn>
          </nav>
        </v-toolbar>
    </v-card>
  </div>
  <RouterView />
</template>

<style>
  .head {
    width: 90%;
  }
  .v-toolbar {
    height: fit-content;
  }
  #app {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .tool {
    margin-right: 10px;
  }
  nav {
    padding-right: 4px;
  }
  body {
    width: auto;
    padding: 4px;
    margin: 0%;
  }
</style>