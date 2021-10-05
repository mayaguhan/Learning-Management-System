<template>
    <div>
        <h1>
            Quiz Test
        </h1>
        <ol>
            <li v-for="question in questions" v-bind:key="question.quiz_question_id">
                {{ question.question_name}}
                <div v-for="questionOption in question.question_options" v-bind:key="questionOption.quiz_option_id">
                    <input type="radio" :name="question.quiz_question_id" v-bind:value="questionOption.quiz_option_id" v-model="question.selectedAnswer">
                    {{ questionOption.option }}
                </div>
            </li>
        </ol>

        <v-btn @click="submit()">Submit</v-btn>
    </div>
</template>

<script>

export default {
    name: "QuizTest",
    data: () => ({
        section_id: 1,
        questions: [],


    }),
    methods: {
        // Get all Quiz Question and Quiz Option by section_id
        getOptions(section_id) {
            let updatedApiWithEndpoint = this.apiLink + "/TBC";
            let dataObj = { "sectionId": section_id  }
            console.log(updatedApiWithEndpoint, dataObj);

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
                question["selectedAnswer"] = 0
            });
            this.questions = questionArr;
            console.log(this.questions);
        },

        submit() {
            // Check the answer
            console.log(this.questions);

        }
    },
    created() {

        // Calls method to get question options
        this.getOptions(this.section_id)
    }
}
</script>

<style>

</style>