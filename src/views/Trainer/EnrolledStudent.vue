<template>
    <div>
        <h1>
            Enrolled Students 
        </h1>
    </div>
</template>

<script>
export default {
    name: "EnrolledStudent",
    props: {
        course_id: parseInt({ type: Number }), 
        trainer_id: parseInt({ type: Number })
    },
    data: () => ({
        // data
    }),
    methods: {
        // methods
    },
    created() {
        // 
    }
}
</script>

<style>

</style>