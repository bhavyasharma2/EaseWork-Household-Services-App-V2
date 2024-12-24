import { createApp } from 'vue';
import App from './App.vue';
import router from './router';


const app = createApp(App);


router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  
  
  if (to.meta.requiresAuth && !token) {
    next('/auth/login'); 
  } else {
    next(); 
  }
});

app.use(router);
app.mount('#app');



