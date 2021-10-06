<template>
    <div>
        <v-row>
            <v-col cols="10">
                <h1>
                    Enrolled Students
                </h1>
            </v-col>
            <v-col cols="2">
                <h2>
                    {{ courseDetail.enrollment_count }} out of {{ courseDetail.capacity }}
                </h2>
            </v-col>
        </v-row>
        
        
        <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table :headers="headers" :items="enrolledStudents" :search="search">
        <template v-slot:item="row">
            <tr>
                <td>
                    {{ row.item.name }} <br>
                    {{ row.item.username }}
                </td>
                <td>
                    {{ row.item.seniority_level }}
                </td>
                <td>
                    {{ row.item.email }} <br>
                    {{ row.item.contact }}
                </td>
                <td>
                    <v-progress-linear color="blue" rounded 
                        :value=" row.item.progress / sectionCount * 100 ">
                    </v-progress-linear>
                    {{ (row.item.progress / sectionCount * 100).toFixed(0) }}%  Complete
                </td>
                <td>
                    <!-- TO DO: View Student Information -->
                    <!-- <router-link :to="{ name: 'TBC', params: { TBC }}"> -->
                        <v-btn depressed small color="#0062E4">
                            <span style="color: white">View Details</span> 
                        </v-btn>
                    <!-- </router-link> -->
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
    name: "EnrolledStudent",
    props: {
        course_id: parseInt({ type: Number })
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        courseDetail: {},
        sectionCount: 0,
        enrolledStudents: [],
        search: '',
        headers: [
            { text: 'Student Name', value: 'name', align: 'start', sortable: true},
            { text: 'Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: 'Progress', value: 'progress', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
    }),
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    methods: {
        // Get a Course information by course_id and trainer_id
        getCourseDetail(course_id, currentUserId) {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobytrainerandcourse";
            let dataObj = { "courseId": course_id, "trainerId": currentUserId }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data[0];
                })
        },
        // Get the total amount of section for a given course
        getSectionCount(course_id, trainer_id) {
            console.log(course_id, trainer_id);
            // let updatedApiWithEndpoint = this.apiLink + "/TBC";
            // let dataObj = { "courseId": course_id, "trainerId": trainer_id }
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         this.sectionCount = response.data[0];
            //     })
            this.sectionCount = 3;
        },

        // Get all Learners that are enrolled into a course by course_id and trainer_id
        getEnrolledStudents(course_id, trainer_id) {
            let updatedApiWithEndpoint = this.apiLink + "/getalllearnersenrolledtocoursebycourseidandtrainerid";
            let dataObj = { "courseId": course_id, "trainerId": trainer_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.enrolledStudents = response.data;
                })
        }

    },
    created() {
        // Calls method to get course details
        this.getCourseDetail(this.course_id, this.currentUserId);
        
        // Get Section count by course_id and trainer_id
        this.getSectionCount(this.course_id, this.currentUserId);

        // Retrieves all the learners that are enrolled into a course by course_id and trainer_id 
        this.getEnrolledStudents(this.course_id, this.currentUserId);

    }
}
</script>

<style>

</style>