<template>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Manage Companies
        </h2>

        <input type="text" class="form-control mb-4" placeholder="Search company by name" v-model="searchText">

        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Company Name</th>
                    <th>Email</th>
                    <th>HR Name</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="company in filteredCompanies" :key="company.id">
                    <td>{{ company.id }}</td>
                    <td>{{ company.name }}</td>
                    <td>{{ company.email }}</td>
                    <td>{{ company.hr_name }}</td>
                    <td>
                        <span v-if="company.blacklist_status">
                            Blacklisted
                        </span>
                        <span v-else>
                            {{ company.approval_status }}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-primary btn-sm me-2" @click="viewCompany(company.id)">
                            View
                        </button>
                        <button v-if="company.approval_status=='Pending'" class="btn btn-success btn-sm me-2" @click="approveCompany(company.id)">
                            Approve
                        </button>
                        <button v-if="company.approval_status=='Pending'" class="btn btn-danger btn-sm me-2" @click="rejectCompany(company.id)">
                            Reject
                        </button>
                        <button v-if="company.approval_status=='Approved' && !company.blacklist_status" class="btn btn-warning btn-sm" @click="blacklistCompany(company.id)">
                            Blacklist
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>

export default {

    data() {

        return {
            companies: [],
            searchText: ""
        }

    },

    computed: {
        filteredCompanies() {
            return this.companies.filter(company =>
                company.name.toLowerCase().includes(this.searchText.toLowerCase())
            )
        }
    },

    mounted() {
        this.loadCompanies()
    },

    methods: {

        async loadCompanies() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/companies",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.companies = result.companies
            }
        },

        async approveCompany(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/company/approve/" + id,
                {
                    method: "PUT",

                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadCompanies()
        },

        async rejectCompany(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/company/reject/" + id,
                {
                    method: "PUT",

                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadCompanies()
        },

        async blacklistCompany(id) {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/company/blacklist/" + id,
                {
                    method: "PUT",

                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            alert(result.message)
            this.loadCompanies()

        },

        viewCompany(id) {
            this.$router.push("/admin/company/" + id)
        }
    }
}

</script>