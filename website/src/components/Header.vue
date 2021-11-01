<template>
  <div>
    <v-app-bar
      color="#0062E4"
      dense
      dark
    >
      <v-toolbar-title>

        <!-- Default home page -->
        <template v-if="type == ''">
          <router-link to="/" id="textRouterLink" style="text-decoration: none;">
            <span class="text-2xl">Bidding Cats</span>
          </router-link>   
        </template>

        <!-- For learner -->
        <template v-if="type == 'learner'">
          <router-link to="/learnercourses" id="textRouterLink" style="text-decoration: none;">
            <span class="text-2xl">Bidding Cats</span>
          </router-link> 
        </template>

        <!-- For trainer -->
        <template v-if="type == 'trainer'">
          <router-link to="/trainercourses" id="textRouterLink" style="text-decoration: none;">
            <span class="text-2xl">Bidding Cats</span>
          </router-link> 
        </template>

      </v-toolbar-title>

      <v-spacer></v-spacer>
      
      <template v-if="!login">
        <router-link to="/about" id="textRouterLink">
          <span class="mr-3" style="font-weight: bold">
              About Us
          </span>
        </router-link>

        <!-- <router-link to="/login" id="textRouterLink">
          <span class="mr-3" style="font-weight: bold">
              Login
          </span>
        </router-link> -->
      </template>

      <template v-else>
          <button class="mr-3" style="font-weight: bold" @click="logout()">
              Logout
          </button  >
      </template>



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
        logout() {
            this.$store.commit('setUserId', "");
            this.$store.commit('setLogin', false);
            this.$store.commit('setType', "");

            this.$router.push("/");
        }
        
    },
    computed: {
        login(){
            return this.$store.state.login;
        },
        type(){
          return this.$store.state.type;
        }
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
