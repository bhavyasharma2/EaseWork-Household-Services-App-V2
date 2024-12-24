<template>
  <router-link to="/customers/customer_home">
    <button class="btn btn-secondary">Back to Dashboard</button>
  </router-link>
  <div class="service-history-container">
    <h1 class="page-title">Your Service Request History</h1>
    <div v-if="serviceRequests.length === 0" class="no-data-message">
      No service requests found.
    </div>
    <div v-else>
      <table class="service-history-table">
        <thead>
          <tr>
            <th>Service Request ID</th>
            <th>Professional Name</th>
            <th>Service ID</th>
            <th>Service Name</th>
            <th>Service Type ID</th>
            <th>Status</th>
            <th>Requested Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.professional_name }}</td>
            <td>{{ request.service_id }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.service_type_id }}</td>
            <td>{{ request.status }}</td>
            <td>{{ formatDate(request.requested_date) }}</td>
            <td>
              <button
                v-if="request.status === 'Pending' && !isBlocked"
                class="action-btn edit-btn"
                @click="goToEditServiceRequest(request.id)"
                :disabled="isBlocked"
              >
                Edit Service
              </button>
              <button
                v-if="request.status === 'Assigned' && !isBlocked"
                class="action-btn close-btn"
                @click="closeServiceRequest(request.id)"
                :disabled="isBlocked"
              >
                Close Service
              </button>
              <button
                v-if="request.status === 'Rejected' && !isBlocked"
                class="action-btn book-btn"
                @click="bookAnotherProfessional(request.id)"
                :disabled="isBlocked"
              >
                Book Another Professional or Service
              </button>
              <button
                v-if="request.status === 'Completed' && !isBlocked"
                class="action-btn review-btn"
                @click="serviceReview(request.id)"
                :disabled="isBlocked"
              >
                Submit Review for this Service
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div v-if="isBlocked" class="blocked-message">
      You are blocked/flagged by admin. You can only see your Closed Requests. You cannot Edit or Close a Service Request.
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      serviceRequests: [], 
      isBlocked: false, 
    };
  },
  methods: {
    async fetchServiceRequestHistory() {
      const token = localStorage.getItem("token");

      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      try {
        const response = await axios.get(
          "http://127.0.0.1:5000/customers/service_request_history",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.serviceRequests = response.data.service_requests;
        this.isBlocked = response.data.is_blocked; 
      } catch (error) {
        console.error("Error fetching service request history:", error);
        if (error.response && error.response.status === 403) {
          this.redirectToLogin("Unauthorized access. Customers only.");
        } else {
          alert("Failed to fetch service request history. Please try again.");
        }
      }
    },
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    goToEditServiceRequest(requestId) {
      this.$router.push(`/customers/edit_service_request/${requestId}`);
    },
    async closeServiceRequest(requestId) {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          `http://127.0.0.1:5000/customers/close_service/${requestId}`,
          {},
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        alert(response.data.message || "Service closed successfully.");
        this.fetchServiceRequestHistory(); 
      } catch (error) {
        console.error("Error closing service request:", error);
        alert("Failed to close service. Please try again.");
      }
    },
    bookAnotherProfessional() {
      this.$router.push(`/customers/available_services`);
    },
    serviceReview(requestId) {
      if (!requestId) {
        alert("Invalid service request. Cannot navigate to review form.");
        return;
      }

      
      this.$router.push({
        path: `/customers/service_review_form/${requestId}`,
        params: { requestId }, 
      });
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem("token");
      this.$router.push("/auth/login");
    },
  },
  async mounted() {
    await this.fetchServiceRequestHistory();
  },
};
</script>

  
  <style>
  .service-history-container {
    max-width: 1000px;
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
  
  .service-history-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }
  
  .service-history-table th,
  .service-history-table td {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
  }
  
  .service-history-table th {
    background-color: #007bff;
    color: white;
  }
  
  .action-btn {
    padding: 5px 10px;
    margin: 2px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  }
  
  .edit-btn {
    background-color: #ffc107;
    color: white;
  }
  
  .close-btn {
    background-color: #28a745;
    color: white;
  }
  
  .book-btn {
    background-color: #17a2b8;
    color: white;
  }
  
  .review-btn {
    background-color: #9d00ff;
    color: white;
  }
  
  .action-btn:hover {
    opacity: 0.9;
  }
  
  .no-data-message {
    text-align: center;
    font-size: 18px;
    color: #555;
    margin-top: 20px;
  }
  </style>
  