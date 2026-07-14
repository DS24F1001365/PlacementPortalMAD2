<template>
    <Navbar role="admin"/>
    
    <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
    </div>
    
    <div v-else class="container mt-5">
        <h2 class="mb-4">
            Company Profile
        </h2>

        <div class="card p-4">
            <p><b>Name:</b> {{ company.name }}</p>
            <p><b>Email:</b> {{ company.email }}</p>
            <p><b>HR Name:</b> {{ company.hr_name }}</p>
            <p><b>HR Email:</b> {{ company.hr_email }}</p>
            <p><b>Contact:</b> {{ company.hr_contact }}</p>
            <p><b>Website:</b> {{ company.website }}</p>
            <p><b>Description:</b> {{ company.description }}</p>
            <p><b>Status:</b> {{ company.approval_status }}</p>
        </div>
        <br>
        <router-link class="btn btn-primary" to="/admin/companies">
            Back
        </router-link>
    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            company: {},
            errorMessage: ""
        }
    },

    components:{
        Navbar,
    },

 
    async mounted() {
        const response = await fetch(
            "http://127.0.0.1:5000/api/admin/company/" + this.$route.params.id,
            {
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token")
                }
            }
        )

        const result = await response.json()
        if (result.success) {
            this.company = result.company
        }
        else {
            this.errorMessage = result.message
        }
    }
}

</script>