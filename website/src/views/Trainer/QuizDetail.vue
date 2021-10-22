<template>
    <div>
        <h1>
            Manage Quiz: {{ sectionDetail.section_name }}
        </h1>

        <h2>
            Quiz Information
            <!-- Toggle: Edit Section -->
            <v-btn icon @click="toggleEditSection=!toggleEditSection" 
            v-show="toggleEditSection == false">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <!-- Save Section Edit -->
            <v-btn class="primary" @click="toggleEditSection=!toggleEditSection, saveSectionEdit()" 
            v-show="toggleEditSection == true" >
                Save
            </v-btn>

            <!-- Cancel Section Edit -->
            <v-btn class="light"  @click="toggleEditSection=!toggleEditSection" 
            v-show="toggleEditSection == true">
                Cancel
            </v-btn>
        </h2>
        <p>
            Quiz Duration: 
            <span v-show="toggleEditSection == false">{{ sectionDetail.quiz_duration }} minutes <br></span>
            
            <v-text-field v-model="sectionDetail.quiz_duration" :rules="[rules.required, rules.durationMin, rules.durationMax]"
            v-show="toggleEditSection == true" type="number" label="Quiz Duration"  maxlength="4" ></v-text-field>
            
            Pass Criteria: 
            <span v-show="toggleEditSection == false">{{ sectionDetail.passing_grade }}% to pass <br></span>
            <v-text-field v-model="sectionDetail.passing_grade" :rules="[rules.required, rules.gradeMin, rules.gradeMax]"
            v-show="toggleEditSection == true" type="number" label="Passing Grade %"  maxlength="3" ></v-text-field>
        </p>

        <h2>
            Quiz Questions
            <!-- Toggle: Edit Questions -->
            <v-btn icon @click="toggleEditQuestion=!toggleEditQuestion, editAction('edit')" 
            v-show="toggleEditQuestion == false">
                <v-icon>mdi-pencil</v-icon>
            </v-btn>

            <!-- Save Question Edits -->
            <v-btn class="primary" @click="toggleEditQuestion=!toggleEditQuestion, saveEditQuestion()" 
            v-show="toggleEditQuestion == true" :disabled="toggleEditChoice">
                Save
            </v-btn>

            <!-- Cancel Question Edits -->
            <v-btn class="light"  @click="toggleEditQuestion=!toggleEditQuestion, editAction('cancel')" 
            v-show="toggleEditQuestion == true" :disabled="toggleEditChoice">
                Cancel
            </v-btn>

            <v-btn class="primary" v-show="toggleEditQuestion == true" 
            @click="addQuestion()">
                Add Question
            </v-btn>
        </h2>

        <v-expansion-panels focusable :items="questions">
            <v-expansion-panel v-for="(question, indexQ) in questions" :key="question.quiz_question_id" :disabled="toggleEditChoice">
                <v-expansion-panel-header>
                    {{ question.question_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-text-field v-model="question.question_name" :rules="[rules.required, rules.counter]"
                    v-show="toggleEditQuestion == true" label="Question Name"  maxlength="100" ></v-text-field>

                    <ol type="A" v-if="editChoices[indexQ].length != 0">
                        <li v-for="(questionChoice, indexO) in editChoices[indexQ]" v-bind:key="questionChoice.quiz_choice_id"
                        :style="choiceColour(questionChoice.correct)" >
                            <v-row>
                                <v-col cols="7">
                                    <span v-show="toggleEditChoice == false">{{ questionChoice.choice }}</span>
                                    <v-text-field v-model="questionChoice.choice" :rules="[rules.required, rules.counter]"
                                    v-show="toggleEditChoice == true" label="Question Choice" maxlength="100" ></v-text-field>
                                </v-col>
                                <v-col cols="2">
                                    <p>{{ questionChoice.answer_count / quizStats.total_attempt * 100 }}% Chose this answer</p>
                                </v-col>
                                <v-col cols="2">
                                    <v-switch v-model="questionChoice.correct" v-show="toggleEditChoice == true" label="Correct"></v-switch>
                                </v-col>
                                <v-col cols="1">
                                    <v-btn class="primary" v-show="toggleEditChoice" @click="deleteChoice(questionChoice.quiz_choice_id, indexQ, indexO)">
                                        Delete
                                    </v-btn>
                                </v-col>
                            </v-row>
                            
                        </li>
                    </ol>
                    <b v-else>This question has no answer choices yet.</b>

                    <div v-show="toggleEditQuestion == true">
                        <v-divider></v-divider>
                        <!-- Delete Question Button -->
                        <v-btn class="primary"  @click="deleteQuestion(question.quiz_question_id, indexQ)" :disabled="toggleEditChoice">
                            Delete Question
                        </v-btn>
                        
                        <!-- Toggle: Edit Question Choices -->
                        <v-btn class="primary" @click="toggleEditChoice=!toggleEditChoice, editChoice('edit') " v-show="toggleEditChoice == false">
                            Edit Choices
                        </v-btn>

                        <v-btn class="primary" v-show="toggleEditChoice == true" @click="addChoice(question.quiz_question_id, indexQ)">
                            Add Question Choice
                        </v-btn>

                        <!-- Save Question Choice Edits -->
                        <v-btn class="primary" @click="toggleEditChoice=!toggleEditChoice, saveEditChoice(indexQ)" v-show="toggleEditChoice == true">
                            Save
                        </v-btn>

                        <!-- Cancel Question Choice Edits -->
                        <v-btn class="light"  @click="toggleEditChoice=!toggleEditChoice, editChoice('cancel')" v-show="toggleEditChoice == true">
                            Cancel
                        </v-btn>
                    </div>
                    
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>


        <h2>Quiz Statistics</h2>
        <v-expansion-panels multiple>
            <v-expansion-panel>
                <v-expansion-panel-header>
                    Quiz Performance
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    
                    {{ studentAttempts.length }}/{{ sectionDetail.enrollment_count }} Student<span v-if="studentAttempts.length > 0">s</span> passed this quiz.<br><br>
                    <v-card>
                    <v-card-title>
                    <v-text-field v-model="searchStudentAttempts" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                    </v-card-title>
                    <v-data-table :headers="headersStudentAttempts" :items="studentAttempts" :search="searchStudentAttempts">
                    <template v-slot:item="row">
                        <tr>
                            <td>
                                {{ row.item.name }} <br>
                                {{ row.item.username }}
                            </td>
                            <td>
                                {{ row.item.seniority_level }}
                            </td>
                            <td>
                                {{ row.item.email }} <br>
                                {{ row.item.contact }}
                            </td>
                            <td>
                                {{ row.item.pass_attempt }}
                            </td>
                            <td>
                                {{ row.item.quiz_attempt }}
                            </td>
                            <td>
                                {{ row.item.best_grade }}
                            </td>
                        </tr>
                    </template>
                    </v-data-table>
                    </v-card>
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header>
                    Quiz Attempts
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    Total Quiz Attempts: {{ quizStats.total_attempt }} <br>
                    {{ quizStats.pass_rate * 100 }}% pass rate per quiz attempt<br><br>

                    <v-card>
                    <v-card-title>
                    <v-text-field v-model="searchQuizAttempts" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                    </v-card-title>
                    <v-data-table :headers="headersQuizAttempts" :items="quizAttempts" :search="searchQuizAttempts">
                    <template v-slot:item="row">
                        <tr>
                            <td>
                                {{ row.item.name }} <br>
                                {{ row.item.username }}
                            </td>
                            <td>
                                {{ row.item.seniority_level }}
                            </td>
                            <td>
                                {{ row.item.email }} <br>
                                {{ row.item.contact }}
                            </td>
                            <td>
                                {{ row.item.grade }}
                            </td>
                            <td>
                                {{ row.item.result }}
                            </td>
                            <td>
                                {{ formatDate(row.item.attempt_date) }}
                            </td>
                            <td>
                                <!-- TO DO: Get Learner's Quiz Performance by quiz_attempt_id and section_id -->
                                <v-btn depressed small color="#0062E4">
                                    <span style="color: white">View Submission</span> 
                                </v-btn>
                            </td>
                        </tr>
                    </template>
                    </v-data-table>
                    </v-card>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </div>
</template>

<script>
import axios from 'axios';
import moment from "moment";

export default {
    name: "QuizDetail",
    props: {
        section_id: parseInt({ type: Number })
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        },
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user
        toggleEditSection: false,
        sectionDetail: {},
        
        toggleEditQuestion: false,
        questions: [],
        questionsCopy: [],
        deleteQuestionId: [],
        
        toggleEditChoice: false,
        choices: [],
        choicesCopy: [],
        deleteChoiceId: [],
        editChoices: [],

        studentAttempts: [],
        quizStats: {},
        quizAttempts: [],
        questionPerformance: [],

        searchStudentAttempts: '',
        headersStudentAttempts: [
            { text: 'Student Name', value: 'name', align: 'start', sortable: true},
            { text: 'Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: 'Pass Attempts', value: 'pass_attempt', filterable: false, sortable: true},
            { text: 'Quiz Attempts', value: 'quiz_attempt', filterable: false, sortable: true}, 
            { text: 'Best Grade', value: 'best_grade', filterable: false, sortable: true}, 
        ],

        searchQuizAttempts: '',
        headersQuizAttempts: [
            { text: 'Student Name', value: 'name', align: 'start', sortable: true},
            { text: 'Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: 'Grade', value: 'grade', filterable: false, sortable: true},
            { text: 'Result', value: 'result', filterable: false, sortable: true}, 
            { text: 'Attempt Date', value: 'attempt_date', filterable: false, sortable: true}, 
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],

        rules: {
            required: value => !!value || 'Required.',
            counter: value => value.length <= 100 || 'Max 100 characters',
            durationMin: value => value >= 10 || 'Min duration is 10 minutes',
            durationMax: value => value <= 120 || 'Max duration is 120 minutes',
            gradeMin: value => value >= 50 || 'Min passing grade is 50%',
            gradeMax: value => value <= 100 || 'Max passing grade is 100%',
        },
    }),
    methods: {
        // Get Section information by section_id
        getSectionDetail() {
            // let updatedApiWithEndpoint = this.apiLink + "/TBC";
            // let dataObj = { "sectionId": this.section_id }
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         this.sectionDetail = response.data[0];
            //     })

        },

        // Get Quiz's Question Performance by section_id
        getQuestionChoices() {
            let updatedApiWithEndpoint = this.apiLink + "/getquizquestionperformancebysection";
            let dataObj = { "sectionId": this.section_id  }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    // Groups question choices into question groups by question_id
                    let questionArr = Object.values(response.data.reduce((result, 
                    { quiz_question_id, question_name, type, quiz_choice_id, choice, correct, answer_count }) => {
                        // Create new question group
                        if (!result[quiz_question_id]) result[quiz_question_id] = {
                            quiz_question_id, question_name,  type, question_choices: []
                        };
                        // Append question choice to question group
                        result[quiz_question_id].question_choices.push({ quiz_choice_id,  choice, correct, answer_count });
                        return result;
                        },{}
                    ));
                    questionArr.forEach(question => {
                        this.editChoices.push(question.question_choices)
                    });
                    this.questions = questionArr;
                })
        },
        choiceColour: function (correct) {
            const color = correct == 0 ? 'red' : 'green';
            return { color };
        },


        // --- Section ---
        saveSectionEdit() {
            // TO DO: Save Section Edits
            console.log("Save");
            console.log("New Section Duration:", parseInt(this.sectionDetail.quiz_duration));
            console.log("New Section Passing", parseInt(this.sectionDetail.passing_grade));
        },


        // --- Question ---
        // Add new Quiz Question
        addQuestion() {
            this.questions.push({ "question_name": "New Question", "type": "MCQ", "question_choices": [] });
            this.editChoices.push([]);
        },
        deleteQuestion(quiz_question_id, indexQ) {
            this.questions.splice(indexQ, 1);
            this.deleteQuestionId.push(quiz_question_id);
        },
        editAction(action) {
            if (action == "edit") {  
                // Creates a copy of questions and stores it in sectionsCopy
                this.questionsCopy = JSON.parse(JSON.stringify(this.questions));
            } else if (action == "cancel") {
                // Reverts changes made to questions by using the data from sectionsCopy
                this.questions = JSON.parse(JSON.stringify(this.questionsCopy));
            }
        },
        saveEditQuestion() {
            // Save edit question changes
            let changes = this.questions.filter(this.questionComparer(this.questionsCopy)); // Questions to update
            // console.log("Edited:", this.questions);
            // console.log("Original:", this.questionsCopy);
            // console.log("Changes:", changes);

            changes.forEach(change => {
                if (change.quiz_question_id == null) {
                    // Add new Quiz Question
                    let updatedApiWithEndpoint = this.apiLink + "/addnewquizquestion";
                    let dataObj = { "sectionId": this.section_id, "questionName": change.question_name, "type": change.type };
                    axios.post(updatedApiWithEndpoint, dataObj)
                        .then((response) => {
                            console.log("New quiz_question_id: ", response.data[0].insertId);
                    })
                } else {
                    console.log("UPDATE: ", change);
                    // TO DO: UPDATE lms_quiz_question ... SET ... WHERE quiz_question_id = quiz_question_id
                    // Update Quiz Question by quiz_question_id

                }
            });
            this.deleteQuestionId.forEach(quiz_question_id => {
                if (quiz_question_id != null) {
                    console.log("DELETE: ", quiz_question_id);
                    // TO DO: DELETE FROM lms_quiz_question database WHERE quiz_question_id = quiz_question_id
                    // Delete Quiz Question by quiz_question_id

                }
            });
            this.deleteQuestionId = [];
        },
        questionComparer(otherArray){
            return function(current){
                return otherArray.filter(function(other){
                    return (
                        other.quiz_question_id == current.quiz_question_id &&
                        other.question_name == current.question_name &&
                        other.type == current.type
                    )
                }).length == 0;
            }
        },


        // --- Question Choice -- 
        addChoice(quiz_question_id, indexQ) {
            this.editChoices[indexQ].push({ "quiz_question_id": quiz_question_id, "choice": "New Choice", "correct": 0, "answer_count": 0 });
        },
        deleteChoice(quiz_choice_id, indexQ, indexO) {
            console.log(quiz_choice_id, indexQ, indexO);
            this.editChoices[indexQ].splice(indexO, 1);
            this.deleteChoiceId.push(quiz_choice_id);
        }, 
        editChoice(action) {
            if (action == "edit") {  
                // Creates a copy of choices and stores it in choicesCopy
                this.choicesCopy = JSON.parse(JSON.stringify(this.editChoices));
            } else if (action == "cancel") {
                // Reverts changes made to questions by using the data from sectionsCopy
                this.editChoices = JSON.parse(JSON.stringify(this.choicesCopy));
            }
        },
        saveEditChoice(indexQ) {
            // Save Edit Choice Changes
            let changes = this.editChoices[indexQ].filter(this.choiceComparer(this.choicesCopy[indexQ]));
            // console.log("Edited:", this.editChoices[indexQ]);
            // console.log("Original:", this.choicesCopy[indexQ]);
            // console.log("Changes:", changes);

            changes.forEach(change => {
                if (change.quiz_choice_id == null) {
                    // Add new Quiz Choice
                    let updatedApiWithEndpoint = this.apiLink + "/addnewquizoption";
                    let dataObj = { "quizQuestionId": change.quiz_question_id, "choice": change.choice, "correct": change.correct };
                    axios.post(updatedApiWithEndpoint, dataObj)
                        .then((response) => {
                            console.log("New quiz_option_id: ", response.data[0].insertId);
                        })
                } else {
                    console.log("UPDATE: ", change);
                    // TO DO: UPDATE lms_quiz_choice ... SET ... WHERE quiz_choice_id = quiz_choice_id
                    // Update Quiz Choice by quiz_choice_id


                }
            });
            this.deleteChoiceId.forEach(quiz_choice_id => {
                if (quiz_choice_id != null) {
                    console.log("DELETE: ", quiz_choice_id);
                    // TO DO: DELETE FROM lms_quiz_choice database WHERE quiz_question_id = quiz_choice_id
                    // Delete Quiz Choice by quiz_choice_id


                }
            });
            this.deleteQuestionId = [];
            console.log(this.questions);
        },
        choiceComparer(otherArray){
            return function(current){
                return otherArray.filter(function(other){
                    return (
                        other.quiz_choice_id == current.quiz_choice_id &&
                        other.choice == current.choice &&
                        other.correct == current.correct
                    )
                }).length == 0;
            }
        },


        // --- Quiz Statistics ---
        // Get Quiz Attempt of each student who had taken the quiz by section_id
        getStudentAttempt() {
            let updatedApiWithEndpoint = this.apiLink + "/quizattemptofstudentbysection";
            let dataObj = { "sectionId": this.section_id  }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.studentAttempts = response.data;
                })
        },
        // Get Quiz Attempt passing rate and attempt count by section_id
        getQuizStats() {
            let updatedApiWithEndpoint = this.apiLink + "/getquizpassingrateandattemptcountbysection";
            let dataObj = { "sectionId": this.section_id  }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.quizStats = response.data[0];
                })
        },
        // Get all Quiz Attempt by section_id
        getQuizAttempts() {
            let updatedApiWithEndpoint = this.apiLink + "/getallquizattemptbysection";
            let dataObj = { "sectionId": this.section_id  }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.quizAttempts = response.data;
                })
        },
        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD HH:mm');
        },
    },
    created() {
        // Calls method to get section details
        this.getSectionDetail();

        // Calls method to get question choices
        this.getQuestionChoices();

        // Calls method to get quiz attempt of each student who had taken the quiz
        this.getStudentAttempt();

        // Calls method to get quiz statistics
        this.getQuizStats();

        // Calls method to get all quiz attempts
        this.getQuizAttempts();
    }
}
</script>

<style>

</style>