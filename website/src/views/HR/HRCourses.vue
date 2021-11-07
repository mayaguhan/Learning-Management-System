<template>
    <div>
        <v-tabs>
            <v-tab @click="allcourses=true, allengineers=false, allrequest=false">All Courses</v-tab>
            <v-tab @click="allcourses=false, allengineers=true, allrequest=false">Engineers</v-tab>
            <v-tab @click="allcourses=false, allengineers=false, allrequest=true">Requests</v-tab>
        </v-tabs>

        <div>
          <!-- All Courses Content -->
          <div v-if="allcourses">
            <v-card>
              <v-card-title>
                <v-text-field v-model="searchCourses" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
                <v-dialog v-model="courseDialog" persistent max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn class="primary ml-5" v-bind="attrs" v-on="on">
                      Add New Course
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="text-h5">Add New Course</span>
                    </v-card-title>
                    <v-card-text>
                      <v-form v-model="courseFormValid">
                        <v-text-field v-model="newCourseCode" counter :rules="[rules.required, rules.courseCode]" 
                        label="Course Code" maxlength="10"></v-text-field>

                        <v-text-field v-model="newTitle" counter :rules="[rules.required, rules.courseTitle]" 
                        label="Course Title" maxlength="100"></v-text-field>

                        <v-textarea v-model="newOutline" :rules="[rules.required, rules.courseOutline]" 
                        label="Course Outline" maxlength="500" filled auto-grow background-color="light-grey"></v-textarea>

                        <v-select v-model="newRequisite" :items="courses" :menu-props="{ top: true, offsetY: true }"
                          label="Courses" item-text="title" item-value="course_id"></v-select>

                        <v-file-input v-model="newBadge" prepend-icon="mdi-camera" 
                        accept="image/png, image/jpeg, image/bmp" label="Upload Badge Image" ></v-file-input>
                      </v-form>
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="blue darken-1" text @click="courseDialog=false">
                          Close
                      </v-btn>
                      <v-btn color="blue darken-1" text :disabled="!courseFormValid" @click="courseDialog=false, addNewCourse()">
                          Add
                      </v-btn>
                    </v-card-actions>
                  </v-card>
              </v-dialog>

              </v-card-title>
              <v-data-table :headers="headersCourses" :items="courses" :search="searchCourses">
                <template v-slot:item="row">
                    <tr>
                        <td>
                            {{row.item.course_code}} - {{row.item.title}} 
                        </td>
                        <td>
                          {{row.item.trainer_count}} 
                        </td>
                        <td>
                          {{row.item.trainer_all - row.item.trainer_count}} 
                        </td>
                        <td>
                          {{row.item.trainer_all}} 
                        </td>
                        <td>
                          {{getActiveStatus(row.item.active)}} 
                        </td>
                        <td width="10">
                          <!-- Enrol Course Dialog -->
                          <v-btn color="primary" @click.stop="$set(selectedCourse, row.item.course_id, true), getCourseTrainer(row.item.course_id)">
                            View Classes
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

                                <!-- Assign Trainer Dialog -->
                                <v-btn color="primary" @click.stop="$set(selectedAssign, row.item.course_id, true), getCourseAssign(row.item.course_id)">
                                  View Trainers Eligible To Teach
                                </v-btn>
                                <v-dialog v-model="selectedAssign[row.item.course_id]" scrollable max-width="1200" :key="row.item.course_id">
                                  <v-card>
                                    <v-card-title>
                                      {{ row.item.course_code }} - {{ row.item.title }}
                                    </v-card-title>
                                    <v-card-subtitle>
                                      Assign a Senior Engineer to teach this course
                                    </v-card-subtitle>
                                    <v-card-text>
                                      <!-- List of Trainers to Assign -->
                                      <v-data-table :headers="headersAssigns" :items="assigns">
                                        <template v-slot:item="assign">
                                          <tr>
                                            <td>
                                              {{ assign.item.name }} 
                                            </td>
                                            <td>
                                              {{ assign.item.email }} <br>
                                              {{ assign.item.contact }}
                                            </td>
                                            <td>
                                              <v-btn color="primary" @click.stop="$set(selectedTrainer, assign.item.user_id, true)">
                                                Assign Trainer
                                              </v-btn>
                                              <v-dialog persistent v-model="selectedTrainer[assign.item.user_id]" scrollable max-width="500" :key="assign.item.user_id">
                                                <v-card>
                                                  <v-card-title> 
                                                    Add New Class
                                                  </v-card-title>
                                                  <v-card-subtitle>
                                                    {{ assign.item.name }}'s {{ row.item.course_code }} - {{ row.item.title }}
                                                  </v-card-subtitle>
                                                  <v-card-text>
                                                    <v-form v-model="isFormValid">
                                                    <v-menu v-model="assignStartRegisterMenu">
                                                      <template v-slot:activator="{ on, attrs }">
                                                        <v-text-field v-model="assignStartRegister" prepend-icon="mdi-calendar" :rules="[rules.required, rules.currentDate]"
                                                        label="Registration Start Date" readonly v-bind="attrs" v-on="on"></v-text-field>
                                                      </template>
                                                      <v-date-picker v-model="assignStartRegister" @input="assignStartRegisterMenu = false"></v-date-picker>
                                                    </v-menu>

                                                    <v-menu v-model="assignEndRegisterMenu">
                                                      <template v-slot:activator="{ on, attrs }">
                                                        <v-text-field v-model="assignEndRegister" prepend-icon="mdi-calendar" :rules="[rules.required, rules.currentDate, rules.assignRegister]"
                                                        label="Registration End Date" readonly v-bind="attrs" v-on="on"></v-text-field>
                                                      </template>
                                                      <v-date-picker v-model="assignEndRegister" @input="assignEndRegisterMenu = false"></v-date-picker>
                                                    </v-menu>

                                                    <v-menu v-model="assignStartDateMenu">
                                                      <template v-slot:activator="{ on, attrs }">
                                                        <v-text-field v-model="assignStartDate" prepend-icon="mdi-calendar" :rules="[rules.required, rules.currentDate, rules.assignRegisterPeriod]"
                                                        label="Course Start Date" readonly v-bind="attrs" v-on="on"></v-text-field>
                                                      </template>
                                                      <v-date-picker v-model="assignStartDate" @input="assignStartDateMenu = false"></v-date-picker>
                                                    </v-menu>

                                                    <v-menu v-model="assignEndDateMenu">
                                                      <template v-slot:activator="{ on, attrs }">
                                                        <v-text-field v-model="assignEndDate" prepend-icon="mdi-calendar" :rules="[rules.required, rules.currentDate, rules.assignPeriod]"
                                                        label="Course End Date" readonly v-bind="attrs" v-on="on"></v-text-field>
                                                      </template>
                                                      <v-date-picker v-model="assignEndDate" @input="assignEndDateMenu = false"></v-date-picker>
                                                    </v-menu>

                                                    <v-text-field v-model="newCapacity" type="number" :rules="[rules.required, rules.capacityMin, rules.capacityMax]"
                                                    label="Capacity" hint="Maximum class size" suffix="learners"></v-text-field>
                                                  </v-form>
                                                  </v-card-text>
                                                  <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn color="blue darken-1" text @click="selectedTrainer[assign.item.user_id]=false">
                                                      Close
                                                    </v-btn>
                                                    <v-btn color="blue darken-1" text :disabled="!isFormValid" @click="assignTrainer(row.item.course_id, assign.item.user_id), selectedTrainer[assign.item.user_id]=false">
                                                      Confirm 
                                                    </v-btn>
  
                                                </v-card-actions>
                                                </v-card>
                                              </v-dialog>
                                            </td>
                                          </tr>
                                          </template>
                                        </v-data-table>
                                    </v-card-text>
                                  </v-card>
                                </v-dialog>

                                <!-- List of Trainers Conducting -->
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
                                        {{ row.item.enrolments }} / {{ row.item.capacity }}
                                      </td>
                                      <td>
                                        {{ formatDate(row.item.start_register) }} to <br>
                                        {{ formatDate(row.item.end_register) }}
                                      </td>
                                      <td>
                                        {{ formatDate(row.item.start_date) }} to <br>
                                        {{ formatDate(row.item.end_date) }}
                                      </td>
                                      <td>
                                        <span v-if="formatDate(new Date()) > formatDate(row.item.start_date) ">Started</span>
                                        <span v-else>Registration</span>
                                      </td>
                                      <td>
                                        <router-link :to="{ name: 'HRCourseDetail', params: { conduct_id: row.item.conduct_id }}">
                                        <v-btn class="primary">
                                          View Class
                                        </v-btn>
                                        </router-link>
                                      </td>
                                    </tr>
                                  </template>
                                </v-data-table>
                              </v-card-text>
                            </v-card>
                          </v-dialog>
                        </td>

                        <td>
                          <v-btn color="primary" @click.stop="$set(selectedEdit, row.item.course_id, true)">
                            Edit
                          </v-btn>

                          <v-dialog persistent v-model="selectedEdit[row.item.course_id]" scrollable max-width="800" :key="row.item.course_id">
                            <v-card>
                              <v-card-title>
                                Edit a Course
                              </v-card-title>
                              <v-card-text>
                                <v-form v-model="editFormValid">
                                  <v-text-field v-model="row.item.course_code" counter :rules="[rules.required, rules.courseCode]" 
                                  label="Course Code" maxlength="10"></v-text-field>

                                  <v-text-field v-model="row.item.title" counter :rules="[rules.required, rules.courseTitle]" 
                                  label="Course Title" maxlength="100"></v-text-field>

                                  <v-textarea v-model="row.item.outline" :rules="[rules.required, rules.courseOutline]" 
                                  label="Course Outline" maxlength="500" filled auto-grow background-color="light-grey"></v-textarea>

                                  <v-select v-model="row.item.course_requisite_id" :items="courses" :menu-props="{ top: true, offsetY: true }"
                                    label="Courses" item-text="course_requisite_id" item-value="course_requisite_id"></v-select>

                                  <v-switch v-model="row.item.active" inset ></v-switch>

                                  <v-file-input v-model="editBadge" prepend-icon="mdi-camera" 
                                  accept="image/png, image/jpeg, image/bmp" label="Upload Badge Image" ></v-file-input>
                                </v-form>
                              </v-card-text>
                              <v-card-actions>
                                <v-spacer></v-spacer>

                                <v-btn color="blue darken-1" text :disabled="!editFormValid" 
                                @click="selectedEdit[row.item.course_id]=false, editCourse(row.item), editBadge={}">
                                  Edit
                                </v-btn>
                                <v-btn color="blue darken-1" text @click="selectedEdit[row.item.course_id]=false, editBadge={}, getCoursesDetail(), forceRerender()">
                                  Close
                                </v-btn>
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
                <v-text-field v-model="searchEngineers" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
              </v-card-title>
              <v-data-table :headers="headersEngineers" :items="engineers" :search="searchEngineers">
                <template v-slot:item="row">
                  <tr>
                    <td>
                      {{row.item.name}}
                    </td>
                    <td>
                      {{ row.item.email }}<br>
                      {{ row.item.contact }}
                    </td>
                    <td>
                      {{ row.item.seniority_level }}
                    </td>
                  </tr>
                </template>
              </v-data-table>
            </v-card>
          </div>

          <!-- Self-Enrolment Requests -->
          <div v-if="allrequest">
            <v-card>
              <v-card-title>
                <v-text-field v-model="searchRequest" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
              </v-card-title>
              <v-data-table :headers="headersRequest" :items="requests" :search="searchRequest" >
                <template v-slot:item="row">
                    <tr>
                        <td>
                          {{ row.item.name }}
                        </td>
                        <td>
                          {{ row.item.contact }} <br>
                          {{ row.item.email }}
                        </td>
                        <td>
                          {{ row.item.seniority_level }}
                        </td>
                        <td>
                          {{ row.item.course_code }} - {{ row.item.title }} 
                        </td>
                        <td width="10">
                          <v-btn color="primary" @click.stop="$set(selectedRequest, row.item.learner_id+'|'+row.item.course_id, true)">
                            Action
                          </v-btn>

                          <v-dialog persistent v-model="selectedRequest[row.item.learner_id+'|'+row.item.course_id]" scrollable max-width="800" 
                            :key="row.item.learner_id+'|'+row.item.course_id">
                            <v-card>
                              <v-card-title>
                                {{ row.item.course_code }} - {{ row.item.title }} 
                              </v-card-title>
                              <v-card-subtitle>
                                {{ row.item.outline }}
                              </v-card-subtitle>
                              <v-card-text>
                                <table>
                                  <tr>
                                    <td>Learner Name: </td>
                                    <td>{{ row.item.name }}</td>
                                  </tr>
                                  <tr>
                                    <td>Learner Contact: </td>
                                    <td>{{ row.item.contact }} | {{ row.item.email }}</td>
                                  </tr>
                                  <tr>
                                    <td>Registration Period: </td>
                                    <td>{{ formatDate(row.item.start_register)}} - {{ formatDate(row.item.end_register)}}</td>
                                    
                                  </tr>
                                  <tr>
                                    <td>Course Period: </td>
                                    <td>{{ formatDate(row.item.start_date)}} - {{ formatDate(row.item.end_date)}}</td>
                                  </tr>
                                </table>
                                <v-text-field v-model="enrolmentRemarks" label="Remarks" maxlength="50" ></v-text-field>
                              </v-card-text>
                              <v-card-actions>
                                <v-btn class="success" @click="selfEnrolmentAction(row.item, 'Progress'), selectedRequest[row.item.learner_id+'|'+row.item.course_id]=false">
                                  Accept 
                                </v-btn>
                                <v-btn class="error" @click="selfEnrolmentAction(row.item, 'Reject'),  selectedRequest[row.item.learner_id+'|'+row.item.course_id]=false">
                                  Reject 
                                </v-btn>
                                <v-spacer></v-spacer>
                                <v-btn @click="selectedRequest[row.item.learner_id+'|'+row.item.course_id]=false, enrolmentRemarks=''">
                                  Close
                                </v-btn>
                              </v-card-actions>
                            </v-card>
                          </v-dialog>
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
        currentUserId: 1, // To be replaced with user_id of logged in user

        allcourses: true,
        allengineers: false,
        allrequest: false,

        selectedCourse: {},
        selectedAssign: {},
        selectedRequest: {},
        selectedTrainer: {},
        selectedEdit: {},
        selectedEditCopy: {},
        enrolmentRemarks: "",
        assignStartDate: "",
        assignEndDate: "",
        assignStartRegister: "",
        assignEndRegister: "",
        assignStartDateMenu: false,
        assignEndDateMenu: false,
        assignStartRegisterMenu: false,
        assignEndRegisterMenu: false,
        newCapacity: 10,
        courseDialog: false,
        courseFormValid: false,
        editFormValid: false,
        isFormValid: false,

        newRequisite: null,
        newCourseCode: "",
        newTitle: "",
        newOutline: "",

        newBadge: {},
        editBadge: {},
        componentKey: 0,

        courses: [],
        searchCourses: '',
        headersCourses: [
            { text: 'Course Name', value: 'title', align: 'start', sortable: true},
            { text: 'Open Classes', value: 'trainer_count', filterable: false, sortable: true},
            { text: 'Ongoing Classes', value: 'trainer_progress', filterable: false, sortable: true},
            { text: 'Total Classes', value: 'trainer_all', filterable: false, sortable: true},
            { text: 'Status', value: 'active', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],

        engineers: [],
        searchEngineers: '',
        headersEngineers: [
            { text: 'Name', value: 'name', align: 'start', sortable: true},
            { text: 'Contact Details', value: 'contact_details', sortable: false},
            { text: 'Seniority Level', value: 'seniority_level', filterable: false, sortable: false},
        ],
        
        trainers: [],
        headersTrainers: [
            { text: 'Trainer', value: 'name', align: 'start', sortable: true},
            { text: 'Contact Details', value: 'contact_details', sortable: false},
            { text: 'Enrolments', value: 'remaining', align: 'start', sortable: true},
            { text: 'Registration Period', value: 'end_register', align: 'start', sortable: true},
            { text: 'Class Period', value: 'start_date', sortable: true},
            { text: 'Class Status', value: 'actions', sortable: false},
            { text: '', value: 'actions', sortable: false}
        ],

        assigns: [],
        headersAssigns: [
            { text: 'Trainer', value: 'name', align: 'start', sortable: true},
            { text: 'Contact Details', value: 'contact_details', sortable: false},
            { text: '', value: 'actions', sortable: false}
        ],

        requests: [],
        searchRequest: '',
        headersRequest: [
            { text: 'Name', value: 'name', align: 'start', sortable: true},
            { text: 'Contact', value: 'email', filterable: false, sortable: false},
            { text: 'Seniority Level', value: 'seniority_level', filterable: false, sortable: true},
            { text: 'Course', value: 'course_code', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],

        rules: {
            required: value => !!value || 'Required.',
            currentDate: value => value >= this.formatDate(new Date()) || "You can't select a date in the past",
            assignRegister: value => value > this.assignStartRegister || "Your registration end date must be later than your start date",
            assignPeriod: value => value > this.assignStartDate || "Your class end date must be later than your start date",
            assignRegisterPeriod: value => value > this.assignEndRegister || "Your class start date must be after your class registration end date",
            capacityMin: value => value >= 10 || 'Class minimum capacity is 10',
            capacityMax: value => value <= 100 || 'Class capacity is capped at 100',
            courseCode: value => value.length <= 10 || 'Max Length is 10',
            courseTitle: value => value.length <= 100 || 'Max Length is 100',
            courseOutline: value => value.length <= 500 || 'Max Length is 500'
        },
      }
    },

    methods: {
        forceRerender() {
            this.componentKey += 1;
        },
        s3link(material_link) {
            let updatedS3WithEndpoint = this.s3Link + material_link;
            return updatedS3WithEndpoint;
        },
        getActiveStatus(active) {
          if (active == 1) {
            return "Active";
          } else {
            return "Inactive";
          }
        },
        // Get all Courses
        getCoursesDetail() {
            let updatedApiWithEndpoint1 = this.apiLink + "/getallcourses";
            axios.get(updatedApiWithEndpoint1)
            .then((response) => {
                this.courses = response.data.data;
            })
            .catch((error) => {
              console.log(error, "No courses found")
            })
        },

        // Get all Users
        getEngineersDetail() {
            let updatedApiWithEndpoint = this.apiLink + "/getusers";
            axios.get(updatedApiWithEndpoint)
            .then((response) => {
                this.engineers = response.data.data;
            })
            .catch((error) => {
              console.log(error, "No users found")
            })
          },

        // Get all Trainers that are conducting a Course by course_id
        getCourseTrainer(course_id) {
          let updatedApiWithEndpoint = this.apiLink + "/gettrainersconductingacourse";
          let dataObj = { 'courseId' : course_id};
          console.log(updatedApiWithEndpoint, dataObj);
          axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
              this.trainers = response.data.data;
          })
          .catch((error) => {
            if (error) {
              this.trainers = [];
            }
          })
          .catch((error) => {
            console.log(error, "No trainers found")
          })
        },

        // Get all Trainers eligible to teach a Course by course_id
        getCourseAssign(course_id) {
          let updatedApiWithEndpoint = this.apiLink + "/getalltrainerseligibletoteachacourse";
          let dataObj = { 'courseId' : course_id};
          axios.post(updatedApiWithEndpoint, dataObj)
          .then((response) => {
              this.assigns = response.data.data;
          })
          .catch((error) => {
            console.log(error, "No trainers found")
          })
        },

        // Add new Course Conduct
        assignTrainer(course_id, trainer_id) {
          let updatedApiWithEndpoint = this.apiLink + "/addcourseconduct";
          let dataObj = { "course_id" : course_id, "trainer_id": trainer_id, "capacity": this.newCapacity, 
                          "start_date" : this.assignStartDate, "end_date":  this.assignEndDate, 
                          "start_register": this.assignStartRegister, "end_register" : this.assignEndRegister };
          console.log(updatedApiWithEndpoint, dataObj)
          axios.post(updatedApiWithEndpoint, dataObj)
            .then((response) => {
                console.log(response.data.data)
                this.getCoursesDetail();
                this.forceRerender();
            })
          this.assignStartDate = '';
          this.assignEndDate = '';
          this.assignStartRegister = '';
          this.assignEndRegister = '';
          this.newCapacity = 10;
        },

        // Get all Self-Enrolment request
        getEnrolmentRequest() {
          let updatedApiWithEndpoint = this.apiLink + "/getallselfenrolmentrequest";
          axios.get(updatedApiWithEndpoint)
          .then((response) => {
              this.requests = response.data.data;
          })
          .catch((error) => {
            console.log(error, "No enrolments found")
          })
        },

        // Update Enrolment by learner_id and conduct_id
        selfEnrolmentAction(request, action) {
          console.log(request, action)
          let updatedApiWithEndpoint = this.apiLink + "/updateenrolment";
          let dataObj = { "learnerId" : request.learner_id, "conductId": request.conduct_id, "status" : action, "remarks": this.enrolmentRemarks };
          console.log(updatedApiWithEndpoint, dataObj)
          axios.put(updatedApiWithEndpoint, dataObj)
          .then((response) => {
              console.log(response.data.data)
              this.getEnrolmentRequest();
              this.forceRerender();
          })
          this.enrolmentRemarks = '';
        },

        uploadBadge(file, courseDataObj) {
            console.log(file, courseDataObj)

            // var nameWithExtension = file['name']
            // var extensionArray = file['type'].split("/")
            // var extension = extensionArray[1]

            // var indexOfExtension = nameWithExtension.indexOf(extension);
            // var name = nameWithExtension.slice(0, indexOfExtension-1)

            // var content = "";
            // var updatedApiWithEndpointM = this.apiLink + "/uploadfile";

            // let reader = new FileReader();
            // reader.readAsDataURL(file);
            // reader.onload = function () {
            //     content = reader.result.split(',')[1];
            //     let dataObj = {"courseId": courseDataObj.course_id.toString(),"fileName": name, 
            //                 "fileExtension": extension, "content": content };
            //     console.log(updatedApiWithEndpointM, dataObj);
            //     axios.post(updatedApiWithEndpointM, dataObj)
            //         .then((response) => {
            //             console.log(response.data)
            //             // courseDataObj['badge'] = response.data
            //             // this.updateCourse(courseDataObj)

            //         })
            // }
            // this.newBadge = {};
            this.editBadge = {};
        },

        // Add a Course
        addNewCourse() {
          let updatedApiWithEndpoint = this.apiLink + "/addacourse";
          let courseDataObj = { "course_requisite_id": this.newRequisite, "course_code" : this.newCourseCode, "title": this.newTitle, 
                          "outline": this.newOutline, "badge" : "placeholder", "active":  1 };
          console.log(updatedApiWithEndpoint, courseDataObj)
          axios.post(updatedApiWithEndpoint, courseDataObj)
            .then((response) => {
                console.log(response.data.data);
                if (this.newBadge.name != null) {
                  courseDataObj["course_id"] = response.data.data.course_id
                  this.uploadBadge(this.newBadge, courseDataObj);
                }
                this.getCoursesDetail();
                this.forceRerender();
            })
          this.newRequisite = 0;
          this.newCourseCode = "";
          this.newTitle = "";
          this.newOutline = "";
        },

        editCourse(course) {
          let courseDataObj = { "course_id" : course.course_id, "course_requisite_id": course.course_requisite_id, 
                                "course_code" : course.course_code, "title": course.title, "outline": course.outline,
                                "active": course.active };
          if (this.editBadge.name != null ) {
              this.uploadBadge(this.editBadge, courseDataObj);
          } else {
              courseDataObj['badge'] = course.badge;
              this.updateCourse(courseDataObj)
          }
        },

        // Update Course by course_id
        updateCourse(courseDataObj) {
          let updatedApiWithEndpoint = this.apiLink + "/updatecourse";
          console.log(updatedApiWithEndpoint, courseDataObj)
          axios.put(updatedApiWithEndpoint, courseDataObj)
          .then((response) => {
              console.log(response.data.data)


          })
        },

        formatDate(date) {  
            return moment(date).format('yyyy-MM-DD');
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

        // Calls method to get trainer details
        this.getEngineersDetail();

        // Calls method to get all self-enrolment requests
        this.getEnrolmentRequest();
    }
  }
</script>

<style>

</style>