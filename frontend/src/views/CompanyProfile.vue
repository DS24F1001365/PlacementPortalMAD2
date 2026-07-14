<template>
    <Navbar role="company"/>
    
    <div class="container mt-5">

        <div v-if="success">

            <h2 class="text-center mb-4">
            Company Profile
            </h2>

            <div class="card p-4">
                <p>                    
                    <b>Company Name:</b> {{ profile.company_name }}
                </p>
                <p>
                    <b>Email:</b> {{ profile.email }}
                </p>
                <p>
                    <b>HR Name:</b> {{ profile.hr_name }}
                </p>
                <p>
                    <b>HR Email:</b> {{ profile.hr_email }}
                </p>
                <p>
                    <b>HR Contact:</b> {{ profile.hr_contact }}
                </p>
                <p>
                    <b>Website:</b> {{ profile.website }}
                </p>
                <p>
                    <b>Description:</b> {{ profile.description }}
                </p>

                <router-link class="btn btn-primary" to="/company/profile/edit">
                    Edit Profile
                </router-link>
            </div>
        </div>

        <div v-else>
            <div class="alert alert-danger text-center">
                {{ message }}
            </div>
        </div>

    </div>
</template>


<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            success: false,
            message: "",
            profile: {}
        }
    },

    components:{
        Navbar,
    },

    mounted() {
        this.loadProfile()
    },

    methods: {

        async loadProfile() {

            const response = await fetch(
                "http://127.0.0.1:5000/api/company/profile",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.success = true
                this.profile = result.profile
            }

            else {
                this.success = false
                this.message = result.message
            }
        }
    }
}
</script>