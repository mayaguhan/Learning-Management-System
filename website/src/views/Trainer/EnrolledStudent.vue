<template>
    <div>
        <v-row>
            <v-col cols="10">
                <h1>
                    {{ courseDetail.course_code }} - {{ courseDetail.title }} Students
                </h1>
            </v-col>
            <v-col cols="2">
                <h2>
                    {{ courseDetail.enrolments }} out of {{ courseDetail.capacity }}
                </h2>
            </v-col>
        </v-row>
        <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        </v-card-title>
        <v-data-table :headers="headers" :items="enrolledStudents" :search="search">
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
                <td>
                    <v-progress-linear color="blue" rounded 
                        :value=" row.item.progress / row.item.section_count * 100 ">
                    </v-progress-linear>
                    {{ (row.item.progress / row.item.section_count * 100).toFixed(0) }}%  Complete
                </td>
                <td>
                    <!-- TO DO: View Student Information -->
                    <!-- View Learner Dialog -->
                    <v-btn color="primary"
                    @click.stop="$set(selectedLearner, row.item.user_id, true)  ">
                        View Learner
                    </v-btn>
                    <v-dialog v-model="selectedLearner[row.item.user_id]" scrollable max-width="1200" :key="row.item.user_id">
                        <v-card>
                        <v-card-title>
                            <span>{{ row.item.name }}</span>
                        </v-card-title>
                        <v-card-subtitle>
                            Email: {{ row.item.email }} <br>
                            Contact: {{ row.item.contact }} <br>
                            Seniority Level: {{ row.item.seniority_level }} <br>
                        </v-card-subtitle>
                        <v-card-text>
                            <!-- TO DO: View Student's Quiz Attempts -->
                        </v-card-text>
                        <v-card-actions>
                            <!-- <v-btn color="primary" @click.stop="$set(selectedLearner, row.item.course_id, false)">Close</v-btn> -->
                        </v-card-actions>
                        </v-card>
                    </v-dialog>
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
        conduct_id: parseInt({ type: Number })
    },
    data: () => ({
        currentUserId: 2, // To be replaced with user_id of logged in user

        courseDetail: {},
        enrolledStudents: [],
        search: '',
        selectedLearner: {},

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
        // Get a Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data.data[0];
                })
        },
        // Get all Learners that are enrolled into a course by conduct_id
        getEnrolledStudents() {
            let updatedApiWithEndpoint = this.apiLink + "/getalllearnersenrolledbyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.enrolledStudents = response.data.data;
                })
                .catch((error) => {
                    console.log(error, "No learners found")
                })
        }

    },
    created() {
        // Calls method to get course details
        this.getCourseDetail();

        // Retrieves all the learners that are enrolled into a course by course_id and trainer_id 
        this.getEnrolledStudents();

    }
}
</script>

<style>

</style>