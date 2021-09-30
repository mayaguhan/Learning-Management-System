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
                    {{ row.item.current  }} / {{ row.item.capacity  }}
                </td>
                <td>
                    {{ row.item.start_date }}
                </td>
                <td>
                    {{ row.item.end_date }}
                </td>
                <td width="10">
                    <router-link :to="{ name: 'CourseDetail', params: { course_id: row.item.course_id }}">
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

export default {
    name: 'TrainerCourses',
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        courses: [],
        search: '',
        headers: [
            { text: 'Course Name', value: 'title', align: 'start', sortable: true},
            { text: 'Capacity', value: 'current', filterable: false, sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
    }),
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    methods: {
        getCoursesDetail() {
            // Get all Courses that are conducted by user_id
            let updatedApiWithEndpoint = this.apiLink + "/getallcoursesthatareconductedbyuser";
            let dataObj = { "trainerId": this.currentUserId }
            axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                console.log(response);
                this.courses = response.data;
            })
        },
    },
    created() {
        // Calls method to get course details
        this.getCoursesDetail();

    }
}
</script>

<style>

</style>