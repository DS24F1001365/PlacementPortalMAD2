<template>
    <div class="container mt-5">

        <div v-if="success">
            <h2 class="text-center mb-4">
                {{ message }}
            </h2>

            <div v-if="isPlaced" class="alert alert-success">
                Congratulations! You have accepted an offer.
            </div>

            <div class="row">

                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Total Applications</h5>
                        <h2>{{ stats.total_applications }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Selected Applications</h5>
                        <h2>{{ stats.selected_applications }}</h2>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card p-3 text-center">
                        <h5>Pending Offers</h5>
                        <h2>{{ stats.pending_offers }}</h2>
                    </div>
                </div>

            </div>

            <router-link class="btn btn-primary m-2" to="/student/profile">
                Profile
            </router-link>
            <router-link class="btn btn-primary m-2" to="/student/drives">
                Available Drives
            </router-link>
            <router-link class="btn btn-primary m-2" to="/student/applications">
                Applications
            </router-link>
            <router-link class="btn btn-primary m-2" to="/student/offers">
                Offers
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
            isPlaced: false,
            stats: {}
        }
    },

    mounted() {
        this.loadDashboard()
    },

    methods: {

        async loadDashboard() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/student/dashboard",
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
                this.isPlaced = result.is_placed
                this.stats = result.stats
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