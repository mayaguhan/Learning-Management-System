import Vue from 'vue';
import Vuex from 'vuex';


Vue.use(Vuex);



export default new Vuex.Store({
    state:{
        
        apiLink: "https://wsphrnze6b.execute-api.us-east-1.amazonaws.com/beta",
        userId: "",
        login: false,
        type: ""

    },
    mutations: { //synchronous way to update data
        setUserId(state, payload){
            state.userId = payload;
        },
        setLogin(state, payload){
            state.login = payload;
        },
        setType(state, payload){
            state.type = payload;
        },
    },
    actions: {},
    modules: {},
    getters: {
        getApiLink(state){
            return state.apiLink;
        },
        getUserId(state){
            return state.userId;
        },
        getLogin(state){
            return state.login;
        },
        getType(state){
            return state.type;
        }
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