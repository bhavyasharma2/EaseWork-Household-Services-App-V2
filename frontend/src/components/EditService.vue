<template>
  <div class="edit-service-container mt-5">
    <div class="header">
      <h2>Edit Service Details</h2>
    </div>

    
    <form @submit.prevent="updateService" class="edit-service-form">
      <div class="form-group">
        <label for="serviceName">Service Name</label>
        <input type="text" class="form-control" v-model="service.name" required placeholder="Enter service name">
      </div>
      <div class="form-group">
        <label for="timeRequired">Time Required (hrs)</label>
        <input type="number" class="form-control" v-model="service.time_required" required placeholder="e.g., 2">
      </div>
      <div class="form-group">
        <label for="price">Price (₹)</label>
        <input type="number" class="form-control" v-model="service.price" required placeholder="e.g., 500">
      </div>
      <div class="form-group">
        <label for="description">Description</label>
        <textarea class="form-control" v-model="service.description" required placeholder="Describe the service"></textarea>
      </div>
      <div class="form-group">
        <label for="newServiceTypes">Add a New Service Type</label>
        <input type="text" class="form-control" v-model="newServiceType" placeholder="Comma-separated service types (e.g., cleaning, maintenance)">
      </div>

      
      <button type="submit" class="btn btn-success confirm-btn">Confirm Changes</button>
    </form>

    
    <router-link to="/admin/service_details" class="btn btn-secondary back-btn">Back to Service Details</router-link>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      service: {
        id: null,
        name: '',
        time_required: '',
        price: '',
        description: '',
        service_types: []
      },
      newServiceType: ''
    };
  },
  mounted() {
    if (this.checkToken()) {
    this.fetchServiceDetails();
    }
  },
  methods: {
    
    checkToken() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return false;  
      }
      return true;  
    },
    fetchServiceDetails() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      const serviceId = this.$route.params.serviceId;
      axios
        .get(`http://127.0.0.1:5000/admin/service_details`, {
          headers: { Authorization: `Bearer ${token}` },
          params: { service_id: serviceId }
        })
        .then(response => {
          this.service = response.data.service;
        })
        .catch(error => {
          console.error("Error fetching service details:", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Access forbidden: Admins only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        });
    },
    updateService() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      const serviceId = this.$route.params.serviceId;
      const updatedService = {
        service_name: this.service.name,
        time_required: this.service.time_required,
        price: this.service.price,
        description: this.service.description,
        new_service_types: this.newServiceType.split(',').map(type => type.trim())
      };

      axios
        .post(`http://127.0.0.1:5000/admin/edit_service/${serviceId}`, updatedService, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          alert("Service updated successfully.");
          this.$router.push({ path: '/admin/service_details' });
        })
        .catch(error => {
          console.error("Error updating service:", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Access forbidden: Admins only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        });
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    }
  }
};
</script>


<style scoped>
.edit-service-container {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8fafc;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.header h2 {
  color: #444;
  text-align: center;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.edit-service-form {
  background-color: #fff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
  display: inline-block;
}

.form-control {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
}

textarea.form-control {
  resize: vertical;
}

.confirm-btn {
  width: 100%;
  padding: 0.75rem;
  font-size: 1.1rem;
  font-weight: 500;
  color: #fff;
  background-color: #28a745;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.3s;
}

.confirm-btn:hover {
  background-color: #218838;
}

.back-btn {
  display: block;
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  color: #555;
  text-align: center;
  margin-top: 1.25rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f8f9fa;
  text-decoration: none;
  transition: background-color 0.3s;
}

.back-btn:hover {
  background-color: #e2e6ea;
}
</style>

  