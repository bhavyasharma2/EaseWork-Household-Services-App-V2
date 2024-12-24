<template>
    <div class="signup-container">
      <div class="signup-form">
        <h1 class="heading">Customer Sign Up</h1>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="email">Email ID</label>
            <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Enter your email"
              required
              class="input-field"
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
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="fullName">Full Name</label>
            <input
              type="text"
              id="fullName"
              v-model="fullName"
              placeholder="Enter your full name"
              required
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="address">Address</label>
            <input
              type="text"
              id="address"
              v-model="address"
              placeholder="Enter your address"
              required
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="pinCode">Pin Code</label>
            <input
              type="text"
              id="pinCode"
              v-model="pinCode"
              placeholder="Enter your pin code"
              required
              class="input-field"
            />
          </div>
          <div class="form-group">
            <label for="mobile">Mobile Number</label>
            <input
              type="text"
              id="mobile_number"
              v-model="mobile_number" 
              placeholder="Enter your mobile number"
              required
              class="input-field"
            />
          </div>
          <button type="submit" class="submit-btn">Register</button>
        </form>
        <p class="login-link">
          Already have an account? <router-link to="/auth/login">Login here</router-link>
        </p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/axios';
  
  export default {
    data() {
      return {
        email: '',
        password: '',
        fullName: '', // change
        address: '', 
        pinCode: '', // change
        mobile_number: '',
      };
    },
    methods: {
      async handleRegister() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/register/register_customer', {
            email: this.email,
            password: this.password,
            full_name: this.fullName, //change
            address: this.address,
            pin_code: this.pinCode, // change
            mobile_number: this.mobile_number, // change
          });
          // Change
          if (response.status === 200 && response.data.msg === 'Customer registered successfully. Please log in.') {
            alert('Registration successful!');
            this.$router.push('/auth/login'); 
          } else {
            alert('Registration failed. Please try again.');
          }
        } catch (error) {
          console.error('Error during registration:', error);
          alert('Something went wrong. Please try again.');
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #007bff;
  }
  
  .signup-form {
    background-color: #ffffff;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 500px;
  }
  
  .heading {
    font-size: 2rem;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 1rem;
  }
  
  .form-group {
    margin-bottom: 1.5rem;
  }
  
  label {
    font-weight: 500;
    margin-bottom: 0.5rem;
    display: block;
  }
  
  .input-field {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1rem;
  }
  
  .input-field:focus {
    border-color: #5c6bc0;
    outline: none;
  }
  
  .submit-btn {
    width: 100%;
    padding: 0.8rem;
    background-color: #007bff;
    border: none;
    border-radius: 5px;
    color: white;
    font-size: 1.2rem;
    cursor: pointer;
  }
  
  .submit-btn:hover {
    background-color: #3f4f90;
  }
  
  .login-link {
    text-align: center;
    margin-top: 1.5rem;
    font-size: 1rem;
  }
  
  .login-link router-link {
    color: #5c6bc0;
    font-weight: bold;
  }
  </style>
  