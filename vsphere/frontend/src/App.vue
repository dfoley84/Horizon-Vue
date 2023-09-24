<template>
  <div id="app">
    <Headerbar v-if="!hideUI" />
    <div class="main-section columns">
      <Navigation v-if="!hideUI" />
      <main class="column">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import Headerbar from '@/components/Header/Header.vue';
import Navigation from '@/components/Header/NavigationBar/Navigation.vue';

export default {
  components: {
    Headerbar,
    Navigation,
  },
  computed: {
    hideUI() {
      return this.$route.meta.hideUI;
    }
  }
}
</script>

<style lang="scss">
@import '@/styles/index.scss';
</style>
