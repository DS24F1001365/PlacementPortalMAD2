<template>
<div class="container mt-5">

    <div v-if="success">
        <h2 class="text-center mb-4">
            Available Placement Drives
        </h2>
        <div v-if="message" class="alert alert-danger">
            {{ message }}
        </div>

        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>Company</th>
                    <th>Role</th>
                    <th>Specialization</th>
                    <th>Description</th>
                    <th>Deadline</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.company }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.specialization }}</td>
                    <td>{{ drive.description }}</td>
                    <td>{{ drive.deadline }}</td>
                    <td>
                        <button v-if="!drive.applied" class="btn btn-success btn-sm" @click="apply(drive.id)">
                            Apply
                        </button>
                        <button v-else class="btn btn-secondary btn-sm" disabled>
                            Applied
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

    </div>

    <div v-else>
        <div class="alert alert-danger">
            {{ message }}
        </div>
    </div>

</div>

</template>

<script>

export default{

    data(){
        return{
            success:false,
            message:"",
            drives:[],
            is_placed:false,
            is_active:true
        }
    },

    mounted(){
        this.loadDrives()
    },

    methods:{

        async loadDrives(){
            const response=await fetch(
                "http://127.0.0.1:5000/api/student/drives",
                {
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )

            const result=await response.json()
            if(result.success){
                this.success=true
                this.drives=result.drives
                this.is_active=result.is_active
                this.is_placed=result.is_placed
                if (this.is_placed){
                    this.success=false,
                    this.message="Placed Students cannot apply for drives"
                    return
                }
                if (!this.is_active){
                    this.success=false,
                    this.message="Inactive Students cannot apply for drives"
                    return
                }
            }

            else{
                this.message=result.message
            }
        },

        async apply(driveId){

            const response=await fetch(
                "http://127.0.0.1:5000/api/student/apply/"+driveId,
                {
                    method:"POST",
                    headers:{
                        "Authorization":"Bearer "+localStorage.getItem("token")
                    }
                }
            )
            const result=await response.json()
            alert(result.message)
            this.loadDrives()
        }
    }
}

</script>