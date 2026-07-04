<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card shadow p-4">

                    <h2 class="text-center mb-4">
                        Placement Portal Login
                    </h2>

                    <form @submit.prevent="login">
                        <div class="mb-3">
                            <label class="form-label">
                                Email
                            </label>
                            <input type="email" class="form-control" v-model="email" required>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">
                                Password
                            </label>
                            <input type="password" class="form-control" v-model="password" required>
                        </div>

                        <button class="btn btn-primary w-100" type="submit">
                            Login
                        </button>

                    </form>

                    <hr>

                    <p class="text-center">
                        New Student?
                        <router-link to="/student/register">
                            Register Here
                        </router-link>
                    </p>

                    <p class="text-center">
                        New Company?
                        <router-link to="/company/register">
                            Register Here
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
            email: "",
            password: ""
        }
    },

    methods: {

        async login() {
            try {
                const response = await fetch(
                    "http://127.0.0.1:5000/api/login",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            email: this.email,
                            password: this.password
                        })
                    }
                )

                const result = await response.json()
                if (result.success) {
                    localStorage.setItem("token",result.token)
                    localStorage.setItem("role",result.role)
                    localStorage.setItem("name",result.name)
                    localStorage.setItem("user_id",result.user_id)
                    alert(result.message)

                    if (result.role === "admin") {
                        this.$router.push("/admin/dashboard")
                    }
                    else if (result.role === "student") {
                        this.$router.push("/student/dashboard")
                    }
                    else {
                        this.$router.push("/company/dashboard")
                    }
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