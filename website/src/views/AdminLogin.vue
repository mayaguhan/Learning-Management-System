<template>
    <div class="mt-5" style="justify-content: center">
        <div class="loginBox pr-5 pl-5">
            <v-container>
                <v-row class="pb-5 pt-4">
                    <h4>User Login</h4>
                </v-row>
                <v-row>
                    Enter your company email
                </v-row>
                <v-row class="mt-0 pt-2">
                    <v-text-field
                        v-model="email"
                        :rules="emailRules"
                        label="E-mail"
                        required
                    ></v-text-field>
                </v-row>
                <v-row class="mt-2 mb-2 pt-2">
                    <v-btn style="width:30%" depressed color="primary" @click="login()">
                        Submit
                    </v-btn>
                </v-row>
            </v-container>
        </div>
        <div class="message" v-bind:style="styleObj">
            <div class="errorMsg mt-10">
            
                <span style="color: red">Incorrect email entered. Please try again.</span>
            </div>

        </div>


    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "Login",
    components: {
        //
    },
    data() {
        return {
            email: '',
            emailRules: [
                v => !!v || 'E-mail is required',
                v => /.+@.+/.test(v) || 'E-mail must be valid',
            ],
            styleObj: {
                display: "none"
            }
        }
    },
    methods: {
        login() {

            var updatedApiWithEndpoint = this.apiLink + "/retrieveuseridbyemail";
            
            var dataObj = {
                "email": this.email
            }

            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) =>{
                    // Login OKAY
                    if (response.data.code == 200){
                        // Store required data in vuex store
                        this.$store.commit('setUserId', response.data.user_id);
                        this.$store.commit('setLogin', true);
                        this.$store.commit('setType', "admin");
                        this.$router.push("/hrcourses");

                    } else {
                        this.styleObj.display = "block";
                    }
                })
                .catch(error => {
                    console.log(error);
                    this.styleObj.display = "block";
                })
        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    }
}
</script>

<style>

.loginBox {
    border: 3px solid #0062E4;
    margin: auto;
    width: 25%;
}

.errorMsg{
    border: 3px solid black;
    margin: auto;
    width: 25%;    
    text-align: center;
}

</style>