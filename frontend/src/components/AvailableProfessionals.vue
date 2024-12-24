<template>
    <div class="professionals-container">
      <h1 class="professionals-heading">Following are the service professionals available in your area</h1>
  
      
      <table v-if="professionals.length > 0" class="professionals-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Full Name</th>
            <th>Mobile Number</th>
            <th>Experience</th>
            <th>Rating</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professional in professionals" :key="professional.id">
            <td>{{ professional.id }}</td>
            <td>{{ professional.full_name }}</td>
            <td>{{ professional.mobile_number }}</td>
            <td>{{ professional.experience }}</td>
            <td>{{ professional.rating }}</td>
            <td>
              <button @click="bookService(professional.id)" class="book-btn">Book</button>
            </td>
          </tr>
        </tbody>
      </table>
  
      
      <p v-else class="no-professionals">Sorry, no service professionals available in your area.</p>
  
      <router-link to="/customers/available_services" class="back-btn">Back to Available Services</router-link>
    </div>
  </template>
  
  <script>
  import axios from '@/axios';

  export default {
    data() {
      return {
        professionals: [],
      };
    },
    async mounted() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin('Session expired. Please log in again.');
        return;
      }

      const { serviceId, serviceTypeId } = this.$route.params;
      if (!serviceTypeId) {
        alert('Service Type is missing. Please try again.');
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/customers/available_professionals/${serviceId}?service_type_id=${serviceTypeId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        if (response.data.no_professionals) {
          alert('No professionals are available for this service type at the moment.');
        } else {
          this.professionals = response.data.professionals;
        }
      } catch (error) {
        console.error('Error fetching professionals:', error);
        alert('Failed to fetch professionals. Please try again later.');
      }
    },
    methods: {
      redirectToLogin(message) {
        alert(message);
        localStorage.removeItem('token');
        this.$router.push('/auth/login');
      },
      bookService(professionalId) {
        const { serviceId } = this.$route.params;
        this.$router.push({ name: 'BookService', params: { professionalId, serviceId } });
      },
    },
  };
</script>




  
  <style scoped>
  .professionals-container {
    padding: 20px;
  }
  
  .professionals-heading {
    font-size: 30px;
    text-align: center;
    margin-bottom: 30px;
  }
  
  .professionals-table {
    width: 100%;
    border-collapse: collapse;
  }
  
  .professionals-table th,
  .professionals-table td {
    padding: 12px;
    text-align: left;
  }
  
  .professionals-table th {
    background-color: #f2f2f2;
  }
  
  .book-btn {
    padding: 8px 16px;
    background-color: #28a745;
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 5px;
  }
  
  .book-btn:hover {
    background-color: #218838;
  }
  
  .no-professionals {
    text-align: center;
    font-size: 18px;
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
  
  