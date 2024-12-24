<template>
    <div class="signup-container">
      <div class="signup-card">
        <h2 class="signup-heading">Service Professional Sign Up</h2>
        
        
        <form @submit.prevent="registerProfessional">
          <div class="form-group">
            <label for="email">Email ID</label>
            <input
              type="email"
              id="email"
              v-model="form.email"
              placeholder="Enter your email"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="password">Password</label>
            <input
              type="password"
              id="password"
              v-model="form.password"
              placeholder="Enter your password"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="full_name">Full Name</label>
            <input
              type="text"
              id="full_name"
              v-model="form.full_name"
              placeholder="Enter your full name"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="service_id">Service Name</label>
            <select
              id="service_id"
              v-model="form.service_id"
              @change="fetchServiceTypes"
              required
            >
              <option value="" disabled>Select a service</option>
              <option v-for="service in services" :key="service.id" :value="service.id">
                {{ service.name }}
              </option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="service_type_id">Service Type</label>
            <select id="service_type_id" v-model="form.service_type_id" required>
              <option value="" disabled>Select a service type</option>
              <option v-for="type in serviceTypes" :key="type.id" :value="type.id">
                {{ type.type_name }}
              </option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="experience">Experience (in years)</label>
            <input
              type="number"
              id="experience"
              v-model="form.experience"
              placeholder="Enter your experience in years"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="documents">Attach Documents (PDF)</label>
            <input
              type="file"
              id="documents"
              @change="handleFileUpload"
              accept=".pdf"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="address">Address</label>
            <input
              type="text"
              id="address"
              v-model="form.address"
              placeholder="Enter your address"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="pin_code">Pin Code</label>
            <input
              type="text"
              id="pin_code"
              v-model="form.pin_code"
              placeholder="Enter your pin code"
              required
            />
          </div>
  
          <div class="form-group">
            <label for="mobile_number">Mobile Number</label>
            <input
              type="text"
              id="mobile_number"
              v-model="form.mobile_number"
              placeholder="Enter your mobile number"
              required
            />
          </div>
  
          <button type="submit" class="btn-register">Register</button>
        </form>
  
        <div v-if="message" class="success-message">{{ message }}</div>
      </div>
    </div>
  </template>
  
  <script>
import axios from "@/axios";

export default {
  data() {
    return {
      form: {
        email: "",
        password: "",
        full_name: "",
        service_id: "",
        service_type_id: "",
        experience: "",
        address: "",
        pin_code: "",
        mobile_number: "",
        documents: null,
      },
      services: [],
      serviceTypes: [],
      message: "",
    };
  },
  created() {
    
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/register/get_services");
        this.services = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async fetchServiceTypes() {
      if (this.form.service_id) {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/register/get_service_types/${this.form.service_id}`);
          this.serviceTypes = response.data;
        } catch (error) {
          console.error("Error fetching service types:", error);
        }
      }
    },
    handleFileUpload(event) {
      this.form.documents = event.target.files[0];
    },
    async registerProfessional() {
      const formData = new FormData();
      formData.append("email", this.form.email);
      formData.append("password", this.form.password);
      formData.append("full_name", this.form.full_name);
      formData.append("service_id", this.form.service_id);
      formData.append("service_type_id", this.form.service_type_id);
      formData.append("experience", this.form.experience);
      formData.append("address", this.form.address);
      formData.append("pin_code", this.form.pin_code);
      formData.append("mobile_number", this.form.mobile_number);
      if (this.form.documents) {
        formData.append("documents", this.form.documents);
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/register/register_professional", formData);
        this.message = response.data.msg;
        
        this.form = {
          email: "",
          password: "",
          full_name: "",
          service_id: "",
          service_type_id: "",
          experience: "",
          documents: null,
          address: "",
          pin_code: "",
          mobile_number: "",
        };
      } catch (error) {
        this.message = error.response.data.msg || "An error occurred";
      }
    },
  },
};
</script>

  
  <style scoped>
  .signup-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #007bff;
  }
  
  .signup-card {
    background-color: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 500px;
  }
  
  .signup-heading {
    font-size: 2em;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .form-group label {
    font-weight: bold;
  }
  
  .form-group input,
  .form-group select {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group input[type="file"] {
    padding: 5px;
  }
  
  .btn-register {
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
  }
  
  .btn-register:hover {
    background-color: #45a049;
  }
  
  .success-message {
    margin-top: 15px;
    padding: 10px;
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 5px;
    text-align: center;
  }
  </style>
  