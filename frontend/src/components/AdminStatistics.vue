<template>
  <router-link to="/admin/admin_home" class="btn btn-secondary back-button">
      Back to Dashboard
    </router-link>
  <div class="container mt-5">
    <div class="text-center mb-4">
      <h1 class="text-primary font-weight-bold">Admin Statistics</h1>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4">
        <h4 class="text-center">Distribution of Professionals based on Rtings</h4>
        <canvas id="ratingChart"></canvas>
      </div>
      <div class="col-md-6 mb-4">
        <h4 class="text-center">Distribution of Service Requests by Services</h4>
        <canvas id="serviceRequestChart"></canvas>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 mb-4">
        <h4 class="text-center">Distribution of Customers by Pincode</h4>
        <canvas id="customerPincodeChart"></canvas>
      </div>
      <div class="col-md-6 mb-4">
        <h4 class="text-center">Distrubution of Service Requests by Status</h4>
        <canvas id="statusChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';
import { Chart, registerables } from 'chart.js';


Chart.register(...registerables);

export default {
  data() {
    return {
      professionalRatings: [],
      serviceRequestsByName: [],
      customersByPincode: [],
      serviceRequestsByStatus: [],
    };
  },
  mounted() {
    this.fetchStatisticsData();
  },
  methods: {
    async fetchStatisticsData() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      try {
        const response = await axios.get(
          'http://127.0.0.1:5000/admin/admin_statistics',
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        console.log("Statistics data fetched:", response.data);
        this.professionalRatings = response.data.professional_ratings;
        this.serviceRequestsByName = response.data.service_requests_by_name;
        this.customersByPincode = response.data.customers_by_pincode;
        this.serviceRequestsByStatus = response.data.service_requests_by_status;
        this.renderCharts();
      } catch (error) {
        console.error("Error fetching statistics data:", error);
        if (error.response && error.response.status === 403) {
          this.redirectToLogin("Access forbidden: Admins only.");
        } else {
          this.redirectToLogin("Session expired or invalid.");
        }
      }
    },
    renderCharts() {
      console.log("Rendering charts...");

      
      const ratingData = {
        labels: ['Rating >= 4', 'Rating 3-2', 'Rating < 2'],
        datasets: [
          {
            label: 'Number of Professionals',
            data: [
              this.professionalRatings.filter((rating) => rating.rating >= 4).length,
              this.professionalRatings.filter((rating) => rating.rating >= 2 && rating.rating < 4).length,
              this.professionalRatings.filter((rating) => rating.rating < 2).length,
            ],
            backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
          },
        ],
      };

      const ratingChart = document.getElementById('ratingChart');
      if (ratingChart) {
        new Chart(ratingChart, {
          type: 'pie',
          data: ratingData,
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => tooltipItem.raw + ' Professionals',
                },
              },
            },
          },
        });
      }

      
      const serviceRequestData = {
        labels: this.serviceRequestsByName.map((item) => item.name),
        datasets: [
          {
            label: 'Number of Service Requests',
            data: this.serviceRequestsByName.map((item) => item.request_count),
            backgroundColor: '#007bff',
          },
        ],
      };

      const serviceRequestChart = document.getElementById('serviceRequestChart');
      if (serviceRequestChart) {
        new Chart(serviceRequestChart, {
          type: 'bar',
          data: serviceRequestData,
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true },
            },
            plugins: {
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => tooltipItem.raw + ' Requests',
                },
              },
            },
          },
        });
      }

      
      const pincodeData = {
        labels: this.customersByPincode.map((item) => item.pin_code),
        datasets: [
          {
            label: 'Number of Customers',
            data: this.customersByPincode.map((item) => item.customer_count),
            backgroundColor: '#ff5722',
          },
        ],
      };

      const pincodeChart = document.getElementById('customerPincodeChart');
      if (pincodeChart) {
        new Chart(pincodeChart, {
          type: 'bar',
          data: pincodeData,
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true },
            },
            plugins: {
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => tooltipItem.raw + ' Customers',
                },
              },
            },
          },
        });
      }

      
      const statusData = {
        labels: ['Pending', 'Assigned', 'Rejected', 'Completed'],
        datasets: [
          {
            label: 'Number of Service Requests',
            data: [
              this.serviceRequestsByStatus.find((item) => item.status === 'Pending')?.request_count || 0,
              this.serviceRequestsByStatus.find((item) => item.status === 'Assigned')?.request_count || 0,
              this.serviceRequestsByStatus.find((item) => item.status === 'Rejected')?.request_count || 0,
              this.serviceRequestsByStatus.find((item) => item.status === 'Completed')?.request_count || 0,
            ],
            backgroundColor: ['#ff9800', '#4caf50', '#f44336', '#2196f3'],
          },
        ],
      };

      const statusChart = document.getElementById('statusChart');
      if (statusChart) {
        new Chart(statusChart, {
          type: 'pie',
          data: statusData,
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => tooltipItem.raw + ' Requests',
                },
              },
            },
          },
        });
      }
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },
  },
};
</script>


<style scoped>
.container {
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 10px;
}

h1 {
  font-family: 'Arial', sans-serif;
  color: #0056b3;
  font-weight: bold;
}

.row {
  margin-top: 20px;
}

canvas {
  max-height: 400px;
  max-width: 100%;
}

.mb-4 {
  margin-bottom: 40px;
}
</style>

  
  