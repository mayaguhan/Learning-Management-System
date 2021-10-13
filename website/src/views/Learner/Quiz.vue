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
                                    <label :for="questionOption.quiz_option_id" v-for="questionOption in testOptions[indexQ]" :key="questionOption.quiz_option_id">
                                        <input type="radio" 
                                        :id="questionOption.quiz_option_id" 
                                        :name="question.quiz_question_id"
                                        :value="questionOption.quiz_option_id"
                                        v-model="question.selectedAnswer">
                                        {{questionOption.option}}
                                        <!-- {{question.quiz_question_id}} -->
                                        <!-- {{questionOption.quiz_option_id}} -->
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
        
        options: [],

        testOptions: [],
        
        // Timer
        countdown: 300

    }),
    methods: {
        // SELECT qq.quiz_question_id, qo.quiz_option_id, qq.question_name, qq.type, qo.option, qo.correct
        // Get all Quiz Question and Quiz Option by section_id
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
                question["selectedAnswer"] = 0;
                question["hyperlink"] = "#" + question.question_name;
                this.testOptions.push(question.question_options);
                console.log(question.question_options);
            });
            console.log(this.testOptions);
            this.questions = questionArr;
            this.questionCount = this.questions.length;
            console.log(this.questions);
        },
        submit() {
            // Check the answer
            console.log("Submitted Options:");
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
        this.getOptions();
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