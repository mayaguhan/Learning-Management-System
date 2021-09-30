<template>
    <div>
        <h1>
            Manage Quiz
        </h1>
        <!-- Toggle: Edit Questions -->
        <v-btn icon @click="toggleEdit=!toggleEdit, editAction('edit')" v-show="toggleEdit == false">
            <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <!-- Cancel Question Edits -->
        <v-btn class="light"  @click="toggleEdit=!toggleEdit, editAction('cancel')" v-show="toggleEdit == true">
            Cancel
        </v-btn>

        <template>
        <v-expansion-panels focusable :items="questions">
            <v-expansion-panel v-for="(question, indexS) in questions" :key="question.question_id">
                <v-expansion-panel-header>
                    {{ question.question_name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>

                    <ul v-for="questionOption in question.question_options" v-bind:key="questionOption.quiz_option_id">
                        <li>
                            {{ questionOption.option }}
                        </li>
                    </ul>


                    <v-divider></v-divider>

                    <v-btn class="primary" v-show="toggleEdit == true" @click="deleteSection(indexS)">
                        Delete Question
                    </v-btn>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
        </template>

        <!-- <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table :headers="headers" :items="questions" :search="search">
        <template v-slot:item="row">
            <tr>
                <td>
                    {{ row.item.question_name }} 
                </td>
                <td>
                    {{ row.item.type }}
                </td>
            </tr>
        </template>
        </v-data-table>
        </v-card> -->



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
        }
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        questions: {},
        options: {},
        toggleEdit: false,

        search: '',
        headers: [
            { text: 'Question Name', value: 'question_name', align: 'start', sortable: true},
            { text: 'Type', value: 'type', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
    }),
    methods: {
        getQuestionOptions(section_id) {
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
                    quiz_question_id,
                    question_name, 
                    type, 
                    question_options: []
                };
                // Append question option to question group
                result[quiz_question_id].question_options.push({
                    quiz_option_id,
                    option,
                    correct
                });
                return result;
            }, {}));

            this.questions = questionArr;
            console.log(this.questions);
        },
        deleteSection(indexS) {
            this.questions.splice(indexS, 1);
        },
        editAction(action) {
            if (action == "edit") {  
                console.log("Edit")
                // Creates a copy of questions and stores it in sectionsCopy
                // this.questionsCopy = JSON.parse(JSON.stringify(this.questions));
            } else if (action == "cancel") {
                console.log("Cancel")
                // Reverts changes made to questions by using the data from sectionsCopy
                // this.questions = JSON.parse(JSON.stringify(this.questionsCopy));
            }
        },
        saveEdit() {
            // Save edit question changes

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

    },
    created() {
        // Calls method to get question options
        this.getQuestionOptions(this.section_id)



    }
}
</script>

<style>

</style>