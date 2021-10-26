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
                        

                        <!-- Upload slide decks -->
                        <b>Topic's Slide Decks</b><br>
                        <ul v-for="material in materials" v-bind:key="material.material_id">
                            
                        </ul>
                        <!-- TO DO: Method to upload new materials -->

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
        // Get a Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data[0];
                })
        },
        // Get all Sections by conduct_id and user_id (Learner)
        getCourseSections() {
            let updatedApiWithEndpoint = this.apiLink + "/getallsectionsbyconductanduserid";
            let dataObj = { "conductId": this.conduct_id, "learnerId": this.currentUserId } 
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    let sections = response.data;
                    let boldSection = false;
                    sections.forEach(section => {
                        if (section.result == "No Attempt" && boldSection == false) {
                            section["boldSection"] = true
                            boldSection = true;
                        } else if (section.result == "No Attempt" && boldSection == true) {
                            section["disabled"] = true
                        }
                    });
                    console.log(sections);
                    this.sections = sections;
                })
        },
        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
        },
        expandSection(section_id) {
            // console.log(section_id);
            // Get all Materials by section_id
            // Dummy JSON, to be replaced with API call
            let materialData = [{
                "material_id": 1, 
                "material_name": "Section " + section_id + " Material 1",
                "type": "pdf",
                "link": "https://www.google.com.sg/"
                },
                {
                "material_id": 2, 
                "material_name": "Section " + section_id + " Material 2",
                "type": "pdf",
                "link": "https://www.google.com.sg/"
            }];
            this.materials = materialData;
        },
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
        // Calls method to get course details
        this.getCourseDetail();

        // Calls method to get section details
        this.getCourseSections();
    }
}
</script>