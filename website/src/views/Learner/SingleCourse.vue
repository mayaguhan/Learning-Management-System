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
            <v-expansion-panel v-for="section in sections" :key="section.course_id">
                <v-expansion-panel-header :disabled="section.disabled">
                    <span v-if="section.boldSection==true"><b>{{ section.section_name }}</b></span>
                    <span v-else>{{ section.section_name }}</span>
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <b>Topic's Slide Decks</b><br>
                    <div v-if="section.materials[0].file_name != null">
                        <b>Learning Materials</b>
                        <ul class="mb-3" v-for="material in section.materials" v-bind:key="material.material_id">
                            <li>
                                {{ material.file_name }}<br>
                                <div v-if="material.link.includes('youtube')">
                                    <video-embed css="embed-responsive-16by9" :src="material.link"></video-embed>
                                </div>

                                <v-btn v-else v-bind:href="s3link(material.link)" target="_blank">
                                    {{ material.file_name }}
                                </v-btn>
                                <div v-if="material.vist == null">
                                    <v-btn class="primary" @click="addMaterialVisit(material)" v-show="material.visit == 0">
                                        Mark as Viewed
                                    </v-btn>
                                </div>

                            </li>
                        </ul>
                    </div>
                    <div v-else>This topic does not have any learning materials</div>

                    <v-divider></v-divider>

                    <div v-if="section.best_grade !== null">
                        <b>Best Grade: {{ section.best_grade }} / 100</b>
                    </div>
                    <v-divider></v-divider>
                    <div style="padding-top:5px">
                            <v-btn :disabled="getVisitedCount(section.materials)">
                                <router-link class="text-decoration-none" :to="{ name: 'Quiz', params: { section_id: section.section_id }}">
                                    Attempt Quiz 
                                </router-link>
                            </v-btn>
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
        courseDetail: {},
        sections: [],
        materials: [],
    }),
    methods: {
        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },
        forceRerender() {
            this.componentKey += 1;
        },
        // Get a Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data.data[0];
                })
        },
        // Get all Sections by conduct_id and user_id (Learner)
        getCourseSections() {
            let updatedApiWithEndpoint = this.apiLambda + "/getallsectionsbyconductanduserid";
            let dataObj = { "conductId": this.conduct_id, "learnerId": this.getUserId } 
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    let sectionArr = Object.values(response.data.reduce((sectionResult, { 
                        section_id, section_name, sequence, quiz_duration, passing_grade, best_grade, result, 
                        material_id, file_name, link, visit }) => {
                        // Create section section
                        if (!sectionResult[section_id]) sectionResult[section_id] = {
                            section_id, section_name, sequence, quiz_duration, passing_grade, best_grade, result, materials: []
                        };
                        // Append material to section
                        sectionResult[section_id].materials.push({ material_id, file_name, link, visit });
                        return sectionResult;
                        },{}
                    ));

                    let boldSection = false;
                    sectionArr.forEach(section => {
                        if ((section.best_grade == null && boldSection == false) || ((section.best_grade !== null) && (section.best_grade < section.passing_grade))) {
                            section["boldSection"] = true
                            boldSection = true;
                        } else if (section.best_grade == null && boldSection == true) {
                            section["disabled"] = true
                        }
                    });
                    this.sections = sectionArr;
                })
        },
        // Disables Quiz Attempt if user has not viewed all materials
        getVisitedCount(materials) {
            // If section has no materials Learner can attempt quiz
            if (materials[0].material_id == null) {
                return false
            }
            // No. of links visited = No. of links
            if (materials.reduce((sum, material) => sum + material.visit, 0) == materials.length) {
                return false;
            }
            return true;
        },
        // Add new Visited Material
        addMaterialVisit(material) {
            let updatedApiWithEndpoint = this.apiLink + "/addnewmaterialvisit";
            let dataObj = { "learnerId" : this.getUserId, "conductId" : this.conduct_id, "materialId" : material.material_id };
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response.data.data)
                    this.getCourseSections();
                    this.forceRerender();
                })
        },
        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
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
        getUserId() {
            return this.$store.state.userId;
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