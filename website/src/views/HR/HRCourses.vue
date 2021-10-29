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
                          <!-- Enrol Course Dialog -->
                          <v-btn color="primary" :disabled="row.item.trainer_count == 0"
                          @click.stop="$set(selectedCourse, row.item.course_id, true), getCourseTrainer(row.item.course_id)">
                            View Trainers
                          </v-btn>
                          <v-dialog v-model="selectedCourse[row.item.course_id]" scrollable max-width="1200" :key="row.item.course_id">
                            <v-card>
                              <v-card-title>
                                <span>Classes: {{ row.item.course_code }} - {{ row.item.title }}</span>
                              </v-card-title>
                              <v-card-subtitle>
                                {{ row.item.outline }}
                              </v-card-subtitle>
                              <v-card-text>
                                <v-data-table :headers="headersTrainers" :items="trainers">
                                  <template v-slot:item="row">
                                    <tr>
                                      <td>
                                        {{ row.item.name }} 
                                      </td>
                                      <td>
                                        {{ row.item.email }} <br>
                                        {{ row.item.contact }}
                                      </td>
                                      <td>
                                        {{ row.item.remaining }}
                                      </td>
                                      <td>
                                        {{ formatDate(row.item.end_register) }} to <br>
                                        {{ formatDate(row.item.start_date) }}
                                      </td>
                                      <td>
                                        {{ formatDate(row.item.end_date) }}
                                      </td>
                                      <td>
                                        {{ formatDate(row.item.end_date) }}
                                      </td>
                                      <td>
                                        <router-link :to="{ name: 'HRCourseDetail', params: { conduct_id: row.item.conduct_id }}">
                                        <v-btn depressed small color="#0062E4" @click="dialog = false">
                                          <span style="color: white">View Class</span> 
                                        </v-btn>
                                        </router-link>
    
                                      </td>
                                    </tr>
                                  </template>
                                </v-data-table>
                              </v-card-text>
                              <v-card-actions>
                                <v-btn color="primary" @click.stop="$set(selectedCourse, row.item.course_id, false)">Close</v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
      
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
        dialog: false, 

        selectedCourse: {},

        searchCourses: '',
        headersCourses: [
            { text: 'Course Name', value: 'title', align: 'start', sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        courses: [],
        trainers: [],

        searchEngineers: '',
        headersEngineers: [
            { text: 'Name', value: 'name', align: 'start', sortable: true},
            { text: 'Seniority Level', value: 'seniority_level', filterable: false, sortable: false},
        ],
        engineers: [],
        headersTrainers: [
            { text: 'Trainer', value: 'name', align: 'start', filterable: true, sortable: true},
            { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
            { text: 'Available', value: 'remaining', align: 'start', filterable: true, sortable: true},
            { text: 'Registration', value: 'end_register', align: 'start', filterable: true, sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ]
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
        },

        getCourseTrainer(course_id) {
          let updatedApiWithEndpoint = this.apiLink + "/retrievealltrainersconductingcourse";
          let dataObj = { 'courseId' : course_id};
          console.log(dataObj, course_id);
          axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
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
        this.getCoursesDetail();
        this.getEngineersDetail();


    }

  }
</script>

<style>

</style>