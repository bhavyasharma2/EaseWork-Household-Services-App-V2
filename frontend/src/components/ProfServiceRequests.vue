<template>
    <div class="prof-service-requests">
      <header class="page-header">
        <h1>Your Service Requests</h1>
        <button class="btn btn-primary" @click="goBackToDashboard">Back to Dashboard</button>
      </header>
  
      <div class="table-container">
        
        <h2>Services Requested</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Service Request ID</th>
              <th>Customer Name</th>
              <th>Requested Date</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in pendingRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.requested_date }}</td>
              <td>
                <button class="btn btn-success" @click="acceptRequest(request.id)" :disabled="isBlocked">Accept</button>
                <button class="btn btn-danger" @click="rejectRequest(request.id)" :disabled="isBlocked">Reject</button>
              </td>
            </tr>
          </tbody>
        </table>
  
        
        <h2>Services Assigned or Rejected</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Service Request ID</th>
              <th>Customer Name</th>
              <th>Requested Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in assignedRejectedRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.requested_date }}</td>
              <td>{{ request.status }}</td>
            </tr>
          </tbody>
        </table>
  
        
        <h2>Services Completed</h2>
        <table class="table">
          <thead>
            <tr>
              <th>Service Request ID</th>
              <th>Customer Name</th>
              <th>Requested Date</th>
              <th>Status</th>
              <th>Completion Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in completedRequests" :key="request.id">
              <td>{{ request.id }}</td>
              <td>{{ request.customer_name }}</td>
              <td>{{ request.requested_date }}</td>
              <td>{{ request.status }}</td>
              <td>{{ request.completion_date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/axios";
  
  export default {
    data() {
      return {
        pendingRequests: [],
        assignedRejectedRequests: [],
        completedRequests: [],
        isBlocked: false, 
      };
    },
    async created() {
      await this.fetchServiceRequests();
    },
    methods: {
      
      async fetchServiceRequests() {
        const token = localStorage.getItem("token");
  
        try {
          const response = await axios.get(
            "http://127.0.0.1:5000/professional/prof_service_requests",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          this.pendingRequests = response.data.pending_requests;
          this.assignedRejectedRequests = response.data.assigned_rejected_requests;
          this.completedRequests = response.data.closed_requests;
          this.isBlocked = response.data.is_blocked; 
        } catch (error) {
          console.error("Error fetching service requests:", error);
          alert("Failed to load service requests.");
        }
      },
  
      
      async acceptRequest(requestId) {
        const token = localStorage.getItem("token");
  
        try {
          await axios.get(
            `http://127.0.0.1:5000/professional/accept_request/${requestId}`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          alert("Request accepted successfully!");
          this.fetchServiceRequests();
        } catch (error) {
          console.error("Error accepting request:", error);
          alert("Failed to accept the request.");
        }
      },
  
      
      async rejectRequest(requestId) {
        const token = localStorage.getItem("token");
  
        try {
          await axios.get(
            `http://127.0.0.1:5000/professional/reject_request/${requestId}`,
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          alert("Request rejected successfully!");
          this.fetchServiceRequests();
        } catch (error) {
          console.error("Error rejecting request:", error);
          alert("Failed to reject the request.");
        }
      },
  
      
      goBackToDashboard() {
        this.$router.push("/professional/professional_home");
      },
    },
  };
  </script>
  
  <style scoped>
  .prof-service-requests {
    margin: 30px;
    font-family: "Arial", sans-serif;
  }
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .page-header h1 {
    font-size: 2rem;
    color: #2c3e50;
  }
  
  .table-container {
    margin-top: 20px;
  }
  
  h2 {
    color: #2c3e50;
    margin-bottom: 25px;
  }
  
  .table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 60px;
  }
  
  .table th, .table td {
    border: 1px solid #ddd;
    text-align: left;
    padding: 10px;
  }
  
  .table th {
    background-color: #f4f4f4;
    color: #333;
  }
  
  .table tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  
  .btn {
    padding: 10px 15px;
    font-size: 1rem;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  .btn-success {
    background-color: #27ae60;
    color: white;
  }
  
  .btn-danger {
    background-color: #e74c3c;
    color: white;
  }
  
  .btn-primary {
    background-color: #3498db;
    color: white;
  }
  
  .btn:hover {
    opacity: 0.9;
  }
  </style>
  
  