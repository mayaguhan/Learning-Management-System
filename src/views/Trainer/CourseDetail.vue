<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ courseDetail.start_date }} <br>
            End Date: {{ courseDetail.end_date }} <br>
            Enrolled Students: {{ courseDetail.current }} / {{ courseDetail.capacity }} <br>
            <router-link :to="{ name: 'EnrolledStudent', params: { course_id: course_id, trainer_id: trainer_id } }">
                <v-btn depressed small color="#0062E4">
                    <span style="color: white">View Enrolled Students</span> 
                </v-btn>
            </router-link>
        </p>

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Content
            <!-- Toggle: Edit sections -->
            <v-btn icon @click="toggleEdit=!toggleEdit" v-show="toggleEdit == false">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn class="primary" @click="addSection(sections)" v-show="toggleEdit == true">
                Add Section
            </v-btn>
            <v-btn class="primary" @click="toggleEdit=!toggleEdit, editSection(sections)" v-show="toggleEdit == true">
                Save
            </v-btn>
            <v-btn class="light"  @click="toggleEdit=!toggleEdit" v-show="toggleEdit == true">
                Cancel
            </v-btn>
        </h2>

        <template>
        <v-expansion-panels focusable :items="sections">
            <v-expansion-panel v-for="section in sections" :key="section.course_id" @click="expandSection(section.section_id)">
                <v-expansion-panel-header>
                    {{ section.section_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <div>
                        <b>Quiz Statistics: </b> 
                        {{ section.pass_count }} / {{ courseDetail.current }} Learners have passed this quiz <br>
                        <router-link :to="{ name: 'QuizDetail', params: { section_id: section.section_id } }">
                            <v-btn depressed small color="#0062E4">
                                <span style="color: white">Manage Quiz</span> 
                            </v-btn>
                        </router-link>
                    </div>
                    <v-divider></v-divider>
                    <!-- Checks a section has pre-requisite whether -->
                    <div v-if=" section.requisite_section_name != null">
                        <b>Pre-requisite Section: </b> {{ section.requisite_section_name }}
                        <v-btn icon v-show="toggleEdit == true">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </div>
                    <div v-else>
                        <b>This section has no pre-requisites</b>
                        <v-btn icon v-show="toggleEdit == true">
                            <v-icon>mdi-pencil</v-icon>
                        </v-btn>
                    </div>
                    <!-- TO DO: Method to update section's pre-requisite -->
                    <v-divider></v-divider>

                    <!-- Upload slide decks -->
                    <b>Topic's Slide Decks</b><br>
                    <ul v-for="(material, index) in materials" v-bind:key="material.material_id">
                        <li v-if="materials.length > 0" >
                            <v-btn v-bind:href="material.link" target="_blank">
                                <v-icon>mdi-pencil</v-icon> {{ material.material_name }}
                            </v-btn>
                            <v-btn icon v-show="toggleEdit == true" @click="deleteMaterial(material, index)">
                                <v-icon>mdi-trash-can</v-icon>
                            </v-btn>
                        </li>
                        <li v-else>
                            <b>This section has no materials</b>
                        </li>
                    </ul>


                    <v-file-input chips multiple label="Upload Material(s)" v-show="toggleEdit == true"></v-file-input>
                    <!-- TO DO: Method to upload new materials -->
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
        trainer_id: parseInt({ type: Number })
    },
    data: () => ({
        courseDetail: {},
        sections: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        toggleEdit: false
    }),
    methods: {
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
                "pass_count": 2,
                "section_requisite_id": null,
                "requisite_section_name": null
            },
            {
                "section_id": 2,
                "section_name": "PQ101 - Section 2",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "pass_count": 1,
                "section_requisite_id": 1,
                "requisite_section_name": "PQ101 - Section 1"
            },
            {
                "section_id": 3,
                "section_name": "PQ101 - Section 3",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "pass_count": 0,
                "section_requisite_id": 2,
                "requisite_section_name": "PQ101 - Section 2"
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
            console.log("Requisite Courses: ", this.requisiteCourses);
        },
        addSection() {
            for (let i=0; i<1; i++) {
                // Add new Section
                // Dummy JSON input, to be replaced with API call
                this.sections.push({
                    "section_id": 2,
                    "section_name": "PQ101 - Section " + (this.sections.length+i+1),
                    "quiz_duration": 600,
                    "passing_grade": 80,
                    "pass_count": 0,
                    "section_requisite_id": (this.sections.length+i+1),
                    "requisite_section_name": "PQ101 - Section " + (this.sections.length+i+1)
                });
            }
        },
        editSection(sections) {
            // Edit section, change section name & section requirement
            console.log("Editing in progress")
            console.log(sections)
            // TO DO: Edit Section
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
        deleteMaterial(material, index) {
            this.materials.splice(index, 1);
            console.log("Deleting: " + material.material_id);
            // Execute Delete query
            // TO DO: Delete material
        }
    },
    created() {
        // Calls method to get course details
        this.getCourseDetail();

        // Calls method to get section details
        this.getCourseSections();

        // Calls method to get course requisite details
        this.getRequisiteCourses()

    }
}
</script>
