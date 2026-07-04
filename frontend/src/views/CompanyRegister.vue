<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow p-4">

                    <h2 class="text-center mb-4">
                        Company Registration
                    </h2>

                    <form @submit.prevent="registerCompany">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" class="form-control" v-model="name" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Email</label>
                            <input type="email" class="form-control" v-model="email" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Password</label>
                            <input type="password" class="form-control" v-model="password" minlength="6" required
                            >
                        </div>

                        <div class="mb-3">
                            <label class="form-label">HR Name</label>
                            <input type="text" class="form-control" v-model="hr_name" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">HR Email</label>
                            <input type="email" class="form-control" v-model="hr_email" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">HR Contact</label>
                            <input type="tel" class="form-control" v-model="hr_contact" pattern="[0-9]{10}" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Website</label>
                            <input type="url" class="form-control" v-model="website" placeholder="https://example.com">
                        </div>

                        <div class="mb-4">
                            <label class="form-label">Description</label>
                            <textarea class="form-control" rows="4" v-model="description"></textarea>
                        </div>

                        <button class="btn btn-success w-100" type="submit">
                            Register
                        </button>
                    </form>

                    <hr>

                    <p class="text-center mb-0">
                        Already have an account?
                        <router-link to="/login">
                            Login
                        </router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {

    data() {

        return {
            name: "",
            email: "",
            password: "",
            hr_name: "",
            hr_email: "",
            hr_contact: "",
            website: "",
            description: ""
        }
    },

    methods: {

        async registerCompany() {

            try {
                const response = await fetch(
                    "http://127.0.0.1:5000/api/company/register",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            name: this.name,
                            email: this.email,
                            password: this.password,
                            hr_name: this.hr_name,
                            hr_email: this.hr_email,
                            hr_contact: this.hr_contact,
                            website: this.website,
                            description: this.description
                        })
                    }
                )

                const result = await response.json()
                if (result.success) {
                    alert(result.message)
                    this.$router.push("/login")
                }
                else {
                    alert(result.message)
                }
            }
            catch (error) {
                console.log(error)
                alert("Server Error")
            }
        }
    }
}
</script>