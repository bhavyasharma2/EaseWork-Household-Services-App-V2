<template>
  <div class="available-services-container">
    <h1 class="available-services-heading">Available Services</h1>
    <table class="services-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Service Name</th>
          <th>Description</th>
          <th>Price</th>
          <th>Time Required</th>
          <th>Service Types</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in filteredServices" :key="service.id">
          <td>{{ service.id }}</td>
          <td>{{ service.name }}</td>
          <td>{{ service.description }}</td>
          <td>{{ service.price }}</td>
          <td>{{ service.time_required }}</td>
          <td>
            <select v-model="selectedServiceType[service.id]" :key="service.id">
              <option v-for="type in service.types" :key="type.id" :value="type.id">{{ type.type_name }}</option>
            </select>
          </td>
          <td>
            <button @click="bookProfessional(service.id)" class="action-btn">Book A Professional</button>
          </td>
        </tr>
      </tbody>
    </table>
    <router-link to="/customers/customer_home" class="back-btn">Back to Dashboard</router-link>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
data() {
  return {
    services: [],
    selectedServiceType: {},
    searchQuery: this.$route.query.searchQuery || '', 
  };
},
computed: {
  
  filteredServices() {
    return this.services.filter(service => 
      service.name.toLowerCase().includes(this.searchQuery.toLowerCase())
    );
  }
},
async mounted() {
  const token = localStorage.getItem('token');
  if (!token) {
    this.redirectToLogin('Session expired. Please log in again.');
    return;
  }

  try {
    const response = await axios.get('http://127.0.0.1:5000/customers/available_services', {
      headers: { Authorization: `Bearer ${token}` }
    });
    this.services = response.data.services;
  } catch (error) {
    console.error('Error fetching services:', error);
    alert('Failed to fetch services. Please try again later.');
    this.redirectToLogin('Session expired. Please log in again.');
  }
},
methods: {
  redirectToLogin(message) {
    alert(message);
    localStorage.removeItem('token');
    this.$router.push('/auth/login');
  },
  bookProfessional(serviceId) {
    const serviceTypeId = this.selectedServiceType[serviceId];
    if (!serviceTypeId) {
      alert('Please select a service type.');
      return;
    }
    this.$router.push({ name: 'AvailableProfessionals', params: { serviceId, serviceTypeId } });
  },
},
};
</script>


  <style scoped>
  .available-services-container {
    padding: 20px;
  }
  
  .available-services-heading {
    font-size: 30px;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .services-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }
  
  .services-table th,
  .services-table td {
    padding: 12px;
    text-align: left;
  }
  
  .services-table th {
    background-color: #f2f2f2;
  }
  
  .action-btn {
    padding: 8px 16px;
    background-color: #28a745;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .action-btn:hover {
    background-color: #218838;
  }
  
  .back-btn {
    display: inline-block;
    margin-top: 20px;
    padding: 10px 20px;
    background-color: #007bff;
    color: white;
    text-decoration: none;
    border-radius: 5px;
  }
  
  .back-btn:hover {
    background-color: #0056b3;
  }
  </style>
  
  