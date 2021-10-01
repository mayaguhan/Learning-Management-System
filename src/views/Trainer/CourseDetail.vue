<template>
    <div>
        <h1>
            {{ courseDetail.course_code }} - {{ courseDetail.title }}
        </h1>
        <p>
            Start Date: {{ courseDetail.start_date }} <br>
            End Date: {{ courseDetail.end_date }} <br>
            Enrolled Students: {{ courseDetail.current }} / {{ courseDetail.capacity }} <br>
            <router-link :to="{ name: 'EnrolledStudent', params: { course_id: course_id } }">
                <v-btn class="primary">
                    View Enrolled Students
                </v-btn>
            </router-link>
        </p>

        <h2>Course Description</h2>
        <p>
            {{ courseDetail.outline }}
        </p>

        <h2>Course Requisites</h2>
        <p>
            <ul v-if="requisiteCourses.length > 0">
                <li v-for="requisite in requisiteCourses" v-bind:key="requisite.course_requisite_id">
                    {{ requisite.course_code }} - {{ requisite.title }} 
                </li>
            </ul>
            <b v-else>This course has no pre-requisites.</b>
        </p>

        <h2>Course Content
            <!-- Toggle: Edit sections -->
            <v-btn icon @click="toggleEdit=!toggleEdit, editAction('edit')" v-show="toggleEdit == false">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <!-- Add New Section Dialog -->
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn color="primary" dark v-bind="attrs" v-on="on" v-show="toggleEdit == true">
                        Add Section Dialog
                    </v-btn>
                </template>
                <v-card>
                    <v-card-title>
                        <span class="text-h5">Add New Section</span>
                    </v-card-title>
                    <v-card-text>
                    <v-form v-model="isFormValid">
                        <v-row>
                            <v-col>
                                <v-text-field v-model="newSectionName" counter :rules="[rules.required, rules.counter]"
                                label="Section Name" maxlength="50" ></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-text-field v-model="newQuizDuration" type="number" :rules="[rules.required, rules.durationMin, rules.durationMax]"
                                label="Quiz Duration" hint="Duration of the quiz" suffix="minutes"></v-text-field>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-text-field v-model="newQuizPassingGrade" type="number" :rules="[rules.required, rules.gradeMin, rules.gradeMax]"
                                label="Passing Grade" hint="Grade % learner needs to get to clear this section" suffix="%"></v-text-field>
                            </v-col>
                        </v-row>
                    </v-form>
                    </v-card-text>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1"  text  @click="dialog = false">
                        Close
                    </v-btn>
                    <v-btn color="blue darken-1" text :disabled="!isFormValid" @click="dialog = false, addSection(sections)">
                        Add
                    </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <!-- TO DO: Change Sequence of Sections -->
            <v-btn class="primary" v-show="toggleEdit == true">
                Section Sequence
            </v-btn>

            <!-- Save Section Edits -->
            <v-btn class="primary" @click="toggleEdit=!toggleEdit, saveEdit()" v-show="toggleEdit == true">
                Save
            </v-btn>

            <!-- Cancel Section Edits -->
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
                    <v-text-field v-model="section.section_name" v-show="toggleEdit == true" 
                    label="Section Name"  maxlength="50" ></v-text-field>

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
                        </router-link><br>

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

                    <v-btn class="primary" v-show="toggleEdit == true" @click="deleteSection(section, indexS)">
                        Delete Section
                    </v-btn>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        </template>

    </div>
</template>

<script>
// import axios from 'axios';

