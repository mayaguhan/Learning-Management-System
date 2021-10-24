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
            </v-container>

            <div class="pb-4 pt-3">
                <v-btn depressed color="primary" @click="login()">
                    Submit
                </v-btn>
            </div>
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
            type: this.$route.params.type,
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
                    console.log(response);

                    // Login OKAY
                    if (response.status == 200 && response.data.length > 0){
                        console.log(response.data[0].user_id);


                        // Store required data in vuex store
                        this.$store.commit('setUserId', response.data[0].user_id);
                        this.$store.commit('setLogin', true);
                        this.$store.commit('setType', this.type);
                        
                        // Check if it is updated
                        // console.log(this.$store.state.userId);
                        // console.log(this.$store.state.login);
                        // console.log(this.$store.state.type);


                        if (this.type == "learner"){
                            this.$router.push("/learnercourses");
                        }
                        if (this.type == "trainer" && response.data[0].seniority_level == "Senior Engineer") {
                            this.$router.push("/trainercourses");
                        }
                    } else {
                        this.styleObj.display = "block";
                    }

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