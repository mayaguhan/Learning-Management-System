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
    data() {
        //
    },
    methods: {
        // SELECT qq.quiz_question_id, qo.quiz_option_id, qq.question_name, qq.type, qo.option, qo.correct
        // Get all Quiz Question and Quiz Option by section_id
        
    },
    computed() {
        //
    },
    created() {
        // Calls method to get quiz details
        // this.getQuizDetail();
    }
}
</script>

<style>

</style>