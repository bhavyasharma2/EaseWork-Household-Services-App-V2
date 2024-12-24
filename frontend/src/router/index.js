import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '@/components/LoginPage.vue';
import AdminDashboard from '@/components/AdminDashboard.vue';
import CustomerDashboard from '@/components/CustomerDashboard.vue';
import ProfessionalDashboard from '@/components/ProfessionalDashboard.vue';
import ServiceProfessionalSignUp from '@/components/ServiceProfessionalSignUp.vue';
import CustomerSignUp from '@/components/CustomerSignUp.vue';
import CustomerDetails from '@/components/CustomerDetails.vue';
import ProfessionalDetails from '@/components/ProfessionalDetails.vue';
import ProfViewDocument from '@/components/ProfViewDocument.vue';
import NewRegistrationRequests from '@/components/NewRegistrationRequests.vue';
import NewRegViewDocument from '@/components/NewRegViewDocument.vue';
import ServiceDetails from '@/components/ServiceDetails.vue';
import EditService from '@/components/EditService.vue';
import AddService from '@/components/AddService.vue';
import AdminStatistics from '@/components/AdminStatistics.vue';
import AdminEditProfile from '@/components/AdminEditProfile.vue';
import AdminServiceRequests from '@/components/AdminServiceRequests.vue';
import AvailableServices from '@/components/AvailableServices.vue';
import AvailableProfessionals from '@/components/AvailableProfessionals.vue';
import BookService from '@/components/BookService.vue';
import CustomerEditProfile from '@/components/CustomerEditProfile.vue';
import ServiceRequestHistory from '@/components/ServiceRequestHistory.vue';
import EditServiceRequest from '@/components/EditServiceRequest.vue';
import ServiceReviewForm from '@/components/ServiceReviewForm.vue';
import ProfEditProfile from '@/components/ProfEditProfile.vue';
import ProfServiceRequests from '@/components/ProfServiceRequests.vue';
import ProfStatistics from '@/components/ProfStatistics.vue';
import CustomerStatistics from '@/components/CustomerStatistics.vue';


const routes = [
  { path: '/auth/login', name: 'LoginPage', component: LoginPage },
  { path: '/admin/admin_home', name: 'AdminDashboard', component: AdminDashboard },
  { path: '/customers/customer_home', name: 'CustomerDashboard', component: CustomerDashboard },
  { path: '/professional/professional_home', name: 'ProfessionalDashboard', component: ProfessionalDashboard },
  { path: '/register/register_professional', name: 'ServiceProfessionalSignUp', component: ServiceProfessionalSignUp },
  { path: '/register/register_customer', name: 'CustomerSignUp', component: CustomerSignUp },
  { path: '/admin/customer_details', name: 'CustomerDetails', component: CustomerDetails },
  { path: '/admin/professional_details', name: 'ProfessionalDetails', component: ProfessionalDetails },
  { path: '/admin/view_document/:userId', name: 'ProfViewDocument', component: ProfViewDocument },
  { path: '/admin/new_registration_requests', name: 'NewRegistrationRequests', component: NewRegistrationRequests },
  { path: '/admin/view_document_new_reg/:requestId', name: 'NewRegViewDocument', component: NewRegViewDocument },
  { path: '/admin/service_details', name: 'ServiceDetails', component: ServiceDetails },
  { path: '/admin/edit_service/:serviceId', name: 'EditService', component: EditService },
  { path: '/admin/add_service', name: 'AddService', component: AddService },
  { path: '/admin/admin_statistics', name: 'AdminStatistics', component: AdminStatistics },
  { path: '/admin/admin_edit_profile', name: 'AdminEditProfile', component: AdminEditProfile },
  { path: '/admin/admin_service_requests', name: 'AdminServiceRequests', component: AdminServiceRequests },
  { path: '/customers/available_services', name: 'AvailableServices', component: AvailableServices },
  { path: '/customers/available_professionals/:serviceId/:serviceTypeId', name: 'AvailableProfessionals', component: AvailableProfessionals },
  { path: '/customers/book_service/:professionalId/:serviceId', name: 'BookService', component: BookService },
  { path: '/customers/customer_edit_profile', name: 'CustomerEditProfile', component: CustomerEditProfile },
  { path: '/customers/service_request_history', name: 'ServiceRequestHistory', component: ServiceRequestHistory },
  { path: '/customers/edit_service_request/:requestId', name: 'EditServiceRequest', component: EditServiceRequest },
  { path: '/customers/service_review_form/:requestId', name: 'ServiceReviewForm', component: ServiceReviewForm },
  { path: '/professional/prof_edit_profile', name: 'ProfEditProfile', component: ProfEditProfile },
  { path: '/professional/prof_service_requests', name: 'ProfServiceRequests', component: ProfServiceRequests },
  { path: '/professional/professional_statistics', name: 'ProfStatistics', component: ProfStatistics },
  { path: '/customers/customer_statistics', name: 'CustomerStatistics', component: CustomerStatistics },
  { path: '/:pathMatch(.*)*', component: LoginPage }
];


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;





