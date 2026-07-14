<template>
    <Navbar role="student"/>

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

                <div class="mt-4">
                <button class="btn btn-success" @click="exportApplications" :disabled="exporting">
                    {{ exporting ? "Generating CSV..." : "Export Applications CSV" }}
                </button>
                <a v-if="downloadUrl" class="btn btn-primary ms-3" @click="downloadCSV">
                    Download CSV
                </a>

            </div>

        </div>

        <div v-else>
            <div class="alert alert-danger text-center">
                {{ message }}
            </div>
        </div>

    </div>
</template>

<script>
import Navbar from "../components/Navbar.vue"

export default {

    data() {
        return {
            success: false,
            message: "",
            isPlaced: false,
            stats: {},
            exporting: false,
            downloadUrl: "",
            polling: null
        }
    },

    components:{
        Navbar,
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
        },

        async exportApplications(){

            this.exporting = true
            this.downloadUrl = ""

            const response = await fetch(
                "http://127.0.0.1:5000/api/student/export-applications",
                {
                    method:"POST",
                    headers:{
                        Authorization:"Bearer " + localStorage.getItem("token")
                    }
                }
            )

            const result = await response.json()
            if(result.success){
                this.pollExport(result.task_id)
            }
            else{
                alert(result.message)
                this.exporting=false
            }
        },

        pollExport(taskId){

            this.polling = setInterval(
                async()=>{
                    const response = await fetch(
                        "http://127.0.0.1:5000/api/student/export-status/" + taskId,
                        {
                            headers:{
                                Authorization:"Bearer " + localStorage.getItem("token")
                            }
                        }
                    )

                    const result = await response.json()
                    if(result.state=="SUCCESS"){
                        clearInterval(this.polling)
                        this.exporting=false
                        this.downloadUrl=
                            "http://127.0.0.1:5000/api/student/download-export/"+ result.filename
                    }
                },3000)
        },

        async downloadCSV() {

            const response = await fetch(
                this.downloadUrl,
                {
                    headers: {
                        Authorization: "Bearer " + localStorage.getItem("token")
                    }
                }
            )

            if (!response.ok) {
                alert("Download failed.")
                return
            }

            const blob = await response.blob()
            const url = window.URL.createObjectURL(blob)
            const link = document.createElement("a")
            link.href = url
            link.download = this.downloadUrl.split("/").pop()
            document.body.appendChild(link)
            link.click()
            link.remove()
            window.URL.revokeObjectURL(url)
        },

        beforeUnmount(){
            if(this.polling){
            clearInterval(this.polling)

            }
        }


    }
}

</script>