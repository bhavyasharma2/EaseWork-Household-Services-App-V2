<template>
    <div class="edit-service-request">
        <router-link to="/customers/customer_home">
        <button class="btn btn-secondary">Back to Dashboard</button>
      </router-link>
      <h2>Edit Service Request</h2>
      
      <form @submit.prevent="submitChanges">
        <div class="form-group">
          <label for="requested_date">Requested Date:</label>
          <input
            type="date"
            v-model="requestedDate"
            id="requested_date"
            class="form-control"
            :min="minDate"
          />
        </div>
  
        <button type="submit" class="btn btn-primary">
          Submit Changes
        </button>
      </form>
  
      
      <div v-if="message" :class="messageType" class="mt-3">
        {{ message }}
      </div>
    </div>
  </template>
  
  <script>
import axios from '@/axios'; 

export default {
  data() {
    return {
      requestedDate: '', 
      message: '', 
      messageType: '', 
    };
  },
  computed: {
    
    minDate() {
      return new Date().toISOString().split('T')[0];
    }
  },
  methods: {
    
    async submitChanges() {
      const serviceRequestId = this.$route.params.requestId; 

      try {
        const token = localStorage.getItem("token"); 

        if (!token) {
          alert('You need to be logged in to update a service request.');
          this.$router.push('/auth/login');
          return;
        }

        
        const response = await axios.put(
          `http://127.0.0.1:5000/customers/edit_service_request/${serviceRequestId}`,
          { requested_date: this.requestedDate },
          {
            headers: { Authorization: `Bearer ${token}` }, 
          }
        );

        this.message = response.data.message;
        this.messageType = 'text-success'; 
      } catch (error) {
        
        this.message = error.response?.data?.error || 'An error occurred';
        this.messageType = 'text-danger'; 
      }
    },
  },
  mounted() {
    
    const serviceRequest = this.$route.params.serviceRequest;
    if (serviceRequest && serviceRequest.requested_date) {
      this.requestedDate = serviceRequest.requested_date;
    }
  }
};
</script>

  
  <style scoped>
  .edit-service-request {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 5px;
    max-width: 400px;
    margin: auto;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  button {
    width: 100%;
  }
  
  .text-success {
    color: green;
  }
  
  .text-danger {
    color: red;
  }
  </style>
  
  
