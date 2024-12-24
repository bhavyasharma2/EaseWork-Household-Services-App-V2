<template>
    <div class="book-service-container">
      <h1 class="book-service-heading">Book a Service</h1>
      <div class="book-form">
        <label for="service-date">Select Service Date:</label>
        <input type="date" id="service-date" v-model="serviceDate" class="input-field" />
        <button @click="confirmBooking" class="confirm-btn">Confirm Booking</button>
      </div>
      <router-link to="/customers/customer_home" class="back-btn">Back to Dashboard</router-link>
    </div>
  </template>
  
<script>
import axios from '@/axios';

export default {
  data() {
    return {
      serviceDate: '', 
    };
  },
  methods: {
    
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },

    
    async confirmBooking() {
      const { professionalId, serviceId } = this.$route.params;

      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin('You are not logged in. Please log in to book a service.');
        return;
      }

      if (!this.serviceDate) {
        alert('Please select a date for the service.');
        return;
      }

      try {
        const response = await axios.post(
          `http://127.0.0.1:5000/customers/book_service/${professionalId}/${serviceId}`,
          { requested_date: this.serviceDate },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        alert(response.data.message || 'Booking successful!');
        this.$router.push('/customers/customer_home'); 
      } catch (error) {
        console.error('Service booking failed:', error);

        if (error.response) {
          const status = error.response.status;
          const message = error.response.data.error || 'An error occurred. Please try again.';
          
          if (status === 401 || status === 403) {
            this.redirectToLogin(message);
          } else {
            alert(message);
          }
        } else {
          alert('Unable to book the service. Please try again later.');
        }
      }
    },
  },
};
</script>

  
  <style scoped>
  .book-service-container {
    padding: 20px;
  }
  
  .book-service-heading {
    font-size: 30px;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .book-form {
    text-align: center;
  }
  
  .input-field {
    padding: 10px;
    margin: 10px 0;
    font-size: 16px;
  }
  
  .confirm-btn {
    padding: 12px 24px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
  }
  
  .confirm-btn:hover {
    background-color: #0056b3;
  }
  
  .back-btn {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
  }
  
  .back-btn:hover {
    background-color: #0056b3;
  }
  </style>
  