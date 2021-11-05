<template>
  <div>
    <v-tabs>
      <v-tab @click="allcourses = true; myprogress = false; inProgress = false; completed = false; myRequests = false">All Courses</v-tab>
      <v-tab @click="myprogress = true; allcourses = false; inProgress= true; completed = false; myRequests = false">My Progress</v-tab>
      <v-tab @click="myRequests= true; myprogress = false; allcourses = false; inProgress= false; completed = false">Requests</v-tab>
    </v-tabs>

    <v-tabs v-if="myprogress">
        <v-tab @click="inProgress = true; completed = false">In Progress</v-tab>
        <v-tab @click="completed = true; inProgress = false">Completed</v-tab>
    </v-tabs>

    <div>
    <!-- All Courses Content -->
      <div v-if="allcourses">
        <v-card>
          <v-card-title>
            <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
          </v-card-title>
          <v-data-table :headers="headersNotEnrolled" :items="coursesNotEnrolled" :search="search">
            <template v-slot:item="row">
              <tr>
                <td>
                  {{ row.item.course_code }} - {{ row.item.title }}
                </td>
                <td>
                  {{ row.item.cr_course_code }} - {{ row.item.cr_title }} 
                </td>
                <td>
                  {{ row.item.trainer_count }} 
                  <!-- {{row.item}} -->
                </td>
                <td width="10">
                  <!-- Enrol Course Dialog -->
                  <v-btn color="primary" :disabled="row.item.trainer_count == null || doesNotMeetReq(row.item.course_requisite_id)"
                  @click.stop="$set(selectedCourse, row.item.course_id, true), getCourseTrainer(row.item.course_id)">
                    View Trainers
                  </v-btn>
                  <v-dialog v-model="selectedCourse[row.item.course_id]" scrollable max-width="1200" :key="row.item.course_id">
                    <v-card>
                      <v-card-title>
                        <span>Enrol: {{ row.item.course_code }} - {{ row.item.title }}</span>
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
                                <v-btn depressed small color="#0062E4" 
                                @click="dialog = false, addEnrolment(row.item.conduct_id, row.item.name)">
                                  <span style="color: white">Enrol Class</span> 
                              </v-btn>
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

      <!-- My Progress Content -->
      <div v-if="inProgress">
        <v-data-table :headers="headersProgress" :items="coursesProgress">
          <template v-slot:item="row">
            <tr>
              <td>
                {{ row.item.course_code }} - {{ row.item.title }} 
              </td>
              <td>
                {{ row.item.name }}
              </td>
              <td>
                {{ formatDate(row.item.start_date) }}
              </td>
              <td>
                {{ formatDate(row.item.end_date) }}
              </td>
              <td>
                <v-progress-linear color="blue" rounded 
                  :value=" row.item.progress / row.item.section_count * 100 ">
                </v-progress-linear>
                {{ (row.item.progress / row.item.section_count * 100).toFixed(0) }}%  Completed
              </td>
              <td width="10">
                <router-link :to="{ name: 'SingleCourse', params: { conduct_id: row.item.conduct_id }}">
                  <v-btn depressed small color="#0062E4">
                      <span style="color: white">View Class</span> 
                  </v-btn>
                </router-link>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- Completed Content -->
      <div v-if="completed">
        <v-data-table :headers="headersCompleted" :items="coursesCompleted">
          <template v-slot:item="row">
            <tr>
              <td>
                {{ row.item.badge }} 
              </td>
              <td>
                {{ row.item.course_code }} - {{ row.item.title }} 
              </td>
              <td>
                {{ row.item.name }}
              </td>
              <td>
                {{ formatDate(row.item.start_date) }}
              </td>
              <td>
                {{ formatDate(row.item.end_date) }}
              </td>
              <td width="10">
                <router-link :to="{ name: 'SingleCourse', params: { conduct_id: row.item.conduct_id }}">
                  <v-btn depressed small color="#0062E4">
                      <span style="color: white">View Class</span> 
                  </v-btn>
                </router-link>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>

      <!-- My Requests Content -->

    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import moment from "moment";

  export default {
    name:"Courses",
    data () {
      return {
        currentUserId: 12, // To be replaced with user_id of logged in user

        allcourses: true,
        myprogress: false,
        inProgress: false,
        completed: false,
        myRequests: false,
        dialog: false, 
        search: '',

        coursesNotEnrolled: [],
        coursesProgress: [],
        coursesCompleted: [],
        trainers: [],
        
        selectedCourse: {},
        
        headersNotEnrolled: [
          { text: 'Course', value: 'title', align: 'start', sortable: true},
          { text: 'Requisite', value: 'cr_course_code'},
          { text: 'Trainers', value: 'trainer_count'},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        headersProgress: [
          { text: 'Course', value: 'title', align: 'start', sortable: true},
          { text: 'Trainer', value: 'name', sortable: true},
          { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
          { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
          { text: 'Progress', value: 'progress', filterable: false, sortable: true},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        headersCompleted: [
          { text: 'Badge', value: 'badge', align: 'start', filterable: false, sortable: false},
          { text: 'Course', value: 'title', sortable: true},
          { text: 'Trainer', value: 'name', sortable: true},
          { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
          { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
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
      // Get all Courses a User has not Enrolled In
      getCoursesNotEnrolledIn() {
        let updatedApiWithEndpoint = this.apiLink + "/getallcoursesauserhasnotenrolledin";
        let dataObj = { 'learnerId' : this.currentUserId};
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            this.coursesNotEnrolled = response.data.data;
          })
      },
      // Get all in-progress Courses a User has by learner_id
      getCoursesProgress() {
        let dataObj = { 'learnerId' : this.currentUserId};
        let updatedApiWithEndpoint = this.apiLink + "/getallcoursesauserhasbystatus";
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            this.coursesProgress = response.data.data;
          })
      },
      // Get all completed courses that a user has by learner id
      getCoursesCompleted() {
        let dataObj = { 'learnerId' : this.currentUserId};
        let updatedApiWithEndpoint = this.apiLink + "/getallcompletedcoursesbyuserid";
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            this.coursesCompleted = response.data.data;
          })
      },
      // Get all Self-Enrolment request by learner_id
      getSelfEnrolmentRequest() {
        let dataObj = { 'learnerId' : this.currentUserId};
        let updatedApiWithEndpoint = this.apiLink + "/getlearnerselfenrolmentrequests";
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            console.log(response.data.data);
            // TO DO: Display self-enrolment requests


          })
      },
      // Get all Trainers that are conducting a Course by course_id
      getCourseTrainer(course_id) {
        let updatedApiWithEndpoint = this.apiLink + "/gettrainersconductingacourse";
        let dataObj = { 'courseId' : course_id};
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            this.trainers = response.data.data;
          })
      },
      formatDate(date) {  
        return moment(date).format('yyyy-MM-DD HH:mm');
      },
      // Add new Enrolment
      addEnrolment(conduct_id, courseName) {
        let updatedApiWithEndpoint = this.apiLink + "/addnewenrolment";
        let dataObj = { "learner_id" : this.currentUserId, "conduct_id": conduct_id, "self_enrolment": 1, "status" : "Request" };
        axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
            console.log(response.data.code);
            if (response.data.code == 201) {
              this.getCoursesNotEnrolledIn();
              alert(`You have successfully submitted the enrollment request for ${courseName}'s class`);
            }
            else {
              alert("Sorry, you have already enrolled into the class");
            }
        })
        console.log(conduct_id);
      },
      doesNotMeetReq(course_requisite_id_para){
        if (course_requisite_id_para == null) {
          return false
        }
        for (let i = 0; i < this.coursesCompleted.length; i++) {
          if (course_requisite_id_para === this.coursesCompleted[i]["course_id"]){
            return false;
          }
          return true;
        }
      }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
      this.getCoursesNotEnrolledIn();
      this.getCoursesProgress();
      this.getCoursesCompleted();
      this.getSelfEnrolmentRequest()
    },
  }
</script>

<style>

</style>
