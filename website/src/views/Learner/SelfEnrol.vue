<template>  
    <div>
        <v-container>
            <v-row>
                <v-col>
                    <h3>Please Select a Trainer:</h3>
                    <br>
                    <label :for="trainer.user_id" v-for="trainer in trainerList" :key="trainer.name">
                        <input type="radio"
                        name="selectedTrainer"
                        :value="trainer.user_id"
                        v-model="selectedTrainerId"
                        :id="trainer.user_id"
                        >
                        {{ trainer.name }}
                        <br>
                        <br>
                    </label>
                    <!-- <div>You have selected Trainer ID: {{ selectedTrainerId }}</div> -->
                    <br>
                    <v-btn depressed small color="#0062E4" @click="enrolCourse(selectedTrainerId)">
                        <span style="color: white">Submit</span> 
                    </v-btn>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "SelfEnrol",
    props: {
        course_id: parseInt({ type: Number }),
    },
    data() {
        return {
            currentUserId: 4,
            selectedTrainerId: null,
            trainerList: [],
        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created(){

        var updatedApiWithEndpoint = this.apiLink + "/retrievealltrainersconductingcourse";
        var dataObj = {
              "courseId" : this.course_id,
        };
        axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                console.log(response.data);
                this.trainerList = response.data;
            })

    },
    methods: {
        enrolCourse(selectedTrainerId){
            //console.log(selectedTrainerId);
            alert("You have successfully enrolled into the selected course")
            // Insert API Call
            var dataObjEnroll = {
              "learnerId" : this.currentUserId,
              "courseId" : this.course_id,
              "trainerId" : selectedTrainerId,
              "status" : "Progress"
            }
            //console.log(dataObjEnroll);
            const axios = require('axios');
            var updatedApiWithEndpoint = this.apiLink + "/addnewenrolment";
            console.log(this.apiLink);
            axios.post(updatedApiWithEndpoint, dataObjEnroll)
                .then((response) => {
                  console.log(response.data);
                })
        }
    }

}
</script>

<style>

</style>