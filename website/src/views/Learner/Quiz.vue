<template>
    <div class="mt-5">
        <v-container fluid>
            <v-row>
                <v-col><h1 class="text-center">{{ sectionName }} Quiz</h1></v-col>
            </v-row>
            <v-row align="center">
                <v-col><h1 class="text-center">{{ formatedCountdown || 'countdown over' }}</h1></v-col>
            </v-row>
            <v-row>
                <v-col cols="2">
                    <v-simple-table>
                        <template v-slot:default>
                        <thead>
                        </thead>
                        <tbody>
                            <tr v-for="(question, index) in questions" :key="question.question_id">
                                <td><a :href='question.hyperlink'>Question {{ index + 1 }}</a></td>
                            </tr>
                        </tbody>
                        </template>
                    </v-simple-table>
                </v-col>

                <v-col>
                    <div v-for="(question, index) in questions" v-bind:key="question.quiz_question_id">
                        <v-container>
                            <v-row>
                                <v-col>
                                    <div :id="question.quiz_question_id">{{ "Q" + (index+1) + ") " + question.question_name }}</div>
                                    
                                    <div v-for="questionChoice in question.question_choices" v-bind:key="questionChoice.quiz_choice_id">
                                        <input type="radio" :name="question.quiz_question_id" v-bind:value="questionChoice.quiz_choice_id" v-model="question.selectedAnswer">
                                        {{ questionChoice.choice }}
                                    </div>
                                </v-col>
                            </v-row>
                        </v-container>
                    </div>
                    <template>
                        <div>
                            <v-btn
                            dark
                            color="blue darken-2"
                            @click="submit()"
                            >
                            Submit
                            </v-btn>

                            <v-snackbar
                            v-model="snackbar"
                            :timeout="timeout"
                            >
                            {{ text }}

                            <template v-slot:action="{ attrs }">
                                <v-btn
                                color="blue"
                                text
                                v-bind="attrs"
                                @click="snackbar = false"
                                >
                                Close
                                </v-btn>
                            </template>
                            </v-snackbar>
                        </div>
                    </template>
                </v-col>
            </v-row> 
        </v-container>
        
    </div>
</template>

<script>
/* Timer */
import  moment from 'moment'
import 'moment-duration-format'
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
        currentUserId: 14, // To be replaced with user_id of logged in user
        quizAttemptId: 0,
        conductId: 0,
        sectionName: "",
        
        questions: [],
        quizResult: 0,
        // Timer
        countdown: 0,
        // Snackbar
        snackbar: false,
        text: 'My timeout is set to 2000.',
        timeout: 2000,
    }),
    methods: {
        // Get Section information by section_id
        getSectionDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getsectioninfobysectionid";
            let dataObj = { 
                "sectionId": this.section_id
            }
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                    this.conductId = response.data[0]["conduct_id"];
                    this.countdown = response.data[0]["quiz_duration"] * 60;
                    this.sectionName = response.data[0]["section_name"];               
                }) 
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
                    this.questions.forEach(question => {
                        question["hyperlink"] = "#" + question.quiz_question_id;
                    });
                    console.log(this.questions);
                })
        },
        submit() {
            // Check the answer
            var totalScore = 0;
            var correctAnswer = 0;
            let updatedApiWithEndpoint = this.apiLink + "/addnewquizperformance ";
            this.questions.forEach(answer => {
                var dataObj = { "quizAttemptId": this.quizAttemptId, "questionId": answer.quiz_question_id, "quizChoiceId": answer.selectedAnswer };
                answer.question_choices.forEach(choice => {
                    if (choice.correct == 1){
                        correctAnswer = choice.quiz_choice_id;
                    }
                });
                if (answer["selectedAnswer"] == correctAnswer) {
                    totalScore += 100 / (this.questions.length);
                }
                console.log(dataObj);
                console.log(updatedApiWithEndpoint);
                console.log(totalScore);      
            });
            totalScore = totalScore.toFixed(2);
            this.updateGrade(totalScore);
        },
        updateGrade(studentScore){
            // Update Quiz attempt with grade
            let quizAttemptEndPoint = this.apiLink + "/updatequizattemptwithgrade ";
            let quizAttemptObj = {
                "grade" : studentScore,
                "attemptId" : this.quizAttemptId
            }
            axios.post(quizAttemptEndPoint, quizAttemptObj)
                .then((response) => {
                    console.log(studentScore);
                    console.log(response);
                    this.text = `You got ${studentScore}/100`
                    this.showSnackbar();
                })
        },
        showSnackbar() {
            // Show snackbar, once snackbar disappears (due to timeout set), redirect
            this.snackbar = true;
            setTimeout(() => { this.$router.replace(`/singlecourse/${this.conductId}`); }, this.timeout);
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
        // Calls method to retrieve section details
        this.getSectionDetail();

        // Calls method to get question choices
        this.getQuestionChoices();

        // Calls method to add a new quiz attempt
        this.addQuizAttempt();
    },
    // Timer
    mounted() {
        const stopCountdown = setInterval(() => {
            console.log('current countdown', this.countdown)
            this.countdown -= 1
            if (!this.countdown) clearInterval(stopCountdown)
        }, 1000)
    },
    watch: {
        countdown: function(newValue, oldValue){
            console.log("old value: ", oldValue);
            console.log("new value: ", newValue)
            if (newValue == 0) {
                alert("Time's up, your answers have been automatically submitted.");
                this.submit();   
            }
        }
    }
}
</script>

<style>

</style>
