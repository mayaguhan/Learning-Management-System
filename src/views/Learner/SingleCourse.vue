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

                    

                    

                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        </template>

    </div>
</template>

<script>
export default {
    name: "CourseDetail",
    props: {
        course_id: parseInt({ type: Number }), 
        learner_id: parseInt({ type: Number })
    },
    data: () => ({
        courseDetail: {},
        sections: [],
        sectionsCopy: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        boldSection: false,
    }),
    methods: {
        ifUpdated(grade) {
            if ((grade == null) && this.boldSection == false) {
                console.log("hello david");
                this.boldSection = true;
                return true;
            }
        },
        getCourseDetail() {
            this.courseDetail = {
                "course_id": this.course_id,
                "course_code": "PQ101",
                "title": "Print Quality Control I",
                "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a printing press and auxiliary equipment to produce quality printed products on papers and other materials as well as trouble shooting and maintenance of printing machines",
                "capacity": 20,
                "current": 2,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31",
                "trainer_id": 1
            };
        },
        getCourseSections() {
            // Get all Sections by course_id, trainer_id and user_id
            // Dummy JSON, to be replaced with API call
            let courseSectionData = [{
                "section_id": 1,
                "section_name": "PQ101 - Section 1",
                "quiz_duration": 600,
                "passing_grade": 80,
                "best_grade" : 100
            },
            {
                "section_id": 2,
                "section_name": "PQ101 - Section 2",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "best_grade" : 100
            },
            {
                "section_id": 3,
                "section_name": "PQ101 - Section 3",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "best_grade" : 100
            }];
            this.sections = courseSectionData;
            console.log("Sections", this.sections);
        },
        getRequisiteCourses() {
            // Get a Course's requisite(s)
            // Dummy JSON, to be replaced with API call
            let requisiteCourseData = [{
                "course_requisite_id": 15, 
                "course_code": "EX201",
                "title": "Microsoft Excel: Formulas and Functions",
                "outline": "Learn how to become a formula master who is proficient in reading and writing even the most complex formulas in Excel.",
                "capacity": 20,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31"
            },
            {
                "course_requisite_id": 16, 
                "course_code": "EX202",
                "title": "Microsoft Excel: Visualisation and Cleaning",
                "outline": "You will learn Excel Formulas, Pivot Tables, Vlookup, Hlookup, Excel Charts, Sorting & Filtering data, Conditional formatting and many more tips and tricks in Excel",
                "capacity": 20,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31"
            }];
            this.requisiteCourses = requisiteCourseData;
            // console.log("Requisite Courses: ", this.requisiteCourses);
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
        this.getCourseDetail();

        // Calls method to get section details
        // this.getCourseSections();
        var dataObj = {
                        'learnerId' : '6',
                        'trainerId' : '1',
                        'courseId'  : '1'
                        };

        const axios = require('axios');
        var updatedApiWithEndpoint = this.apiLink + "/getallsectionsbycourseidtraineriduserid";
        axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                console.log(response.data);
                this.sections = response.data;
            })

        // Calls method to get course requisite details
        this.getRequisiteCourses()
    }
}
</script>