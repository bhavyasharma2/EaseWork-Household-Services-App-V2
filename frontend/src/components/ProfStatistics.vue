<template>
    <router-link to="/professional/professional_home" class="btn btn-secondary back-button">
      Back to Dashboard
    </router-link>
    <div class="container mt-5">
      
      <div class="text-center mb-5">
        <h2 class="text-primary font-weight-bold">Professional Statistics</h2>
      </div>
  
      
      <div class="rating-section text-center mb-5">
        <h4 class="text-info">Your Rating</h4>
        <div v-if="professionalRating !== 'No rating available'" class="rating-display">
          <span class="badge bg-success text-white p-3">{{ professionalRating }}</span>
        </div>
        <div v-else>
          <span class="badge bg-warning text-dark p-3">No rating available</span>
        </div>
      </div>

      
    <div class="text-center mt-4">
      <button class="btn btn-primary" @click="exportCSV">Export Closed Requests as CSV</button>
    </div>
  
      
      <div class="chart-section">
        <h4 class="text-center mb-3">Service Requests by Status</h4>
        <canvas id="statusChart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/axios";
  import { Chart, registerables } from "chart.js";
  
  
  Chart.register(...registerables);
  
  export default {
    data() {
      return {
        professionalRating: "No rating available",
        serviceRequestsByStatus: [],
      };
    },
    mounted() {
      this.fetchProfessionalStatistics();
    },
    methods: {
      exportCSV() {
        const token = localStorage.getItem("token");
        axios
          .post(
            "http://127.0.0.1:5000/professional/export_csv",
            {},
            { headers: { Authorization: `Bearer ${token}` }, responseType: "blob" }
          )
          .then((response) => {
            
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement("a");
            link.href = url;
            link.setAttribute("download", "exported_requests.csv"); 
            document.body.appendChild(link);
            link.click();  
            alert("CSV Export started. You will be notified when it is ready.");
          })
          .catch((error) => {
            console.error("Error exporting CSV:", error);
          });
      },
      async fetchProfessionalStatistics() {
        const token = localStorage.getItem("token");
        if (!token) {
          this.redirectToLogin("You are not logged in.");
          return;
        }
  
        try {
          const response = await axios.get(
            "http://127.0.0.1:5000/professional/professional_statistics",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
  
          console.log("Professional statistics fetched:", response.data);
  
          
          this.professionalRating = response.data.professional_rating || "No rating available";
          this.serviceRequestsByStatus = response.data.service_requests_by_status || [];
  
          
          this.renderChart();
        } catch (error) {
          console.error("Error fetching professional statistics:", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Unauthorized access. Professionals only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        }
      },
      renderChart() {
        
        const chartData = {
          labels: this.serviceRequestsByStatus.map((item) => item.status),
          datasets: [
            {
              label: "Requests",
              data: this.serviceRequestsByStatus.map((item) => item.count),
              backgroundColor: ["#007bff", "#28a745", "#ffc107", "#dc3545"],
            },
          ],
        };
  
        
        const statusChart = document.getElementById("statusChart");
        if (statusChart) {
          new Chart(statusChart, {
            type: "pie",
            data: chartData,
            options: {
              responsive: true,
              plugins: {
                legend: { position: "top" },
                tooltip: {
                  callbacks: {
                    label: (tooltipItem) => `${tooltipItem.raw} Requests`,
                  },
                },
              },
            },
          });
        }
      },
      redirectToLogin(message) {
        alert(message);
        localStorage.removeItem("token");
        this.$router.push("/auth/login");
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    background-color: #f8f9fa;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .text-center {
    color: #0056b3;
  }
  
  h2 {
    font-size: 2.5rem;
    letter-spacing: 1px;
  }
  
  h4 {
    font-size: 1.5rem;
    color: #495057;
  }
  
  .rating-section {
    padding: 15px;
  }
  
  .rating-display {
    font-size: 2rem;
    margin-top: 10px;
  }
  
  .chart-section canvas {
    max-height: 400px;
  }
  </style>
  