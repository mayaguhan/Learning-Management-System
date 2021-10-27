<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ formatDate(courseDetail.start_date) }} <br>
            End Date: {{ formatDate(courseDetail.end_date) }} <br>
        </p>

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
                    <div style="padding-top:5px">
                        <router-link :to="{ name: 'Quiz', params: { section_id: section.section_id }}">
                            <v-btn depressed small color="#0062E4">
                                <span style="color: white">Attempt Quiz</span> 
                            </v-btn>
                        </router-link>
                    </div>
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
        currentUserId: 12, // To be replaced with user_id of logged in user

        courseDetail: {},
        sections: [],
        materials: [],
    }),
    methods: {

        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },

        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response.data);
                    this.courseDetail = response.data[0];
                    // To be removed
                    this.courseDetail.start_date = "2021-10-31 12:00";
                })
        },
        // Get all Sections by conduct_id (Trainer)
        getCourseSections() {
            let updatedApiWithEndpoint = this.apiLink + "/getsectionsbyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response.data);
                    this.sections = response.data;
                })
        },



        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
        },

        expandSection(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/retrieveallmaterialsinasection";
            let dataObj = { "sectionId": section_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.materials = response.data;
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