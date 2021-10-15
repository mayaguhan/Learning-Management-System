<template>
  <v-app>
    <div id="app">
      <Header />
    </div>

    <v-main>
      <router-view/>
    </v-main>

    <div class="footer">
      <Footer />
    </div>
  </v-app>
</template>

<script>

import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"


export default {
  name: 'App',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      //
    }
  }
}
</script>

<style>
.footer {
  text-align: center;
    clear: both;
    position: relative;
    bottom: 0;
}
</style>
