<template>
  <div class="container mt-5 professional-details-page">
    
    <div class="back-button">
      <button class="btn btn-primary" @click="goBackToDashboard">Back to Dashboard</button>
    </div>

    
    <h2 class="text-center mb-4">Service Professional Details</h2>

    
    <div class="card table-container">
      <table class="table table-bordered table-hover mx-auto" style="width: 95%;">
        <thead class="thead-dark">
          <tr>
            <th>ID</th>
            <th>Email ID</th>
            <th>Full Name</th>
            <th>Experience</th>
            <th>Service</th>
            <th>Service Type</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Service Requests</th>
            <th>Documents</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.email }}</td>
            <td>{{ professional.full_name }}</td>
            <td>{{ professional.experience }} years</td>
            <td>{{ professional.service_name }}</td>
            <td>{{ professional.service_type_name }}</td>
            <td>{{ professional.address }}</td>
            <td>{{ professional.pin_code }}</td>
            <td>{{ professional.service_request_count }}</td>
            <td>
              <button class="btn btn-info" @click="viewDocument(professional.id)">Open Document</button>
            </td>
            <td>
              <button 
                :class="professional.is_blocked ? 'btn btn-success' : 'btn btn-danger'"
                @click="toggleBlock(professional)">
                {{ professional.is_blocked ? 'Unblock' : 'Block' }}
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
  data() {
    return {
      professionals: [] 
    };
  },
  created() {
    this.fetchProfessionalDetails();
  },
  methods: {
    
    async fetchProfessionalDetails() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      const searchResult = this.$route.query.searchResult;
      if (searchResult) {
        
        this.professionals = JSON.parse(searchResult);
      } else {
        
        try {
          const response = await axios.get('http://127.0.0.1:5000/admin/professional_details', {
            headers: { Authorization: `Bearer ${token}` } 
          });
          this.professionals = response.data;
        } catch (error) {
          console.error("Error fetching professional details:", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Access forbidden: Admins only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        }
      }
    },

    
    async toggleBlock(professional) {
      const token = localStorage.getItem('token');
      const url = professional.is_blocked
        ? `http://127.0.0.1:5000/admin/unblock_user/${professional.id}`
        : `http://127.0.0.1:5000/admin/block_user/${professional.id}`;

      try {
        const response = await axios.post(url, {}, {
          headers: { Authorization: `Bearer ${token}` }  
        });
        if (response.data.message) {
          professional.is_blocked = !professional.is_blocked;
        }
      } catch (error) {
        console.error("Error updating block status:", error);
      }
    },

    
    viewDocument(userId) {
      this.$router.push({ name: 'ProfViewDocument', params: { userId } });
    },

    
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },

    
    goBackToDashboard() {
      this.$router.push('/admin/admin_home');
    }
  }
};
</script>



<style scoped>

.professional-details-page {
  background-color: #f9f9fb;
  padding: 40px 0;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}


.back-button {
  position: absolute;
  top: 20px;
  right: 30px;
}
.back-button .btn {
  font-size: 1rem;
  padding: 10px 20px;
  font-weight: bold;
}


h2 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #495057;
  text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 30px;
}


.table-container {
  background: white;
  border-radius: 10px;
  padding: 20px;
  width: 97%;
  max-width: 1230px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-top: 30px;
}


.table {
  border-collapse: collapse;
  width: 100%;
  font-size: 1rem;
}
thead {
  background-color: #343a40;
  color: white;
}
th, td {
  padding: 15px;
  text-align: center;
}
th {
  font-weight: bold;
}
tr:hover {
  background-color: #f1f1f1;
}


button {
  font-size: 0.9rem;
  padding: 8px 15px;
  border-radius: 4px;
  font-weight: bold;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
  transition: background-color 0.3s ease;
}
.btn-info:hover {
  background-color: #138496;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  transition: background-color 0.3s ease;
}
.btn-danger:hover {
  background-color: #c82333;
}

.btn-success {
  background-color: #28a745;
  color: white;
  transition: background-color 0.3s ease;
}
.btn-success:hover {
  background-color: #218838;
}


@media (max-width: 768px) {
  .professional-details-page {
    padding: 20px;
  }
  h2 {
    font-size: 2rem;
  }
  .back-button .btn {
    font-size: 0.9rem;
  }
}
</style>


  