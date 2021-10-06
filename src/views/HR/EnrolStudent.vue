<template>
    <div>

        <h1 style="padding: 15px">
            Enrol Eligible Students
        </h1>       
        
        <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table :headers="headers" :items="enrolStudents" :search="search">
        <template v-slot:item="row">
            <tr>
                <td>
                    {{ row.item.name }}
                </td>
                <td>
                    {{ row.item.seniority_level }}
                </td>
                <td>
                    {{ row.item.email }} <br>
                    {{ row.item.contact }}
                </td>
                <td width="10">
                        <v-btn
                        depressed
                        small
                        color="#0062E4"
                        @click="enrolStudent(row.item.user_id)">
                            <span style="color: white">Enroll</span>
                        </v-btn>
                </td>
            </tr>
        </template>
        </v-data-table>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "EnrolStudent",
    props: {
        course_id: parseInt({ type: Number }),
        trainer_id: parseInt({ type: Number })
    },
    data: () => ({

        status: "Progress",

        enrolStudents: [],
        search: '',
        headers: [
            { text: 'Student Name', value: 'name', align: 'start', sortable: true},
            { text: 'Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ]
    }),

    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },

    methods: {

        // Get all Learners that are eligible for the course
        getEnrolStudents() {
            let updatedApiWithEndpoint1 = this.apiLink + "/getuserseligibleforcourse";
            let dataObj = { "courseId": this.course_id}
            axios.post(updatedApiWithEndpoint1, dataObj)
                .then((response) => {
                    console.log(response);
                    this.enrolStudents = response.data;
                })
        },

        // TO-DO: ensure HR doesn't enrol the same student twice before refreshing the page

        enrolStudent(learner_id){
            let updatedApiWithEndpoint3 = this.apiLink + "/addnewenrolment";
            let dataObj = { "learnerId": learner_id, "courseId": this.course_id, "trainerId": this.trainer_id, "status": status}
            axios.post(updatedApiWithEndpoint3, dataObj)
                .then((response) => {
                    console.log(response);
                })
            var message = "This student has successfully been enrolled into the course!";
            alert(message);
        },

    },

    created() {
        // Retrieves all the learners that are eligible for the course
        this.getEnrolStudents();



    }
}
</script>

<style>

</style>