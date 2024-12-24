<template>
  <div class="container mt-5">
    
    <div class="text-center mb-5">
      <h1 class="display-4 text-primary font-weight-bold">Welcome to your Dashboard, Admin!</h1>
    </div>

    
    <div class="search-bar-container d-flex justify-content-center mb-4">
      <input
        type="text"
        v-model="searchQuery"
        class="form-control search-bar"
        placeholder="Search by function or professional name..."
      />
      <button @click="search" class="btn btn-search ml-2">Search</button>
    </div>

    
    <div class="list-group">
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToCustomerDetails">Customer Details</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToProfessionalDetails">Service Professional Details</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToServiceDetails">Services</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToServiceRequests">Service Requests</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToNewRegistrationRequests">New Service Professional Registration Requests</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToSummary">Summary</button>
      <button class="list-group-item list-group-item-action btn-dashboard mb-4" @click="goToEditProfile">Edit Profile</button>
      <button class="list-group-item list-group-item-action btn-logout mb-4" @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      searchQuery: '', 
      adminData: null 
    };
  },
  methods: {
    async search() {
      const query = this.searchQuery.trim().toLowerCase();
      const token = localStorage.getItem('token');

      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      
      switch (query) {
        case 'customer details':
          this.goToCustomerDetails();
          break;
        case 'service professional details':
          this.goToProfessionalDetails();
          break;
        case 'services':
          this.goToServiceDetails();
          break;
        case 'service requests':
          this.goToServiceRequests();
          break;
        case 'new service professional registration requests':
          this.goToNewRegistrationRequests();
          break;
        case 'summary':
          this.goToSummary();
          break;
        case 'edit profile':
          this.goToEditProfile();
          break;
        case 'logout':
          this.logout();
          break;
        default:
          await this.searchProfessionalByName(query, token);
      }
    },

    async searchProfessionalByName(query, token) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/admin/search_professional_by_name', {
          params: { query },
          headers: { Authorization: `Bearer ${token}` }
        });

        if (response.data.professionals.length) {
          this.$router.push({
            path: '/admin/professional_details',
            query: { searchResult: JSON.stringify(response.data.professionals) }
          });
        } else {
          alert("No professionals found with that name.");
        }
      } catch (error) {
        console.error("Error during search:", error);
        alert("An error occurred while searching.");
      }
    },

    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },

    goToCustomerDetails() {
      this.$router.push('/admin/customer_details');
    },

    goToProfessionalDetails() {
      this.$router.push('/admin/professional_details');
    },

    goToServiceDetails() {
      this.$router.push('/admin/service_details');
    },

    goToServiceRequests() {
      this.$router.push('/admin/admin_service_requests');
    },

    goToNewRegistrationRequests() {
      this.$router.push('/admin/new_registration_requests');
    },

    goToSummary() {
      this.$router.push('/admin/admin_statistics');
    },

    goToEditProfile() {
      this.$router.push('/admin/admin_edit_profile');
    },

    logout() {
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    }
  },

  async mounted() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.redirectToLogin("You are not logged in.");
      return;
    }

    
    try {
      const response = await axios.get('http://127.0.0.1:5000/admin/admin_home', {
        headers: { Authorization: `Bearer ${token}` }
      });

      
      this.adminData = response.data.message; 
      console.log("Admin Dashboard data:", this.adminData);
    } catch (error) {
      console.error("Failed to fetch dashboard data:", error);
      this.redirectToLogin("Session expired. Please log in again.");
    }
  }
};
</script>



<style scoped>
.container {
  background-color: #f8f9fa;
  border-radius: 15px;
  padding: 40px;
  box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.1);
  max-width: 85%;
  margin: auto;
}

h1 {
  font-family: 'Segoe UI', sans-serif;
  color: #004f8c;
  font-weight: 700;
  font-size: 2.5rem;
}

.search-bar-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 30px;
}

.search-bar {
  font-size: 1.2rem;
  padding: 12px 18px;
  border-radius: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 75%;
}

.btn-search {
  background-color: #17a2b8;
  color: #fff;
  padding: 12px 20px;
  font-size: 1rem;
  border-radius: 50px;
  transition: background-color 0.3s ease;
  margin-left: 10px;
}

.btn-search:hover {
  background-color: #138496;
}

.list-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.list-group-item {
  background-color: #007bff;
  color: #fff;
  font-size: 1.1rem;
  text-align: center;
  padding: 15px 30px;
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
  margin-bottom: 10px;
  transition: background-color 0.3s ease;
}

.list-group-item:hover {
  background-color: #0056b3;
  box-shadow: 0 6px 18px rgba(0, 123, 255, 0.4);
}

.btn-logout {
  background-color: #dc3545;
  color: white;
  font-size: 1.1rem;
  padding: 12px 30px;
  width: 100%;
  max-width: 400px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.btn-logout:hover {
  background-color: #c82333;
}

button {
  font-weight: 600;
  text-align: center;
}

@media (max-width: 768px) {
  .search-bar-container {
    width: 80%;
  }

  .list-group-item {
    font-size: 1rem;
    padding: 12px 25px;
    max-width: 100%;
  }
}
</style>









  