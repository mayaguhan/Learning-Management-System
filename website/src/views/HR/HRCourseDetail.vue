<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ formatDate(courseDetail.start_date) }} <br>
            End Date: {{ formatDate(courseDetail.end_date) }} <br>
            Registration Start Date: {{ formatDate(courseDetail.start_register) }} <br>
            Registration End Date: {{ formatDate(courseDetail.end_register) }} <br>
            Enrolled Students: {{ courseDetail.enrolments }} / {{ courseDetail.capacity }} <br>
            <router-link :to="{ name: 'EnrolledStudent', params: { conduct_id: conduct_id } }">
                <v-btn class="primary">
                    View Enrolled Students
                </v-btn>
            </router-link><br>

            <v-dialog v-model="dialog" max-width="800px">
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

        </p>

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Requisites</h2>
        <span v-if="courseDetail.course_requisite_id > 0">
            {{ courseDetail.cr_course_code }} - {{ courseDetail.cr_title }}
        </span>
        <span v-else>This course has no pre-requisites.</span>

        <h2>Course Content</h2>
        <template>
        <v-expansion-panels focusable :items="sections">
            <v-expansion-panel v-for="section in sections" :key="section.courseId">
                <v-expansion-panel-header>
                    {{ section.section_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <b>Topic's Slide Decks</b><br>
                    <b>Learning Materials</b>
                    <div v-if="section.materials[0].file_name != null">
                        <ul class="mb-3" v-for="material in section.materials" v-bind:key="material.material_id">
                            <li>
                                {{ material.file_name }}<br>
                                <div v-if="material.link.includes('youtube')">
                                    <video-embed css="embed-responsive-16by9" :src="material.link"></video-embed>
                                </div>

                                <v-btn v-else v-bind:href="s3link(material.link)" target="_blank">
                                    {{ material.file_name }}
                                </v-btn>
                            </li>
                        </ul>
                    </div>
                    <div v-else>This topic does not have any learning materials</div>
                    <v-divider></v-divider>
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
            let updatedApiWithEndpoint = this.apiLambda + "/getsectionsbyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    let sectionArr = Object.values(response.data.reduce((result, { 
                        section_id, section_name, sequence, quiz_duration, passing_grade, pass_count, section_count, learner_count, 
                        material_id, file_name, link }) => {
                        // Create section section
                        if (!result[section_id]) result[section_id] = {
                            section_id, section_name, sequence, quiz_duration, passing_grade, pass_count, section_count, learner_count, materials: []
                        };
                        // Append material to section
                        result[section_id].materials.push({ material_id, file_name, link });
                        return result;
                        },{}
                    ));
                    this.sections = sectionArr;
                })
                .catch((error) => {
                    console.log(error, "No sections found")
                })
        },

        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
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
                .catch((error) => {
                    console.log(error, "No trainers found")
                })
        },
        // Add new Enrolment
        enrolStudent(learner_id){
            let updatedApiWithEndpoint = this.apiLink + "/addnewenrolment";
            let dataObj = { "learner_id": learner_id, "conduct_id": this.conduct_id, "self_enrolment": 0, "status": "Progress"}

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
        apiLambda() {
            return this.$store.state.apiLambda;
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