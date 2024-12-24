<template>
  <div class="professional-dashboard">
    <header class="dashboard-header">
      <h1>Welcome to your Dashboard, Professional!</h1>
    </header>

    <div v-if="isBlocked" class="blocked-message">
      <p>You are blocked/flagged by the admin. You cannot access your statistics, edit your profile or accept/reject any service requests. You can only view your completed requests.</p>
    </div>

    <div class="dashboard-buttons">
      <button @click="goToServiceRequests" class="dashboard-btn">
        Service Requests
      </button>
      <button @click="goToSummary" class="dashboard-btn" :disabled="isBlocked">
        Summary
      </button>
      <button @click="goToEditProfile" class="dashboard-btn" :disabled="isBlocked">
        Edit Profile
      </button>
      <button @click="logout" class="dashboard-btn logout-btn">
        Logout
      </button>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      searchQuery: "",
      isBlocked: false, 
    };
  },
  async created() {
    await this.checkProfessionalAccess();
  },
  methods: {
    async checkProfessionalAccess() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }
      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/professional/professional_home",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.isBlocked = response.data.is_blocked; 
      } catch (error) {
        console.error("Access denied:", error);
        this.redirectToLogin("Access denied. Please log in again.");
      }
    },
    goToServiceRequests() {
      this.$router.push("/professional/prof_service_requests");
    },
    goToSummary() {
      this.$router.push("/professional/professional_statistics");
    },
    goToEditProfile() {
      this.$router.push("/professional/prof_edit_profile");
    },
    logout() {
      localStorage.removeItem("token");
      this.redirectToLogin("You have been logged out.");
    },
    redirectToLogin(message) {
      alert(message);
      this.$router.push("/auth/login");
    },
  },
};
</script>


<style scoped>
.professional-dashboard {
  font-family: "Arial", sans-serif;
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  max-width: 800px;
  margin: 50px auto;
  text-align: center;
}

.dashboard-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3e50;
  margin-bottom: 30px;
}

.search-bar {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  gap: 10px;
}

.search-input {
  width: 300px;
  padding: 10px;
  border: 2px solid #ced4da;
  border-radius: 5px;
}

.search-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3;
}

.dashboard-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.dashboard-btn {
  padding: 15px 25px;
  font-size: 1.2rem;
  color: white;
  background-color: #28a745;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.dashboard-btn:hover {
  background-color: #218838;
  transform: scale(1.05);
}

.logout-btn {
  background-color: #dc3545;
}

.logout-btn:hover {
  background-color: #c82333;
}
</style>


