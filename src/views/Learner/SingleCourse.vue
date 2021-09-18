<template>
    <div>
        <h1>
            HELLO {{ name }}!
        </h1>
    </div>
</template>

<script>
export default {

    name: "SingleCourse",
    props: [
        'name'
    ],
    data(){
        return {
            //
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
        // can make an api to retrieve course details
    }



}
</script>

<style>

</style>