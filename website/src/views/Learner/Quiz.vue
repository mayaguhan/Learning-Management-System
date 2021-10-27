<template>
    <div class="mt-5">
        <v-container fluid>
            <v-row>
                <v-col>
                    <h1></h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="2">
                    <v-simple-table>
                        <template v-slot:default>
                        <thead>
                        </thead>
                        <tbody>
                            <tr v-for="question in questions" :key="question.question_id">
                                <td>Question {{ question.quiz_question_id }}</td>
                            </tr>
                        </tbody>
                        </template>
                    </v-simple-table>
                </v-col>

                <v-col>
                    <div v-for="question in questions" v-bind:key="question.quiz_question_id">
                        <v-container>
                            <v-row>
                                <v-col>
                                    <div>{{ question.question_name }}</div>
                                    
                                    <div v-for="questionChoice in question.question_choices" v-bind:key="questionChoice.quiz_choice_id">
                                        <input type="radio" :name="question.quiz_question_id" v-bind:value="questionChoice.quiz_choice_id" v-model="question.selectedAnswer">
                                        {{ questionChoice.choice }}
                                    </div>
                                </v-col>
                            </v-row>
                        </v-container>
                    </div>
                    <v-btn @click="submit()">Submit</v-btn>
                </v-col>
            </v-row> 
        </v-container>
        
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Quiz",
    props: {
        section_id: parseInt({ type: Number })
    },
    components: {
        //
    },
    data: () => ({
        currentUserId: 12, // To be replaced with user_id of logged in user
        quizAttemptId: 0,
        
        questions: [],
        options: [],
    }),
    methods: {
        // Get Section information by section_id
        getSectionDetail() {
            // let updatedApiWithEndpoint = this.apiLink + "/getsectioninfobysectionandtrainer";
            // let dataObj = { "sectionId": this.section_id }
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         this.sectionDetail = response.data[0];
            //     })
        },
        // Add new Quiz attempt
        addQuizAttempt() {
            let updatedApiWithEndpoint = this.apiLink + "/addnewquizattempt ";
            let dataObj = { "sectionId": this.section_id, "learnerId": this.currentUserId }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    console.log(response.data.insertId);
                    this.quizAttemptId = response.data.insertId;
                })
        },
        // Get Quiz's Question Performance by section_id
        getQuestionChoices() {
            let updatedApiWithEndpoint = this.apiLink + "/getquizquestionperformancebysection ";
            let dataObj = { "sectionId": this.section_id  }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    // Groups question choices into question groups by question_id
                    let questionArr = Object.values(response.data.reduce((result, 
                    { quiz_question_id, question_name, quiz_choice_id, choice, correct, answer_count }) => {
                        // Create new question group
                        if (!result[quiz_question_id]) result[quiz_question_id] = {
                            quiz_question_id, question_name, question_choices: []
                        };
                        // Append question choice to question group
                        result[quiz_question_id].question_choices.push({ quiz_choice_id,  choice, correct, answer_count });
                        return result;
                        },{}
                    ));
                    this.questions = questionArr;
                    console.log(questionArr);
                })
        },
        submit() {
            // Check the answer
            let updatedApiWithEndpoint = this.apiLink + "/addnewquizperformance ";
            this.questions.forEach(answer => {
                let dataObj = { "quizAttemptId": this.quizAttemptId, "questionId": answer.quiz_question_id, "quizChoiceId": answer.selectedAnswer }
                console.log(dataObj);
                axios.post(updatedApiWithEndpoint, dataObj)
                    .then((response) => {
                        console.log(response);
                    })
            });
            // Get Quiz Performance by quiz_attempt_id
            // let quizPerformanceEndPoint = this.apiLink + "/getquizperformancebyattemptid";
            // let quizPerformanceObj = {}


            // Update Quiz attempt with grade
            // let quizAttemptEndPoint = this.apiLink + "/updatequizattemptwithgrade ";
            // let quizAttemptObj = {}

            
        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
        // Calls method to retrieve section details
        this.getSectionDetail();

        // Calls method to get question choices
        this.getQuestionChoices();

        // Calls method to add a new quiz attempt
        this.addQuizAttempt();
    }
}
</script>

<style>

</style>