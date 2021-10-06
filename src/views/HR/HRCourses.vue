<template>
    <div>
        <v-tabs>
            <v-tab @click="allcourses = true; allengineers = false;">All Courses</v-tab>
            <v-tab @click="allengineers = true; allcourses = false;">Engineers</v-tab>
        </v-tabs>

        <div>
          <!-- All Courses Content -->
          <div v-if="allcourses">
            <v-card>
              <v-card-title>
                <v-text-field
                  v-model="searchCourses"
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
                :headers="headersCourses"
                :items="courses"
                :search="searchCourses"
              >
                <template v-slot:item="row">
                    <tr>
                        <td>
                            {{row.item.course_code}} - {{row.item.title}} 
                        </td>
                        <td>
                            {{ formatDate(row.item.start_date) }}
                        </td>
                        <td>
                           {{ formatDate(row.item.end_date) }}
                        </td>
                        <td width="10">
                          <router-link :to="{ name: 'HRConduct', params: { course_id: row.item.course_id }}">
                              <v-btn depressed small color="#0062E4">
                                  <span style="color: white">View Course</span> 
                              </v-btn>
                          </router-link>
                        </td>
                    </tr>
                </template>
              </v-data-table>
            </v-card>
          </div>

          <!-- Engineers Content -->
          <div v-if="allengineers">
            <v-card>
              <v-card-title>
                <v-text-field
                  v-model="searchEngineers"
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
                :headers="headersEngineers"
                :items="engineers"
                :search="searchEngineers"
              >
                <template v-slot:item="row">
                    <tr>
                        <td>
                            {{row.item.name}}
                        </td>
                        <td>
                            {{ row.item.seniority_level }}
                        </td>
                    </tr>
                </template>
              </v-data-table>
            </v-card>

          </div>

        </div>
    </div>
</template>

<script>

import axios from 'axios';
import moment from "moment";

export default {
    name:"HRCourses",
    
    data () {
      return {

        allcourses: true,
        allengineers: false,

        searchCourses: '',
        headersCourses: [
            { text: 'Course Name', value: 'title', align: 'start', sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        courses: [],

        searchEngineers: '',
        headersEngineers: [
            { text: 'Name', value: 'name', align: 'start', sortable: true},
            { text: 'Seniority Level', value: 'seniority_level', filterable: false, sortable: false},
        ],
        engineers: []
      }
    },

    methods: {
        getCoursesDetail() {
            let updatedApiWithEndpoint1 = this.apiLink + "/getallcourses";
            axios.get(updatedApiWithEndpoint1)
            .then((response) => {
               console.log(response);
               this.courses = response.data;
            })
        },

        getEngineersDetail() {
            let updatedApiWithEndpoint2 = this.apiLink + "/getusers";
            axios.get(updatedApiWithEndpoint2)
            .then((response) => {
                console.log(response);
                this.engineers = response.data;
            })

        },

        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD');
        }

    },

    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
        // Calls method to get course details
        this.getCoursesDetail();
        this.getEngineersDetail();


    }

  }
</script>

<style>

</style>