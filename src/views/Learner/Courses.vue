<template>
  <div>
    <v-tabs>
      <v-tab @click="allcourses = true; myprogress = false; inProgress = false; completed = false">All Courses</v-tab>
      <v-tab @click="myprogress = true; allcourses = false; inProgress= true; completed = false">My Progress</v-tab>
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
                <td width="10">
                  <!-- Enrol Course Dialog -->
                  <v-dialog v-model="dialog" max-width="1200px">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn color="primary" dark v-bind="attrs" v-on="on" @click="getCourseTrainer(row.item.course_id)">
                        View Trainers
                      </v-btn>
                    </template>
                    <v-card>
                      <v-card-title>
                        <span>Enrol: {{ row.item.course_code }} - {{ row.item.title }}</span>
                      </v-card-title>
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
                                {{ row.item.remaining  }} / {{ row.item.capacity  }}
                              </td>
                              <td>
                                {{ formatDate(row.item.start_register) }}
                              </td>
                              <td>
                                {{ formatDate(row.item.end_register) }} to 
                                {{ formatDate(row.item.start_date) }}
                              </td>
                              <td>
                                {{ formatDate(row.item.end_date) }}
                              </td>
                              <td>
                                <v-btn @click="dialog = false, addEnrolment(row.item.conduct_id)">
                                  Enrol Class
                              </v-btn>
                              </td>
                            </tr>
                          </template>
                        </v-data-table>
                      </v-card-text>
                    </v-card>
                  </v-dialog>
                  <!-- 
                  <router-link :to="{ name: 'SelfEnrol', params: { course_id: row.item.course_id }}">
                    <v-btn depressed small color="#0062E4">
                      <span style="color: white">Enrol</span> 
                    </v-btn>
                  </router-link> -->
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
    </div>
  </div>
</template>

