<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow p-4">

                    <h2 class="text-center mb-4">
                        Student Registration
                    </h2>

                    <form @submit.prevent="registerStudent">
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
                            <label class="form-label">Phone</label>
                            <input type="tel" class="form-control" v-model="phone" pattern="[0-9]{10}" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Branch</label>
                            <select class="form-select" v-model="branch" required>
                                <option disabled value="">
                                    Select Branch
                                </option>

                                <option>CSE</option>
                                <option>Data Science</option>
                                <option>AI & ML</option>
                                <option>IT</option>
                                <option>ECE</option>
                                <option>EEE</option>
                                <option>Mechanical</option>
                                <option>Civil</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Year</label>
                            <select class="form-select" v-model="year" required>
                                <option disabled value="">
                                    Select Year
                                </option>

                                <option :value="1">1</option>
                                <option :value="2">2</option>
                                <option :value="3">3</option>
                                <option :value="4">4</option>
                            </select>
                        </div>

                        <div class="mb-4">
                            <label class="form-label">CGPA</label>
                            <input type="number" class="form-control" v-model="cgpa" min="0" max="10" step="0.01" required>
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
            phone: "",
            branch: "",
            year: "",
            cgpa: ""
        }

    },

    methods: {

        async registerStudent() {
            try {
                const response = await fetch(
                    "http://127.0.0.1:5000/api/student/register",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            name: this.name,
                            email: this.email,
                            password: this.password,
                            phone: this.phone,
                            branch: this.branch,
                            year: this.year,
                            cgpa: this.cgpa
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