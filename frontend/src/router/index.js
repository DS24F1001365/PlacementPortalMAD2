import { createRouter, createWebHistory } from 'vue-router'

import Login from '../views/Login.vue'
import StudentRegister from '../views/StudentRegister.vue'
import CompanyRegister from '../views/CompanyRegister.vue'
import CompanyDashboard from '../views/CompanyDashboard.vue'
import StudentDashboard from '../views/StudentDashboard.vue'
import AdminDashboard from '../views/AdminDashboard.vue'


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