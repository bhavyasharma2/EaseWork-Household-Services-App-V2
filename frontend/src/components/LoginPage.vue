<template>
  <div class="login-container">
    <div class="login-box">
      <h1 class="title">EaseWork</h1>
      <p class="tagline">Connecting you to expert professionals to ease your work</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Enter your email"
            required
            class="form-control"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
            class="form-control"
          />
        </div>
        
        <button type="submit" class="btn btn-primary login-btn">Login</button>
        
        <div class="footer-links">
          <a @click="goToProfessionalRegister" class="link">Register as Service Professional</a>
          <a @click="goToCustomerRegister" class="link">Create Account</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: "LoginPage",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/auth/login', {
          email: this.email,
          password: this.password,
        });

        const { token, role } = response.data;
          
        localStorage.setItem("token", token); 

        
        switch (role) {
          case 'admin':
            this.$router.push('/admin/admin_home');
            break;
          case 'professional':
            this.$router.push('/professional/professional_home');
            break;
          case 'customer':
            this.$router.push('/customers/customer_home');
            break;
          default:
            alert('Unknown role. Please contact support.');
        }
      }catch (error) {
        console.error(error);
        alert('Login error');
      }
    },
    goToProfessionalRegister() {
      this.$router.push('/register/register_professional');
    },
    goToCustomerRegister() {
      this.$router.push('/register/register_customer');
    }
  }
};
</script>

  
  <style scoped>
  .login-container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background-color: #007bff;   
  }
  
  .login-box {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 400px;
  }
  
  .title {
    font-size: 2.5rem;
    font-weight: 700;
    color: #007bff;
    margin-bottom: 0.5rem;
  }
  
  .tagline {
    font-size: 1rem;
    color: #666;
    margin-bottom: 2rem;
  }
  
  .login-form .form-group {
    margin-bottom: 1.5rem;
    text-align: left;
  }
  
  .login-form label {
    display: block;
    font-weight: bold;
    color: #333;
  }
  
  .form-control {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }
  
  .login-btn {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .footer-links {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
  }
  
  .footer-links .link {
    font-size: 0.9rem;
    color: #007bff;
    cursor: pointer;
    text-decoration: none;
  }
  </style>
  