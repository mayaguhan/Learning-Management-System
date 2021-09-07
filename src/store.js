import Vue from 'vue';
import Vuex from 'vuex';


Vue.use(Vuex);



export default new Vuex.Store({
    state:{
        //

    },
    mutations: { //synchronous way to update data
        // setLogin(state, payload){
        //     state.login = payload;
        // },
    },
    actions: {},
    modules: {},
    getters: {
        // getLogin(state){
        //     return state.login;
        // },
        // getMessage(state){
        //     return state.message;
        // }
    }
})


// To access the state variables in components
//  import { mapState } from 'vuex';
//         ...mapState({
//     user: (state) =>state.user
// })