<template>
    <div class="container mt-5">

        <h2 class="text-center mb-4">
            Applicants
        </h2>


        <div v-if="success">

            <h5 class="mb-3">
                {{ driveTitle }}
            </h5>


            <table class="table table-bordered table-striped">

                <thead>

                    <tr>

                        <th>Student</th>
                        <th>Application Status</th>
                        <th>Offer Status</th>
                        <th>Eligibility</th>
                        <th>Actions</th>

                    </tr>

                </thead>


                <tbody>

                    <tr
                        v-for="application in applications"
                        :key="application.application_id"
                    >

                        <td>

                            <router-link
                                :to="'/company/application/' + application.application_id + '/student'"
                            >
                                {{ application.student_name }}
                            </router-link>

                        </td>


                        <td>

                            {{ application.application_status }}

                        </td>


                        <td>

                            {{ application.offer_status }}

                        </td>


                        <td>

                            {{ application.eligibility }}

                        </td>


                        <td>


                            <button
                                v-if="application.application_status=='Applied'"
                                class="btn btn-warning btn-sm me-2"
                                @click="updateStatus(application.application_id,'Shortlisted')"
                            >
                                Shortlist
                            </button>



                            <button
                                v-if="application.application_status=='Applied' || application.application_status=='Shortlisted'"
                                class="btn btn-success btn-sm me-2"
                                @click="updateStatus(application.application_id,'Selected')"
                            >
                                Select
                            </button>



                            <button
                                v-if="application.application_status=='Applied' || application.application_status=='Shortlisted'"
                                class="btn btn-danger btn-sm"
                                @click="updateStatus(application.application_id,'Rejected')"
                            >
                                Reject
                            </button>


                        </td>


                    </tr>

                </tbody>

            </table>

        <router-link class="btn btn-primary m-2" to="/company/drives">
                    Back
        </router-link>
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

            driveTitle:"",

            applications:[]

        }

    },


    mounted(){

        this.loadApplicants()

    },


    methods:{


        async loadApplicants(){

            const response=await fetch(

                "http://127.0.0.1:5000/api/company/drive/"+this.$route.params.id+"/applicants",

                {

                    headers:{

                        "Authorization":"Bearer "+localStorage.getItem("token")

                    }

                }

            )


            const result=await response.json()


            if(result.success){

                this.success=true

                this.driveTitle=result.drive_title

                this.applications=result.applicants

            }

            else{

                this.message=result.message

            }

        },



        async updateStatus(applicationId,status){

            const response=await fetch(

                "http://127.0.0.1:5000/api/company/update-application-status/"+applicationId,

                {

                    method:"PUT",

                    headers:{

                        "Content-Type":"application/json",

                        "Authorization":"Bearer "+localStorage.getItem("token")

                    },

                    body:JSON.stringify({

                        application_status:status

                    })

                }

            )


            const result=await response.json()

            alert(result.message)

            this.loadApplicants()

        }

    }

}

</script>