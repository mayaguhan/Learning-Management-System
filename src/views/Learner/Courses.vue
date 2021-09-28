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
            text: 'Title',
            align: 'start',
            sortable: false,
            value: 'name',
          },
          { text: 'Start Date', value: 'start_date' },
          { text: 'End Date', value: 'end_date' },
          { text: 'Capacity', value: 'capacity' },
          { text: '', value: 'action' }
        ],
        courses: [
          {
            name: 'Ink Changing Course',
            start_date: "12/3/2021",
            end_date: "20/3/2021",
            capacity: '12',
          },
          {
            name: 'Voltage Recognition Course',
            start_date: "15/3/2021",
            end_date: "15/4/2021",
            capacity: '11',
          },
          {
            name: 'Customer Relations Course',
            start_date: "12/1/2021",
            end_date: "20/1/2021",
            capacity: '16',
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