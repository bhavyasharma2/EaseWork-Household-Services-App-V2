<template>
  <div class="container mt-5">
    <div class="form-card">
      <h2 class="form-title">Add a New Service</h2>

      <form @submit.prevent="addNewService">
        <div class="form-group">
          <label for="serviceName">Service Name</label>
          <input type="text" class="form-control" v-model="newService.name" required>
        </div>
        <div class="form-group">
          <label for="timeRequired">Time Required (hrs)</label>
          <input type="number" class="form-control" v-model="newService.time_required" required>
        </div>
        <div class="form-group">
          <label for="price">Price (₹)</label>
          <input type="number" class="form-control" v-model="newService.price" required>
        </div>
        <div class="form-group">
          <label for="description">Description</label>
          <textarea class="form-control" v-model="newService.description" required></textarea>
        </div>
        <div class="form-group">
          <label for="serviceTypes">Service Types (Comma Separated)</label>
          <input type="text" class="form-control" v-model="serviceTypes" placeholder="Type names separated by commas">
        </div>

        
        <button type="submit" class="btn btn-primary submit-btn mt-4">Add Service</button>
      </form>

      
      <router-link to="/admin/service_details" class="btn btn-secondary back-btn mt-3">Back to Service Details</router-link>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      newService: {
        name: '',
        time_required: '',
        price: '',
        description: ''
      },
      serviceTypes: ''
    };
  },
  methods: {
    addNewService() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      const serviceData = {
        service_name: this.newService.name,
        time_required: this.newService.time_required,
        price: this.newService.price,
        description: this.newService.description,
        service_types: this.serviceTypes.split(',').map(type => type.trim())
      };

      axios
        .post('/admin/add_service', serviceData, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          alert("New service added successfully.");
          this.$router.push('/admin/service_details');
        })
        .catch(error => {
          console.error("Error adding new service:", error);
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
.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.form-card {
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
  padding: 40px;
  width: 100%;
}

.form-title {
  text-align: center;
  font-size: 1.8em;
  color: #333333;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  font-weight: 500;
  color: #666666;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.2s ease;
}

input[type="text"]:focus,
input[type="number"]:focus,
textarea:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.submit-btn {
  background-color: #007bff;
  color: #ffffff;
  border: none;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: 500;
  width: 100%;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.back-btn {
  display: inline-block;
  margin-top: 1rem;
  text-align: center;
  color: #555;
  font-weight: 500;
  padding: 12px 20px;
  background-color: #e2e6ea;
  border-radius: 8px;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.back-btn:hover {
  background-color: #cfd4d8;
}

.mt-3 {
  margin-top: 1rem;
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>

  