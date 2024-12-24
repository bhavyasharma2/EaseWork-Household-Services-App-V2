<template>
    <div class="container mt-5">
      <div class="text-right mb-3">
        <button class="btn btn-primary" @click="goBackToDetails">Back to Professional Details</button>
      </div>
  
      
      <div class="text-center">
        <h3>View Professional Document</h3>
  
        <div v-if="loading" class="spinner-border text-primary" role="status">
          <span class="sr-only">Loading...</span>
        </div>
  
        <div v-else>
          <iframe v-if="documentUrl" :src="documentUrl" width="100%" height="600px" frameborder="0"></iframe>
          <p v-else>No document available.</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import axios from '@/axios';

export default {
  data() {
    return {
      documentUrl: null,
      loading: true
    };
  },
  created() {
    this.fetchDocument();
  },
  methods: {
    async fetchDocument() {
      const token = localStorage.getItem('token');
      const userId = this.$route.params.userId;

      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:5000/admin/view_document/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
          responseType: 'blob'
        });

        
        const url = URL.createObjectURL(response.data);
        this.documentUrl = url;
        this.loading = false;
      } catch (error) {
        console.error("Error fetching document:", error);
        this.loading = false;
        if (error.response && error.response.status === 403) {
          this.redirectToLogin("Access forbidden: Admins only.");
        } else {
          this.redirectToLogin("Session expired or invalid.");
        }
      }
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    },
    goBackToDetails() {
      this.$router.push('/admin/professional_details');
    }
  }
};
</script>

  
  <style scoped>
  
  iframe {
    border: none;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .spinner-border {
    margin-top: 20px;
  }
  </style>
  