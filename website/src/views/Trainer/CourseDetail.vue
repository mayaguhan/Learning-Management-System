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
            <v-btn icon @click="toggleEdit=!toggleEdit, editAction('edit')" 
            v-show="toggleEdit == false && formatDate(currentDate) < formatDate(courseDetail.start_date)">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>
        </h2>

        <v-form v-model="isSaveValid">
        <!-- Add New Section Dialog -->
        <v-dialog v-model="dialog" persistent max-width="600px">
            <template v-slot:activator="{ on, attrs }">
                <v-btn color="primary mr-3 mb-3" dark v-bind="attrs" v-on="on" v-show="toggleEdit == true">
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
                            <v-text-field v-model="newQuizDuration" type="number" 
                            :rules="[rules.required, rules.durationMin, rules.durationMax]"
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
        <v-btn class="primary mr-3 mb-3" @click="toggleEdit=!toggleEdit, saveEdit()" 
        v-show="toggleEdit == true" :disabled="!isSaveValid">
            Save
        </v-btn>
        <!-- Cancel Section Edits -->
        <v-btn class="light mb-3"  @click="toggleEdit=!toggleEdit, editAction('cancel')" 
        v-show="toggleEdit == true">
            Cancel
        </v-btn>
        
        <template>
        <v-expansion-panels focusable :items="sections" :key="componentKey">
            <v-expansion-panel v-for="(section, indexS) in sections" :key="section.courseId">
                <v-expansion-panel-header>
                    {{ section.section_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-row v-show="toggleEdit == true">
                        <v-col cols=10>
                            <v-text-field v-model="section.section_name" label="Section Name" 
                            maxlength="50" ></v-text-field>
                        </v-col>
                        <v-col cols=2>
                            <v-text-field v-model="section.sequence" label="Section Sequence" type="number" 
                            :rules="[rules.required, rules.sequenceMin, sequenceChecker(section.sequence)]"></v-text-field>
                        </v-col>
                    </v-row>

                    <!-- Quiz and Slide Decks can only if a section exists (i.e. has section_id).
                    Newly added sections have to be Saved before quiz or materials can be added -->
                    <div v-if=" section.section_id != null">
                        <!-- Quiz Statistics -->
                        <b>Quiz Statistics: </b>
                        <v-progress-linear color="blue" rounded height="10"
                            :value=" section.pass_count / section.learner_count * 100 ">
                        </v-progress-linear>
                        {{ section.pass_count }} / {{ section.learner_count }} Learners have passed this quiz <br>
                        <router-link :to="{ name: 'QuizDetail', params: { section_id: section.section_id, conduct_id: conduct_id } }" 
                        v-show="formatDate(currentDate) < courseDetail.start_date">
                            <v-btn class="primary mr-3">
                                Manage Quiz
                            </v-btn>
                        </router-link><br>
                        <v-divider class="mt-3 mb-3"></v-divider>
                        <!-- Upload slide decks -->
                        <b v-if="section.materials.length > 0">Learning Materials</b>
                        <b v-else>This topic does not have any learning materials</b>
                        <br>
                        <div v-if="section.materials[0].file_name != null">
                            <ul class="mt-3" v-for="material in section.materials" v-bind:key="material.materialId">
                                <li class="mb-3">
                                    {{ material.file_name }}<br>
                                    <div v-if="material.link.includes('youtube')">
                                        <video-embed css="embed-responsive-16by9" :src="material.link"></video-embed>
                                    </div>

                                    <v-btn v-else v-bind:href="s3link(material.link)" target="_blank">
                                        {{ material.file_name }}
                                    </v-btn>

                                    <v-btn icon v-show="toggleEdit == true" @click="deleteMaterial(material.material_id)">
                                        <v-icon>mdi-trash-can</v-icon>
                                    </v-btn>
                                </li>
                            </ul>
                        </div>
                        <div v-else>This topic does not have any learning materials yet</div>

                        <v-file-input v-model="files" counter multiple show-size label="Upload file" v-show="toggleEdit == true"></v-file-input>
                        <v-btn class="primary" v-show="toggleEdit == true" @click="uploadFiles(section.section_id)">
                            Upload File
                        </v-btn>

                        <!-- video material -->
                        <v-dialog v-model="materialDialog" persistent max-width="600px">
                            <template v-slot:activator="{ on, attrs }">
                                <v-btn class="primary ml-5" v-bind="attrs" v-on="on" v-show="toggleEdit == true">
                                Add Video Material
                                </v-btn>
                            </template>
                            <v-card>
                                <v-card-title>
                                <span class="text-h5">Add Video Material</span>
                                </v-card-title>
                                <v-card-text>
                                <v-form v-model="materialFormValid">
                                    <v-text-field v-model="file_name" counter :rules="[rules.required, rules.fileName]" 
                                    label="File Name" maxlength="100"></v-text-field>

                                    <v-text-field v-model="link" counter :rules="[rules.required, rules.fileLink]" 
                                    label="Youtube Link" maxlength="200"></v-text-field>
                                </v-form>
                                </v-card-text>
                                <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="blue darken-1" text @click="materialDialog=false">
                                    Close
                                </v-btn>
                                <v-btn color="blue darken-1" text :disabled="!materialFormValid" @click="materialDialog=false, addVideoMaterial(section.section_id)">
                                    Add
                                </v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-dialog>
                    </div>
                    <div v-else>
                        <b>You have to save your edits before you create a new quiz or upload materials.</b>
                    </div>
                    <v-divider class="mt-3 mb-3" v-show="toggleEdit == true"></v-divider>

                    <v-btn class="error" v-show="toggleEdit == true" @click="deleteSection(section, indexS)">
                        Delete Section
                    </v-btn>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        </template>
        </v-form>
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
        isSaveValid: false,
        selectedSection: 0,

        materialDialog: false,
        materialFormValid: false,

        deleteMaterialId: [],

        rules: {
            required: value => !!value || 'Required.',
            counter: value => value.length <= 50 || 'Max 50 characters',
            durationMin: value => value >= 10 || 'Min duration is 10 minutes',
            durationMax: value => value <= 120 || 'Max duration is 120 minutes',
            sequenceMin: value => value >= 1 || 'Min sequence is 1',
            fileName: value => value.length <= 100 || 'Max Length is 100',
            fileLink: value => value.length <= 100 || 'Max Length is 200',
        },
        componentKey: 0
    }),
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
    methods: {
        forceRerender() {
            this.componentKey += 1;
        },
        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },
        change() {
            this.$refs.youtube.src = "https://www.youtube.com/watch?v=nqwQpXoSN7Q";
        },
        // Get a Single Course Conducted information by conduct_id
        getCourseDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getcourseinfobyconductid";
            let dataObj = { "conductId": this.conduct_id }
            console.log(updatedApiWithEndpoint, dataObj);
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.courseDetail = response.data.data[0];
                    // Enable this to toggle edit
                    // this.courseDetail.start_date = "2021-11-31 12:00";
                })
        },
        // Get all Sections by conduct_id (Trainer)
        getCourseSections() {
            let updatedApiWithEndpoint = this.apiLambda + "/getsectionsbyconductid";
            let dataObj = { "conductId": this.conduct_id }
            console.log(updatedApiWithEndpoint, dataObj);
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
        sequenceChecker(sequence) {
            let sequenceCount = 0;
            this.sections.forEach(section => {
                if (sequence == section.sequence) {
                    sequenceCount++;
                }
            })
            if (sequenceCount > 1) {
                return "Duplicated Sequence";
            } else if (sequence > this.sections.length) {
                return "Max sequence is "+this.sections.length;
            } else {
                return true
            }
        },
        addSectionForm() {
            this.sections.push({
                "conductId": this.conduct_id, 
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
            let sectionLength = this.sectionsCopy.length - this.deleteSectionId.length + 1;
            if (changes.length > 0) {
                let changeCounter = 0;
                changes.forEach(change => {
                    changeCounter++;
                    if (change.section_id == null) {
                        // Add new Section
                        let updatedApiWithEndpoint = this.apiLink + "/addnewsection";
                        let dataObj = { "conduct_id": this.conduct_id, "sequence": sectionLength++, 
                                        "section_name": change.section_name, "quiz_duration": change.quiz_duration, "passing_grade": 0 };               
                        axios.post(updatedApiWithEndpoint, dataObj)
                            .then((response) => {
                                this.getCourseSections();
                                this.forceRerender();
                                console.log(response.data);
                                if (changeCounter == changes.length) {
                                    // Update last sequence in course to be 85
                                    this.updatePassingGrade();
                                }
                        })
                    } else {
                        // Update Section by section_id
                        let updatedApiWithEndpoint = this.apiLink + "/updatesectionbysectionid";
                        let dataObj = { "sectionId": change.section_id, "sectionName": change.section_name, "sequence": change.sequence,
                                        "quizDuration": change.quiz_duration, "passingGrade": change.passing_grade};
                        axios.put(updatedApiWithEndpoint, dataObj)
                            .then((response) => {
                                console.log(response);
                                if (changeCounter == changes.length) {
                                    // Update last sequence in course to be 85
                                    this.updatePassingGrade();
                                }
                            })
                    }
                });
            }
            this.deleteSectionId.forEach(section => {
                if (section.section_id != null) {
                    this.selectedSection = section.section_id;
                    this.expandSection();

                    let materialCount = this.materials.length;
                    if (materialCount > 0) {
                        let materialCounter = 0;
                        this.materials.forEach(material => {
                        // Delete Material by material_id
                        let updatedApiWithEndpoint = this.apiLink + "/deletematerialbyid";
                        let dataObj = { "materialId" : material.material_id };
                        console.log(updatedApiWithEndpoint, dataObj)
                        axios.delete(updatedApiWithEndpoint, { data: dataObj })
                            .then((response) => {
                                console.log(response);
                                materialCounter++;
                                if (materialCounter == materialCount) {
                                    this.deleteSectionChecker(section.section_id);
                                }
                            })
                            .catch((error) => {
                                console.log(error, "Error in deleting material")
                            })    
                        });
                    }

                    // Delete all question related to the section
                    // Get all Quiz Question by section_id
                    let deleteQuestionEndpoint = this.apiLink + "/getallquizquestionbysectionid";
                    let deleteQuestionObj = { "sectionId": section.section_id  }
                    axios.post(deleteQuestionEndpoint, deleteQuestionObj)
                        .then((response) => {
                            let questionCount = response.data.data.length;
                            if (questionCount > 0) {
                                let questionCounter = 0;
                                let sectionQuestions = response.data.data
                                sectionQuestions.forEach(question => {
                                    // Delete Quiz Question by quiz_question_id
                                    let deleteChoiceEndpoint = this.apiLink + "/deletequizquestionbyquestionid";
                                    let deleteChoiceObj = { "questionId" : question.quiz_question_id };
                                    axios.delete(deleteChoiceEndpoint, { data: deleteChoiceObj })
                                        .then((response) => {
                                            console.log(response);
                                            questionCounter++
                                            if (questionCounter == questionCount) {
                                                this.deleteSectionChecker(section.section_id);
                                            }
                                        })
                                        
                                });
                            } else {
                                this.deleteSectionChecker(section.section_id);
                            }
                        })
                }
            });
            this.deleteSectionId = [];

            // Delete Material by material_id
            this.deleteMaterialId.forEach(material_id => {
                if (material_id != null) {
                let updatedApiWithEndpoint = this.apiLink + "/deletematerialbyid";
                let dataObj = { "materialId" : material_id };
                    axios.delete(updatedApiWithEndpoint, { data: dataObj })
                        .then((response) => {
                            console.log(response);
                        })
                    }
                });
            this.deleteMaterialId = [];
        },
        // Delete Section by section_id
        deleteSectionChecker(section_id) {
            let deleteSectionEndpoint = this.apiLink + "/deletesectionbysectionid";
            let deleteSectionObj = { "sectionId" : section_id };
            axios.delete(deleteSectionEndpoint, { data: deleteSectionObj })
                .then((response) => {
                    console.log(response);
                    this.updatePassingGrade();
                })
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
        // Update all course section's passing grade by section_id
        updatePassingGrade() {
            this.forceRerender();
            let updatedApiWithEndpoint = this.apiLink + "/getsectionsbyconductid";
            let dataObj = { "conductId": this.conduct_id }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    let finalSection = response.data.data.reduce((a,b)=>a.sequence>b.sequence?a:b).section_id;
                    let finalSectionEndpoint = this.apiLink + "/updateallcoursesectionspassinggradebysectionid";
                    let finalSectionObj = { "conductId": this.conduct_id, "sectionId" : finalSection };
                    axios.put(finalSectionEndpoint, finalSectionObj)
                        .then((response) => {
                            console.log(response);
                        })
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
            let updatedApiWithEndpoint = this.apiLink + "/addnewcoursematerial";

            // Uploading to S3
            let nameWithExtension = file['name']
            let extensionArray = file['type'].split("/")
            let extension = extensionArray[1]

            let indexOfExtension = nameWithExtension.indexOf(extension);
            let name = nameWithExtension.slice(0, indexOfExtension-1)

            let content = "";
            // var uploadS3Endpoint = this.apiLink + "/uploadfile";
            let uploadS3Endpoint = "https://wsphrnze6b.execute-api.us-east-1.amazonaws.com/beta/uploadfile";

            let reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function () {
                content = reader.result.split(',')[1];
                let dataObj = {"sectionNumber": str.toString(),"fileName": name, 
                            "fileExtension": extension, "content": content };
                console.log("Uploading to S3", uploadS3Endpoint, dataObj);
                axios.post(uploadS3Endpoint, dataObj)
                    .then((response) => {
                        // Saving filepath to DB
                        let dataObj = { "sectionId": str, "fileName": name, "link": response.data }
                        axios.post(updatedApiWithEndpoint, dataObj)
                            .then((response) => {
                                console.log(response.data.data);
                                // this.getCourseSections();
                                // this.forceRerender();
                            })
                    })
            }
        },

        addVideoMaterial(section_id) {
            var updatedApiWithEndpoint = this.apiLink + "/addnewcoursematerial";
            let dataObj = { "sectionId": section_id, "fileName": this.file_name, "link":  this.link }
            console.log(updatedApiWithEndpoint, dataObj);
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response.data.data);
                    // this.getCourseSections();
                    // this.forceRerender();
                })
        },
        
        deleteMaterial(material_id) {
            this.deleteMaterialId.push(material_id);
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