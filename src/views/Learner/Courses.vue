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
                :items="courses"
                :search="search"
              >
                <template v-slot:item="row">
                    <tr>
                        <td>
                            {{row.item.title}}
                        </td>
                        <td>
                            {{ row.item.start_date }}
                        </td>
                        <td>
                            {{ row.item.end_date }}
                        </td>
                        <td>
                           {{ row.item.remaining }} slots left
                        </td>
                        <td width="10">
                            <v-btn
                                depressed
                                small
                                color="#0062E4"
                                @click="enrollCourse(row.item)"
                                v-if="row.item.remaining !== 0"
                            >
                                <span style="color: white">Enroll</span> 
                            </v-btn>
                        </td>
                    </tr>
                </template>
              </v-data-table>
            </v-card>
          </div>

          <!-- My Progress Content -->
          <div v-if="inProgress">
            <template>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">
                        Title
                      </th>
                      <th class="text-left">
                        Start Date
                      </th>
                      <th class="text-left">
                        End Date
                      </th>
                      <th class="text-left">
                        
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="item in progressCourses"
                      :key="item.title"
                    >
                      <td>{{ item.title }}</td>
                      <td>{{ item.start_date }}</td>
                      <td>{{ item.end_date }}</td>
                      <td width="10">
                          <router-link :to="{ name: 'SingleCourse', params: { course_id: 1, learner_id: 1 }}">
                              <v-btn depressed small color="#0062E4">
                                  <span style="color: white">View Class</span> 
                              </v-btn>
                          </router-link>
                      </td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </template>
          </div>

          <!-- Completed Content -->
          <div v-if="completed">
            <template>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th class="text-left">
                        Title
                      </th>
                      <th class="text-left">
                        Start Date
                      </th>
                      <th class="text-left">
                        End Date
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="item in completedCourses"
                      :key="item.title"
                    >
                      <td>{{ item.title }}</td>
                      <td>{{ item.start_date }}</td>
                      <td>{{ item.end_date }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </template>
          </div>

        </div>
    </div>
</template>

<script>
  export default {
    name:"Courses",
    data () {
      return {
        allcourses: true,
        myprogress: false,
        inProgress: false,
        completed: false,
        learner_id: 6,

        search: '',
        headers: [
          {
            text: 'Title',
            align: 'start',
            sortable: false,
            value: 'title',
          },
          { text: 'Start Date', value: 'start_date' },
          { text: 'End Date', value: 'end_date' },
          { text: 'Capacity', value: 'capacity' },
          { text: '', value: 'action' }
        ],
        courses: [
          
        ],
        progressCourses: [
          
        ],
        completedCourses: [
          
        ]
      }
    },
    methods: {
        enrollCourse(item){
            //console.log(item);
            var title = item.title;
            alert(title);

            /* // Insert API Call
            var dataObjEnroll = {
              'learnerId' : "7",
              'courseId' : item.course_id,
              'trainerId' : "3",
              'status' : "Progress"
            }
            //console.log(dataObjEnroll);
            const axios = require('axios');
            var updatedApiWithEndpoint = this.apiLink + "/getallcoursesauserhasnotenrolledin";
            axios.post(updatedApiWithEndpoint, dataObjEnroll)
                .then((response) => {
                  console.log(response.data);
                }) */
        }
    },
    computed: {
        apiLink(){
            return this.$store.state.apiLink;
        }
    },
    created() {
            // Simulate login
            var dataObj = {
              'learnerId' : "7"
            };
            var dataObjForProgress = {
                'learnerId' : "7",
                'status' : 'Progress'
            };
            var dataObjForComplete = {
                "learnerId" : 7,
                "status" : "Complete"
            };

            const axios = require('axios');
            var updatedApiWithEndpoint = this.apiLink + "/getallcoursesauserhasnotenrolledin";
            axios.post(updatedApiWithEndpoint, dataObj)
                .then((response) => {
                  //console.log(response.data);
                  let courseArray = response.data;
                  for (let index = 0; index < courseArray.length; index++) {
                    const courseObj = courseArray[index];
                    courseObj.start_date = courseObj.start_date.slice(0, -14);
                    courseObj.end_date = courseObj.end_date.slice(0, -14);
                  }
                  this.courses = response.data;
                })
            
            var updatedApiWithEndpoint2 = this.apiLink + "/getallcoursesauserhasbystatus";
            axios.post(updatedApiWithEndpoint2, dataObjForProgress)
                .then((response) => {
                  //console.log(response.data);
                  let courseArray = response.data;
                    for (let index = 0; index < courseArray.length; index++) {
                      const courseObj = courseArray[index];
                      courseObj.start_date = courseObj.start_date.slice(0, -14);
                      courseObj.end_date = courseObj.end_date.slice(0, -14);
                    }
                  this.progressCourses = response.data;
                })

            var updatedApiWithEndpoint3 = this.apiLink + "/getallcoursesauserhasbystatus";
            axios.post(updatedApiWithEndpoint3, dataObjForComplete)
                .then((response) => {
                  //console.log(response.data);
                  let courseArray = response.data;
                    for (let index = 0; index < courseArray.length; index++) {
                      const courseObj = courseArray[index];
                      courseObj.start_date = courseObj.start_date.slice(0, -14);
                      courseObj.end_date = courseObj.end_date.slice(0, -14);
                    }
                  this.completedCourses = response.data;
                })
            
    },
  }
</script>

<style>

</style>