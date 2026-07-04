<template>
    <div class="container mt-5">

        <h2>{{ message }}</h2>

        <button class="btn btn-danger mt-3" @click="logout">
            Logout
        </button>

    </div>
</template>


<script>

export default {

    data() {
        return {
            message: ""
        }
    },

    async mounted() {

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
            this.message = result.message
        }
        else {
            alert(result.message)
            this.$router.push("/login")
        }

    },

    methods: {

        logout() {

            localStorage.clear()

            this.$router.push("/login")

        }

    }

}

</script>