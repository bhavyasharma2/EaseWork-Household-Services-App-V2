<template>
  <div class="registration-requests-container">
    <div class="header">
      <button class="btn-back" @click="goBackToDashboard">Back to Dashboard</button>
    </div>
    <div class="registration-requests">
      <h2 class="title">New Professional Registration Requests</h2>
      <table class="requests-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Service</th>
            <th>Service Type</th>
            <th>Pin Code</th>
            <th>Documents</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="request in requests" :key="request.request_id">
            <td>{{ request.request_id }}</td>
            <td>{{ request.email }}</td>
            <td>{{ request.service_name }}</td>
            <td>{{ request.service_type_name }}</td>
            <td>{{ request.pin_code }}</td>
            <td>
              <button @click="viewDocument_new_reg(request.request_id)" class="btn-docs">
                Open Documents
              </button>
            </td>
            <td>
              <button @click="approveRegistration(request.request_id)" class="btn-action approve">
                Approve
              </button>
              <button @click="rejectRegistration(request.request_id)" class="btn-action reject">
                Reject
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  name: "NewRegistrationRequests",
  data() {
    return {
      requests: [],
    };
  },
  methods: {
    fetchRequests() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      axios
        .get("http://127.0.0.1:5000/admin/new_registration_requests", {
          headers: { Authorization: `Bearer ${token}` }  
        })
        .then((response) => {
          this.requests = response.data.registration_requests.map((request) => ({
            ...request,
            service_name: request.service_id,
            service_type_name: request.service_type_id,
          }));
        })
        .catch((error) => {
          console.error("Failed to fetch registration requests", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Access forbidden: Admins only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        });
    },
    viewDocument_new_reg(requestId) {
      
      this.$router.push({ name: 'NewRegViewDocument', params: { requestId } });
    },
    approveRegistration(requestId) {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      axios
        .post(`http://127.0.0.1:5000/admin/approve_registration/${requestId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }  
        })
        .then(() => {
          this.requests = this.requests.filter((request) => request.request_id !== requestId);
          alert("Registration approved successfully.");
        })
        .catch((error) => {
          console.error("Failed to approve registration", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Access forbidden: Admins only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        });
    },
    rejectRegistration(requestId) {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      axios
        .post(`http://127.0.0.1:5000/admin/reject_registration/${requestId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }  
        })
        .then(() => {
          this.requests = this.requests.filter((request) => request.request_id !== requestId);
          alert("Registration request rejected.");
        })
        .catch((error) => {
          console.error("Failed to reject registration", error);
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
    },
    goBackToDashboard() {
      this.$router.push('/admin/admin_home');
    }
  },
  mounted() {
    this.fetchRequests();
  },
};
</script>


<style scoped>
.registration-requests-container {
  background-color: #f9f9fb;
  padding: 20px;
  max-width: 1200px;
  margin: auto;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.btn-back {
  background-color: #2d8bfd;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-back:hover {
  background-color: #1e6dc2;
}

.registration-requests {
  text-align: center;
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
}

.requests-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
  border-radius: 8px;
  overflow: hidden;
}

.requests-table th,
.requests-table td {
  padding: 14px;
  text-align: center;
}

.requests-table th {
  background-color: #4a90e2;
  color: white;
  font-weight: bold;
}

.requests-table td {
  background-color: #fdfdfd;
  color: #333;
  border-bottom: 1px solid #e2e8f0;
}

.btn-docs {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-docs:hover {
  background-color: #2980b9;
}

.btn-action {
  padding: 8px 12px;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 14px;
  cursor: pointer;
  margin-right: 5px;
  transition: background-color 0.3s;
}

.approve {
  background-color: #27ae60;
}

.approve:hover {
  background-color: #219150;
}

.reject {
  background-color: #e74c3c;
}

.reject:hover {
  background-color: #c0392b;
}

.btn-docs:focus,
.btn-action:focus,
.btn-back:focus {
  outline: none;
  box-shadow: 0px 0px 5px 2px rgba(100, 100, 255, 0.3);
}

@media (max-width: 768px) {
  .requests-table th, .requests-table td {
    font-size: 12px;
    padding: 10px;
  }

  .title {
    font-size: 24px;
  }

  .btn-back {
    font-size: 12px;
    padding: 8px 12px;
  }
}
</style>

  