<template>
    <div>
        <v-tabs>
            <v-tab @click="allcourses = true; myprogress = false">All Courses</v-tab>
            <v-tab @click="myprogress = true; allcourses = false">My Progress</v-tab>
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
                            {{row.item.name}}
                        </td>
                        <td>
                            {{ row.item.category }}
                        </td>
                        <td>
                            {{ row.item.startdate }}
                        </td>
                        <td>
                            {{ row.item.enddate }}
                        </td>
                        <td>
                            {{ row.item.trainer }}
                        </td>
                        <td>
                           {{ row.item.capacity }} 
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
          <div v-if="myprogress">
            My Progress
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

        search: '',
        headers: [
          {
            text: 'Course Name',
            align: 'start',
            sortable: false,
            value: 'name',
          },
          { text: 'Category', value: 'category' },
          { text: 'Start Date', value: 'startdate' },
          { text: 'End Date', value: 'enddate' },
          { text: 'Trainer', value: 'trainer' },
          { text: 'Capacity', value: 'capacity' },
          { text: '', value: 'actions' }
        ],
        courses: [
          {
            name: 'Ink Changing Course',
            category: "Ink",
            startdate: "12/3/2021",
            enddate: "20/3/2021",
            trainer: "LeBron James",
            capacity: '23/40',
          },
          {
            name: 'Voltage Recognition Course',
            category: "Misc",
            startdate: "15/3/2021",
            enddate: "15/4/2021",
            trainer: "Guhan James",
            capacity: '23/40',
          },
          {
            name: 'Customer Relations Course',
            category: "Misc",
            startdate: "12/1/2021",
            enddate: "20/1/2021",
            trainer: "Yuquan Yeo",
            capacity: '10/40',
          },
        ],
      }
    },
    methods: {
        enrollCourse(item){
            var name = item.name
            alert(name);
        }
    }
  }
</script>

<style>

</style>