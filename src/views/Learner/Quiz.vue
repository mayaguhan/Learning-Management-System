<template>
    <div class="mt-5" style="text-align: center">
        <v-container fluid>
            <v-row>
                <v-col>
                    <h1>Section {{section_id}} Quiz</h1>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="2">
                    <v-simple-table>
                        <template v-slot:default>
                        <thead>
                        </thead>
                        <tbody>
                            <tr
                            v-for="question in questions"
                            :key="question.question_id"
                            >
                            <td>Question {{ question.quiz_question_id }}</td>
                            </tr>
                        </tbody>
                        </template>
                    </v-simple-table>
                </v-col>

                <v-col>
                    <div v-for="question in questions" :key="question.question_id">
                        <v-container>
                            <v-row>
                                <v-col>
                                    <div>{{ question.question_name }}</div>
                                    <!-- <v-checkbox v-for="optionObj in quizOptionsList" :key="optionObj.option"></v-checkbox> -->
                                    <div>
                                        <input type="radio" id="html" name="fav_language" value="HTML" v-for="item in options" :key="item.option">
                                    </div>
                                </v-col>
                            </v-row>
                        </v-container>
                    </div>
                </v-col>
            </v-row>
        </v-container>
    </div>
</template>

<script>
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
        questions: [],
        options: [],
    }),
    methods: {
        // SELECT qq.quiz_question_id, qo.quiz_option_id, qq.question_name, qq.type, qo.option, qo.correct
        // Get all Quiz Question and Quiz Option by section_id
        getQuizQuestions() {
            let quizQuestions = [
                {
                    'quiz_question_id': 1,
                    'question_name': "This is question 1",
                    'type' : "MCQ",
                },
                {
                    'quiz_question_id': 2,
                    'question_name': "This is question 2",
                    'type' : "MCQ",
                },
                {
                    'quiz_question_id': 3,
                    'question_name': "This is question 3",
                    'type' : "MCQ",
                },
            ];
            this.questions = quizQuestions;
        },
        getQuizOptions() {
            let quizOptions = [
                {
                    'quiz_question_id': 1,
                    'quiz_option_id': 1,
                    'question_name': 'Lorem ipsum dolor sit amet, consectetur adipiscing...',
                    'type': 'MCQ',
                    'option': 'True',
                    'correct': 1,
                },
                {
                    'quiz_question_id': 1,
                    'quiz_option_id': 2,
                    'question_name': 'Lorem ipsum dolor sit amet, consectetur adipiscing...',
                    'type': 'MCQ',
                    'option': 'False',
                    'correct': 0,
                },
            ];
            this.options = quizOptions;
        },
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
        // Calls method to get quiz details
        // this.getQuizDetail();
        this.getQuizOptions();
        this.getQuizQuestions();
        
    }
}
</script>

<style>

</style>