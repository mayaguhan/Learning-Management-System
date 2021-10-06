<template>
    <div>
        <h1 style="padding:15px">
            <!-- course name -->
            {{ courseObj.title }}
        </h1>

        <v-card>
              <v-card-title>
                <v-text-field
                  v-model="search"
                  append-icon="mdi-magnify"
                  label="Search"
                  single-line
                  hide-details
                ></v-text-field>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
                <v-spacer></v-spacer>
              </v-card-title>
              <v-data-table
                :headers="headers"
                :items="trainers"
                :search="search"
              >
                <template v-slot:item="row">
                    <tr>
                        <td>
                            <!-- trainer name -->
                            {{ row.item.name }}
                        </td>
                        <td width="10">
                            <router-link :to="{ name: 'HRCourseDetail', params: { course_id: course_id, trainer_id: row.item.user_id }}">
                                <v-btn depressed small color="#0062E4">
                                    <span style="color: white">View Conduct</span> 
                                </v-btn>
                            </router-link>
                        </td>
                    </tr>
                </template>
              </v-data-table>
            </v-card>
          </div>
</template>

<script>

import axios from 'axios';

export default {
    name:"HRConduct",
        props: {
        course_id: parseInt({ type: Number })
    },
    
    data () {
      return {

        courseObj: {},

        search: '',
        headers: [
            { text: 'Trainer Name', value: 'name', align: 'start', sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        trainers: []
      }
    },

    methods: {

        // get course name

            getCourseDetail() {
                let updatedApiWithEndpoint1 = this.apiLink + "/getasinglecourse";
                let dataObj = { "courseId": this.course_id }
                axios.post(updatedApiWithEndpoint1, dataObj)
                .then((response) => {
                    console.log(response);
                    var array = response.data;
                    this.courseObj = array[0];
                })
            },

        // get trainers conducting that course

            getTrainerDetail() {

                let updatedApiWithEndpoint2 = this.apiLink + "/retrievealltrainersconductingcourse";
                let dataObj = { "courseId": this.course_id }
                axios.post(updatedApiWithEndpoint2, dataObj)
                .then((response) => {
                    console.log(response);
                    this.trainers = response.data;
                })

        },


    },

    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    
    created() {
        // Calls method to get course details
        this.getCourseDetail();
        this.getTrainerDetail();

    }

  }
</script>