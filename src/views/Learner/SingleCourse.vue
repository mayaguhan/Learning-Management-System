<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ courseDetail.start_date }} <br>
            End Date: {{ courseDetail.end_date }} <br>
            Enrolled Students: {{ courseDetail.current }} / {{ courseDetail.capacity }} <br>
        </p>

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Content</h2>

        <template>
        <v-expansion-panels focusable :items="sections">
            <v-expansion-panel v-for="section in sections" :key="section.course_id" @click="expandSection(section.section_id)">
                <v-expansion-panel-header>
                    <div v-if="ifUpdated(section.best_grade)"><b>{{ section.section_name }}</b></div>
                    <div v-else>{{ section.section_name }}</div>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <!-- Checks a section has pre-requisite -->
                    <!-- Removed ^ -->

                    <!-- TO DO: Method to update section's pre-requisite -->
                    <v-divider></v-divider>

                    <!-- Quiz and Slide Decks can only if a section exists (i.e. has section_id).
                    Newly added sections have to be Saved before quiz or materials can be added -->
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
                        <router-link :to="{ name: 'Quiz', params: { section_id: section.section_id,
                                                                            learner_id: 1,
                                                                            course_id: 1,
                                                                            trainer_id: 1,
                                                                            }}">
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
import axios from "axios";
export default {
    name: "CourseDetail",
    props: {
        course_id: parseInt({ type: Number }), 
        trainer_id: parseInt({ type: Number })
    },
    data: () => ({
        courseDetail: {},
        sections: [],
        sectionsCopy: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        boldSection: false,
        currentUserId: 6,
    }),
    methods: {
        ifUpdated(grade) {
            if ((grade == null) && (this.boldSection == false)) {
                console.log(this.boldSection);
                this.boldSection = true;
                console.log(this.boldSection);
                return true;
            }
            else {
                return false;
            }
            
        },
        getCourseDetail(course_id, trainer_id) {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobytrainerandcourse";
            let dataObj = { "courseId": course_id, "trainerId": trainer_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data[0];

                    // Check if course has pre-requisites
                    if (this.courseDetail.course_requirement > 0) {
                        this.getRequisiteCourses(course_id);
                    }
                })

        },
        getCourseSections(course_id, trainer_id) {
            let updatedApiWithEndpoint = this.apiLink + "/getsectionsbycourseandtrainer";
            let dataObj = { "courseId": course_id, "trainerId": trainer_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.sections = response.data;
                    console.log("Sections", this.sections);
                })
        },
        getRequisiteCourses(course_id) {
            let updatedApiWithEndpoint = this.apiLink + "/getcourserequisites";
            let dataObj = { "courseId": course_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.requisiteCourses = response.data;
                })
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
        // TO DO: Section Requisite Logic Checker
        sectionRequisiteChecker() {

        },
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
        // Calls method to get course details
        this.getCourseDetail(this.course_id, this.trainer_id);

        // Calls method to get section details
        // this.getCourseSections();
        var dataObj = {
                        'learnerId' : this.currentUserId,
                        'trainerId' : this.trainer_id,
                        'courseId'  : this.course_id
                        };

        const axios = require('axios');
        var updatedApiWithEndpoint = this.apiLink + "/getallsectionsbycourseidtraineriduserid";
        axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                console.log(response.data);
                this.sections = response.data;
            })

        // Calls method to get course requisite details
        this.getRequisiteCourses(this.course_id)
    }
}
</script>