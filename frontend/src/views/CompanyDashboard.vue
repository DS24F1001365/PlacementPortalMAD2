<template>
    <div class="container mt-5">

        <div v-if="success">

            <h2 class="text-center mb-4">
                {{ message }}
            </h2>

            <div class="row">

                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Total Drives</h5>
                        <h2>{{ stats.total_drives }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Approved Drives</h5>
                        <h2>{{ stats.approved_drives }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Total Applicants</h5>
                        <h2>{{ stats.total_applicants }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Pending Applications</h5>
                        <h2>{{ stats.pending_applications }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Selected Students</h5>
                        <h2>{{ stats.selected_students }}</h2>
                    </div>
                </div>

            </div>

            <h4 class="mt-4">
                Drives Requiring Action
            </h4>

            <table class="table table-bordered">

                <thead>
                    <tr>
                        <th>Drive ID</th>
                        <th>Title</th>
                        <th>Pending Applications</th>
                    </tr>
                </thead>

                <tbody>
                    <tr v-for="drive in pendingDrives" :key="drive.drive_id">
                        <td>{{ drive.drive_id }}</td>
                        <td>{{ drive.title }}</td>
                        <td>{{ drive.pending_count }}</td>
                    </tr>
                </tbody>

            </table>

            <router-link class="btn btn-primary m-2" to="/company/drives">
                My Drives
            </router-link>
            <router-link class="btn btn-primary m-2" to="/company/profile">
                Profile
            </router-link>
            <br>
            <button class="btn btn-danger mt-3" @click="logout">
                Logout
            </button>

        </div>


        <div v-else>
            <div class="alert alert-danger text-center">
                {{ message }}
            </div>
        </div>

    </div>
</template>

<script>

export default {

    data() {
        return {
            success: false,
            message: "",
            stats: {},
            pendingDrives: []
        }
    },

    mounted() {
        this.loadDashboard()
    },

    methods: {

        async loadDashboard() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/company/dashboard",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.success = true
                this.message = result.message
                this.stats = result.stats
                this.pendingDrives = result.pending_drives
            }
            else {
                this.success = false
                this.message = result.message
            }
        },

        logout() {
            localStorage.clear()
            this.$router.push("/login")
        }
    }
}

</script>