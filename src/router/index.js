import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/exampleapicall',
    name: 'ExampleAPI',
    component: () => import('../views/ExampleRetrieveData.vue')
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/Login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/learnercourses',
    name: 'LearnerCourses',
    component: () =>import('../views/Learner/Courses.vue'),
    props: true
  },
  {
    path: '/trainercourses',
    name: 'TrainerCourses',
    component: () =>import('../views/Trainer/TrainerCourses.vue')
  },
  {
    path: '/singlecourse/:course_id/:learner_id',
    name: 'SingleCourse',
    component: () =>import('@/views/Learner/SingleCourse.vue'),
    props: true
  },
  {
    path: '/quiz/:section_id/:learner_id/:course_id/:trainer_id',
    name: 'Quiz',
    component: () =>import('@/views/Learner/Quiz.vue'),
    props: true
  },
  {
    path: '/trainercoursedetail/:course_id',
    name: 'CourseDetail',
    component: () =>import('@/views/Trainer/CourseDetail.vue'),
    props: true
  },
  {
    path: '/trainerenrolledstudent/:course_id',
    name: 'EnrolledStudent',
    component: () =>import('../views/Trainer/EnrolledStudent.vue'),
    props: true
  },
  {
    path: '/trainerquizdetail/:section_id',
    name: 'QuizDetail',
    component: () =>import('../views/Trainer/QuizDetail.vue'),
    props: true
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
