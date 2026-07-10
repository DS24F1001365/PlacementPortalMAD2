<template>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Applications
        </h2>

        <input type="text" class="form-control mb-4" placeholder="Search by student/company/title" v-model="searchText">

        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Student</th>
                    <th>Drive ID</th>
                    <th>Job Title</th>
                    <th>Company</th>
                    <th>Application Status</th>
                    <th>Offer Status</th>
                    <th>Student Status</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="application in filteredApplications" :key="application.id">
                    <td>{{ application.id }}</td>
                    <td>{{ application.student_name }}</td>
                    <td>{{ application.drive_id }}</td>
                    <td>{{ application.title }}</td>
                    <td>{{ application.company_name }}</td>
                    <td>{{ application.application_status }}</td>
                    <td>{{ application.offer_status }}</td>
                    <td>{{ application.student_status }}</td>
                </tr>
            </tbody>
        </table>

    </div>
</template>

<script>

export default {

    data() {
        return {
            applications: [],
            searchText: ""
        }
    },

    computed: {
        filteredApplications() {
            return this.applications.filter(application =>
                application.student_name.toLowerCase().includes(this.searchText.toLowerCase())
                ||
                application.company_name.toLowerCase().includes(this.searchText.toLowerCase())
                ||
                application.title.toLowerCase().includes(this.searchText.toLowerCase())
            )
        }
    },

    mounted() {
        this.loadApplications()
    },

    methods: {
        async loadApplications() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/applications",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.applications = result.applications
            }
        }
    }
}

</script>