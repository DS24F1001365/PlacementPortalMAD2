<template>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Placement History
        </h2>

        <input type="text" class="form-control mb-4" placeholder="Search student/company" v-model="searchText">

        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Student</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Company</th>
                    <th>Drive</th>
                    <th>Applied On</th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="placement in filteredPlacements" :key="placement.id">
                    <td>{{ placement.id }}</td>
                    <td>{{ placement.student_name }}</td>
                    <td>{{ placement.branch }}</td>
                    <td>{{ placement.cgpa }}</td>
                    <td>{{ placement.company_name }}</td>
                    <td>{{ placement.drive_title }}</td>
                    <td>{{ placement.applied_on }}</td>
                </tr>
            </tbody>
        </table>

    </div>
</template>

<script>

export default {

    data() {
        return {
            placements: [],
            searchText: ""
        }
    },

    computed: {
        filteredPlacements() {
            return this.placements.filter(placement =>
                placement.student_name.toLowerCase().includes(this.searchText.toLowerCase())
                ||
                placement.company_name.toLowerCase().includes(this.searchText.toLowerCase())
            )
        }
    },

    mounted() {
        this.loadPlacements()
    },


    methods: {

        async loadPlacements() {
            const response = await fetch(
                "http://127.0.0.1:5000/api/admin/placement-history",
                {
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if (result.success) {
                this.placements = result.placements
            }
        }
    }
}

</script>