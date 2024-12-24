<template>
  <div class="service-details-container mt-5">
    
    <router-link to="/admin/admin_home" class="btn btn-secondary back-button">
      Back to Dashboard
    </router-link>
    
    <div class="header-section d-flex justify-content-between align-items-center mb-4">
      <h2 class="page-title">Service Details</h2>
    </div>

    
    <div class="table-responsive shadow">
      <table class="table table-hover table-striped">
        <thead>
          <tr>
            <th>ID</th>
            <th>Service Name</th>
            <th>Time Required</th>
            <th>Price</th>
            <th>Description</th>
            <th>Service Types</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in services" :key="service.id">
            <td>{{ service.id }}</td>
            <td>{{ service.name }}</td>
            <td>{{ service.time_required }} hrs</td>
            <td>₹{{ service.price }}</td>
            <td>{{ service.description }}</td>
            <td>
              <ul class="service-types-list">
                <li v-for="type in service.service_types" :key="type" class="service-type-item">{{ type }}</li>
              </ul>
            </td>
            <td class="action-buttons">
              <button @click="editService(service.id)" class="btn btn-edit">Edit</button>
              <button @click="deleteService(service.id)" class="btn btn-delete">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    
    <div class="add-service-section d-flex justify-content-center mt-4">
      <router-link to="/admin/add_service" class="btn btn-add-service">Add a New Service</router-link>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      services: []
    };
  },
  created() {
    this.fetchServices();
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

    
    async fetchServices() {
      if (!this.checkToken()) return;  

      const token = localStorage.getItem('token');

      try {
        const response = await axios.get("http://127.0.0.1:5000/admin/service_details", {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.services = response.data.services;
      } catch (error) {
        console.error("Error fetching services:", error);
        if (error.response && error.response.status === 401) {
          this.redirectToLogin("Session expired or invalid.");
        } else if (error.response && error.response.status === 403) {
          this.redirectToLogin("Access forbidden: Admins only.");
        } else {
          this.redirectToLogin("An error occurred. Please try again.");
        }
      }
    },

    
    editService(serviceId) {
      if (this.checkToken()) {
        this.$router.push({ name: "EditService", params: { serviceId: serviceId } });
      }
    },

    
    async deleteService(serviceId) {
      if (!this.checkToken()) return;

      if (!confirm("Are you sure you want to delete this service?")) return;

      const token = localStorage.getItem('token');

      try {
        await axios.delete(`http://127.0.0.1:5000/admin/delete_service/${serviceId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Service deleted successfully.");
        this.fetchServices();
      } catch (error) {
        console.error("Error deleting service:", error);
      }
    },

    
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem("token");  
      this.$router.push("/auth/login"); 
    },

    
    goBackToDashboard() {
      this.$router.push("/admin/admin_home");
    },
  },
};
</script>



<style scoped>
.service-details-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  position: relative; 
}

.header-section {
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.page-title {
  color: #343a40;
  font-size: 2rem;
  font-weight: bold;
  margin-top: 40px; 
}

.back-button {
  position: absolute;
  top: 20px; 
  right: 20px; 
  font-size: 1rem;
  font-weight: bold;
  padding: 10px 16px;
  color: #ffffff !important;
  background-color: #007bff;
  border: 2px solid #0056b3;
  border-radius: 6px;
  text-decoration: none;
  z-index: 10;
}

.back-button:hover {
  background-color: #0056b3;
  color: #ffffff;
  text-decoration: none;
  opacity: 0.9;
}

.table {
  background: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  margin-top: 20px;
}

.table-hover tbody tr:hover {
  background: #f1f5f9;
}

thead {
  background-color: #007bff;
  color: #fff;
  text-align: center;
}

td, th {
  text-align: center;
  vertical-align: middle;
  padding: 12px;
  font-size: 0.95rem;
}

.service-types-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
}

.service-type-item {
  background-color: #4e73df;
  color: #fff;
  font-size: 0.85rem;
  padding: 4px 8px;
  border-radius: 5px;
  display: inline-block;
  margin: 2px 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-edit {
  background-color: #ffc107;
  color: #212529;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
  margin-right: 5px;
}

.btn-delete {
  background-color: #dc3545;
  color: #fff;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
}

.btn-edit:hover, .btn-delete:hover {
  opacity: 0.85;
  cursor: pointer;
}

.add-service-section {
  margin-top: 20px;
}

.btn-add-service {
  background-color: #28a745;
  color: #fff;
  font-size: 1.1rem;
  font-weight: bold;
  padding: 10px 25px;
  border-radius: 8px;
  border: none;
}

.btn-add-service:hover {
  background-color: #218838;
  text-decoration: none;
}

</style>


  