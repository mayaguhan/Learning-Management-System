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
                    <div v-for="(question, indexQ) in questions" :key="question.question_id">
                        <v-container>
                            <v-row>
                                <v-col>
                                    <div>{{ question.question_name }}</div>
                                    <label :for="questionOption.quiz_option_id" v-for="questionOption in testOptions[indexQ]" :key="questionOption.quiz_option_id">
                                        <input type="radio" 
                                        :id="questionOption.quiz_option_id" 
                                        :name="question.quiz_question_id"
                                        :value="questionOption.quiz_option_id">
                                        {{questionOption.option}}
                                        <!-- {{question.quiz_question_id}} -->
                                        <!-- {{questionOption.quiz_option_id}} -->
                                    </label>
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

        testOptions: [],

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
        // SELECT qq.quiz_question_id, qo.quiz_option_id, qq.question_name, qq.type, qo.option, qo.correct
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
                this.testOptions.push(question.question_options)
                console.log(question.question_options)
            });
            console.log(this.testOptions);
            this.questions = questionArr;
            this.questionCount = this.questions.length;
            console.log(this.questions);
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
        this.getOptions();
    }
}
</script>

<style>

</style>