export default {
    name: "CourseDetail",
    props: {
        course_id: parseInt({ type: Number })
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        courseDetail: {},
        sections: [],
        sectionsCopy: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        newSectionName: "",
        newQuizDuration: 10,
        newQuizPassingGrade: 50,
        toggleEdit: false,
        deleteSectionId: [],
        dialog: false,
        isFormValid: false,
        rules: {
            required: value => !!value || 'Required.',
            counter: value => value.length <= 50 || 'Max 50 characters',
            durationMin: value => value >= 10 || 'Min duration is 10 minutes',
            durationMax: value => value <= 120 || 'Max duration is 120 minutes',
            gradeMin: value => value >= 50 || 'Min passing grade is 50%',
            gradeMax: value => value <= 100 || 'Max passing grade is 100%',
        },
    }),
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    methods: {
        // Get a Course information by course_id and trainer_id
        getCourseDetail(course_id) {
            // let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "courseId": course_id }
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.courseDetail = response.data;
            //     })
            console.log(dataObj)
            this.courseDetail = {
                "course_id": this.course_id,
                "course_code": "PQ101",
                "title": "Print Quality Control I",
                "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a printing press and auxiliary equipment to produce quality printed products on papers and other materials as well as trouble shooting and maintenance of printing machines",
                "capacity": 20,
                "current": 2,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31",
                "course_requirement": 2,
                "enrollment_count": 2
            };
            if (this.courseDetail.course_requirement > 0) {
                console.log("This course has Requisites");
                this.getRequisiteCourses(this.course_id);
            }
        },
        // Get all Sections by course_id, trainer_id and user_id (Trainer)
        getCourseSections() {
            // Dummy JSON, to be replaced with API call
            let courseSectionData = [{
                "section_id": 1,
                "section_name": "Managing Printers",
                "quiz_duration": 600,
                "passing_grade": 80,
                "pass_count": 2,
                "section_sequence": 1
            },
            {
                "section_id": 2,
                "section_name": "Managing Ink Catridges",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "pass_count": 1,
                "section_sequence": 2
            },
            {
                "section_id": 3,
                "section_name": "Ensuring Printing Accuracy",
                "quiz_duration": 1800,
                "passing_grade": 80,
                "pass_count": 0,
                "section_sequence": 3
            }];
            this.sections = courseSectionData;
            console.log("Sections", this.sections);
        },
        // Get a Course's requisite(s)
        getRequisiteCourses(course_id) {
            // let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "courseId": course_id }
            // axios.post(updatedApiWithEndpoint, dataObj)
            // .then((response) => {
            //     console.log(response);
            //     this.requisiteCourses = response.data;
            // })
            console.log(dataObj);

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
        },
        addSection() {
            // Add new Section
            // Dummy JSON input, to be replaced with API call
            this.sections.push({
                "section_name": this.newSectionName,
                "quiz_duration": this.newQuizDuration * 60,
                "passing_grade": this.newQuizPassingGrade
            });
        },
        deleteSection(section_id, indexS) {
            this.sections.splice(indexS, 1);
            this.deleteSectionId.push(section_id);
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
            let changes = this.sections.filter(this.comparer(this.sectionsCopy));
            console.log("Edited: ", this.sections);
            console.log("Original: ", this.sectionsCopy);
            console.log("Changes: ", changes);

            changes.forEach(change => {
                if (change.section_id == null) {
                    console.log("INSERT: ", change);
                    // Adds a new section (4 parameters)

                } else {
                    console.log("UPDATE: ", change);
                    // TO DO: UPDATE lms_section ... SET ... WHERE lms_section_id = section_id

                }
            });

            this.deleteSectionId.forEach(section => {
                if (section.section_id != null) {
                    console.log("DELETE: ", section);
                    // TO DO: DELETE FROM lms_section database WHERE section_id = section.section_id

                }
            });
            this.deleteSectionId = [];
        },
        comparer(otherArray){
            return function(current){
                return otherArray.filter(function(other){
                    return (
                        other.section_id == current.section_id &&
                        other.section_name == current.section_name &&
                        other.quiz_duration == current.quiz_duration && 
                        other.passing_grade == current.passing_grade && 
                        other.pass_count == current.pass_count
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
    },
    created() {
        // Calls method to get course details
        this.getCourseDetail(this.course_id);

        // Calls method to get section details
        this.getCourseSections();

        // Calls method to get course requisite details
        this.getRequisiteCourses();
    }
}
</script>