<template>
  <div class="container mt-5">
    <div class="header d-flex justify-content-end mb-3">
      <router-link to="/admin/admin_home">
        <button class="btn btn-secondary">Back to Dashboard</button>
      </router-link>
    </div>

    <div class="profile-box">
      <h2 class="text-center mb-4">Edit Profile</h2>

      <form @submit.prevent="updatePassword" class="form-container">
        <div class="form-group">
          <label for="newPassword" class="form-label">New Password</label>
          <input
            type="password"
            v-model="newPassword"
            class="form-control"
            id="newPassword"
            placeholder="Enter new password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary btn-confirm">Confirm</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';

export default {
  data() {
    return {
      newPassword: ''
    };
  },
  methods: {
    updatePassword() {
      const token = localStorage.getItem('token');
      if (!token) {
        this.redirectToLogin("You are not logged in.");
        return;
      }

      if (this.newPassword) {
        axios.post('http://127.0.0.1:5000/admin/admin_edit_profile', { new_password: this.newPassword }, {
          headers: { Authorization: `Bearer ${token}` }  
        })
          .then(() => {
            alert('Password updated successfully');
            this.$router.push('/admin/admin_home');
          })
          .catch(error => {
            console.error('Error updating password:', error);
            alert('Error updating password.');
            if (error.response && error.response.status === 403) {
              this.redirectToLogin("Access forbidden: Admins only.");
            } else {
              this.redirectToLogin("Session expired or invalid.");
            }
          });
      }
    },
    redirectToLogin(message) {
      alert(message);
      localStorage.removeItem('token');
      this.$router.push('/auth/login');
    }
  }
};
</script>


<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: #f3f4f6;
  border-radius: 16px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: auto;
}

.header {
  width: 100%;
  display: flex;
  justify-content: flex-end;
}

.profile-box {
  width: 100%;
  background: #ffffff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

h2 {
  font-family: 'Arial', sans-serif;
  color: #004f8c;
  font-weight: bold;
}

.form-container {
  margin-top: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  font-weight: 600;
  color: #4a4a4a;
}

.form-control {
  border-radius: 8px;
  border: 1px solid #ced4da;
  padding: 10px;
  font-size: 1rem;
}

.form-control:focus {
  border-color: #004f8c;
  box-shadow: 0 0 8px rgba(0, 79, 140, 0.2);
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
  font-weight: bold;
  padding: 8px 15px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background-color: #5a6268;
}

.btn-confirm {
  background-color: #007bff;
  color: white;
  width: 100%;
  padding: 12px;
  font-size: 1.1rem;
  font-weight: bold;
  border-radius: 8px;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.btn-confirm:hover {
  background-color: #0056b3;
}
</style>


  