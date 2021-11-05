<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ formatDate(courseDetail.start_date) }} <br>
            End Date: {{ formatDate(courseDetail.end_date) }} <br>
        </p>

        <router-link :to="{ name: 'EnrolledStudent', params: { conduct_id: conduct_id } }">
            <v-btn class="primary">
                View Enrolled Students
            </v-btn>
        </router-link>
        <br>

        <v-dialog v-model="dialog" max-width="600px">
            <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary mt-3" dark v-bind="attrs" v-on="on">
                    Enrol Students
                </v-btn>
            </template>
            <v-card>
                <v-card-title>
                    Enrol Students
                </v-card-title>
                <v-card-text>
                    <v-data-table :headers="headers" :items="enrolStudents" :search="search" :key="componentKey">
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
                                <v-btn class="primary" @click="enrolStudent(row.item.user_id)">
                                    Enrol
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                    </v-data-table>
                </v-card-text>
            </v-card>
        </v-dialog>

        <!-- <router-link :to="{ name: 'EnrolStudent', params: { conduct_id: conduct_id, course_id: courseDetail.course_id } }"> -->
        
        <!-- </router-link>  -->

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Content</h2>

        <template>
        <v-expansion-panels focusable :items="sections">
            <v-expansion-panel v-for="section in sections" :key="section.course_id" @click="expandSection(section.section_id)">
                <v-expansion-panel-header :disabled="section.disabled">
                    <span v-if="section.boldSection==true"><b>{{ section.section_name }}</b></span>
                    <span v-else>{{ section.section_name }}</span>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <div v-if=" section.section_id != null">

                        <!-- Display materials -->

                        <!-- Upload slide decks -->
                        <b>Topic's Slide Decks</b><br>
                        <ul v-for="material in materials" v-bind:key="material.material_id">
                            <li v-if="materials.length > 0" >
                                <v-btn v-bind:href="s3link(material.link)" target="_blank">
                                    {{ material.file_name }}
                                </v-btn>
                            </li>
                            <li v-else>
                                <b>This section has no materials</b>
                            </li>
                        </ul>
                        
                    </div>
                    <v-divider></v-divider>

                    <div v-if="section.best_grade !== null">
                        <b>Best Grade: {{ section.best_grade }} / 100</b>
                    </div>
                    <v-divider></v-divider>
                    <!-- <div style="padding-top:5px">
                        <router-link :to="{ name: 'Quiz', params: { section_id: section.section_id }}">
                            <v-btn depressed small color="#0062E4">
                                <span style="color: white">Attempt Quiz</span> 
                            </v-btn>
                        </router-link>
                    </div> -->
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        </template>

    </div>
</template>

<script>
import axios from 'axios';
import moment from "moment";

export default {
    name: "CourseDetail",
    props: {
        conduct_id: parseInt({ type: Number })
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        courseDetail: {},
        sections: [],
        materials: [],
        enrolStudents: [],
        search: '',
        dialog: false,
        headers: [
            { text: 'Student Name', value: 'name', align: 'start', sortable: true},
            { text: 'Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        componentKey: 0
    }),
    methods: {
        forceRerender() {
            this.componentKey += 1;
        },
        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },

        // Get a Single Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data.data[0];
                    this.getEnrolStudents(response.data.data[0].course_id, response.data.data[0].course_requisite_id)
                })
        },
        // Get all Sections by conduct_id (Trainer)
        getCourseSections() {
            let updatedApiWithEndpoint = this.apiLink + "/getsectionsbyconductid"; // Not up yet
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.sections = response.data.data;
                })
        },

        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
        },
        
        // Retrieves all materials of a section
        expandSection(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/retrieveallmaterialsinasection";
            let dataObj = { "sectionId": section_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.materials = response.data.data;
            })
        },

        // Get all Engineers that are eligible for a course by course id
        getEnrolStudents(course_id, requisite_id) {
            let updatedApiWithEndpoint = this.apiLink;
            if (requisite_id == null) {
                updatedApiWithEndpoint += "/getallengineerseligibleforcoursebycourse";
            } else {
                updatedApiWithEndpoint += "/getallengineerseligibleforcoursewithreqbycourse";
            }
            let dataObj = { "courseId": course_id}
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.enrolStudents = response.data.data;
                })
        },

        enrolStudent(learner_id){
            let updatedApiWithEndpoint = this.apiLink + "/addnewenrolment";
            let dataObj = { "learnerId": learner_id, "conductId": this.conduct_id, "selfEnrolment": 0, "status": "Progress"}

            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response);
                    this.getEnrolStudents(this.courseDetail.course_id, this.courseDetail.course_requisite_id)
                    this.forceRerender();
                    alert("This student has successfully been enrolled into the course!");
                })
        },

    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        },

        s3Link(){
            return this.$store.state.s3Link;
        },
    },
    created() {
        // Calls method to get course details
        this.getCourseDetail();

        // Calls method to get section details
        this.getCourseSections();
    }
}
</script>