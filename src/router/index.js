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
    component: () =>import('../views/Learner/Courses.vue')
  },
  {
    path: '/singlecourse',
    name: 'SingleCourse',
    component: () =>import('../views/Learner/SingleCourse.vue')
  },


  {
    path: '/trainerCourses',
    name: 'TrainerCourses',
    component: () =>import('../views/Trainer/TrainerCourses.vue')
  },
  {
    path: '/trainerCourseDetail/:course_id/:trainer_id',
    name: 'CourseDetail',
    component: () =>import('@/views/Trainer/CourseDetail.vue'),
    props: true
  },
  {
    path: '/trainerEnrolledStudent/:course_id/:trainer_id',
    name: 'EnrolledStudent',
    component: () =>import('../views/Trainer/EnrolledStudent.vue'),
    props: true
  },
  {
    path: '/trainerQuizDetail/:section_id',
    name: 'QuizDetail',
    component: () =>import('../views/Trainer/QuizDetail.vue'),
    props: true
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
