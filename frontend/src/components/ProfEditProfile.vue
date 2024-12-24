<template>
  <router-link to="/professional/professional_home">
        <button class="btn btn-secondary">Back to Dashboard</button>
      </router-link>
  <div class="edit-profile">
    <h1 class="text-center">Edit Profile</h1>
    <p class="text-center text-muted">
      Professionals are not allowed to change their service category and type.
    </p>
    <form @submit.prevent="saveChanges" class="profile-form">
      <div class="form-group">
        <label>Full Name</label>
        <input
          type="text"
          v-model="profile.full_name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label>Email</label>
        <input
          type="text"
          v-model="profile.email"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label>Password</label>
        <input
          type="password"
          v-model="profile.password"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label>Experience</label>
        <input
          type="text"
          v-model="profile.experience"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label>Address</label>
        <textarea v-model="profile.address" class="form-control"></textarea>
      </div>
      <div class="form-group">
        <label>Mobile Number</label>
        <input
          type="text"
          v-model="profile.mobile_number"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label>Pin Code</label>
        <input
          type="text"
          v-model="profile.pin_code"
          class="form-control"
        />
      </div>
      <div class="form-group">
        <label>Attach New Document</label>
        <input
          type="file"
          @change="handleFileUpload"
          class="form-control-file"
        />
      </div>
      <button type="submit" class="btn btn-primary btn-block">Save Changes</button>
    </form>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  data() {
    return {
      profile: {
        full_name: "",
        email: "",
        password: "",
        experience: "",
        address: "",
        mobile_number: "",
        pin_code: "",
      },
      newDocument: null,
    };
  },
  async created() {
    await this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(
          "http://127.0.0.1:5000/professional/prof_edit_profile",
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        this.profile = { ...response.data, password: response.data.password || "" };
      } catch (error) {
        console.error("Error fetching profile:", error);
      }
    },
    handleFileUpload(event) {
      this.newDocument = event.target.files[0];
    },
    async saveChanges() {
      const formData = new FormData();
      Object.entries(this.profile).forEach(([key, value]) => {
        if (value) {
          formData.append(key, value);  
        }
      });
      if (this.newDocument) {
        formData.append("documents", this.newDocument);
      }
      try {
        const token = localStorage.getItem("token");
        const response = await axios.post(
          "http://127.0.0.1:5000/professional/prof_edit_profile",
          formData,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        alert(response.data.message);
      } catch (error) {
        console.error("Error saving changes:", error);
      }
    },
  },
};
</script>

<style scoped>
.edit-profile {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  border-radius: 10px;
  background-color: #f8f9fa;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #343a40;
}

p {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control,
.form-control-file {
  border: 1px solid #ced4da;
  border-radius: 5px;
  padding: 10px;
}

.btn-primary {
  background-color: #007bff;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>


  