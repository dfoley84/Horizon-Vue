<template>
  <div id="app">
    <Headerbar />
    <div class="main-section columns">
      <Navigation />
      <main class="column">
        <router-view />
        <Footer />
      </main>
    </div>
  </div>
</template>


<script>
import Headerbar from '@/components/Header/Header.vue'
import Navigation from '@/components/NavigationBar/Navigation.vue'
import Footer from '@/components/Footer/Footer.vue'

export default{
   components: { 
    Headerbar,
    Navigation,
    Footer
  },
};
</script>

<style lang="scss">
@import '@/design/index.scss';
</style>


