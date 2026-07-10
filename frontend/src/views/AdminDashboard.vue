<template>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            {{ message }}
        </h2>

        <div class="row">

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Total Students</h5>
                    <h2>{{ stats.total_students }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Total Companies</h5>
                    <h2>{{ stats.total_companies }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Total Drives</h5>
                    <h2>{{ stats.total_drives }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Total Applications</h5>
                    <h2>{{ stats.total_applications }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Placed Students</h5>
                    <h2>{{ stats.placed_students }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Pending Companies</h5>
                    <h2>{{ stats.pending_companies }}</h2>
                </div>
            </div>

            <div class="col-md-4 mb-3">
                <div class="card p-3 text-center">
                    <h5>Pending Drives</h5>
                    <h2>{{ stats.pending_drives }}</h2>
                </div>
            </div>

        </div>

        <hr>

        <div class="text-center">
            <router-link class="btn btn-primary m-2" to="/admin/companies">
                Companies
            </router-link>
            <router-link class="btn btn-primary m-2" to="/admin/students">
                Students
            </router-link>
            <router-link class="btn btn-primary m-2" to="/admin/drives">
                Drives
            </router-link>
            <router-link class="btn btn-primary m-2" to="/admin/applications">
                Applications
            </router-link>
            <router-link class="btn btn-primary m-2" to="/admin/placement-history">
                Placement History
            </router-link>
            <router-link class="btn btn-primary m-2" to="/admin/statistics">
                Statistics
            </router-link>
        </div>

        <button class="btn btn-danger mt-4" @click="logout">
            Logout
        </button>

    </div>
</template>


<script>

export default {

    data() {
        return {
            message: "",
            stats: {}
        }
    },

    mounted() {
        this.loadDashboard()
    },

    methods: {
        async loadDashboard() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/dashboard",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.message = result.message
                this.stats = result.stats
            }
        },

        logout() {
            localStorage.clear()
            this.$router.push("/login")
        }
    }
}

</script>