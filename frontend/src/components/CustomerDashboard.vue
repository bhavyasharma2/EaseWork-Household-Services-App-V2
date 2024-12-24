<template>
  <div class="dashboard-container">
    <h1 class="dashboard-heading">Welcome to EaseWork, Customer!</h1>
    <h4 v-if="customerData && customerData.is_blocked">You are blocked/flagged by admin. You cannot book any new service, see statistics or edit your profile. You can only see your Closed Requests.</h4>
    <div class="search-container">
      <input v-model="searchQuery" class="search-bar" placeholder="Search for services..." :disabled="customerData && customerData.is_blocked"/>
      <button @click="handleSearch" class="search-btn" :disabled="customerData && customerData.is_blocked">Search</button>
    </div>
    <div class="button-container">
      <button @click="goToAvailableServices" class="dashboard-btn" :disabled="customerData && customerData.is_blocked">List of Services Available</button>
      <button @click="goToServiceRequestHistory" class="dashboard-btn">Service Request History</button>
      <button @click="goToSummary" class="dashboard-btn" :disabled="customerData && customerData.is_blocked">Summary</button>
      <button @click="goToEditProfile" class="dashboard-btn" :disabled="customerData && customerData.is_blocked">Edit Profile</button>
      <button @click="logout" class="dashboard-btn logout-btn">Logout</button>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      searchQuery: '',
      customerData: null, 
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
        const response = await axios.get('http://127.0.0.1:5000/customers/customer_home', {
          headers: { Authorization: `Bearer ${token}` }
        });

        
        this.customerData = response.data;
        console.log("Customer Dashboard Data:", this.customerData);
      } catch (error) {
        console.error("Error fetching customer data:", error);

        if (error.response && error.response.status === 403) {
          this.redirectToLogin("Unauthorized access. Customers only.");
        } else {
          this.redirectToLogin("Session expired. Please log in again.");
        }
      }
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },
    goToAvailableServices() {
      this.$router.push('/customers/available_services');
    },
    goToServiceRequestHistory() {
      this.$router.push('/customers/service_request_history');
    },
    goToSummary() {
      this.$router.push('/customers/customer_statistics');
    },
    goToEditProfile() {
      this.$router.push('/customers/customer_edit_profile');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },
    handleSearch() {
      
      this.$router.push({ name: 'AvailableServices', query: { searchQuery: this.searchQuery } });
    }
  },
  async mounted() {
    const token = localStorage.getItem('token');
  
    
    if (!token) {
      this.redirectToLogin("You are not logged in.");
      return;
    }
    
    await this.fetchCustomerData();
  }
};
</script>


<style scoped>
.dashboard-container {
  text-align: center;
  padding: 20px;
}

.dashboard-heading {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
}

.search-container {
  margin-bottom: 30px;
}

.search-bar {
  padding: 10px;
  font-size: 16px;
  width: 300px;
}

.search-btn {
  padding: 10px 20px;
  margin-left: 10px;
  font-size: 16px;
}

.button-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 15px;
}

.dashboard-btn {
  padding: 15px 30px;
  font-size: 18px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-btn {
  background-color: #dc3545;
}

.dashboard-btn:hover {
  background-color: #0056b3;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>

