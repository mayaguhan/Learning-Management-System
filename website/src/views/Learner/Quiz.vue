<template>
    <div class="mt-5" style="text-align: center">
        <v-container fluid>
            <v-row>
                <v-col>
                    <h1>Section {{section_id}} Quiz</h1>
                    <!-- Timer -->
                    <h1>{{ formatedCountdown || 'countdown over' }}</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="1">
                    <v-simple-table>
                        <template v-slot:default>
                        <thead>
                        </thead>
                        <tbody>
                            <tr
                            v-for="question in questions"
                            :key="question.question_id"
                            >
                            <td>
                                <a :href='question.hyperlink'>
                                    Q{{ question.quiz_question_id }}
                                </a>
                            </td>
                            </tr>
                        </tbody>
                        </template>
                    </v-simple-table>
                </v-col>

                <v-col>
                    <div v-for="(question, indexQ) in questions" :key="question.question_id">
                        <v-container>
                            <v-row>
                                <v-col>
                                    <div :id="question.question_name">{{ question.question_name }}</div>
                                    <label :for="questionchoice.quiz_choice_id" v-for="questionchoice in testchoices[indexQ]" :key="questionchoice.quiz_choice_id">
                                        <input type="radio" 
                                        :id="questionchoice.quiz_choice_id" 
                                        :name="question.quiz_question_id"
                                        :value="questionchoice.quiz_choice_id"
                                        v-model="question.selectedAnswer">
                                        {{questionchoice.choice}}
                                        <!-- {{question.quiz_question_id}} -->
                                        <!-- {{questionchoice.quiz_choice_id}} -->
                                        <!-- <br>
                                        {{ question }}
                                        <br> -->
                                    </label>
                                    
                                </v-col>
                            </v-row>
                        </v-container>
                    </div>
                </v-col>
            </v-row>

            <v-row>
                <v-col cols="1"></v-col>
                <v-col>
                    <v-btn @click="submit()">Submit</v-btn>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
/* import axios from "axios" */

/* Timer */
import  moment from 'moment'
import 'moment-duration-format'
export default {
    name: "Quiz",
    props: {
        course_id: parseInt({ type: Number }), 
        learner_id: parseInt({ type: Number }),
        section_id: parseInt({ type: Number }),
    },
    components: {
        //
    },
    data: () => ({
        currentUserId: 1, // To be replaced with user_id of logged in user

        questions: [],
        
        choices: [],

        testchoices: [],
        
        // Timer
        countdown: 300

    }),
    methods: {
        // SELECT qq.quiz_question_id, qo.quiz_choice_id, qq.question_name, qq.type, qo.choice, qo.correct
        // Get all Quiz Question and Quiz choice by section_id
        /* addQuizAttempt(section_id, learner_id, course_id, trainer_id){
            let updatedApiWithEndpoint2 = this.apiLink + "/TBC";
            let dataObj2 = {
                "sectionId" : section_id,
                "learnerId" : learner_id,
                "courseId" : course_id,
                "trainerId" : trainer_id

            };
            axios.post(updatedApiWithEndpoint2, dataObj2)
                .then((response) => {
                    console.log(response);
                })
        }, */
        getchoices(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);
            // axios.post(updatedApiWithEndpoint, dataObj)
            //     .then((response) => {
            //         console.log(response);
            //         this.questions = response.data;
            //     })

            let questionchoices = [
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", 
                "quiz_choice_id": 1, "choice": "choice A", "correct": 1 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?",
                "quiz_choice_id": 2, "choice": "choice B", "correct": 0 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?", 
                "quiz_choice_id": 3, "choice": "choice C", "correct": 0 },
                { "quiz_question_id": 1, "question_name": "What are the steps to replace a printer catridge?",
                "quiz_choice_id": 4, "choice": "choice D", "correct": 0 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?", 
                "quiz_choice_id": 5, "choice": "True", "correct": 1 },
                { "quiz_question_id": 2, "question_name": "How to setup a printer?",
                "quiz_choice_id": 6, "choice": "False", "correct": 0 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?", 
                "quiz_choice_id": 7, "choice": "True", "correct": 1 },
                { "quiz_question_id": 3, "question_name": "How to ensure printing quality?",
                "quiz_choice_id": 8, "choice": "False", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?",
                "quiz_choice_id": 9, "choice": "choice A", "correct": 1 },
                { "quiz_question_id": 4, "question_name": "How to colour code?",
                "quiz_choice_id": 10, "choice": "choice B", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?", 
                "quiz_choice_id": 11, "choice": "choice C", "correct": 0 },
                { "quiz_question_id": 4, "question_name": "How to colour code?",
                "quiz_choice_id": 12, "choice": "choice D", "correct": 0 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?",
                "quiz_choice_id": 13, "choice": "True", "correct": 1 },
                { "quiz_question_id": 5, "question_name": "What do you do with faulty machines?",
                "quiz_choice_id": 14, "choice": "True", "correct": 0 }
            ];

            // Groups question choices into question groups by question_id
            let questionArr = Object.values(questionchoices.reduce((result, 
            { quiz_question_id, question_name, type, quiz_choice_id, choice, correct }) => {
                // Create new question group
                if (!result[quiz_question_id]) result[quiz_question_id] = {
                    quiz_question_id, question_name,  type, question_choices: []
                };
                // Append question choice to question group
                result[quiz_question_id].question_choices.push({ quiz_choice_id,  choice, correct });
                return result;
                },{}
            ));
            questionArr.forEach(question => {
                question["selectedAnswer"] = 0;
                question["hyperlink"] = "#" + question.question_name;
                this.testchoices.push(question.question_choices);
                console.log(question.question_choices);
            });
            console.log(this.testchoices);
            this.questions = questionArr;
            this.questionCount = this.questions.length;
            console.log(this.questions);
        },
        submit() {
            // Check the answer
            console.log("Submitted choices:");
            console.log(this.questions);

        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        },
        // Timer
        formatedCountdown() {
            return moment.duration(this.countdown, 'seconds').format('m:ss')
        },
    },
    created() {
        // Calls method to get quiz details
        // this.getQuizDetail();
        this.getchoices();
    },
    // Timer
    mounted() {
        const stopCountdown = setInterval(() => {
        console.log('current countdown', this.countdown)
        this.countdown -= 1
        if (!this.countdown) clearInterval(stopCountdown)
        }, 1000)
    },
}
</script>

<style>

</style>