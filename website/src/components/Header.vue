<template>
  <div>
    <v-app-bar
      color="#0062E4"
      dense
      dark
    >
      <v-toolbar-title>
        <router-link to="/" id="textRouterLink" style="text-decoration: none;">
          <span class="text-2xl">Bidding Cats</span>
        </router-link> 
      </v-toolbar-title>

      <v-spacer></v-spacer>
      

      <router-link to="/about" id="textRouterLink">
        <span class="mr-3" style="font-weight: bold">
            About Us
        </span>
      </router-link>

      <router-link to="/login" id="textRouterLink">
        <span class="mr-3" style="font-weight: bold">
            Login
        </span>
      </router-link>


    </v-app-bar>
  </div>
</template>

<script>


  export default {
    name: 'Header',

    data () {
      return {
        //
      }
    },
    methods: {
        //
        
    },
    computed: {
        //
    },
    created() {
      //
    }
  }
</script>


<style scoped>

#textRouterLink {
  text-decoration: none;
  color: white;
}
  
</style>