<script>
  // import axios from 'axios';
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
        dialog: false, 
        search: '',

        coursesNotEnrolled: [],
        coursesProgress: [],
        coursesCompleted: [],
        trainers: [],
        
        headersNotEnrolled: [
          { text: 'Course', value: 'course_code', align: 'start', sortable: true},
          { text: 'Requisite', value: 'cr_course_code'},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        headersProgress: [
          { text: 'Course', value: 'course_code', align: 'start', sortable: true},
          { text: 'Trainer', value: 'name', sortable: true},
          { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
          { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
          { text: 'Progress', value: 'progress', filterable: false, sortable: true},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        headersCompleted: [
          { text: 'Badge', value: 'badge', align: 'start', filterable: false, sortable: false},
          { text: 'Course', value: 'course_code', sortable: true},
          { text: 'Trainer', value: 'name', sortable: true},
          { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
          { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
          { text: '', value: 'actions', filterable: false, sortable: false}
        ],
        headersTrainers: [
          { text: 'Trainer', value: 'name', align: 'start', filterable: true, sortable: true},
          { text: 'Contact Details', value: 'contact_details', filterable: false, sortable: false},
          { text: 'Capacity', value: 'remaining', align: 'start', filterable: true, sortable: true},
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
        // let updatedApiWithEndpoint = this.apiLink + "/getallcoursesauserhasnotenrolledin";
        // let dataObj = { 'learnerId' : this.currentUserId};
        // axios.post(updatedApiWithEndpoint, dataObj)
        //   .then((response) => {
        //     console.log(response.data);
        //     this.coursesNotEnrolled = response.data;
        //   })
        this.coursesNotEnrolled = [
          {
            "course_id": 1,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "trainer_count": 4,
            "course_requisite_id": null,
            "cr_course_code": null,
            "cr_title": null,
          },
          {
            "course_id": 9,
            "course_code": "203",
            "title": "Fundamentals of Xerox WorkCentre XXXX",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "trainer_count": 4,
            "course_requisite_id": 5,
            "cr_course_code": "X107",
            "cr_title": "X107 Title",
          },
        ];
      },
      // Get all in-progress Courses a User has by learner_id
      getCoursesProgress() {
        // let dataObj = { 'learnerId' : this.currentUserId};
        // let updatedApiWithEndpoint = this.apiLink + "/TBC";
        // axios.post(updatedApiWithEndpoint, dataObj)
        //   .then((response) => {
        //     console.log(response.data);
        //     this.coursesProgress = response.data;
        //   })
        this.coursesProgress = [
          {
            "conduct_id": 52,
            "course_id": 7,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "badge": "placeholder",
            "name": "Yeo Yu Quan",
            "progress": 0,
            "section_count": 3
          },
          {
            "conduct_id": 53,
            "course_id": 8,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "badge": "placeholder",
            "name": "Yeo Yu Quan",
            "progress": 1,
            "section_count": 3
          }
        ];
      },
      // Get all completed Courses User has by learner_id
      getCoursesCompleted() {
        // let dataObj = { 'learnerId' : this.currentUserId};
        // let updatedApiWithEndpoint = this.apiLink + "/TBC";
        // axios.post(updatedApiWithEndpoint, dataObj)
        //   .then((response) => {
        //     console.log(response.data);
        //     this.coursesCompleted = response.data;
        //   })
        this.coursesCompleted = [
          {
            "conduct_id": 46,
            "course_id": 1,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "badge": "placeholder",
            "name": "Yeo Yu Quan"
          },
          {
            "conduct_id": 47,
            "course_id": 2,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "badge": "placeholder",
            "name": "Yeo Yu Quan"
          },
          {
            "conduct_id": 48,
            "course_id": 3,
            "course_code": "X105",
            "title": "Fundamentals of Xerox WorkCentre 6515",
            "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a  printing press and auxiliary equipment to produce quality printed products on papers and other materials.",
            "badge": "placeholder",
            "name": "Yeo Yu Quan"
          },
        ];
      },
      // Get all Trainers that are conducting a Course by course_id
      getCourseTrainer(course_id) {
        // let updatedApiWithEndpoint = this.apiLink + "/retrievealltrainersconductingcourse";
        // let dataObj = { 'courseId' : course_id};
        // axios.post(updatedApiWithEndpoint, dataObj)
        //   .then((response) => {
        //     console.log(response.data);
        //   })
        console.log(course_id);
        this.trainers = [
          {
            "conduct_id": 46,
            "course_id": 1,
            "name": "Yeo Yu Quan",
            "email": "email",
            "capacity": 10,
            "start_date": "2021-11-01 00:00:00",
            "end_date": "2021-11-01 00:00:00",
            "start_register": "2021-11-01 00:00:00",
            "end_register": "2021-11-01 00:00:00",
            "enrolments": 1,
            "remaining": 10
          },
          {
            "conduct_id": 46,
            "course_id": 1,
            "name": "Yeo Yu Quan",
            "email": "email",
            "capacity": 10,
            "start_date": "2021-11-01 00:00:00",
            "end_date": "2021-11-01 00:00:00",
            "start_register": "2021-11-01 00:00:00",
            "end_register": "2021-11-01 00:00:00",
            "enrolments": 1,
            "remaining": 10
          },
        ];
        console.log(this.trainers);
      },
      formatDate(date) {  
        return moment(date).format('yyyy-MM-DD HH:mm');
      },
      // Add new Enrolment
      addEnrolment(conduct_id) {
        // let updatedApiWithEndpoint = this.apiLink + "/TBC";
        // let dataObj = { "learnerId" : this.currentUserId, "conductId": conduct_id, "selfEnrolment": 1, "status" : "New" };
        // axios.post(updatedApiWithEndpoint, dataObj)
        //   .then((response) => {
        //     console.log(response);
        //     // TO DO: Display successful enrolment
        // })
        console.log(conduct_id);
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
    },
  }
</script>

<style>

</style>