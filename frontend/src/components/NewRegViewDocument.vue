<template>
  <div class="container mt-5">
    <div class="text-right mb-3">
      <button class="btn btn-primary" @click="goBackToPendingRegs">Back to Pending Registrations</button>
    </div>

    
    <div class="text-center">
      <h3>View Document for Review</h3>

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
import axios from "@/axios";

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
      const requestId = this.$route.params.requestId;
      const token = localStorage.getItem("token"); 

      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      try {
        const response = await axios.get(
          `http://127.0.0.1:5000/admin/view_document_new_reg/${requestId}`,
          {
            headers: {
              Authorization: `Bearer ${token}` 
            },
            responseType: "blob" 
          }
        );

        if (response.data) {
          console.log("Blob response:", response.data);
          const url = URL.createObjectURL(response.data);
          this.documentUrl = url; 
        }
        this.loading = false;
      } catch (error) {
        console.error("Error fetching document:", error);
        this.loading = false;
      }
    },
    goBackToPendingRegs() {
      this.$router.push("/admin/new_registration_requests");
    },
    
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem("token"); 
      this.$router.push("/auth/login");
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