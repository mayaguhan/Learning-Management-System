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
            </router-link>
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

        <h2>Course Content
            <!-- Toggle: Edit sections -->
            <v-btn icon @click="toggleEdit=!toggleEdit, editAction('edit')" v-show="toggleEdit == false && formatDate(currentDate) < courseDetail.start_date">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <!-- Add New Section Dialog -->
            <v-dialog v-model="dialog" persistent max-width="600px">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn color="primary mr-3" dark v-bind="attrs" v-on="on" v-show="toggleEdit == true">
                        Add New Section
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
                    </v-form>
                    </v-card-text>
                    <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1"  text  @click="dialog = false">
                        Close
                    </v-btn>
                    <v-btn color="blue darken-1" text :disabled="!isFormValid" @click="dialog = false, addSectionForm()">
                        Add
                    </v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>

            <!-- Save Section Edits -->
            <v-btn class="primary mr-3" @click="toggleEdit=!toggleEdit, saveEdit()" v-show="toggleEdit == true">
                Save
            </v-btn>

            <!-- Cancel Section Edits -->
            <v-btn class="light mr-3"  @click="toggleEdit=!toggleEdit, editAction('cancel')" v-show="toggleEdit == true">
                Cancel
            </v-btn>
        </h2>

        <template>
        <v-expansion-panels focusable :items="sections" :key="componentKey">
            <v-expansion-panel v-for="(section, indexS) in sections" :key="section.course_id" @click="expandSection(section.section_id)">
                <v-expansion-panel-header>
                    {{ section.section_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-row v-show="toggleEdit == true">
                        <v-col cols=10>
                            <v-text-field v-model="section.section_name" label="Section Name"  maxlength="50" ></v-text-field>
                        </v-col>
                        <v-col cols=2>
                            <v-text-field v-model="section.sequence" label="Section Sequence" type="number" min=1 :max="sections.length"></v-text-field>
                            <span> {{ sequenceChecker(section.sequence) }}</span>
                        </v-col>
                    </v-row>

                    <!-- Quiz and Slide Decks can only if a section exists (i.e. has section_id).
                    Newly added sections have to be Saved before quiz or materials can be added -->
                    <div v-if=" section.section_id != null">
                        <!-- Quiz Statistics -->
                        <b>Quiz Statistics: </b> 
                        {{ section.pass_count }} / {{ section.learner_count }} Learners have passed this quiz <br>
                        <router-link :to="{ name: 'QuizDetail', params: { section_id: section.section_id } }" v-show="formatDate(currentDate) < courseDetail.start_date">
                            <v-btn class="primary mr-3">
                                Manage Quiz
                            </v-btn>
                        </router-link><br>

                        <!-- Upload slide decks -->
                        <b>Topic's Slide Decks</b><br>
                        <ul v-for="(material, indexM) in materials" v-bind:key="material.material_id">
                            <li v-if="materials.length > 0" >
                                <v-btn v-bind:href="s3link(material.link)" target="_blank">
                                    {{ material.file_name }}
                                </v-btn>
                                <v-btn icon v-show="toggleEdit == true" @click="deleteMaterial(material, indexM)">
                                    <v-icon>mdi-trash-can</v-icon>
                                </v-btn>
                            </li>
                            <li v-else>
                                <b>This section has no materials</b>
                            </li>
                        </ul>
                        <v-file-input v-model="files" counter multiple show-size label="Upload file" v-show="toggleEdit == true"></v-file-input>
                        <v-btn class="primary" v-show="toggleEdit == true" @click="uploadFiles(section.section_id)">
                            Upload
                        </v-btn>

                    </div>
                    <div v-else>
                        <b>You have to save your edits before you create a new quiz or upload materials.</b>
                    </div>
                    <v-divider></v-divider>

                    <v-btn class="primary mr-3" v-show="toggleEdit == true" @click="deleteSection(section, indexS)">
                        Delete Section
                    </v-btn>
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
        currentUserId: 2, // To be replaced with user_id of logged in user

        files: {},
        content: "",
        file_name: "",
        file_extension: "",
        link: "",

        courseDetail: {},
        sections: [],
        sectionsCopy: [],
        requisiteCourses: [],
        materials: [],
        newSection: {},
        newSectionName: "",
        newQuizDuration: 10,
        currentDate: new Date(),
        toggleEdit: false,
        deleteSectionId: [],
        dialog: false,
        isFormValid: false,

        rules: {
            required: value => !!value || 'Required.',
            counter: value => value.length <= 50 || 'Max 50 characters',
            durationMin: value => value >= 10 || 'Min duration is 10 minutes',
            durationMax: value => value <= 120 || 'Max duration is 120 minutes'
        },
        componentKey: 0
    }),
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        },
        s3Link(){
            return this.$store.state.s3Link;
        },
    },
    methods: {
        forceRerender() {
            this.componentKey += 1;
        },
        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },

        // Get a Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
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
                    this.sections = response.data;
                })
        },
        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD hh:mm');
        },
        sequenceChecker(sequence) {
            let sequenceCount = 0;
            this.sections.forEach(section => {
                if (sequence == section.sequence) {
                    sequenceCount++;
                }
            })
            if (sequenceCount > 1) {
                return "Duplicated Sequence"
            }
        },
        addSectionForm() {
            this.sections.push({
                "conduct_id": this.conduct_id, 
                "sequence": this.sections.length+1,
                "section_name": this.newSectionName,
                "quiz_duration": this.newQuizDuration,
                "passing_grade": 0
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
            if (changes.length > 0) {
                changes.forEach(change => {
                    if (change.section_id == null) {
                        console.log("INSERT: ", change);
                        // Add new Section
                        let updatedApiWithEndpoint = this.apiLink + "/addnewsection";
                        let dataObj = { "conductId": change.conduct_id, "sequence": this.sections.length+1, 
                                        "sectionName": change.section_name, "quizDuration": change.quiz_duration, "passingGrade": 0 };                  
                        axios.post(updatedApiWithEndpoint, dataObj)
                            .then((response) => {
                                console.log(response);
                        })
                    } else {
                        console.log("UPDATE: ", change);
                        // Update Section by section_id
                        let updatedApiWithEndpoint = this.apiLink + "/TBC";
                        let dataObj = { "sectionId" : change.section_id, "section_name": change.section_name, "sequence": change.sequence,
                                        "quiz_duration": change.quiz_duration, "passing_grade": change.passing_grade};
                        console.log(updatedApiWithEndpoint, dataObj);
                        // axios.post(updatedApiWithEndpoint, dataObj)
                        //     .then((response) => {
                        //         console.log(response);
                        //     })
                    }
                });
                // Update last sequence in course to be 85
                let finalSection = this.sections.reduce((a,b)=>a.sequence>b.sequence?a:b).section_id;
                this.updatePassingGrade(finalSection);
            }
            console.log(this.deleteSectionId);
            this.deleteSectionId.forEach(section => {
                if (section.section_id != null) {
                    console.log("DELETE: ", section);
                    // Delete all question related to the section
                    // Get all Quiz Question by section_id
                    let updatedApiWithEndpoint = this.apiLink + "/getallquizquestionbysectionid";
                    let dataObj = { "sectionId": section.section_id  }
                    axios.post(updatedApiWithEndpoint, dataObj)
                        .then((response) => {
                            // Delete Quiz Question by quiz_question_id
                            let sectionQuestions = response.data
                            sectionQuestions.forEach(question => {
                                let updatedApiWithEndpoint = this.apiLink + "/deletequizquestionbyquestionid";
                                let dataObj = { "questionId" : question.quiz_question_id };
                                axios.delete(updatedApiWithEndpoint, { data: dataObj })
                                    .then((response) => {
                                        console.log(response);
                                    })
                            });
                        })
                    // TO DO: Delete all materials related to the section


                    // Delete Section by section_id
                    // let updatedApiWithEndpoint = this.apiLink + "/TBC";
                    // let dataObj = { "sectionId" : section.section_id };
                    // axios.delete(updatedApiWithEndpoint, { data: dataObj })
                    //     .then((response) => {
                    //         console.log(response);
                    //     })
                }
            });
            this.getCourseSections();
            this.forceRerender();
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
                        other.sequence == current.sequence
                    )
                }).length == 0;
            }
        },
        updatePassingGrade(section_id) {
            // Update Section by section_id
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "conductId": this.conduct_id, "sectionId" : section_id, };
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //     })
        },
        expandSection(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/retrieveallmaterialsinasection";
            let dataObj = { "sectionId": section_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.materials = response.data;
                })
        },

        uploadFiles(section_id){
            for (var file in this.files){
                console
                this.upload(this.files[file], section_id);
            }
        },
        upload(file, str) {
            // Api Link for upload
            var updatedApiWithEndpoint = this.apiLink + "/addnewcoursematerial";
            // Uploading to S3
            var nameWithExtension = file['name']
            var extensionArray = file['type'].split("/")
            var extension = extensionArray[1]

            var indexOfExtension = nameWithExtension.indexOf(extension);
            var name = nameWithExtension.slice(0, indexOfExtension-1)

            var content = "";
            var updatedApiWithEndpointM = this.apiLink + "/uploadfile";

            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                // this.expandSection(section_id);
                content = reader.result.split(',')[1];
                let dataObj = {"sectionNumber": str.toString(),"fileName": name, 
                            "fileExtension": extension, "content": content };
                axios.post(updatedApiWithEndpointM, dataObj)
                    .then((response) => {
                        // Saving filepath to DB
                        let dataObj = { "sectionId": str, "fileName": name, "link":  response.data }
                        axios.post(updatedApiWithEndpoint, dataObj)
                            .then((response) => {
                                console.log(response);
                            })
                    })
            }
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
        this.getCourseDetail(this.conduct_id);

        // Calls method to get section details
        this.getCourseSections();
    }
}
</script>
