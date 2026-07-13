<template>
    <div class="container mt-5">

        <div v-if="success">

        <h2 class="text-center mb-4">
            Edit Profile
        </h2>

            <form @submit.prevent="updateProfile">
                <div class="mb-3">
                    <label class="form-label">HR Name</label>
                    <input type="text" class="form-control" v-model="profile.hr_name">
                </div>
                <div class="mb-3">
                    <label class="form-label">HR Email</label>
                    <input type="email" class="form-control" v-model="profile.hr_email">
                </div>
                <div class="mb-3">
                    <label class="form-label">HR Contact</label>
                    <input type="text" class="form-control" v-model="profile.hr_contact">
                </div>
                <div class="mb-3">
                    <label class="form-label">Website</label>
                    <input type="text" class="form-control" v-model="profile.website">
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control" v-model="profile.description">
                    </textarea>
                </div>

                <button class="btn btn-success" type="submit">
                    Save Changes
                </button>

            </form>
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
            profile: {}
        }
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
                this.message = result.message
            }
        },

        async updateProfile() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/company/profile",
                {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    },
                    body: JSON.stringify(this.profile)
                }
            )

            const result = await response.json()
            alert(result.message)
            if (result.success) {
                this.$router.push("/company/profile")
            }
        }
    }
}

</script>