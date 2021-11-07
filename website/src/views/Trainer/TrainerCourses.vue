<template>
    <div>
        <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table :headers="headers" :items="courses" :search="search">
        <template v-slot:item="row">
            <tr>
                <td>
                    {{row.item.course_code}} - {{row.item.title}} 
                </td>
                <td>
                    {{ row.item.enrolments  }} / {{ row.item.capacity  }}
                </td>
                <td>
                    {{ formatDate(row.item.start_date) }}
                </td>
                <td>
                    {{ formatDate(row.item.end_date) }}
                </td>
                <td>
                    {{ formatDate(row.item.start_register) }}
                </td>
                <td>
                    {{ formatDate(row.item.end_register) }}
                </td>
                <td width="10">
                    <router-link :to="{ name: 'CourseDetail', params: { conduct_id: row.item.conduct_id }}">
                        <v-btn depressed small color="#0062E4">
                            <span style="color: white">View Class</span> 
                        </v-btn>
                    </router-link>
                </td>
            </tr>
        </template>
        </v-data-table>
        </v-card>
    </div>
</template>

<script>
import axios from 'axios';
import moment from "moment";

export default {
    name: 'TrainerCourses',
    data: () => ({
        courses: [],
        search: '',
        headers: [
            { text: 'Course', value: 'course_code', align: 'start', sortable: true},
            { text: 'Capacity', value: 'current', filterable: false, sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: 'Register Start Date', value: 'start_register', filterable: false, sortable: true},
            { text: 'Register End Date', value: 'end_register', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
    }),
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        },
        getUserId() {
            return this.$store.state.userId;
        }
    },
    methods: {
        // Get all Courses that are conducted by trainer_id
        getCoursesDetail(trainer_id) {
            let updatedApiWithEndpoint = this.apiLink + "/getallcoursesthatareconductedbyuser";
            let dataObj = { "trainerId": trainer_id }
            axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                this.courses = response.data.data;
            })
            .catch((error) => {
                console.log(error, "No courses found")
            })
        },
        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD HH:mm');
        }
    },
    created() {
        // Calls method to get course details
        this.getCoursesDetail(this.getUserId);

    }
}
</script>

<style>

</style>