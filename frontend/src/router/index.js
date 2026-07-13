import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import StudentRegister from '../views/StudentRegister.vue'
import CompanyRegister from '../views/CompanyRegister.vue'

import CompanyDashboard from '../views/CompanyDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

import AdminCompanies from "../views/AdminCompanies.vue"
import AdminCompanyProfile from "../views/AdminCompanyProfile.vue"
import AdminStudents from "../views/AdminStudents.vue"
import AdminStudentProfile from "../views/AdminStudentProfile.vue"
import AdminDrives from "../views/AdminDrives.vue"
import AdminDriveDetails from "../views/AdminDriveDetails.vue"
import AdminApplications from "../views/AdminApplications.vue"
import AdminPlacementHistory from "../views/AdminPlacementHistory.vue"
import AdminStatistics from "../views/AdminStatistics.vue"

import CompanyProfile from "../views/CompanyProfile.vue"
import CompanyEditProfile from "../views/CompanyEditProfile.vue"
import CompanyDrives from "../views/CompanyDrives.vue"
import CompanyEditDrive from "../views/CompanyEditDrive.vue"
import CompanyApplicants from "../views/CompanyApplicants.vue"
import CompanyStudentProfile from "../views/CompanyStudentProfile.vue"

import StudentProfile from "../views/StudentProfile.vue"
import StudentEditProfile from "../views/StudentEditProfile.vue"
import StudentDrives from "../views/StudentDrives.vue"
import StudentApplications from "../views/StudentApplications.vue"
import StudentOffers from "../views/StudentOffers.vue"

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/login',
        component: Login
    },
    {
        path: '/student/register',
        component: StudentRegister
    },
    {
        path: '/company/register',
        component: CompanyRegister
    },
    {
        path: "/admin/dashboard",
        component: AdminDashboard,
        meta: {
            requiresAuth: true,
            role: "admin"
            }
    },
    {
        path: "/student/dashboard",
        component: StudentDashboard,
        meta: {
            requiresAuth: true,
            role: "student"
        }
    },
    {
        path: "/company/dashboard",
        component: CompanyDashboard,
        meta: {
            requiresAuth: true,
            role: "company"
        }
    },
    {
        path: "/admin/companies",
        component: AdminCompanies,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/company/:id",
        component: AdminCompanyProfile,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/students",
        component: AdminStudents,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/student/:id",
        component: AdminStudentProfile,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/drives",
        component: AdminDrives,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/drive/:id",
        component: AdminDriveDetails,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/applications",
        component: AdminApplications,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/placement-history",
        component: AdminPlacementHistory,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    },
    {
        path: "/admin/statistics",
        component: AdminStatistics,
        meta: {
        requiresAuth: true,
        role: "admin"
        }
    }
    ,
    {
        path: "/company/profile",
        component: CompanyProfile,
        meta: {
        requiresAuth: true,
        role: "company"
        }
    },
    {
        path: "/company/profile/edit",
        component: CompanyEditProfile,
        meta: {
        requiresAuth: true,
        role: "company"
        }
    },
    {
        path: "/company/drives",
        component: CompanyDrives,
        meta: {
        requiresAuth: true,
        role: "company"
        }
    },
    {
        path: "/company/drive/edit/:id",
        component: CompanyEditDrive,
        meta: {
        requiresAuth: true,
        role: "company"
        }
    },
    {
        path:"/company/drive/:id/applicants",
        component:CompanyApplicants,
        meta:{
            requiresAuth:true,
            role:"company"
        }
    },
    {
        path:"/company/application/:id/student",
        component:CompanyStudentProfile,
        meta:{
            requiresAuth:true,
            role:"company"
        }
    },
    {
        path: "/student/profile",
        component: StudentProfile,
        meta:{
            requiresAuth:true,
            role:"student"
        }
    },
    {
        path: "/student/profile/edit",
        component: StudentEditProfile,
        meta:{
            requiresAuth:true,
            role:"student"
        }
    },
    {
        path:"/student/drives",
        component:StudentDrives,
        meta:{
            requiresAuth:true,
            role:"student"
        }
    },
    {
        path:"/student/applications",
        component:StudentApplications,
        meta:{
            requiresAuth:true,
            role:"student"
        }
    },
    {
        path:"/student/offers",
        component:StudentOffers,
        meta:{
            requiresAuth:true,
            role:"student"
        }
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token")
    const role = localStorage.getItem("role")

    if (to.meta.requiresAuth) {
        if (!token) {
            next("/login")
        }
        else if (role !== to.meta.role) {
            next("/login")
        }
        else {
            next()
        }
    }
    else {
        next()
    }
})

export default router