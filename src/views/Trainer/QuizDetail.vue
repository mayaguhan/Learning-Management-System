<template>
    <div>
        <h1>
            Manage Quiz
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
                            <span v-show="toggleEditOption == false">{{ questionOption.option }}</span>
                            <v-row>
                                <v-col cols="9">
                                    <v-text-field v-model="questionOption.option" :rules="[rules.required, rules.counter]"
                                    v-show="toggleEditOption == true" label="Question Option" maxlength="100" ></v-text-field>
                                </v-col>
                                <v-col cols="2">
                                    <v-switch v-model="questionOption.correct" v-show="toggleEditOption == true" label="Correct"></v-switch>
                                </v-col>
                                <v-col cols="1">
                                    <v-btn class="primary" v-show="toggleEditOption" @click="deleteOption(questionOption.quiz_option_id, indexQ, indexO)">Delete</v-btn>
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
                    X/X students cleared this section <br>
                    <!-- Get Quiz Attempt of each student who had taken the quiz by section_id -->
                    Data Table
                    <!-- Get Quiz Attempt of each student who had taken the quiz by section_id -->

                    % pass rate per quiz attempt<br>
                    <!-- Get Quiz Attempt passing rate and attempt count by section_id -->
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header>
                    Quiz Attempts
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    Total Quiz Attempts: 10 <br>
                    <!-- Get Quiz Attempt passing rate and attempt count by section_id -->
                    Data Table
                    <!-- Get all Quiz Attempt by section_id -->
                        <!-- For each entry @click View Submission: -->
                        <!-- Get Learner's Quiz Performance by quiz_attempt_id and section_id -->
                </v-expansion-panel-content>
            </v-expansion-panel>

            <v-expansion-panel>
                <v-expansion-panel-header>
                    Question Breakdown
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <!-- Get Quiz's Question Performance by section_id -->
                    Quesiton Name<br>
                    <ol>
                        <li>Option A - 70%</li>
                        <li>Option A - 10%</li>
                        <li>Option A - 10%</li>
                        <li>Option A - 10%</li>
                    </ol>
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
                "passing_grade": 80
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
                "quiz_option_id": 1, "option": "Option A", "correct": 1 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 2, "option": "Option B", "correct": 0 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 3, "option": "Option C", "correct": 0 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", "type": "MCQ", 
                "quiz_option_id": 4, "option": "Option D", "correct": 0 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?", "type": "T/F", 
                "quiz_option_id": 5, "option": "True", "correct": 1 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?", "type": "T/F", 
                "quiz_option_id": 6, "option": "False", "correct": 0 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?", "type": "T/F", 
                "quiz_option_id": 7, "option": "True", "correct": 1 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?", "type": "T/F", 
                "quiz_option_id": 8, "option": "False", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ",
                "quiz_option_id": 9, "option": "Option A", "correct": 1 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 10, "option": "Option B", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 11, "option": "Option C", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", "type": "MCQ", 
                "quiz_option_id": 12, "option": "Option D", "correct": 0 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?", "type": "T/F", 
                "quiz_option_id": 13, "option": "True", "correct": 1 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?", "type": "T/F", 
                "quiz_option_id": 14, "option": "True", "correct": 0 }
            ];

            // Groups question options into question groups by question_id
            let questionArr = Object.values(questionOptions.reduce((result, 
            { quiz_question_id, question_name, type, quiz_option_id, option, correct }) => {
                // Create new question group
                if (!result[quiz_question_id]) result[quiz_question_id] = {
                    quiz_question_id, question_name,  type, question_options: []
                };
                // Append question option to question group
                result[quiz_question_id].question_options.push({ quiz_option_id,  option, correct });
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
            console.log("Save")
        },


        // --- Question ---
        addQuestion() {
            this.questions.push({ "question_name": "New Question", "type": "MCQ" });
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
                    // UPDATE lms_quiz_question ... SET ... WHERE quiz_question_id = quiz_quesiton_id


                }
            });
            this.deleteQuestionId.forEach(quiz_question_id => {
                if (quiz_question_id != null) {
                    console.log("DELETE: ", quiz_question_id);
                    // DELETE FROM lms_quiz_question database WHERE quiz_question_id = quiz_quesiton_id


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
            this.editOptions[indexQ].push({ "quiz_question_id": quiz_question_id, "option": "Option A", "correct": 0 });
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
            console.log("Save");
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

    },
    created() {
        // Calls method to get section details
        this.getSectionDetail(this.section_id);

        // Calls method to get question options
        this.getOptions(this.section_id)
    }
}
</script>

<style>

</style>