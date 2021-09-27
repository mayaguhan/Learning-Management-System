<template>
    <div>
        <v-card>
        <v-card-title>
        <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details></v-text-field>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        <v-spacer></v-spacer>
        </v-card-title>
        <v-data-table :headers="headers" :items="courses" :search="search">
        <template v-slot:item="row">
            <tr>
                <td>
                    {{row.item.course_code}} - {{row.item.title}} 
                </td>
                <td>
                    {{ row.item.current  }} / {{ row.item.capacity  }}
                </td>
                <td>
                    {{ row.item.start_date }}
                </td>
                <td>
                    {{ row.item.end_date }}
                </td>
                <td width="10">
                    <router-link :to="{ name: 'CourseDetail', params: { course_id: 1, trainer_id: 1 }}">
                        <v-btn depressed small color="#0062E4">
                            <span style="color: white">View Class</span> 
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
export default {
    name: 'TrainerCourses',
    data: () => ({
        courses: [],
        search: '',
        headers: [
            { text: 'Course Name', value: 'title', align: 'start', sortable: true},
            { text: 'Capacity', value: 'current', filterable: false, sortable: true},
            { text: 'Start Date', value: 'start_date', filterable: false, sortable: true},
            { text: 'End Date', value: 'end_date', filterable: false, sortable: true},
            { text: '', value: 'actions', filterable: false, sortable: false}
        ],
    }),

    methods: {
        getCoursesDetail() {
            // Get all Courses that are conducted by user_id
            // Dummy JSON, to be replaced with API call
            let data = [{
                "course_id": 1,
                "course_code": "PQ101",
                "title": "Print Quality Control I",
                "outline": "This course provide trainees with the basic skills and knowledge in setting up and operating a printing press and auxiliary equipment to produce quality printed products on papers and other materials as well as trouble shooting and maintenance of printing machines",
                "capacity": 20,
                "current": 2,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31",
                "trainer_id": 1
            },
            {
                "course_id": 2,
                "course_code": "PQ201",
                "title": "Print Quality Control II",
                "outline": "This course provide trainees with the intermediate skills and knowledge in setting up and operating a printing press and auxiliary equipment to produce quality printed products on papers and other materials as well as trouble shooting and maintenance of printing machines",
                "capacity": 15,
                "current": 1,
                "start_date": "2021-01-01",
                "end_date": "2021-12-31",
                "course_requirement": 1,
                "trainer_id": 1
            }];
            this.courses = data;

        },
    },
    created() {
        // Calls method to get course details
        this.getCoursesDetail();

    }
}
</script>

<style>

</style>