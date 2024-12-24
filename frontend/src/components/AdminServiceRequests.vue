<template>
  <div class="page-container">
    
    <div class="top-bar">
      <button class="btn-back" @click="goBackToDashboard">Back to Dashboard</button>
    </div>

    
    <h2 class="page-title">Service Requests</h2>

    
    <div class="table-wrapper">
      <table class="table table-bordered text-center">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer ID</th>
            <th>Professional ID</th>
            <th>Service Name</th>
            <th>Service Type ID</th>
            <th>Pincode</th>
            <th>Status</th>
            <th>Requested Date</th>
            <th>Completion Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in serviceRequests" :key="request.id">
            <td>{{ request.id }}</td>
            <td>{{ request.customer_id }}</td>
            <td>{{ request.professional_id }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.service_type_id }}</td>
            <td>{{ request.pin_code }}</td>
            <td>{{ request.status }}</td>
            <td>{{ request.requested_date }}</td>
            <td>{{ request.completion_date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      serviceRequests: []
    };
  },
  mounted() {
    this.fetchServiceRequests();
  },
  methods: {
    fetchServiceRequests() {
      
      const token = localStorage.getItem('token');
      
      if (!token) {
        console.error("No token found, user not authenticated");
        
        this.$router.push('/auth/login');
        return;
      }

      
      axios.get('http://127.0.0.1:5000/admin/admin_service_requests', {
        headers: {
          Authorization: `Bearer ${token}`  
        }
      })
        .then(response => {
          this.serviceRequests = response.data.service_requests;
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            
            console.error("Authentication failed. Redirecting to login.");
            this.$router.push('/auth/login');  
          } else {
            console.error("Error fetching service requests:", error);
          }
        });
    },
    goBackToDashboard() {
      this.$router.push('/admin/admin_home');
    }
  }
};
</script>

<style scoped>

.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background: linear-gradient(135deg, #f8fafc, #e3ebf0);
  min-height: 100vh;
}


.top-bar {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.btn-back {
  background-color: #4a90e2;
  color: #fff;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: 5px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.btn-back:hover {
  background-color: #357ab8;
}


.page-title {
  font-size: 2.5rem;
  color: #0056b3;
  margin: 20px 0;
  font-weight: bold;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
  text-align: center;
}


.table-wrapper {
  width: 90%;
  max-width: 1200px;
  margin-top: 20px;
  padding: 20px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
}


.table {
  width: 100%;
  margin-bottom: 0;
  background-color: #fff;
  border-radius: 8px;
}

.table th {
  background-color: #007bff;
  color: #fff;
  font-weight: bold;
  text-transform: uppercase;
  padding: 12px;
}

.table td {
  color: #555;
  padding: 12px;
  font-size: 1rem;
}

.table tbody tr:nth-child(even) {
  background-color: #f7f9fc;
}

.table tbody tr:hover {
  background-color: #e9f2fb;
}


@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }

  .btn-back {
    font-size: 0.9rem;
    padding: 8px 16px;
  }

  .table th,
  .table td {
    font-size: 0.9rem;
    padding: 8px;
  }
}
</style>


  