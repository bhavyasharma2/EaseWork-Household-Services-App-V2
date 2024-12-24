<template>
    <router-link to="/customers/customer_home" class="btn btn-secondary back-button">
      Back to Dashboard
    </router-link>
    <div class="container mt-5">
      
      <div class="text-center mb-5">
        <h2 class="text-success font-weight-bold">Customer Statistics</h2>
      </div>
  
      
      <div class="row justify-content-center">
        
        <div class="col-md-6 mb-5">
          <h4 class="text-center">Service Requests by Status</h4>
          <canvas id="statusChart"></canvas>
        </div>
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
        statistics: null,
        serviceRequestsByStatus: [],
      };
    },
    mounted() {
      this.fetchCustomerStatistics();
    },
    methods: {
      async fetchCustomerStatistics() {
        const token = localStorage.getItem("token");
        if (!token) {
          this.redirectToLogin("You are not logged in.");
          return;
        }
  
        try {
          const response = await axios.get(
            "http://127.0.0.1:5000/customers/customer_statistics",
            {
              headers: { Authorization: `Bearer ${token}` },
            }
          );
          console.log("Statistics fetched:", response.data);
  
          const data = response.data.statistics;
  
          
          this.serviceRequestsByStatus = [
            { status: "Pending", count: data.pending_requests },
            { status: "Completed", count: data.completed_requests },
          ];
  
          this.statistics = data;
          this.renderChart();
        } catch (error) {
          console.error("Error fetching customer statistics:", error);
          if (error.response && error.response.status === 403) {
            this.redirectToLogin("Unauthorized access. Customers only.");
          } else {
            this.redirectToLogin("Session expired or invalid.");
          }
        }
      },
      renderChart() {
        
        const statusData = {
          labels: this.serviceRequestsByStatus.map((item) => item.status),
          datasets: [
            {
              label: "Requests",
              data: this.serviceRequestsByStatus.map((item) => item.count),
              backgroundColor: ["#ffc107", "#28a745"],
            },
          ],
        };
  
        const statusChart = document.getElementById("statusChart");
        if (statusChart) {
          new Chart(statusChart, {
            type: "pie",
            data: statusData,
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
  
  canvas {
    max-height: 400px;
  }
  
  .row {
    display: flex;
    justify-content: center;
  }
  
  .col-md-6 {
    padding: 15px;
  }
  </style>
  
  