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
                           {{ row.item.capacity }} slots left
                        </td>
                        <td width="10">
                            <v-btn
                                depressed
                                small
                                color="#0062E4"
                                @click="enrollCourse(row.item)"
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
          {
            title: 'Customer Support Course',
            start_date: "12/2/2021",
            end_date: "12/3/2021",
            capacity: 10
          },
          {
            title: 'Rotator Changing Course',
            start_date: "12/2/2021",
            end_date: "12/3/2021",
            capacity: 10
          },
          {
            title: 'Painting Course',
            start_date: "12/2/2021",
            end_date: "12/3/2021",
            capacity: 10
          },
          {
            title: 'Sales Course',
            start_date: "12/2/2021",
            end_date: "12/3/2021",
            capacity: 10
          },
        ],
        completedCourses: [
          {
            title: "Print Quality Control I",
            start_date: "12/2/2020",
            end_date: "12/3/2020",
            capacity: 10
          },
          {
            title: "Print Quality Control II",
            start_date: "12/3/2020",
            end_date: "12/4/2020",
            capacity: 10
          },
        ]
      }
    },
    methods: {
        enrollCourse(item){
            var title = item.title
            alert(title);
        }
    },

    created() {
            const axios = require('axios');
            axios.post(`https://wsphrnze6b.execute-api.us-east-1.amazonaws.com/beta/getallcoursesauserhasnotenrolledin`, {"learnerId" : "6"})
                .then((response) => {
                    console.log(response.data);
                    this.courses = response.data;

                    
                })

                .catch(function (error) {
                    //error
                    console.log(error);
                })

                .then(function () {
                    // console.log(response);
                    // console.log("GET Request complete")
                });
        },
  }
</script>

<style>

</style>