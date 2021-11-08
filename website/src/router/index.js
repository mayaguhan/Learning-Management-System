import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import store from '../store.js'

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
    path: '/Login/:type',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    props: true
  },
  {
    path: '/adminlogin',
    name: 'AdminLogin',
    component: () => import('../views/AdminLogin.vue')
  },
  {
    path: '/learnercourses',
    name: 'LearnerCourses',
    component: () =>import('../views/Learner/Courses.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/trainercourses',
    name: 'TrainerCourses',
    component: () =>import('../views/Trainer/TrainerCourses.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/singlecourse/:conduct_id',
    name: 'SingleCourse',
    component: () =>import('@/views/Learner/SingleCourse.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/quiz/:section_id',
    name: 'Quiz',
    component: () =>import('@/views/Learner/Quiz.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/trainercoursedetail/:conduct_id',
    name: 'CourseDetail',
    component: () =>import('@/views/Trainer/CourseDetail.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/trainerquizdetail/:section_id/:conduct_id',
    name: 'QuizDetail',
    component: () =>import('../views/Trainer/QuizDetail.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/trainerenrolledstudent/:conduct_id',
    name: 'EnrolledStudent',
    component: () =>import('../views/Trainer/EnrolledStudent.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/hrcourses',
    name: 'HRCourses',
    component: () =>import('../views/HR/HRCourses.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },

  {
    path: '/hrcoursedetail/:conduct_id',
    name: 'HRCourseDetail',
    component: () =>import('../views/HR/HRCourseDetail.vue'),
    props: true,
    meta: {
      requiresAuth: true
    }
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.

    // console.log(store.getters.getLogin);
    if (!(store.getters.getLogin)) {
      console.log(store.getters.getLogin);
      next("/");
    } else {
      next() // go to wherever I'm going
    }
  } else {
    next() // does not require auth, make sure to always call next()!
  }
})

export default router
