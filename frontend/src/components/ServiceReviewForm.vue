<template>
    <div class="service-review-form">
      <h1 class="heading">Service Review</h1>
      <div class="form-container">
        <form @submit.prevent="submitReview">
          <div class="field">
            <label>Service Request ID:</label>
            <input type="text" :value="serviceRequest.service_request_id" readonly />
          </div>
          <div class="field">
            <label>Service Name:</label>
            <input type="text" :value="serviceRequest.service_name" readonly />
          </div>
          <div class="field">
            <label>Service Type ID:</label>
            <input type="text" :value="serviceRequest.service_type_id" readonly />
          </div>
          <div class="field">
            <label>Requested Date:</label>
            <input type="text" :value="serviceRequest.requested_date" readonly />
          </div>
          <div class="field">
            <label>Completion Date:</label>
            <input type="text" :value="serviceRequest.completion_date" readonly />
          </div>
          <div class="field">
            <label>Professional Name:</label>
            <input type="text" :value="serviceRequest.professional_name" readonly />
          </div>
          <div class="field">
            <label>Professional Contact:</label>
            <input type="text" :value="serviceRequest.professional_contact" readonly />
          </div>
          <div class="field">
            <label>Please provide service rating (out of 5) below:</label>
            <input
              type="number"
              v-model="rating"
              min="1"
              max="5"
              step="1"
              required
              placeholder="Enter rating (1-5)"
            />
          </div>
          <button type="submit" class="submit-btn">Submit Review</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "@/axios";
  
  export default {
    data() {
      return {
        serviceRequest: {},
        rating: null,
      };
    },
    created() {
      this.fetchServiceRequest();
    },
    methods: {
      async fetchServiceRequest() {
        const token = localStorage.getItem("token");
  
        try {
          const response = await axios.get(
            `http://127.0.0.1:5000/customers/service_review_form/${this.$route.params.requestId}`,
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          this.serviceRequest = response.data.service_request;
        } catch (error) {
          console.error("Error fetching service request:", error);
          alert("Unable to fetch service request. Please try again later.");
        }
      },
      async submitReview() {
        const token = localStorage.getItem("token");
  
        try {
          await axios.post(
            `http://127.0.0.1:5000/customers/submit_review/${this.$route.params.requestId}`,
            { service_rating: this.rating },
            {
              headers: {
                Authorization: `Bearer ${token}`,
              },
            }
          );
          alert("Review submitted successfully!");
          this.$router.push("/customers/customer_home");
        } catch (error) {
          console.error("Error submitting review:", error);
          alert("Unable to submit review. Please try again later.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .service-review-form {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .heading {
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }
  
  .form-container {
    display: flex;
    flex-direction: column;
  }
  
  .field {
    margin-bottom: 15px;
  }
  
  .field label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .field input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .submit-btn {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    color: #fff;
    background-color: #007bff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 10px;
  }
  
  .submit-btn:hover {
    background-color: #0056b3;
  }
  </style>
  