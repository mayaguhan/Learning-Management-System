<template>
    <div>
        <h1>
            HELLO WORLD!
        </h1>
        <div>
            <SingleCourse :name="name" />
        </div>
    </div>
</template>

<script>
import SingleCourse from "./SingleCourse.vue";


export default {
    name: "Courses",
    components: {
        SingleCourse
    },
    data(){
        return {
            name: "David"
        }
    },
    methods: {
        heyDavid() {
            //
        }
    },
    computed() {
        //
    },
    created() {
        //
    }



}
</script>

<style>

</style>