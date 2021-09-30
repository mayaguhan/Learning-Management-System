<template>
    <div class="mt-5" style="text-align: center">
        <h1>{{section_id}} Quiz</h1>
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
        quizDetailList: [],
    }),
    methods: {
        // SELECT qq.quiz_question_id, qo.quiz_option_id, qq.question_name, qq.type, qo.option, qo.correct
        // Get all Quiz Question and Quiz Option by section_id
        getQuizDetail() {
            let quizDetail = {
                'quiz_question_id': 1,
                'quiz_option_id': 1,
                'question_name': 'Lorem ipsum dolor sit amet, consectetur adipiscing...',
                'type': 'MCQ',
                'option': 'Ut auctor augue varius vestibulum.',
                'correct': 1,
            };
            this.quizDetailList.push(quizDetail);
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
        this.getQuizDetail();
        
    }
}
</script>

<style>

</style>