<template>  
    <div>
        {{ data }}
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Example",
    data() {
        return {
            data: []
        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created(){

        var updatedApiWithEndpoint = this.apiLink + "/getusers";
        axios.get(updatedApiWithEndpoint)
            .then((response) => {
                console.log(response);
                this.data = response.data;
            })

    }

}
</script>

<style>

</style>