<template>
    <Navbar role="admin"/>
    
    <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
    </div>

    <div v-else class="container mt-5">

        <h2 class="mb-4">
            Placement Drive Details
        </h2>

        <div class="card p-4">
            <p><b>Title:</b> {{ drive.title }}</p>
            <p><b>Specialization:</b> {{ drive.specialization }}</p>
            <p><b>Company:</b> {{ drive.company }}</p>
            <p><b>Description:</b> {{ drive.description }}</p>
            <p><b>Eligible Branches:</b> {{ drive.eligible_branches }}</p>
            <p><b>Minimum CGPA:</b> {{ drive.minimum_cgpa }}</p>
            <p><b>Eligible Year:</b> {{ drive.eligible_year }}</p>
            <p><b>Deadline:</b> {{ drive.deadline }}</p>
            <p><b>Status:</b> {{ drive.status }}</p>
        </div>
        <br>
        <router-link class="btn btn-primary" to="/admin/drives">
            Back
        </router-link>

    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            drive: {},
            errorMessage: ""
        }
    },

    components:{
        Navbar,
    },
    

    async mounted() {
        const response = await fetch(
            "http://127.0.0.1:5000/api/admin/drive/" + this.$route.params.id,
            {
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem("token")
                }
            }
        )

        const result = await response.json()
        if (result.success) {
            this.drive = result.drive
        }
        else {
            this.errorMessage = result.message
        }
    }
}

</script>