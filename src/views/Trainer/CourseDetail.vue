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
                <v-btn class="primary">
                    View Enrolled Students
                </v-btn>
            </router-link>
        </p>

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Content
            <!-- Toggle: Edit sections -->
            <v-btn icon @click="toggleEdit=!toggleEdit, editAction('edit')" v-show="toggleEdit == false">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <v-btn class="primary" @click="addSection(sections)" v-show="toggleEdit == true">
                Add Section
            </v-btn>
            <v-btn class="primary" @click="toggleEdit=!toggleEdit, saveEdit()" v-show="toggleEdit == true">
                Save
            </v-btn>
            <v-btn class="light"  @click="toggleEdit=!toggleEdit, editAction('cancel')" v-show="toggleEdit == true">
                Cancel
            </v-btn>
        </h2>

        <template>
        <v-expansion-panels focusable :items="sections">
            <v-expansion-panel v-for="(section, indexS) in sections" :key="section.course_id" @click="expandSection(section.section_id)">
                <v-expansion-panel-header>
                    {{ section.section_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <!-- Checks a section has pre-requisite -->
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

                    <!-- Quiz and Slide Decks can only if a section exists (i.e. has section_id).
                    Newly added sections have to be Saved before quiz or materials can be added -->
                    <div v-if=" section.section_id != null">
                        <!-- Quiz Statistics -->
                        <b>Quiz Statistics: </b> 
                        {{ section.pass_count }} / {{ courseDetail.current }} Learners have passed this quiz <br>
                        <router-link :to="{ name: 'QuizDetail', params: { section_id: section.section_id } }">
                            <v-btn class="primary">
                                Manage Quiz
                            </v-btn>
                        </router-link>
                        <v-divider></v-divider>

                        <!-- Upload slide decks -->
                        <b>Topic's Slide Decks</b><br>
                        <ul v-for="(material, indexM) in materials" v-bind:key="material.material_id">
                            <li v-if="materials.length > 0" >
                                <v-btn v-bind:href="material.link" target="_blank">
                                    <v-icon>mdi-pencil</v-icon> {{ material.material_name }}
                                </v-btn>
                                <v-btn icon v-show="toggleEdit == true" @click="deleteMaterial(material, indexM)">
                                    <v-icon>mdi-trash-can</v-icon>
                                </v-btn>
                            </li>
                            <li v-else>
                                <b>This section has no materials</b>
                            </li>
                        </ul>
                        <v-file-input chips multiple label="Upload Material(s)" v-show="toggleEdit == true"></v-file-input>
                        <!-- TO DO: Method to upload new materials -->

                    </div>
                    <div v-else>
                        <b>You have to save your edits before you create a new quiz or upload materials.</b>
                    </div>
                    <v-divider></v-divider>

                    <v-btn class="primary" v-show="toggleEdit == true" @click="deleteSection(indexS)">
                        Delete Section
                    </v-btn>
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
        sectionsCopy: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        toggleEdit: false,
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
            // Add new Section
            // Dummy JSON input, to be replaced with API call
            this.sections.push({
                "section_name": "PQ101 - Section " + (this.sections.length+1),
                "quiz_duration": 600,
                "passing_grade": 80,
                "pass_count": 0,
                "section_requisite_id": (this.sections.length+1),
                "requisite_section_name": null
            });
        },
        deleteSection(indexS) {
            this.sections.splice(indexS, 1);
        },
        editAction(action) {
            if (action == "edit") {  
                // Creates a copy of sections and stores it in sectionsCopy
                this.sectionsCopy = JSON.parse(JSON.stringify(this.sections));
            } else if (action == "cancel") {
                // Reverts changes made to sections by using the data from sectionsCopy
                this.sections = JSON.parse(JSON.stringify(this.sectionsCopy));
            }
        },
        saveEdit() {
            // Save edit section changes
            let onlyInA = this.sections.filter(this.comparer(this.sectionsCopy));
            let onlyInB = this.sectionsCopy.filter(this.comparer(this.sections));
            let changes = onlyInA.concat(onlyInB);
            console.log("Edited Section: ", this.sections);
            console.log("Original Section: ", this.sectionsCopy);
            console.log("Changes Made: ", changes);

            // Check all the changes to determine whether to execute INSERT/UPDATE/DELETE
            changes.forEach((change) => {
                // console.log(change);
                if (change.section_id == null) {
                    console.log("INSERT");
                    // INSERT into lms_section database


                } else if (change.action == "update") {
                    console.log("UPDATE", change.section_id);
                    // UPDATE lms_section database

                } else {
                    console.log("DELETE: ", change.section_id);
                    // DELETE FROM lms_section database

                } 
            });
            // Calls getCourseSection to refresh changes made
            // this.getCourseSections();
        },
        comparer(otherArray){
            return function(current){
                return otherArray.filter(function(other){
                    return (
                        other.section_id == current.section_id &&
                        other.section_name == current.section_name &&
                        other.quiz_duration == current.quiz_duration && 
                        other.passing_grade == current.passing_grade && 
                        other.pass_count == current.pass_count && 
                        other.section_requisite_id == current.section_requisite_id && 
                        other.requisite_section_name == current.requisite_section_name
                    )
                }).length == 0;
            }
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
        deleteMaterial(material, indexM) {
            this.materials.splice(indexM, 1);
            console.log("Deleting Material: " + material.material_id);
            // Execute Delete query
            // TO DO: Delete material


        },
        // TO DO: Section Requisite Logic Checker
        sectionRequisiteChecker() {

        },
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