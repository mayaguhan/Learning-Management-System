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
            v-show="toggleEditQuestion == true" :disabled="toggleEditOption">
                Save
            </v-btn>

            <!-- Cancel Question Edits -->
            <v-btn class="light"  @click="toggleEditQuestion=!toggleEditQuestion, editAction('cancel')" 
            v-show="toggleEditQuestion == true" :disabled="toggleEditOption">
                Cancel
            </v-btn>

            <v-btn class="primary" v-show="toggleEditQuestion == true" 
            @click="addQuestion()" :disabled="questionCount >= 20">
                Add Question
            </v-btn>
        </h2>
        <b v-if="questionCount >= 20">You can only have up to 20 questions for a quiz</b>

        <v-expansion-panels focusable :items="questions">
            <v-expansion-panel v-for="(question, indexQ) in questions" :key="question.quiz_question_id" :disabled="toggleEditOption">
                <v-expansion-panel-header>
                    {{ question.question_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-text-field v-model="question.question_name" :rules="[rules.required, rules.counter]"
                    v-show="toggleEditQuestion == true" label="Question Name"  maxlength="100" ></v-text-field>

                    <ol type="A" v-if="editOptions[indexQ].length != 0">
                        <li v-for="(questionOption, indexO) in editOptions[indexQ]" v-bind:key="questionOption.quiz_option_id"
                        :style="optionColour(questionOption.correct)" >
                            <v-row>
                                <v-col cols="7">
                                    <span v-show="toggleEditOption == false">{{ questionOption.option }}</span>
                                    <v-text-field v-model="questionOption.option" :rules="[rules.required, rules.counter]"
                                    v-show="toggleEditOption == true" label="Question Option" maxlength="100" ></v-text-field>
                                </v-col>
                                <v-col cols="2">
                                    <p>{{ questionOption.answer_count / quizStats.total_attempt * 100 }}% Chose this answer</p>
                                </v-col>
                                <v-col cols="2">
                                    <v-switch v-model="questionOption.correct" v-show="toggleEditOption == true" label="Correct"></v-switch>
                                </v-col>
                                <v-col cols="1">
                                    <v-btn class="primary" v-show="toggleEditOption" @click="deleteOption(questionOption.quiz_option_id, indexQ, indexO)">
                                        Delete
                                    </v-btn>
                                </v-col>
                            </v-row>
                            
                        </li>
                    </ol>
                    <b v-else>This question has no answer options yet.</b>

                    <div v-show="toggleEditQuestion == true">
                        <v-divider></v-divider>
                        <!-- Delete Question Button -->
                        <v-btn class="primary"  @click="deleteQuestion(question.quiz_question_id, indexQ)" :disabled="toggleEditOption">
                            Delete Question
                        </v-btn>
                        
                        <!-- Toggle: Edit Question Options -->
                        <v-btn class="primary" @click="toggleEditOption=!toggleEditOption, editOption('edit') " v-show="toggleEditOption == false">
                            Edit Options
                        </v-btn>

                        <v-btn class="primary" v-show="toggleEditOption == true" @click="addOption(question.quiz_question_id, indexQ)">
                            Add Question Option
                        </v-btn>

                        <!-- Save Question Option Edits -->
                        <v-btn class="primary" @click="toggleEditOption=!toggleEditOption, saveEditOption(indexQ)" v-show="toggleEditOption == true">
                            Save
                        </v-btn>

                        <!-- Cancel Question Option Edits -->
                        <v-btn class="light"  @click="toggleEditOption=!toggleEditOption, editOption('cancel')" v-show="toggleEditOption == true">
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
                                {{ row.item.attempt_date }}
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
// import axios from 'axios';

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
        questionCount: 0,
        
        toggleEditOption: false,
        options: [],
        optionsCopy: [],
        deleteOptionId: [],
        editOptions: [],

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
        // Get Section information
        getSectionDetail(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.sectionDetail = response.data;
            //     })

            this.sectionDetail = {
                "section_name": "PQ101 - Section 1",
                "quiz_duration": 10, 
                "passing_grade": 80,
                "enrollment_count": 2
            }
            console.log(this.sectionDetail);
        },

        // Get all Quiz Question and Quiz Option by section_id
        getOptions(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.questions = response.data;
            //     })

            let questionOptions = [
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 1, "option": "Option A", "correct": 1, "answer_count": 2 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 2, "option": "Option B", "correct": 0, "answer_count": 1 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 3, "option": "Option C", "correct": 0, "answer_count": 1 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 4, "option": "Option D", "correct": 0, "answer_count": 0 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?", "type": "T/F", 
                "quiz_option_id": 5, "option": "True", "correct": 1, "answer_count": 3 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?", "type": "T/F", 
                "quiz_option_id": 6, "option": "False", "correct": 0, "answer_count": 1 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?", "type": "T/F", 
                "quiz_option_id": 7, "option": "True", "correct": 1, "answer_count": 4 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?", "type": "T/F", 
                "quiz_option_id": 8, "option": "False", "correct": 0, "answer_count": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ",
                "quiz_option_id": 9, "option": "Option A", "correct": 1, "answer_count": 3 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 10, "option": "Option B", "correct": 0, "answer_count": 1 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 11, "option": "Option C", "correct": 0, "answer_count": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 12, "option": "Option D", "correct": 0, "answer_count": 0 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?", "type": "T/F", 
                "quiz_option_id": 13, "option": "True", "correct": 1, "answer_count": 4 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?", "type": "T/F", 
                "quiz_option_id": 14, "option": "True", "correct": 0, "answer_count": 0 }
            ];

            // Groups question options into question groups by question_id
            let questionArr = Object.values(questionOptions.reduce((result, 
            { quiz_question_id, question_name, type, quiz_option_id, option, correct, answer_count }) => {
                // Create new question group
                if (!result[quiz_question_id]) result[quiz_question_id] = {
                    quiz_question_id, question_name,  type, question_options: []
                };
                // Append question option to question group
                result[quiz_question_id].question_options.push({ quiz_option_id,  option, correct, answer_count });
                return result;
                },{}
            ));
            questionArr.forEach(question => {
                this.editOptions.push(question.question_options)
            });
            console.log(this.editOptions);
            this.questions = questionArr;
            this.questionCount = this.questions.length;
            console.log(this.questions);
        },
        optionColour: function (correct) {
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
        addQuestion() {
            this.questions.push({ "question_name": "New Question", "type": "MCQ", "question_options": [] });
            this.editOptions.push([]);
            this.questionCount = this.questions.length;
        },
        deleteQuestion(quiz_question_id, indexQ) {
            this.questions.splice(indexQ, 1);
            this.deleteQuestionId.push(quiz_question_id);
            this.questionCount = this.questions.length;
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
            console.log("Edited:", this.questions);
            console.log("Original:", this.questionsCopy);
            console.log("Changes:", changes);

            changes.forEach(change => {
                if (change.quiz_question_id == null) {
                    console.log("INSERT: ", change);
                    // Adds a new quiz question (3 parameters)


                } else {
                    console.log("UPDATE: ", change);
                    // UPDATE lms_quiz_question ... SET ... WHERE quiz_question_id = quiz_question_id


                }
            });
            this.deleteQuestionId.forEach(quiz_question_id => {
                if (quiz_question_id != null) {
                    console.log("DELETE: ", quiz_question_id);
                    // DELETE FROM lms_quiz_question database WHERE quiz_question_id = quiz_question_id


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


        // --- Question Option -- 
        addOption(quiz_question_id, indexQ) {
            this.editOptions[indexQ].push({ "quiz_question_id": quiz_question_id, "option": "Option A", "correct": 0, "answer_count": 0 });
            console.log(this.editOptions[indexQ])
        },
        deleteOption(quiz_option_id, indexQ, indexO) {
            console.log(quiz_option_id, indexQ, indexO);
            this.editOptions[indexQ].splice(indexO, 1);
            this.deleteOptionId.push(quiz_option_id);
        }, 
        editOption(action) {
            if (action == "edit") {  
                console.log("Editing Options")
                // Creates a copy of options and stores it in optionsCopy
                this.optionsCopy = JSON.parse(JSON.stringify(this.editOptions));
            } else if (action == "cancel") {
                // Reverts changes made to questions by using the data from sectionsCopy
                this.editOptions = JSON.parse(JSON.stringify(this.optionsCopy));
            }
        },
        saveEditOption(indexQ) {
            // Save Edit Option Changes
            let changes = this.editOptions[indexQ].filter(this.optionComparer(this.optionsCopy[indexQ]));
            console.log("Edited:", this.editOptions[indexQ]);
            console.log("Original:", this.optionsCopy[indexQ]);
            console.log("Changes:", changes);

            changes.forEach(change => {
                if (change.quiz_option_id == null) {
                    console.log("INSERT: ", change);
                    // Adds a new quiz question (3 parameters)


                } else {
                    console.log("UPDATE: ", change);
                    // UPDATE lms_quiz_option ... SET ... WHERE quiz_option_id = quiz_option_id


                }
            });
            this.deleteOptionId.forEach(quiz_option_id => {
                if (quiz_option_id != null) {
                    console.log("DELETE: ", quiz_option_id);
                    // DELETE FROM lms_quiz_option database WHERE quiz_question_id = quiz_option_id


                }
            });
            this.deleteQuestionId = [];
            console.log(this.questions);
        },
        optionComparer(otherArray){
            return function(current){
                return otherArray.filter(function(other){
                    return (
                        other.quiz_option_id == current.quiz_option_id &&
                        other.option == current.option &&
                        other.correct == current.correct
                    )
                }).length == 0;
            }
        },


        // --- Quiz Statistics ---
        // Get Quiz Attempt of each student who had taken the quiz by section_id
        getStudentAttempt(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.studentAttempts = response.data;
            //     })
            let response = [
                {"learner_id": 6, "username": "stevenlim", "name":"Steven Lim", "email":"stevenlim@lms.com", 
                "seniority_level":"Engineer", "contact":90219324, "pass_attempt":2, "quiz_attempt":3, "best_grade":80 },
                {"learner_id": 9, "username": "tanboonlee", "name":"Tan Boon Lee", "email":"tanboonlee@lms.com", 
                "seniority_level":"Engineer", "contact":85548901, "pass_attempt":1, "quiz_attempt":1, "best_grade":80 }
            ];
            this.studentAttempts = response;
            console.log(this.studentAttempts);
        },
        // Get Quiz Attempt passing rate and attempt count by section_id
        getQuizStats(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.quizStats = response.data;
            //     })
            this.quizStats = {"pass_count": 3, "total_attempt": 4, "pass_rate": 0.7500};
            console.log(this.studentAttempts);
        },
        // Get all Quiz Attempt by section_id
        getQuizAttempts(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.quizAttempts = response.data;
            //     })
            let response = [
                {"user_id": 6, "username": "stevenlim", "name":"Steven Lim", "email":"stevenlim@lms.com", 
                "seniority_level":"Engineer", "contact":90219324, "quiz_attempt_id":1, "grade":40, "result":"Fail", "attempt_date":"2021-02-02" },
                {"user_id": 6, "username": "stevenlim", "name":"Steven Lim", "email":"stevenlim@lms.com", 
                "seniority_level":"Engineer", "contact":90219324, "quiz_attempt_id":2, "grade":40, "result":"Pass", "attempt_date":"2021-02-02" },
                {"learner_id": 9, "username": "tanboonlee", "name":"Tan Boon Lee", "email":"tanboonlee@lms.com", 
                "seniority_level":"Engineer", "contact":85548901, "quiz_attempt_id":4, "grade":80, "result":"Pass", "attempt_date":"2021-02-02" },
                {"user_id": 6, "username": "stevenlim", "name":"Steven Lim", "email":"stevenlim@lms.com", 
                "seniority_level":"Engineer", "contact":90219324, "quiz_attempt_id":5, "grade":40, "result":"Pass", "attempt_date":"2021-02-02" },
            ];
            this.quizAttempts = response;
            console.log(this.quizAttempts);
        },

    },
    created() {
        // Calls method to get section details
        this.getSectionDetail(this.section_id);

        // Calls method to get question options
        this.getOptions(this.section_id);

        // Calls method to get quiz attempt of each student who had taken the quiz
        this.getStudentAttempt(this.section_id);

        // Calls method to get quiz statistics
        this.getQuizStats(this.section_id);

        // Calls method to get all quiz attempts
        this.getQuizAttempts(this.section_id);
    }
}
</script>

<style>

</style>