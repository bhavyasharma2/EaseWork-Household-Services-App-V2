<template>
  <div class="container mt-5">
    
    <div class="top-bar">
      <button class="btn btn-primary back-button" @click="goBackToDashboard">Back to Dashboard</button>
    </div>

    
    <h2 class="text-center heading">Customer Details</h2>

    
    <div class="table-container">
      <table class="table table-bordered table-hover mx-auto" style="width: 90%;">
        <thead class="thead-custom">
          <tr>
            <th>ID</th>
            <th>Email</th>
            <th>Full Name</th>
            <th>Address</th>
            <th>Pincode</th>
            <th>Service Requests</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in customers" :key="customer.id">
            <td>{{ customer.id }}</td>
            <td>{{ customer.email }}</td>
            <td>{{ customer.full_name }}</td>
            <td>{{ customer.address }}</td>
            <td>{{ customer.pin_code }}</td>
            <td>{{ customer.service_request_count }}</td>
            <td>
              <button 
                v-if="!customer.is_blocked" 
                @click="toggleBlock(customer)" 
                class="btn btn-danger btn-block-action">Block</button>
              <button 
                v-if="customer.is_blocked" 
                @click="toggleBlock(customer)" 
                class="btn btn-success btn-block-action">Unblock</button>
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
      customers: []
    };
  },
  created() {
    this.fetchCustomerDetails();
  },
  methods: {
    async fetchCustomerDetails() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:5000/admin/customer_details', {
          headers: { Authorization: `Bearer ${token}` } 
        });
        console.log(response.data); 
        this.customers = response.data;
      } catch (error) {
        console.error('Error fetching customer details:', error);
        if (error.response && error.response.status === 403) {
          this.redirectToLogin("Access forbidden: Admins only.");
        } else {
          this.redirectToLogin("Session expired or invalid.");
        }
      }
    },
    toggleBlock(customer) {
      const token = localStorage.getItem('token');
      const url = customer.is_blocked
        ? `http://127.0.0.1:5000/admin/unblock_user/${customer.id}`
        : `http://127.0.0.1:5000/admin/block_user/${customer.id}`;

      axios.post(url, {}, {
        headers: { Authorization: `Bearer ${token}` }  
      })
      .then(response => {
        if (response.data.message) {
          customer.is_blocked = !customer.is_blocked;
        }
      })
      .catch(error => {
        console.error('Error blocking/unblocking user:', error);
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
  }
};
</script>


<style scoped>

.container {
  max-width: 1200px;
  padding: 20px;
  margin: auto;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}


.top-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}


.back-button {
  font-size: 1rem;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #0056b3;
  color: #fff;
}


.heading {
  font-size: 2.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
}


.table-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}


.table {
  width: 100%;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.thead-custom {
  background-color: #007bff;
  color: white;
}

.table th,
.table td {
  padding: 15px;
  text-align: center;
  font-size: 1rem;
  color: #333;
}

.table th {
  font-weight: bold;
}

.table-hover tbody tr:hover {
  background-color: #f2f4f6;
}


.btn-block-action {
  font-size: 0.9rem;
  padding: 8px 16px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.btn-block-action:hover {
  opacity: 0.9;
}


.btn-danger {
  background-color: #e3342f;
  color: white;
}

.btn-danger:hover {
  background-color: #cc1f1a;
}

.btn-success {
  background-color: #38c172;
  color: white;
}

.btn-success:hover {
  background-color: #2d995b;
}
</style>


  
  
  
  
  