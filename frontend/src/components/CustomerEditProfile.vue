<template>
  <router-link to="/customers/customer_home">
        <button class="btn btn-secondary">Back to Dashboard</button>
      </router-link>
    <div class="edit-profile-container">
      <h1 class="page-title">Edit Profile</h1>
      <form @submit.prevent="confirmChanges" class="profile-form">
        <div class="form-group">
          <label for="fullName">Full Name</label>
          <input
            v-model="customer.full_name"
            id="fullName"
            type="text"
            class="form-control"
            placeholder="Enter your full name"
            required
          />
        </div>
        <div class="form-group">
          <label for="address">Address</label>
          <textarea
            v-model="customer.address"
            id="address"
            class="form-control"
            placeholder="Enter your address"
            rows="2"
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="pinCode">Pin Code</label>
          <input
            v-model="customer.pin_code"
            id="pinCode"
            type="text"
            class="form-control"
            placeholder="Enter your pin code"
            required
          />
        </div>
        <div class="form-group">
          <label for="mobileNumber">Mobile Number</label>
          <input
            v-model="customer.mobile_number"
            id="mobileNumber"
            type="tel"
            class="form-control"
            placeholder="Enter your mobile number"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input
            v-model="customer.email"
            id="email"
            type="email"
            class="form-control"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            type="password"
            class="form-control"
            placeholder="Enter a new password (leave blank to keep current password)"
            @input="handlePasswordInput"
          />
        </div>
        <button type="submit" class="btn btn-primary">Confirm Changes</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from '@/axios';
  
  export default {
    data() {
      return {
        customer: {
          full_name: '',
          address: '',
          pin_code: '',
          mobile_number: '',
          email: '',
        },
        newPassword: '' 
      };
    },
    methods: {
      async fetchCustomerData() {
        const token = localStorage.getItem('token');
  
        if (!token) {
          this.redirectToLogin("You are not logged in.");
          return;
        }
  
        try {
          const response = await axios.get('http://127.0.0.1:5000/customers/customer_edit_profile', {
            headers: { Authorization: `Bearer ${token}` }
          });
  
          this.customer = response.data.customer;
        } catch (error) {
          console.error("Error fetching customer data:", error);
          this.redirectToLogin("Session expired or unauthorized access.");
        }
      },
      handlePasswordInput(event) {
        this.newPassword = event.target.value;
      },
      async confirmChanges() {
        const token = localStorage.getItem('token');
        const updatedCustomer = { ...this.customer };
  
        if (this.newPassword.trim() !== '') {
          updatedCustomer.password = this.newPassword;
        }
  
        try {
          const response = await axios.post(
            'http://127.0.0.1:5000/customers/customer_edit_profile',
            updatedCustomer,
            {
              headers: { Authorization: `Bearer ${token}` }
            }
          );
  
          alert(response.data.message || 'Profile updated successfully!');
          this.$router.push('/customers/customer_home'); 
        } catch (error) {
          console.error("Error updating profile:", error);
          alert(error.response?.data?.error || 'Failed to update profile.');
        }
      },
      redirectToLogin(message) {
        alert(message);
        localStorage.removeItem('token');
        this.$router.push('/auth/login');
      }
    },
    async mounted() {
      await this.fetchCustomerData();
    }
  };
  </script>
  
  <style>
  .edit-profile-container {
    max-width: 600px;
    margin: 50px auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .page-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 24px;
    color: #333;
  }
  
  .profile-form {
    display: flex;
    flex-direction: column;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    font-weight: bold;
    margin-bottom: 5px;
    display: block;
    color: #555;
  }
  
  .form-control {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 14px;
  }
  
  .btn {
    padding: 10px;
    background-color: #007bff;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  textarea {
    resize: none;
  }
  </style>
  
  